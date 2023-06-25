from itertools import cycle
import itertools
import tkinter as tk
import customtkinter as ctk

import networkx as nx
from matplotlib.figure import Figure
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import string

from ...interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp

from .etapa import Etapa

#########################################################################
# Clase que engloba la etapa 1 a realizar en la poli-reducción. 
# Se encarga de transformar el grafo seleccionado en la etapa anterior
# en un grafo no dirigido.
#########################################################################
class Etapa1(Etapa):

    def __init__(self, ventana, gestor_etapas):
        
        super().__init__(ventana, gestor_etapas)

        self.panel_grafo = None

    ### Getters ###

    def get_panel_1(self):
        return self.panel_1

    ### Lanzador de etapa ###

    def lanzar_etapa(self):

        # Si no hay grafo hamiltoniano, mostramos mensaje de error
        if self.gestor_etapas.get_grafo_dirigido() == None:

            ventana_error = VentanaPopUp(self.ventana)
            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
            ventana_error.title(" ")

            panel_error = ctk.CTkFrame(ventana_error, corner_radius = 0)
            panel_error.pack()

            # Imagen error
            imagen_error = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"),size=(50, 50))
            label = ctk.CTkLabel(panel_error, image=imagen_error, text="")
            label.grid(row=0,column=0, padx=10, pady=10)

            label = ctk.CTkLabel(panel_error, text = 'Selecciona el grafo hamiltoniano para comenzar \n la poli-reducción.')
            label.grid(row=1, column=0, padx=10, pady=10)

            boton_aceptar = ctk.CTkButton(panel_error, text="Aceptar", command=lambda:ventana_error.exit())
            boton_aceptar.grid(row=2, column=0, padx=10, pady=10)

            ventana_error.center()

        else:

            self.gestor_etapas.get_etapa(0).get_panel_0_2().pack_forget()

            # Si la etapa está realizada, la mostramos
            if self.etapa_realizada == True:
                self.panel_1.pack(padx=10, pady=10, fill="both", expand=True)

            else:
                self.etapa_realizada = True

                self.panel_1 = ctk.CTkFrame(self.ventana, corner_radius = 0)
                self.panel_1.pack(fill="both", expand=True)


                lista_texto = []
                texto = "Partiendo del grafo dirigido anterior G=(V,E), vamos a crear un nuevo grafo G'=(V',E') no dirigido.\n" \
                        "Para ello, debemos de seguir los siguientes pasos:\n"
                lista_texto.append(texto)
                
                texto= "Por cada vértice v ∈ V, creamos los vértices v0, v1, v2 ∈ V' así como las aristas: (v0,v1),(v1,v2) ∈ E'"
                lista_texto.append(texto)

                texto = "Cada vértice de V ha sido transformado en una terna V' donde el 0 significa entrada y el 2 significa salida."
                lista_texto.append(texto)
                
                texto = "Para cada arista dirigida (u,v) ∈ E, creamos la arista no dirigida (u2,v0) ∈ E'; que representa que \n"\
                        "se sale del nodo u y se llega al nodo v."
                lista_texto.append(texto)

                if self.gestor_etapas.get_grafo_dirigido_con_ch():
                    texto = "Para finalizar, como el grafo dirigido sí que tenía un ciclo hamiltoniano, el grafo no dirigido\n también lo tendrá."    
                else:
                    texto = "Para finalizar, como el grafo dirigido no tenía un ciclo hamiltoniano, el grafo no dirigido\n tampoco lo tendrá."
                    
                lista_texto.append(texto)

                panel_info = ctk.CTkFrame(self.panel_1)
                panel_info.pack(padx=10, pady=(10,0))

                canvas = tk.Canvas(panel_info, width=40, height=185)
                canvas.configure(bg='#63BCE9')
                canvas.pack(side="left", padx=(10,0), pady=10)
                canvas.create_text(20, 150, text="Etapa " + str(1) ,angle=90, anchor="w", font=('Arial', 15,'bold'))

                num_pasos = len(lista_texto)
                
                panel_pasos = ctk.CTkTabview(panel_info, height=60, width=100)
                panel_pasos.pack(side="top",padx=10, pady=10, fill="both")

                for paso in range (1, num_pasos+1):
                    panel_pasos.add("Paso " + str(paso) + "º")

                    textbox = ctk.CTkTextbox(panel_pasos.tab("Paso " + str(paso) + "º"), width=700, height= 100)
                    textbox.insert("1.0", lista_texto[paso-1])
                    textbox.configure(state="disabled")
                    textbox.pack(padx=5, pady=10)
                
                
        
                panel_botones_1 = ctk.CTkFrame(self.panel_1)
                panel_botones_1.pack(padx=10, pady=(5,10), fill=tk.Y, side='bottom')

                panel_botones_1_1 = ctk.CTkFrame(panel_botones_1, fg_color=("gray81", "gray20"))
                panel_botones_1_1.grid(row=0, column=1, padx=0, pady=5)

                self.panel_botones_1_1 = panel_botones_1_1

                # Modificar el grafo 
                if not self.gestor_etapas.get_grafo_previo_escogido():
                    # caso en el que no tenemos grafo previo
                    self.crear_panel_grafo_nuevo(self.crear_grafo())
                
                else:
                    # Modificamos el grafo partiendo del grafo previo
                    self.crear_panel_grafo_nuevo(self.crear_grafo_1())

                boton_anterior= ctk.CTkButton(panel_botones_1, text="Anterior", command=lambda:self.gestor_etapas.anterior(0.2))
                boton_anterior.grid(row=0, column=0, padx=10, pady=10)

                boton_siguiente = ctk.CTkButton(panel_botones_1, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(2))
                boton_siguiente.grid(row=0, column=2, padx=10, pady=10)
    
    #############################################################
    ################ CASO GRAFO NO TIENE PREVIO #################
    #############################################################

    # Crea el grafo con el ciclo hamiltoniano.
    def crear_grafo(self):

        # Cargamos el grafo inicial
        grafoDirigido = self.gestor_etapas.get_grafo_dirigido()[0]

        # Creamos el nuevo grafo no dirigido
        grafo_noDirigido = nx.Graph()

        # Creamos los nuevos nodos y las aristas entre dichos nodos
        for nodo in grafoDirigido.nodes(data=True):

            # Obtengo el nombre del nodo
            node_name =nodo[1]['name']

            # Creo los nuevos nodos v0,v1 y v2
            clave0 = node_name+str(0)
            clave1 = node_name+str(1)
            clave2 = node_name+str(2)

            grafo_noDirigido.add_node(clave0)
            grafo_noDirigido.add_node(clave1)
            grafo_noDirigido.add_node(clave2)

            # Añado la arista (v0,v1) y (v1,v2)
            grafo_noDirigido.add_edge(clave0, clave1)
            grafo_noDirigido.add_edge(clave1, clave2)


        # Para cada arista (u,v) original, añadimos la arista (u2,v0)
        for u,v in grafoDirigido.edges():
            # -- Busco el nodo u2
            nombre_nodo_u = grafoDirigido.nodes[u]['name']
        
            # -- Busco el nodo v0
            nombre_nodo_v = grafoDirigido.nodes[v]['name']
        
            # -- Creo la arista (u2,v0)
            grafo_noDirigido.add_edge(nombre_nodo_u+str(2), nombre_nodo_v+str(0))   

        return grafo_noDirigido
    
    # Crea el panel del nuevo grafo no dirigido.
    def crear_panel_grafo_nuevo(self, grafo):

        if self.panel_grafo != None:
            self.panel_grafo.pack_forget()
        
        self.panel_grafo = ctk.CTkFrame(self.panel_1)
        self.panel_grafo.pack(padx=10, pady=10, fill="both", expand=True)

        fig = Figure(figsize=(5,4), dpi=100)
        axis = fig.add_subplot(111)

        boton_agrandar= ctk.CTkButton(self.panel_botones_1_1, text="Agrandar/guardar\n imagen",
                                    fg_color = ("#70AB94","#4D8871"), hover_color = ("#7FB9A2","#52987C"),
                                    command=lambda:self.gestor_etapas.agrandar_grafo(fig,1))
        boton_agrandar.grid(row=0,column=0, padx=5, pady=5)

        boton_repintar = ctk.CTkButton(self.panel_botones_1_1, text="Repintar grafo",
                                            fg_color = ("#8F61D4","#9A42D5"), hover_color=("#8041A9","#8041A9"),
                                            command=lambda:self.crear_panel_grafo_nuevo(grafo))
        boton_repintar.grid(row=1,column=0, padx=5, pady=(5,5))

        # --------- Mapa de color
        nodos = list(grafo.nodes())
        nombres_originales = [nodo[:-1] for nodo in nodos]

        colores = {}
        letras = set(nombres_originales)
        colores_disponibles = ['#87CEFA', '#98FB98', '#EE82EE', '#FFD700', '#FF69B4', '#C0C0C0']

        # Ajustar la longitud de colores_disponibles si es necesario
        if len(colores_disponibles) < len(letras):
            colores_disponibles = list(itertools.islice(itertools.cycle(colores_disponibles), len(letras)))
        
        for letra, color in zip(letras, colores_disponibles):
            colores[letra] = color
        
        # Representar el grafo con los colores asignados
        color_map = [colores[nodo[:-1]] for nodo in grafo.nodes()]

        nx.draw_networkx(grafo, ax=axis, node_color=color_map)

        # Establezco el grafo_UHamcycle_final (pensar los parametros que quiero almacenar)
        grafo_final = [grafo, color_map]
        self.gestor_etapas.set_grafo_noDirigido(grafo_final)

        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(fig, self.panel_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    ################################################################
    ############ CASO CARGAR GRAFO HAMILTONIANO  PREVIO ############
    ################################################################
    

    # Devuelve un diccionario que asocia a cada entero con un string
    def crear_diccionario_letras(self, numNodos):
        diccionario = {}
        letra = 'a'  # Iniciar con la letra 'a' en minúscula
        count = 1
        
        while count <= numNodos:
            diccionario[count] = letra
            
            # Incrementar la letra
            if letra[-1] == 'z':
                letra += 'a'
            else:
                letra = letra[:-1] + chr(ord(letra[-1]) + 1)
            
            count += 1
        
        return diccionario


    # Funcion que crea el grafo no dirigido en el caso de tener grafo hamcycle previo
    def crear_grafo_noDirigido(self, grafoDirigido):

        # Creamos el nuevo grafo no dirigido
        grafo_noDirigido = nx.Graph()

        # Creamos los nuevos nodos y las aristas entre dichos nodos
        for nodo in grafoDirigido.nodes():

            # Creo los nuevos nodos v0,v1 y v2
            clave0 = nodo+str(0)
            clave1 = nodo+str(1)
            clave2 = nodo+str(2)

            grafo_noDirigido.add_node(clave0)
            grafo_noDirigido.add_node(clave1)
            grafo_noDirigido.add_node(clave2)

            # Añado la arista (v0,v1) y (v1,v2)
            grafo_noDirigido.add_edge(clave0, clave1)
            grafo_noDirigido.add_edge(clave1, clave2)


        # Para cada arista (u,v) original, añadimos la arista (u2,v0)
        for u,v in grafoDirigido.edges():
            grafo_noDirigido.add_edge(u+str(2), v+str(0))   

        return grafo_noDirigido


    # Funcion que crea el grafo no dirigido en el caso de tener grafo hamcycle previo compuesto de 3 grafos
    def crear_grafo_noDirigido_con_3grafos(self, g1, g2, g3):

        # Creamos el nuevo grafo no dirigido
        grafo_noDirigido = nx.Graph()

        # Obtenemos la lista de todos los nodos
        listaNodos = []
        listaNodos.extend(nodo for nodo in g1.nodes())
        listaNodos.extend(nodo for nodo in g2.nodes())
        listaNodos.extend(nodo for nodo in g3.nodes())

        # Creamos los nuevos nodos y las aristas entre dichos nodos
        for nodo in listaNodos:

            # Creo los nuevos nodos v0,v1 y v2
            clave0 = nodo+str(0)
            clave1 = nodo+str(1)
            clave2 = nodo+str(2)

            grafo_noDirigido.add_node(clave0)
            grafo_noDirigido.add_node(clave1)
            grafo_noDirigido.add_node(clave2)

            # Añado la arista (v0,v1) y (v1,v2)
            grafo_noDirigido.add_edge(clave0, clave1)
            grafo_noDirigido.add_edge(clave1, clave2)

        # Para cada arista (u,v) original, añadimos la arista (u2,v0) del grafo g1
        for u,v in g1.edges():
            grafo_noDirigido.add_edge(u+str(2), v+str(0)) 

        # Para cada arista (u,v) original, añadimos la arista (u2,v0) del grafo g2
        for u,v in g2.edges():
            grafo_noDirigido.add_edge(u+str(2), v+str(0))  

        # Para cada arista (u,v) original, añadimos la arista (u2,v0) del grafo g3
        for u,v in g3.edges():
            # -- Creo la arista (u2,v0)
            grafo_noDirigido.add_edge(u+str(2), v+str(0))
        
        return grafo_noDirigido

    # Crea el grafo cargado previamente con el ciclo hamiltoniano.
    def crear_grafo_1(self):

        grafo_noDirigido = nx.Graph()

        # Obtenemos todos los grafos que componen el grafo de la bd
        listaGrafosPrevios = self.gestor_etapas.get_grafo_dirigido()
        if len(listaGrafosPrevios)==1:
            # Caso en el que el grafo previo era hamcycle y no dependía de ningun hampath
            tupla_grafo3 = listaGrafosPrevios[0]

            # Obtenemos la info del grafo dirigido
            (grafo_3, posicion_grafo_3, colorMap_grafo_3, edgeMap_grafo_3, grososArcos_grafo_3) = tupla_grafo3
            grafo_noDirigido = self.crear_grafo_noDirigido(grafo_3)


        else:
            # Caso en el que el hamcycle provenía de un grafo hampath
            tupla_grafo1 = listaGrafosPrevios[0]
            tupla_grafo2 = listaGrafosPrevios[1]
            tupla_grafo3 = listaGrafosPrevios[2]
            
            # obtenemos toda la info de los grafos que componen el grafo de la BD (hamcycle con el hampath)
            (grafo_1, pos_1, etiquetas_1, color_map_1, edge_colors_1, posiciones_s_t_1) = tupla_grafo1
            (grafo_2, pos_2, etiquetas_2, color_map_2, edge_colors_2, posiciones_s_t_2) = tupla_grafo2
            ((grafo_3, posicion_grafo_3, colorMap_grafo_3, edgeMap_grafo_3, grososArcos_grafo_3)) = tupla_grafo3

            grafo_noDirigido = self.crear_grafo_noDirigido_con_3grafos(grafo_1, grafo_2, grafo_3)
    

        return grafo_noDirigido
        
  
