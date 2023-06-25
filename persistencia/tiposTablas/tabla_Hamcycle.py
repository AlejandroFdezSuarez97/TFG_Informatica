import json
import networkx as nx
import pickle
from persistencia.tiposTablas.tabla import Tabla
import matplotlib.pyplot as plt

from interfaz_grafica.interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp
from PIL import Image
import customtkinter as ctk


##############################################################################
# Clase que engloba el tipo de tabla_Hamcycle.
##############################################################################

class Tabla_hamycle(Tabla):

    # Constructor
    def __init__(self, bd):
        
        super().__init__(bd)

        self.cargar_tabla_hamcycle()
    


    ###############################################
    ############ CREACIÓN DE LA TABLA  ############
    ###############################################

    # Funcion para crear/cargar la tabla_hamcycle
    def cargar_tabla_hamcycle(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS tabla_hamcycle (
                            id INTEGER PRIMARY KEY,
                            GrafoHampath INTEGER,
                            Grafo BLOB,
                            Posiciones TEXT,
                            ColorMap TEXT,
                            EdgeMap TEXT,
                            GrosorArcos TEXT,
                            CicloHamiltoniano INTEGER
                            )
                    ''')

    ###############################################
    ######### ANADIR ENTRADAS A LA TABLA ##########
    ###############################################    

    # Funcion que almacena una entrada en la tabla_hamcycle
    # Debo serializar la mayoria de sus parametro, por lo que debo tener cuidado a la hora de 
    # sacarlos de la BD.
    def anadir_fila_tabla_hamcycle(self, id, id_grafoHampath, grafo, pos, colorMap, edgeMap, grosorArcos, cicloHamiltoniano):

        sql = "INSERT INTO tabla_hamcycle (id, GrafoHampath, Grafo, Posiciones, ColorMap, EdgeMap, GrosorArcos, CicloHamiltoniano) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"    


        # Transformamos todos los datos para poder almacenarlos en la base de datos
        grafo_serializado = pickle.dumps(grafo)
        posiciones = json.dumps(pos)
        colorMap_serializado = json.dumps(colorMap)
        edgeMap_serializado = json.dumps(edgeMap)
        grosorArcos_serializado = json.dumps(grosorArcos)
        
        # Anado la fila a la tabla
        self.cursor.execute(sql, (id, id_grafoHampath, grafo_serializado, posiciones, colorMap_serializado, edgeMap_serializado, grosorArcos_serializado, cicloHamiltoniano))


        # Guardo los cambios en la base de datos
        self.conexion.commit()


    ###############################################
    ####### EXTRAER ENTRADAS DE LA TABLA ##########
    ###############################################

    # Funcion que sirve para extaer una fila de la tabla_hamcycle
    def extaer_fila_tabla_hamcycle_por_id(self, id):
        sql =  "SELECT * FROM tabla_hamcycle WHERE id = ?"
        self.cursor.execute(sql,(id,) )
        fila = self.cursor.fetchone()

        filaSolucion = []
        if fila is not None:
            filaSolucion.append(fila[0])                   # id
            filaSolucion.append(fila[1])                   # id_grafoHampath

            filaSolucion.append(pickle.loads(fila[2]))     # grafo
            filaSolucion.append(json.loads(fila[3]))       # posiciones
            filaSolucion.append(json.loads(fila[4]))       # colorMap
            filaSolucion.append(json.loads(fila[5]))       # edgeMap
            filaSolucion.append(json.loads(fila[6]))       # grosorArcos
            filaSolucion.append(fila[7])                   # CicloHamiltoniano

            
        else:
            print('No se ha encontrado ninguna formula con dicho id')

        return filaSolucion


    # Obtener lista de todos los grafos almacenados en tabla_hamcycle
    # Identificandolos sólo en base a su grafo3 (sin tener en cuenta 
    # el grafo hampath)
    def get_todos_grafos3_tabla_hamcycle(self):
        sql = "SELECT Grafo FROM tabla_hamcycle"
        self.cursor.execute(sql)
        filas = self.cursor.fetchall() # Lista de todos los grafos serializados

        listaGrafos = []
        for fila in filas:
            g = fila[0]
            listaGrafos.append(pickle.loads(g))

        return listaGrafos

    # Devuelve una lista con todas las filas(entradas) de la tabla hamcycle
    def get_todas_filas_tabla_hamcycle(self):
        sql = "SELECT * FROM tabla_hamcycle"
        self.cursor.execute(sql)
        filas = self.cursor.fetchall()

        entradas = []
        for fila in filas:
            nueva_fila = []
            nueva_fila.append(fila[0])                   # id
            nueva_fila.append(fila[1])                   # id_grafoHampath

            nueva_fila.append(pickle.loads(fila[2]))     # grafo
            nueva_fila.append(json.loads(fila[3]))       # posiciones
            nueva_fila.append(json.loads(fila[4]))       # colorMap
            nueva_fila.append(json.loads(fila[5]))       # edgeMap
            nueva_fila.append(json.loads(fila[6]))       # grosorArcos
            nueva_fila.append(fila[7])                   # CicloHamiltoniano
            entradas.append(nueva_fila)

        return entradas


    # Devuelve el id de la fila que contiene al grafo g.
    # En caso de no contenerlo, devuelve -1
    def is_grafo_in_tabla_hamcycle(self, id_hampath, g):

        id = -1

        # buscar si existe alguna fila que contenga al grafo y coincida el id_hampath
        sql = "SELECT id, GrafoHampath, Grafo FROM tabla_hamcycle WHERE GrafoHampath = ? AND Grafo = ?"
        self.cursor.execute(sql, (id_hampath, pickle.dumps(g),))
        fila = self.cursor.fetchone()

        if fila==None:
            return id
        else:
            print('El valor del id')
            id = fila[0]
            return id
            

    # Funcion que imprime toda la tabla_hamcycle en la terminal
    def imprime_tabla(self):
        
        self.cursor.execute("SELECT * FROM tabla_hamcycle")
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
    # en formato grafico la tabla_hamcycle
    def mostrar_tabla_hamcycle(self, ventana_antigua):

        ventana_antigua.destroy()
        
        # Obtener los datos de la tabla
        sql = "SELECT * FROM tabla_hamcycle"
        self.cursor.execute(sql)
        entradas = self.cursor.fetchall()


        if len(entradas)==0:
            # Caso de tabla vacia

            ventana_error = VentanaPopUp(ventana_padre=None)

            ventana_error.title("No disponible")

            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')

            panel = ctk.CTkFrame(ventana_error, corner_radius=0) 
            panel.pack(fill = "both", expand=True)

            label = ctk.CTkLabel(panel, text='La tabla hamcycle se encuentra actualemente vacía.')
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

                # Obtengo la info de una fila de la tabla_hamcycle
                id = entrada[0]
                id_hampath = entrada[1]
                
                # Obtener los datos del grafo
                grafo_3 = pickle.loads(entrada[2])
                posiciones_3 = json.loads(entrada[3])
                colorMap_3 = json.loads(entrada[4])
                edgeMap_3 = json.loads(entrada[5])
                grosorAristas_3 = json.loads(entrada[6])
                
                # Dibujar el grafo 1 en el primer subgráfico
                if len(entradas)==1:
                    ax1=axs
                else:
                    ax1 = axs[i]
                ax1.set_title("GRAFO: " + str(id))

                if id_hampath==-1:
                    # No se ha usado ningún grafo hampath
                    # Pinto solo el grafo almacenado en esta tabla

                    nx.draw_networkx(grafo_3, ax=ax1, node_color=colorMap_3, edge_color=edgeMap_3,   
                                width=grosorAristas_3)
            
                else:
                    
                    # Necesito sacar la info del grafo hampath del que parte
                    fila_grafoHampath = self.bd.get_tabla_hampath().get_fila_tabla_hampath_por_id(id_hampath)
                    
                    # 1º Grafo
                    (grafo, posicionesGrafo1, etiquetas, color_map, edge_colors, posiciones_s_t) = fila_grafoHampath[2:8]
                    nx.draw_networkx(grafo,ax=ax1,labels=etiquetas, pos=posicionesGrafo1, node_color=color_map, 
                                    edge_color=edge_colors, node_size=190,font_size=6)
                    

                    # 2º Grafo
                    (grafo, posicionesGrafo2, etiquetas, color_map, edge_colors, posiciones_s_t) = fila_grafoHampath[8:14]

                    nx.draw_networkx(grafo,ax=ax1,labels=etiquetas, pos=posicionesGrafo2, node_color=color_map, 
                                    edge_color=edge_colors, node_size=190,font_size=6, connectionstyle = 'arc3, rad=0.4')


                    # 3º Grafo
                    nx.draw_networkx(grafo_3, ax=ax1, pos=posiciones_3, node_color=colorMap_3, edge_color=edgeMap_3,
                                width=grosorAristas_3, node_size=190, font_size=6)
                
            
            # Muestro los graficos
            plt.show()