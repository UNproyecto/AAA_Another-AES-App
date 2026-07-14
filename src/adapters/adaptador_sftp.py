"""Este archivo contiene la implementación del adapatador del sistema
para permitir la conexión a un servidor sftp"""

import paramiko
import os
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

from .storage_provider import StorageProvider

class AdaptadorSFTP(StorageProvider):
    
    def __init__(self, host_address) -> None:
        super().__init__()
        self.host = host_address
        self._conexion = None
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Toca quitar esto porque es inseguro


    def conectar(self, user: str, pwd: str):
        try:
            self._ssh.connect(self.host, username=user, password=pwd)
            self._conexion = self._ssh.open_sftp()
        except Exception as e:
            raise e
    
    def desconectar(self):
        if self._conexion is not None:
            self._conexion.close()
            self._ssh.close()
            self._conexion = None
    
    def cargar(self, data: bytes, remote_name: str):
        if self._conexion is None:
            raise Exception("No hay una conexión activa")
        with BytesIO(data) as archivo:
            self._conexion.putfo(archivo, remote_name)

        
    def descargar(self, remote_name: str) -> bytes:
        if self._conexion is None:
            raise Exception("No hay una conexión activa")
        
        with self._conexion.open(remote_name, 'r') as archivo:
            archivo_bin = archivo.read()
        return archivo_bin

if __name__ == "__main__":
    ip_add = os.getenv("IP_SFTP")
    user = os.getenv("USER_SFTP", "")
    pwd = os.getenv("PWD_SFTP", "")

    server = AdaptadorSFTP(ip_add)
    server.conectar(user, pwd)
    archivito = b'Hola, este es un archivo de prueba!'
    server.cargar(archivito, "holi.txt")
    recuperado = server.descargar("prueba.txt")
    server.desconectar()

    print(recuperado)
        