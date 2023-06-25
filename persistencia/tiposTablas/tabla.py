from abc import ABC, abstractclassmethod

#####################################################
# Clase padre de la que heredarán el resto de tablas.
#####################################################
class Tabla(ABC):
    def __init__(self, bd):
        
        self.bd = bd
        self.cursor = self.bd.get_cursor()
        self.conexion = self.bd.get_conexion()

    @abstractclassmethod
    def imprime_tabla(self):
        pass
    
