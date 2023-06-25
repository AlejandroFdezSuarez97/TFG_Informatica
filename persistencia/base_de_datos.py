import sqlite3 as sq

from persistencia.tiposTablas.tabla_Simulador import Tabla_simulador
from persistencia.tiposTablas.tabla_Sat import Tabla_sat
from persistencia.tiposTablas.tabla_Hampath import Tabla_hampath
from persistencia.tiposTablas.tabla_Hamcycle import Tabla_hamycle
from persistencia.tiposTablas.tabla_Uhamcycle import Tabla_uhamycle
from persistencia.tiposTablas.tabla_TSP import Tabla_tsp
from persistencia.tiposTablas.tabla_Subset import Tabla_subset
from persistencia.tiposTablas.tabla_Mochila import Tabla_mochila


###########################################################
# Clase base_de_datos. Esta clase se encarga de implementar
# todos las funciones asociadas al manejo de la base de 
# datos utilizada durante el simulador.
###########################################################
class BaseDeDatos():

    _unica_instancia = None
    _conexionBD = None
    _cursor = None

    _tabla_simulador = None
    _tabla_sat = None
    _tabla_hampath = None
    _tabla_hamcycle = None
    _tabla_uhamcycle = None
    _tabla_tsp = None
    _tabla_subset = None
    _tabla_mochila = None

    # Constructor
    def __init__(self):

        # Conecto con la base de datos  
        self.conexionBD = sq.connect('memoriaSimulador.db')

        # Creo el objeto que me da acceso a la misma
        self.cursor = self.conexionBD.cursor()
        
        self._tabla_simulador = Tabla_simulador(self)
        self._tabla_sat = Tabla_sat(self)
        self._tabla_hampath = Tabla_hampath(self)
        self._tabla_hamcycle = Tabla_hamycle(self)
        self._tabla_uhamcycle = Tabla_uhamycle(self)
        self._tabla_tsp = Tabla_tsp(self)
        self._tabla_subset = Tabla_subset(self)
        self._tabla_mochila = Tabla_mochila(self)
        
    
    # Instancia del controlador.
    def get_unica_instancia():

        if BaseDeDatos._unica_instancia == None:
            BaseDeDatos._unica_instancia = BaseDeDatos()

        return BaseDeDatos._unica_instancia

    ###############################################
    ################ METODOS GET  #################
    ###############################################

    # Devuelve el objeto que sirve para acceder/modificar datos de la BD
    def get_cursor(self):
        return self.cursor

    # Devuelve el objeto con el que estamos conectados a la base de datos
    def get_conexion(self):
        return self.conexionBD

    # Funcion que devuelve la tabla_simulador de la base de datos
    def get_tabla_simulador(self):
        return self._tabla_simulador
    
    # Funcion que deevuelve la tabla_sat de la base de datos
    def get_tabla_sat(self):
        return self._tabla_sat

    # Funcion que devuelve la tabla_hampath de la base de datos
    def get_tabla_hampath(self):
        return self._tabla_hampath
    
    # Devuelve la tabla_hamcycle de la base de datos
    def get_tabla_hamcycle(self):
        return self._tabla_hamcycle
    
    # Devuelve la tabla_uhamcycle de la base de datos
    def get_tabla_uhamcycle(self):
        return self._tabla_uhamcycle
    
    # Devuelve la tabla_tsp de la base de datos
    def get_tabla_tsp(self):
        return self._tabla_tsp
    
    # Devuelce la tabla_subset de la base de datos
    def get_tabla_subset(self):
        return self._tabla_subset
    
    # Devuelve la tabla_mochila
    def get_tabla_mochila(self):
        return self._tabla_mochila
    
    # -------------------------------------------------

    # Vacia la base de datos completamente
    def vaciar_bd(self):
        # Obtener la lista de tablas en la base de datos
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = self.cursor.fetchall()

        # Vaciar cada tabla
        for tabla in tablas:
            tabla_nombre = tabla[0]
            self.cursor.execute(f"DELETE FROM {tabla_nombre};")

        # Confirmar los cambios y cerrar la conexión
        self.conexionBD.commit()



    
    
    