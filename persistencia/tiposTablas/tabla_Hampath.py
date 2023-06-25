import json
import networkx as nx
import pickle
from interfaz_grafica.interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp
from persistencia.tiposTablas.tabla import Tabla
import matplotlib.pyplot as plt
from PIL import Image
import customtkinter as ctk



##############################################################################
# Clase que engloba el tipo de tabla_Hampah.
##############################################################################

class Tabla_hampath(Tabla):

    # Constructor
    def __init__(self, bd):
        
        super().__init__(bd)

        self.cargar_tabla_hampath()
    


    ###############################################
    ############ CREACIÓN DE LA TABLA  ############
    ###############################################

    # Funcion para crear/cargar la tabla_hampath
    def cargar_tabla_hampath(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS tabla_hampath (
                            id INTEGER PRIMARY KEY,
                            Camino_hamiltoniano INTEGER,
                            Grafo_1 BLOB,
                            Posiciones_grafo_1 TEXT,
                            Etiquetas_grafo_1 TEXT,
                            ColorMap_grafo_1 TEXT,
                            EdgeMap_grafo_1 TEXT,
                            PosicionesNodos_ST_grafo_1 TEXT,
                            Grafo_2 BLOB,
                            Posiciones_grafo_2 TEXT,
                            Etiquetas_grafo_2 TEXT,
                            ColorMap_grafo_2 TEXT,
                            EdgeMap_grafo_2 TEXT,
                            PosicionesNodos_ST_grafo_2 TEXT
                            )
                    ''')

    ###############################################
    ######### ANADIR ENTRADAS A LA TABLA ##########
    ###############################################    

    # Funcion que almacena una entrada en la tabla_hampath
    # Debo serializar la mayoria de sus parametro, por lo que debo tener cuidado a la hora de 
    # sacarlos de la BD.
    def anadir_fila_tabla_hampath(self, id, caminoHamiltoniano, 
                          grafo1, posicionesGrafo1, etiquetasgrafo1, colorMapGrafo1, edgeMapGrafo1, posicionesSTGrafo1,
                          grafo2, posicionesGrafo2, etiquetasgrafo2, colorMapGrafo2, edgeMapGrafo2, posicionesSTGrafo2):

        sql = "INSERT INTO tabla_hampath (id, Camino_hamiltoniano, Grafo_1, Posiciones_grafo_1, Etiquetas_grafo_1, ColorMap_grafo_1, EdgeMap_grafo_1, PosicionesNodos_ST_grafo_1, Grafo_2, Posiciones_grafo_2, Etiquetas_grafo_2, ColorMap_grafo_2, EdgeMap_grafo_2, PosicionesNodos_ST_grafo_2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"    


        # Transformamos todos los datos para poder almacenarlos en la base de datos
        grafo1_json = pickle.dumps(grafo1)
        posicionesGrafo1_json = json.dumps(posicionesGrafo1)
        etiquetasGrafo1_json = json.dumps(etiquetasgrafo1)
        colorMap_grafo1_json = json.dumps(colorMapGrafo1)
        edgeMap_grafo1_json = json.dumps(edgeMapGrafo1)
        posicionesST_grafo1_json = str(posicionesSTGrafo1)


        
        grafo2_json = pickle.dumps(grafo2)
        posicionesGrafo2_json = json.dumps(posicionesGrafo2)
        etiquetasGrafo2_json = json.dumps(etiquetasgrafo2)
        colorMap_grafo2_json = json.dumps(colorMapGrafo2)
        edgeMap_grafo2_json = json.dumps(edgeMapGrafo2)
        posicionesST_grafo2_json = str(posicionesSTGrafo2)



        # Anado la fila a la tabla
        self.cursor.execute(sql, (id, caminoHamiltoniano, 
                                  grafo1_json, posicionesGrafo1_json, etiquetasGrafo1_json, colorMap_grafo1_json, edgeMap_grafo1_json, posicionesST_grafo1_json,
                                  grafo2_json, posicionesGrafo2_json, etiquetasGrafo2_json, colorMap_grafo2_json, edgeMap_grafo2_json, posicionesST_grafo2_json))


        # Guardo los cambios en la base de datos
        self.conexion.commit()


    ###############################################
    ####### EXTRAER ENTRADAS DE LA TABLA ##########
    ###############################################

    # Funcion que sirve para extaer una fila de la tabla_hampath
    def get_fila_tabla_hampath_por_id(self, id):
        sql =  "SELECT * FROM tabla_hampath WHERE id = ?"
        self.cursor.execute(sql,(id,) )
        fila = self.cursor.fetchone()

        filaSolucion = []
        if fila is not None:
            filaSolucion.append(fila[0])                   # id
            filaSolucion.append(fila[1])                   # caminoHamiltoniano

            filaSolucion.append(pickle.loads(fila[2]))     # grafo1
            filaSolucion.append(json.loads(fila[3]))       # posiciones
            filaSolucion.append(json.loads(fila[4]))       # Etiquetas
            filaSolucion.append(json.loads(fila[5]))       # colorMap
            filaSolucion.append(json.loads(fila[6]))       # edgeMap
            filaSolucion.append(eval(fila[7]))             # posiciones_nodos_st

            
            filaSolucion.append(pickle.loads(fila[8]))     # grafo2
            filaSolucion.append(json.loads(fila[9]))       # posiciones
            filaSolucion.append(json.loads(fila[10]))      # Etiquetas
            filaSolucion.append(json.loads(fila[11]))      # colorMap
            filaSolucion.append(json.loads(fila[12]))      # edgeMap
            filaSolucion.append(eval(fila[13]))            # posiciones_nodos_st
            
        else:
            print('No se ha encontrado ninguna formula con dicho id')

        return filaSolucion

    # Funcion que devuelve todos los grafos hampath almacenados 
    # Devuelve una lista de pares (grafo1,grafo2)
    def get_todos_grafos_tabla_hampath(self):

        sql = "SELECT Grafo_1,Grafo_2 FROM tabla_hampath"
        self.cursor.execute(sql)
        grafos = self.cursor.fetchall()
        
        lista_grafos = []
        # Devuelvo los grafos a su estado original para poder compararlos:
        for tupla in grafos:
            g1 = pickle.loads(tupla[0])
            g2 = pickle.loads(tupla[1])
            lista_grafos.append((g1,g2))


        return lista_grafos

    # Devuelve el id de la fila que contiene al grafo G=(G1,G2)  pasados como argumento (Son objeto grafo)
    # En caso de no encontrarse, devuelve id = -1
    def is_grafo_in_tabla_hampath(self, grafo1, grafo2):

        lista_grafos = self.get_todos_grafos_tabla_hampath()

        id = -1

        for (g1,g2) in lista_grafos:
            # Si encuentro una fila que coincida con grafo1 y grafo2, obtengo su id
            if (nx.is_isomorphic(g1, grafo1)) and (nx.is_isomorphic(g2, grafo2)):
                print('El nuevo grafo ya estaba almacenado en la BD')
                

                self.cursor.execute("SELECT * FROM tabla_hampath")
                filas = self.cursor.fetchall()

                for fila in filas:
                    id = fila[0]
                    grafo1_deserializado = pickle.loads(fila[2])
                    grafo2_deserializado = pickle.loads(fila[8])
                    if nx.is_isomorphic(grafo1, grafo1_deserializado) and nx.is_isomorphic(grafo2, grafo2_deserializado):
                        return id
                '''# Devuelvo la fila asociada a dicho grafo
                sql = "SELECT id FROM tabla_hampath WHERE Grafo_1 = ? and Grafo_2 = ?"
                gr1 = pickle.dumps(grafo1)
                gr2 = pickle.dumps(grafo2)
                self.cursor.execute(sql, (gr1, gr2))
                fila = self.cursor.fetchone()
                if fila==None:
                    print('No se ha encontrado ninguna fila en tabla_hampath con ese grafo')
                else:
                    id = fila[0]
                break'''
            
        return id


    # Funcion que devuelve una lista con los id's de los grafos que contienen o no camino hamiltoniano
    # en base al parametro pasado como argumento
    # Si conCamino = 0 -> Buscar los grafos que no contienen camino hamiltoniano
    # Si conCamino = 1 -> Buscar los grafos que contienen camino hamiltoniano
    def get_grafos_por_caminoHamiltoniano(self, conCamino):
        sql =  "SELECT id FROM tabla_hampath WHERE Camino_hamiltoniano = ?"
        self.cursor.execute(sql,(conCamino,) )
        fila = self.cursor.fetchall()

        solucion = []
        if fila== None:
            print('No hemos encontrado un grafo con esas caracteristicas')
        else:
            solucion.extend(item[0] for item in fila)
        return solucion

    # Funcion que devuelve toda la tabla_hampath
    def imprime_tabla(self):
        
        self.cursor.execute("SELECT * FROM tabla_hampath")
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
    # en formato grafico la tabla_hampath
    def mostrar_tabla_hampath(self, ventana_antigua):

        ventana_antigua.destroy()
        
        # Obtener los datos de la tabla
        sql = "SELECT * FROM tabla_hampath"
        self.cursor.execute(sql)
        entradas = self.cursor.fetchall()


        if len(entradas)==0:
            # Caso de tabla vacia

            ventana_error = VentanaPopUp(ventana_padre=None)

            ventana_error.title("No disponible")

            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')

            panel = ctk.CTkFrame(ventana_error, corner_radius=0) 
            panel.pack(fill = "both", expand=True)

            label = ctk.CTkLabel(panel, text='La tabla hampath se encuentra actualemente vacía.')
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

                # Obtengo la info de la base de datos
                id = entrada[0]

                # Obtener los datos del grafo_1
                grafo_1 = pickle.loads(entrada[2])
                posiciones_grafo_1 = json.loads(entrada[3])
                etiquetas_grafo_1 = json.loads(entrada[4])
                colorMap_grafo_1 = json.loads(entrada[5])
                edgeMap_grafo_1 = json.loads(entrada[6])

                # Obtengo los datos del grafo_2
                grafo_2 =  pickle.loads(entrada[8])
                posiciones_grafo_2 = json.loads(entrada[9])
                etiquetas_grafo_2 = json.loads(entrada[10])
                colorMap_grafo_2 = json.loads(entrada[11])
                edgeMap_grafo_2 = json.loads(entrada[12])

                # Dibujar el grafo 1 en el primer subgráfico
                if len(entradas)==1:
                    ax1=axs
                else:
                    ax1 = axs[i]
                ax1.set_title("GRAFO: " + str(id))

                if posiciones_grafo_1=={}:
                    nx.draw_networkx(grafo_1, ax=ax1)

                else:
                    # Aquí puedes utilizar los datos del grafo para dibujarlo utilizando Matplotlib
                    # Grafica el grafo
                    nx.draw_networkx(grafo_1, ax=ax1, labels=etiquetas_grafo_1, pos=posiciones_grafo_1, edge_color = edgeMap_grafo_1, node_color=colorMap_grafo_1,
                                    node_size=200,font_size=6,width=1.5)

                    nx.draw_networkx(grafo_2, ax=ax1, labels=etiquetas_grafo_2, pos=posiciones_grafo_2, edge_color = edgeMap_grafo_2, node_color=colorMap_grafo_2,
                                node_size=200,font_size=6,width=1.5)
            
            # Muestro los graficos
            plt.show()
