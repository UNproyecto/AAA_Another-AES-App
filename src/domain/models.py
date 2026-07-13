"""En este archivo se define un modelo sencillo para homogeneizar
el aspecto de los archivos como un conjunto de metadata (un dict)
y el contenido en bytes"""

from dataclasses import dataclass

@dataclass
class Archivo:
    metadata: dict
    contenido: bytes