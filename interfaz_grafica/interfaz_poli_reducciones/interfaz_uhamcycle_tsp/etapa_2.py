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
# Clase que engloba la etapa 2 a realizar en la poli-reducción. 
# Se encargar de informar sobre  cómo se calcula el peso del ciclo 
# hamiltoniano del grafo generado.
#########################################################################
class Etapa2(Etapa):

    def __init__(self, ventana, gestor_etapas):
        
        super().__init__(ventana, gestor_etapas)

        self.panel_peso = None

    ### Getters ###

    def get_panel_2(self):
        return self.panel_2

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

            self.gestor_etapas.get_etapa(1).get_panel_1().pack_forget()

            # Si la etapa está realizada, la mostramos
            if self.etapa_realizada == True:
                self.panel_2.pack(padx=10, pady=10, fill="both", expand=True)

            else:
                self.etapa_realizada = True

                self.panel_2 = ctk.CTkFrame(self.ventana, corner_radius = 0)
                self.panel_2.pack(fill="both", expand=True)


                lista_texto = []
                texto = "Claramente, la reducción f, ante un grafo dado G=(V,E), genera un G'=(V',E') con un ciclo\n "\
                        "hamiltoniano con peso (p):\n\n"\
                        "       p = 1 x (número de aristas del grafo G) + 2 x (número de aristas añadidas a G' al completarlo)"
                
                lista_texto.append(texto)
                
                texto= "Si G ∈ UHAMCYCLE, entonces contiene un ciclo hamiltoniano de por sí, y el grafo generado por\n"\
                        "la reducción f, G', poseerá ese mismo ciclo hamiltoniano pesado con peso:\n\n"\
                        "                         \t\t\t\t  p = |V| + 2 x 0 = |V| = k"
                lista_texto.append(texto)

                texto = "Sin embargo, si G no pertenece a UHAMCYCLE, G  no posee un ciclo hamiltoniano; aunque el grafo\n"\
                        "G' si que lo contendrá. Ahora bien, este ciclo hamiltoniano estará compuesto por aristas \n"\
                        "pertenecientes a la completación de G, que, al tener peso 2, hacen que el peso total del \n"\
                        "ciclo hamiltoniano sea superior al valor k."
                lista_texto.append(texto)
                
                
                panel_info = ctk.CTkFrame(self.panel_2)
                panel_info.pack(padx=10, pady=(10,0))

                canvas = tk.Canvas(panel_info, width=40, height=185)
                canvas.configure(bg='#63BCE9')
                canvas.pack(side="left", padx=(10,0), pady=10)
                canvas.create_text(20, 150, text="Etapa " + str(2) ,angle=90, anchor="w", font=('Arial', 15,'bold'))

                num_pasos = len(lista_texto)
                
                panel_pasos = ctk.CTkTabview(panel_info, height=60, width=100)
                panel_pasos.pack(side="top",padx=10, pady=10, fill="both")

                for paso in range (1, num_pasos+1):
                    panel_pasos.add("Paso " + str(paso) + "º")

                    textbox = ctk.CTkTextbox(panel_pasos.tab("Paso " + str(paso) + "º"), width=750, height= 100)
                    textbox.insert("1.0", lista_texto[paso-1])
                    textbox.configure(state="disabled")
                    textbox.pack(padx=5, pady=10)
                
                
                # Creo un segundo panel donde imprimo el valor del peso del ciclo hamiltoniano:
                self.crear_panel_peso_ciclo()

                panel_botones_1 = ctk.CTkFrame(self.panel_2)
                panel_botones_1.pack(padx=10, pady=(5,0), fill=tk.Y, side='bottom')

                panel_botones_1_1 = ctk.CTkFrame(panel_botones_1, fg_color=("gray81", "gray20"))
                panel_botones_1_1.grid(row=0, column=1, padx=0, pady=5)

                self.panel_botones_1_1 = panel_botones_1_1


                boton_anterior= ctk.CTkButton(panel_botones_1, text="Anterior", command=lambda:self.gestor_etapas.anterior(1))
                boton_anterior.grid(row=0, column=0, padx=10, pady=10)

                boton_siguiente = ctk.CTkButton(panel_botones_1, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(3))
                boton_siguiente.grid(row=0, column=2, padx=10, pady=10)
    

    # Creo el panel donde imprimo el valor del peso del ciclo
    def crear_panel_peso_ciclo(self):
        
        if self.panel_peso != None:
            self.panel_peso.pack_forget()
        
        # Creo el panel_peso (general)
        self.panel_peso = ctk.CTkFrame(self.panel_2, width=800, height=300)
        self.panel_peso.pack(padx=10, pady=10, fill="both", expand=True)

        # Creo el panel_info dentro del panel_peso donde escribiré la solución
        panel_info = ctk.CTkFrame(self.panel_peso)
        panel_info.pack(padx=10, pady=(10,0))

        # Creo la etiqeuta izquierda que pone: Solucion
        canvas = tk.Canvas(panel_info, width=40, height=185)
        canvas.configure(bg='#63BCE9')
        canvas.pack(side="left", padx=(10,0), pady=10)
        canvas.create_text(20, 150, text="Solución" ,angle=90, anchor="w", font=('Arial', 15,'bold'))


        lista_texto = []
        if self.gestor_etapas.is_grafo_inicial_con_ch():
            # El grafo inicial tenia un ciclo hamiltoniano
            texto = "En nuestro caso, el grafo inicial (no dirigido) sí que contenia un ciclo hamiltoniano; es decir,\nG ∈ UHAMCYCLE y," \
                    " por tanto, el peso del ciclo hamiltoniano es p = " + str(self.gestor_etapas.get_numNodos())
            lista_texto.append(texto)
        else:
            # El grafo inicial no tenia un ciclo hamiltoniano
            texto = "En nuestro caso, el grafo inicial (no dirigido) no contenia un ciclo hamiltoniano; es decir,\nG ∉ UHAMCYCLE y," \
                    " por tanto, el peso del ciclo hamiltoniano  p será mayor que k, ya que el ciclo usará\naristas de peso 2."
            lista_texto.append(texto)
        
        
        num_pasos = len(lista_texto)
                
        panel_pasos = ctk.CTkTabview(panel_info, height=60, width=100)
        panel_pasos.pack(side="top",padx=10, pady=10, fill="both")

        for paso in range (1, num_pasos+1):
            panel_pasos.add("Paso " + str(paso) + "º")

            textbox = ctk.CTkTextbox(panel_pasos.tab("Paso " + str(paso) + "º"), width=750, height= 100)
            textbox.insert("1.0", lista_texto[paso-1])
            textbox.configure(state="disabled")
            textbox.pack(padx=5, pady=10)