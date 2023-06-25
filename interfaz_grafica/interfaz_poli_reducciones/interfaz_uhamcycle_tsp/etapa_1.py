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
# Se encargar de transformar el grafo inicial (no dirigido) en uno nuevo
# de manera que sea compelto y con peso.
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

        # Si no hay grafo, mostramos mensaje de error
        if self.gestor_etapas.get_grafo_inicial() == None:

            ventana_error = VentanaPopUp(self.ventana)
            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
            ventana_error.title(" ")

            panel_error = ctk.CTkFrame(ventana_error, corner_radius = 0)
            panel_error.pack()

            # Imagen error
            imagen_error = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"),size=(50, 50))
            label = ctk.CTkLabel(panel_error, image=imagen_error, text="")
            label.grid(row=0,column=0, padx=10, pady=10)

            label = ctk.CTkLabel(panel_error, text = 'Selecciona el grafo para comenzar \n la poli-reducción.')
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
                texto = "Partiendo del grafo no dirigido G=(V,E), vamos a crear un nuevo grafo G'=(V',E') no dirigido,\n completo y con peso.\n" \
                        "Para ello, debemos de seguir los siguientes pasos:\n\n"\
                        "G' tendrá los mismos nodos que G; es decir, V=V'."
                lista_texto.append(texto)
                
                texto= "Como el grafo G' ha de ser completo, añadimos todas las aristas que falten para completarlo."
                lista_texto.append(texto)

                texto = "La funcion de peso h asignará el peso correspondiente a cada arista de G'. La forma de hacerlo será:\n"\
                        "      Si la arista e ∈ E, entonces h(e) = 1\n"\
                        "      Si la arista e ∈ E'-E, entonces h(e)=2\n\n"\
                        "Para finalizar, se establece el valor de k = |V|"
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

                    textbox = ctk.CTkTextbox(panel_pasos.tab("Paso " + str(paso) + "º"), width=750, height= 100)
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
                    self.crear_panel_grafo_nuevo(self.crear_grafo(True))
                
                else:
                    # Modificamos el grafo partiendo del grafo previo
                    self.crear_panel_grafo_nuevo(self.crear_grafo(False))

                boton_anterior= ctk.CTkButton(panel_botones_1, text="Anterior", command=lambda:self.gestor_etapas.anterior(0.2))
                boton_anterior.grid(row=0, column=0, padx=10, pady=10)

                boton_siguiente = ctk.CTkButton(panel_botones_1, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(2))
                boton_siguiente.grid(row=0, column=2, padx=10, pady=10)
    

    # Crea el grafo con el ciclo hamiltoniano.
    def crear_grafo(self, nuevo):

        if nuevo:
            # Cargamos el grafo inicial
            grafo_inicial = self.gestor_etapas.get_grafo_inicial()[0]
        else:
            lista = self.gestor_etapas.get_grafo_inicial()[0] #En este caso guardo (id,grafo,colorMap)
            grafo_inicial = lista[1]

        # Guardo el numero de nodos del grafo
        self.gestor_etapas.set_numNodos(grafo_inicial.number_of_nodes())
        

        # Asignar peso 1 a las aristas existentes
        for u, v in grafo_inicial.edges():
            grafo_inicial[u][v]['weight'] = 1
        
        # Completar el grafo agregando aristas con peso 2
        nodes = grafo_inicial.nodes()
        for u in nodes:
            for v in nodes:
                if u != v and not grafo_inicial.has_edge(u, v):
                    grafo_inicial.add_edge(u, v, weight=2)
        
        return grafo_inicial
    
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
        
        colores = {}
        letras = set(nodos)
        colores_disponibles = ['red', '#87CEFA', 'green', 'yellow', 'orange', 'purple']

        # Ajustar la longitud de colores_disponibles si es necesario
        if len(colores_disponibles) < len(letras):
            colores_disponibles = list(itertools.islice(itertools.cycle(colores_disponibles), len(letras)))
        
        for letra, color in zip(letras, colores_disponibles):
            colores[letra] = color
        
        # Representar el grafo con los colores asignados
        color_map = [colores[nodo] for nodo in grafo.nodes()]

        nx.draw_networkx(grafo, ax=axis, node_color=color_map)

        # -------------------------- Pensar que parametros guardo en la base de datos ----------------
        grafo_final = [grafo, color_map]
        self.gestor_etapas.set_grafo_final(grafo_final)
        # --------------------------------------------------------------------------------------------

        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(fig, self.panel_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    

        
  
