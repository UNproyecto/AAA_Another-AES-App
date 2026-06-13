'''
AAA.py
Es un modulo que contiene toda la logica de la aplicacion.
Se encarga del encriptado, desencriptado y extension de clave.
Tambien se encarga de todas las tareas adicionales que puedan ser necesarias.
'''

from argon2.low_level import hash_secret_raw, Type #password derivation
'''
Argon permite derivar dos tipos de contraseñas 
(Type.I) para resistir ataques por canal lateral (side-channel attacks) (patrones de acceso a memoria.) 
(Type.D) Prioriza la resistencia a ataques con hardware especializado (GPU, ASIC).
En nuestro caso vamos a prevenir ambas usando Type.ID
'''
from secrets import token_bytes #Salt libraries
from cryptography.hazmat.primitives.ciphers.aead import AESGCM #AES GCM implementation
from cryptography.exceptions import InvalidTag #Para error de tag Invalido
from json import dumps, loads #Metadata

def encrypt(pwd:str, file:bytes, meta:dict):
    salt, key = derive_pwd(pwd).values()

    #Nonce es un numero aleatorio usado 
    #para que un mismo mensaje dada una misma clave no de dos veces el mismo cifrado
    #Su tamaño tipico es 12 bytes por estandar
    nonce =  token_bytes(12)

    helper = AESGCM(key)

    metadata = gen_metadata(meta, salt, nonce)
    ciphertext = helper.encrypt(nonce, file, metadata)

    encrypted_file = metadata + ciphertext

    return encrypted_file

def decrypt(pwd:str, file:bytes):
    #Hay varias formas de procesarlo
    #1. Voy a quitar la metadata
    #Meta es el diccionario con los datos de la metadata y metadata es toda la cadena de bytes para recalcular el tag
    file, metadata = remove_metadata(file).values()
    meta, salt, nonce, meta_bytes = metadata.values()
    
    #2. Voy a derivar la clave nuevamente haciendo uso de la salt
    key = derive_pwd(pwd, salt)["key"]
    #3. Voy a revisar el token
    #4. voy a volver un dict con la info desencriptada y la meta
    #3 y 4 se hacen en automatico gracias a la libreria
    try:
        helper = AESGCM(key)
        plaintext = helper.decrypt(
            nonce,
            file,
            meta_bytes
        )
    except InvalidTag:
        raise InvalidTag("The metadata, archive or password has been modified. Tag mismatch.")
    return  {
            "plaintext": plaintext,
            "metadata": meta
            }

def gen_metadata(meta:dict, salt:bytes, nonce:bytes):
    magic = b"%AAA" #Todos los formatos de archivo lo llevan para indicar el tipo (4-bytes)
    version =  (1).to_bytes(1, "big") #Version del formato (1-byte)

    meta_bytes = dumps(meta).encode("utf-8")
    meta_len = len(meta_bytes).to_bytes(4, "big")

    header =  ( magic
              + version
              + meta_len
              + meta_bytes
              + salt
              + nonce
              )
    
    return header

def remove_metadata(file:bytes) -> dict:
    #Revisamos que el archivo siga el formato
    magic = file[0:4]

    if magic != b"%AAA": raise RuntimeError("Formato del archivo recibido no corresponde a '.AAA'.")
    
    meta_size = int.from_bytes(file[5:9])

    end_meta = 9+meta_size

    meta_bytes = file[9:end_meta]

    meta = loads(
        meta_bytes.decode("utf-8")
    )

    salt = file[end_meta:end_meta+16]

    nonce = file[end_meta+16:end_meta+28]

    raw_file = file[end_meta+28:]
    return  {
            "file":raw_file, 
            "meta": {
                     "meta": meta, 
                     "salt": salt, 
                     "nonce": nonce, 
                     "bytes":file[0:end_meta+28]
                    }
            }

def derive_pwd(pwd:str, salt:bytes=None):

    salt = token_bytes(16) if salt is None else salt

    key = hash_secret_raw(
        secret=pwd.encode(),
        salt=salt,
        time_cost=3, #Pasadas a memoria
        memory_cost=65536, #64 MB de memoria
        parallelism=8, #El algoritmo hace uso de 4 hilos
        hash_len=32, #256 bits
        type=Type.ID 
    )

    #IDEAS DE TEST
    '''
    - Longitud adecuada de key
    - Dada misma pwd diferente key
    - Dada misma pwd y misma salt misma key
    '''

    return {"salt":salt, "key":key}


if __name__ == "__main__":
    # salt, key = derive_pwd("1234").values()
    # print(key)
    # print(derive_pwd("1234", salt)["key"])

    #Prueba de encriptacion
    name = "archivo1.txt"
    metadata = {
        "filename": name,
        "mod_date": "12/06/2026"
    }
    msj = "Prueba1 vamos a encriptar"
    
    pwd = "banana"
    msj = msj.encode("utf-8")
    cypher = encrypt(pwd, msj, metadata)
    print(cypher)
    plain = decrypt(pwd, cypher)
    print(plain)
