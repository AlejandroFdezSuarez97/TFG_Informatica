import json
import networkx as nx
import pickle
from persistencia.tiposTablas.tabla import Tabla
import matplotlib.pyplot as plt

from interfaz_grafica.interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp
from PIL import Image
import customtkinter as ctk

##############################################################################
# Clase que engloba el tipo de tabla_TSP.
##############################################################################

class Tabla_tsp(Tabla):

    # Constructor
    def __init__(self, bd):
        
        super().__init__(bd)

        self.cargar_tabla_tsp()
    

    ###############################################
    ############ CREACIÓN DE LA TABLA  ############
    ###############################################

    # Funcion para crear/cargar la tabla_tsp
    def cargar_tabla_tsp(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS tabla_tsp (
                            id INTEGER PRIMARY KEY,
                            Grafo BLOB,
                            ColorMap TEXT
                            )
                    ''')

    ###############################################
    ######### ANADIR ENTRADAS A LA TABLA ##########
    ###############################################    

    # Funcion que almacena una entrada en la tabla_tsp
    # Debo serializar la mayoria de sus parametro, por lo que debo tener cuidado a la hora de 
    # sacarlos de la BD.
    def anadir_fila_tabla_tsp(self, id, grafo, colorMap):

        sql = "INSERT INTO tabla_tsp (id, Grafo, ColorMap) VALUES (?, ?, ?)"    

        # Transformamos todos los datos para poder almacenarlos en la base de datos
        grafo_serializado = pickle.dumps(grafo)
        colorMap_serializado = json.dumps(colorMap)
        
        # Anado la fila a la tabla
        self.cursor.execute(sql, (id, grafo_serializado, colorMap_serializado))

        # Guardo los cambios en la base de datos
        self.conexion.commit()


    ###############################################
    ####### EXTRAER ENTRADAS DE LA TABLA ##########
    ###############################################

    # Funcion que sirve para extaer una fila de la tabla_tsp
    def extaer_fila_tabla_tsp_por_id(self, id):
        sql =  "SELECT * FROM tabla_tsp WHERE id = ?"
        self.cursor.execute(sql,(id,) )
        fila = self.cursor.fetchone()

        filaSolucion = []
        if fila is not None:
            filaSolucion.append(fila[0])                   # id

            filaSolucion.append(pickle.loads(fila[1]))     # grafo
            filaSolucion.append(json.loads(fila[2]))       # colorMap

        else:
            print('No se ha encontrado ninguna formula con dicho id')

        return filaSolucion


    # Obtener lista de todos los grafos almacenados en tabla_tsp
    def get_todos_grafos_tabla_tsp(self):
        sql = "SELECT Grafo FROM tabla_tsp"
        self.cursor.execute(sql)
        filas = self.cursor.fetchall() # Lista de todos los grafos serializados

        listaGrafos = []
        for fila in filas:
            g = fila[0]
            listaGrafos.append(pickle.loads(g))

        return listaGrafos

    # Devuelve una lista con todas las filas(entradas) de la tabla _tsp
    def get_todas_filas_tabla_tsp(self):
        sql = "SELECT * FROM tabla_tsp"
        self.cursor.execute(sql)
        filas = self.cursor.fetchall()

        entradas = []
        for fila in filas:
            nueva_fila = []
            nueva_fila.append(fila[0])                   # id
            nueva_fila.append(pickle.loads(fila[1]))     # grafo
            nueva_fila.append(json.loads(fila[2]))       # colorMap
            entradas.append(nueva_fila)

        return entradas


    # Devuelve el id de la fila que contiene al grafo g.
    # En caso de no contenerlo, devuelve -1
    def is_grafo_in_tabla_tsp(self, g):

        id = -1

        # buscar si existe alguna fila que contenga al grafo
        sql = "SELECT id, Grafo FROM tabla_tsp WHERE Grafo = ?"
        self.cursor.execute(sql, (pickle.dumps(g),))
        fila = self.cursor.fetchone()

        if fila==None:
            return id
        else:
            id = fila[0]
            return id
            

    # Funcion que imprime toda la tabla_tsp en la terminal
    def imprime_tabla(self):
        
        self.cursor.execute("SELECT * FROM tabla_tsp")
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
    # en formato grafico la tabla_tsp
    def mostrar_tabla_tsp(self, ventana_antigua):

        ventana_antigua.destroy()
        
        # Obtener los datos de la tabla
        sql = "SELECT * FROM tabla_tsp"
        self.cursor.execute(sql)
        entradas = self.cursor.fetchall()


        if len(entradas)==0:
            # Caso de tabla vacia

            ventana_error = VentanaPopUp(ventana_padre=None)

            ventana_error.title("No disponible")

            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')

            panel = ctk.CTkFrame(ventana_error, corner_radius=0) 
            panel.pack(fill = "both", expand=True)

            label = ctk.CTkLabel(panel, text='La tabla TSP-DEC se encuentra actualemente vacía.')
            label.grid(row=1,column=0, padx=10, pady=10)

            boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:ventana_error.exit())
            boton_aceptar.grid(row=4, column=0, padx=10, pady=(0,10))

            # Imagen aviso
            bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"), size=(50, 50))
            label = ctk.CTkLabel(panel, image=bg_image, text="")
            label.grid(row=0,column=0, padx=10, pady=10)

            ventana_error.center()

        else:

            # Crear una ventana para mostrar los gráficos
            fig, axs = plt.subplots(len(entradas), 1, figsize=(10, 5*len(entradas)))

            # Recorrer las entradas y mostrar los gráficos
            for i, entrada in enumerate(entradas):

                # Obtengo la info de una fila de la tabla_uhamcycle
                id = entrada[0]
                
                # Obtener los datos del grafo
                grafo = pickle.loads(entrada[1])
                colorMap = json.loads(entrada[2])


                # Dibujar el grafo 1 en el primer subgráfico
                if len(entradas)==1:
                    ax1=axs
                else:
                    ax1 = axs[i]
                ax1.set_title("GRAFO: " + str(id))

                nx.draw_networkx(grafo, ax=ax1, node_color=colorMap)
                
            # Muestro los graficos
            plt.show()