from persistencia.tiposTablas.tabla import Tabla
import tkinter as tk
from tkinter import ttk


##############################################################################
# Clase que engloba el tipo de tabla_simulador.
##############################################################################

class Tabla_simulador(Tabla):

    # Constructor
    def __init__(self, bd):
        
        super().__init__(bd)

        self.cargar_tabla_simulador()


    ###############################################
    ############ CREACIÓN DE LA TABLA  ############
    ###############################################

    # Creo o cargo la tabla_simulador en la base de datos
    def cargar_tabla_simulador(self):    
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS tabla_simulador (
                            id INTEGER PRIMARY KEY,
                            SAT INTEGER,
                            HAMPATH INTEGER,
                            HAMCYCLE INTEGER,
                            UHAMCYCLE INTEGER,
                            TSP INTEGER,
                            SUBSET INTEGER,
                            MOCHILA INTEGER
                            )
                    ''')

    ###############################################
    ######### ANADIR ENTRADAS A LA TABLA ##########
    ############################################### 

    # Función para añadir una entrada en la base de datos en la tabla_simulador
    def anadir_fila_tabla_simulador(self, id, id_problema1, id_problema2, problema1, problema2):
        sql = "INSERT INTO tabla_simulador (id, SAT, HAMPATH, HAMCYCLE, UHAMCYCLE, TSP, SUBSET, MOCHILA) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        
        sat = hampath = hamcycle = uhamcycle = tsp = subset = mochila = 0

        if problema1=="SAT":
            sat = id_problema1
        elif problema1=="HAMPATH":
            hampath = id_problema1
        elif problema1=="HAMCYCLE":
            hamcycle = id_problema1
        elif problema1=="UHAMCYCLE":
            uhamcycle = id_problema1
        elif problema1=="TSP":
            tsp = id_problema1
        elif problema1=="SUBSET":
            subset=id_problema1
        elif problema1=="MOCHILA":
            mochila=id_problema1

        if problema2=="SAT":
            sat = id_problema2
        elif problema2=="HAMPATH":
            hampath = id_problema2
        elif problema2=="HAMCYCLE":
            hamcycle = id_problema2
        elif problema2=="UHAMCYCLE":
            uhamcycle = id_problema2
        elif problema2=="TSP":
            tsp = id_problema2
        elif problema2=="SUBSET":
            subset=id_problema2
        elif problema2=="MOCHILA":
            mochila=id_problema2

        # Anado la fila a la tabla
        self.cursor.execute(sql, (id, sat, hampath, hamcycle, uhamcycle, tsp, subset, mochila))

        # Guardo los cambios en la base de datos
        self.conexion.commit()


    ###############################################
    ####### EXTRAER ENTRADAS DE LA TABLA ##########
    ###############################################


    # Devuelve el numero de Simulaciones almacenadas en la base de datos
    # (tantas como filas tenga dicha tabla)
    def get_numSimulaciones_enBD(self):
        self.cursor.execute("SELECT COUNT(*) FROM tabla_simulador")
        resultado = self.cursor.fetchone()

        # Nos quedamos con el numero de filas de la tabla_simualdor
        numSimulaciones = resultado[0]

        return numSimulaciones

    # Funcion que sirve para extaer una fila de la tabla_simulador
    def extaer_fila_tabla_simulador_por_id(self, id):
        sql =  "SELECT * FROM tabla_simulador WHERE id = ?"
        self.cursor.execute(sql, (id,))
        fila = self.cursor.fetchone()

        filaSolucion = []
        if fila is not None:
            for item in fila:
                filaSolucion.append(item)
        else:
            print('No se ha encontrado una fila en tabla_simulador con ese id')
        
        return filaSolucion


    # Funcion que devuelve toda la tabla_simulador
    def imprime_tabla(self):
        
        self.cursor.execute("SELECT * FROM tabla_simulador")
        filas = self.cursor.fetchall()

        # Obtener los nombres de las columnas de la tabla
        nombres_columnas = [descripcion[0] for descripcion in self.cursor.description]

        # Imprimir los nombres de las columnas
        print(" | ".join(nombres_columnas))

        # Imprimir los registros de la tabla
        for registro in filas:
            print(" | ".join(str(valor) for valor in registro))



    ###############################################
    ######### ELIMINAR ENTRADAS DE LA TABLA #######
    ###############################################    


    ###############################################
    ######### MOSTRAR TABLA EN VENTANA ############
    ###############################################


    # Funcion que crea una ventana grafica y muestra en ella
    # en formato grafico la tabla_simulador
    def mostrar_tabla_simulador(self, ventana_antigua):

        ventana_antigua.destroy()
        
        # Crear la ventana
        ventana = tk.Tk()
        ventana.title("Tabla Simulador")

        self.cursor.execute("SELECT * FROM tabla_simulador")
        filas = self.cursor.fetchall()

        # Crear el TreeView
        treeview = ttk.Treeview(ventana)

        # Configurar las columnas
        treeview["columns"] = ("SAT", "HAMPATH", "HAMCYCLE", "UHAMCYCLE", "TSP", "SUBSET", "MOCHILA")
        treeview.column("#0", width=50)  # Columna para el ID
        treeview.column("SAT", width=100)
        treeview.column("HAMPATH", width=100)
        treeview.column("HAMCYCLE", width=100)
        treeview.column("UHAMCYCLE", width=100)
        treeview.column("TSP", width=100)
        treeview.column("SUBSET", width=100)
        treeview.column("MOCHILA", width=100)

        # Configurar las cabeceras de las columnas
        treeview.heading("#0", text="ID")
        treeview.heading("SAT", text="SAT")
        treeview.heading("HAMPATH", text="HAMPATH")
        treeview.heading("HAMCYCLE", text="HAMCYCLE")
        treeview.heading("UHAMCYCLE", text="UHAMCYCLE")
        treeview.heading("TSP", text="TSP-DEC")
        treeview.heading("SUBSET", text="SUBSET-SUM")
        treeview.heading("MOCHILA", text="MOCHILA")

        # Insertar los datos en el TreeView
        for fila in filas:
            treeview.insert("", "end", text=fila[0], values=fila[1:])

        # Añadir el TreeView a la ventana
        treeview.pack() 