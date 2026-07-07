"""
En este archivo se define la interface para cualquier adaptador con
algún servicio de alamcenamiento (sea un servidor ftp o un CSP como Google Drive)"""

from abc import ABC, abstractmethod

class StorageProvider(ABC):

    @abstractmethod
    def cargar(self, data: bytes, remote_name: str):
        pass

    @abstractmethod
    def descargar(self, remote_name: str) -> bytes:
        pass

    @abstractmethod
    def conectar(self , user:str , pwd:str):
        pass

    @abstractmethod
    def desconectar(self):
        pass
