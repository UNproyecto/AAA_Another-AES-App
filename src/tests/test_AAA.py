"""
Pruebas unitarias para las funciones core del programa (módulo criptográfico)
Para ejecutar: desde /src/  -   python -m pytest
"""

import pytest
from domain import AAA, models

def _crear_archivo(msj="Prueba1 vamos a encriptar"):
    """Función auxiliar para crear un objeto de tipo Archivo"""
    name = "archivo1.txt"
    metadata = {
        "filename": name,
        "mod_date": "12/06/2026"
    }
    msj = msj.encode("utf-8")

    return models.Archivo(metadata, msj)


## Para la funcion derive_pwd

def test_pwd_length():
    """
    Verifica que la longitud de la contraseña derivada sea constante
    """
    result1 = AAA.derive_pwd("1234")
    result2 = AAA.derive_pwd("1234ABCD5678EFGH9!!!910")

    assert len(result1["key"]) == 32
    assert len(result1["salt"]) == 16
    assert len(result2["key"]) == 32
    assert len(result2["salt"]) == 16
    
def test_same_password_same_salt_same_key():
    """Verifica que ante la misma combinacion
    de salt y pwd, la funcion retorne el mismo output"""

    result1 = AAA.derive_pwd("1234", bytes(123))
    result2 = AAA.derive_pwd("1234", bytes(123))

    assert result1 == result2

def test_same_password_diff_salt_diff_key():
    """Verifica que ante una misma pwd con salts diferentes
    la funcion retorne el mismo output"""

    result1 = AAA.derive_pwd("1234", bytes(123))
    result2 = AAA.derive_pwd("1234", bytes(1000))

    assert result1 != result2

def test_not_salt_sent():
    """Verifica que en caso de omitir la salt, el sistema genera una aleatoria"""
    
    result1 = AAA.derive_pwd("1234")
    result2 = AAA.derive_pwd("1234")

    assert result1 != result2


# Para la función encrypt

def test_encrypt_returns_bytes():
    """Verifica que el tipo de dato de retorno sea el correcto"""
    archivo = _crear_archivo()
    pwd = "banana"

    cypher = AAA.encrypt(pwd, archivo)

    assert type(cypher) is bytes

def test_ciphertext_is_different_than_plaintext():
    """Verfica que la función encripte y retorne un valor diferente al mensaje original"""
    msj = "Hola ¿Cómo estás?"
    archivo = _crear_archivo(msj)
    pwd = "banana"

    cypher = AAA.encrypt(pwd, archivo)

    assert msj != cypher

def test_same_file_twice_diff_encryption():
    """Verfica que la función encripte y retorne un valor diferente
    si se encripta el mismo archivo dos veces."""
    archivo = _crear_archivo()

    pwd = "banana"

    cypher1 = AAA.encrypt(pwd, archivo)
    cypher2 = AAA.encrypt(pwd, archivo)

    assert cypher1 != cypher2

# Para la función decrypt

def test_decrypt_original_msg():
    """Verifica que la desencriptación recupere el mensaje original"""
    msj = "Hola mundoooo!"
    archivo = _crear_archivo(msj)
    pwd = "banana"
    
    cypher = AAA.encrypt(pwd, archivo)
    decypher = AAA.decrypt(pwd, cypher)
    
    plain = decypher.contenido.decode("utf-8")

    assert msj == plain

