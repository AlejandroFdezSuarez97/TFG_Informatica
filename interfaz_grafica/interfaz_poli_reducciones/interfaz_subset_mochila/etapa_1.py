import itertools
import tkinter as tk
import customtkinter as ctk

import networkx as nx
from matplotlib.figure import Figure
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ...interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp

from .etapa import Etapa

#########################################################################
# Clase que engloba la etapa 1 a realizar en la poli-reducción. 
# Se encarga de obtener la de la tabla anterior el enunciado del nuevo
# problema, es decir, de indicar cual es el conjunto de partida S,
# cuáles son sus pesos y beneficios para cada uno de sus elementos e
# indicar tambien cuál es el valor K y B.
#########################################################################
class Etapa1(Etapa):

    
    def __init__(self, ventana, gestor_etapas):
        
        super().__init__(ventana, gestor_etapas)
        self.panel_tabla = None



    ### Getters ###

    def get_panel_1(self):
        return self.panel_1

    ### Lanzador de etapa ###

    def lanzar_etapa(self):

        # Si no hay tabla inicial, mostramos mensaje de error
        if self.gestor_etapas.get_tabla_inicial() == []:

            ventana_error = VentanaPopUp(self.ventana)
            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
            ventana_error.title(" ")

            panel_error = ctk.CTkFrame(ventana_error, corner_radius = 0)
            panel_error.pack()

            # Imagen error
            imagen_error = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"),size=(50, 50))
            label = ctk.CTkLabel(panel_error, image=imagen_error, text="")
            label.grid(row=0,column=0, padx=10, pady=10)

            label = ctk.CTkLabel(panel_error, text = 'Selecciona una tabla para comenzar \n la poli-reducción.')
            label.grid(row=1, column=0, padx=10, pady=10)

            boton_aceptar = ctk.CTkButton(panel_error, text="Aceptar", command=lambda:ventana_error.exit())
            boton_aceptar.grid(row=2, column=0, padx=10, pady=10)

            ventana_error.center()

        else:

            self.gestor_etapas.get_etapa(0).get_panel_0_2().pack_forget()

            self.etapa_realizada = True

            self.panel_1 = ctk.CTkFrame(self.ventana, corner_radius = 0)
            self.panel_1.pack(fill="both", expand=True)


            lista_texto = []
            texto = "Partiendo de la tabla anterior, vamos a especificar el valor del peso y beneficio de cada uno\n de los elementos del conjunto S"\
                    " así como el beneficio mínimo B\ny el peso máximo K que se quiere alcanzar.\n\n"\
                    " · Para cada elemento de S se asigna un nombre con un  peso y un beneficio igual a su valor decimal.\n"\
                    " · Establecemos los valores de K = B = t."
            lista_texto.append(texto)
      

            panel_info = ctk.CTkFrame(self.panel_1)
            panel_info.pack(padx=10, pady=(10,0))

            canvas = tk.Canvas(panel_info, width=40, height=185)
            canvas.configure(bg='#63BCE9')
            canvas.pack(side="left", padx=(10,0), pady=10)
            canvas.create_text(20, 150, text="Etapa " + str(1) ,angle=90, anchor="w", font=('Arial', 15,'bold'))


            panel_pasos = ctk.CTkTabview(panel_info, height=50, width=500)
            panel_pasos.pack(side="top", padx=10, pady=10, fill="both")

            for paso in range (1, len(lista_texto)+1):
                panel_pasos.add("Paso " + str(paso) + "º")

                textbox = ctk.CTkTextbox(panel_pasos.tab("Paso " + str(paso) + "º"), width=600, height=150)
                textbox.insert("1.0", lista_texto[paso-1])
                textbox.configure(state="disabled")
                textbox.pack(padx=5, pady=10)


            panel_botones_1 = ctk.CTkFrame(self.panel_1)
            panel_botones_1.pack(padx=10, pady=(5,10), fill=tk.Y, side='bottom')

            panel_botones_1_1 = ctk.CTkFrame(panel_botones_1, fg_color=("gray81", "gray20"))
            panel_botones_1_1.grid(row=0, column=1, padx=0, pady=5)

            self.panel_botones_1_1 = panel_botones_1_1

            # Imprimimos la nueva tabla
            self.crear_panel_nueva_tabla(self.crear_nueva_tabla())

            boton_anterior= ctk.CTkButton(panel_botones_1, text="Anterior", command=lambda:self.gestor_etapas.anterior(0.2))
            boton_anterior.grid(row=0, column=0, padx=10, pady=10)

            boton_siguiente = ctk.CTkButton(panel_botones_1, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(2))
            boton_siguiente.grid(row=0, column=2, padx=10, pady=10)
    
    

    # Crea la nueva tabla incluyendo dos filas y columnas nuevas
    # Las columnas servirán para especificar el peso y el beneficio de cada elemento de S
    # Las filas nuevas serán para representar el peso máximo K y el beneficio mínimo B. 
    def crear_nueva_tabla(self):

        #[id, datos, nomColumn, existeSub, filasSelec, numFilas_tabla1, numFilas_tabla2] = self.gestor_etapas.get_tabla_inicial()
        [id, conjunto, valor_t, existeSub, subconjunto] = self.gestor_etapas.get_tabla_inicial()


        nomColumn = [" ", "Peso", "Beneficio"]
        
        nuevos_datos = []

        nombres = []
        for i in range(1,len(conjunto)+1):
            nombres.append("x"+str(i))

        

        for elemento,nombre in zip(conjunto,nombres):
            nueva_fila = []
            nueva_fila.append(nombre)
            nueva_fila.append(elemento)
            nueva_fila.append(elemento)

            nuevos_datos.append(nueva_fila)

        
        # Ahora añadimos las dos nuevas filas asociadas al peso máximo y beneficio mínimo
        nuevos_datos.append(["K", valor_t, "---"])
        nuevos_datos.append(["B", "---", valor_t])

        filasSelec = []
        if existeSub==1:

            # Voy a devolver las filas de la nueva tabla que pertenecen al subconjunto
            # Creo un diccionario que me servirá para ver que elementos del conjunto he pintado
            dicc = {}
            
            for fila in nuevos_datos:
                dicc[fila[0], fila[1]] = False


            for elemento in subconjunto:
                for fila in nuevos_datos:
                    
                    if str(fila[1]) == str(elemento) and dicc[fila[0],fila[1]]==False :
                        filasSelec.append(fila)
                        dicc[fila[0],fila[1]] = True
                        break


        # Guardamos la solución en el gestor de etapas para que sea accesible en el resto de etapas
        self.gestor_etapas.set_tabla_final([id, nuevos_datos, nomColumn, existeSub, filasSelec])


        return [id, nuevos_datos, nomColumn, existeSub, subconjunto]

    
    # Crea el panel donde imprimir la nueva tabla
    def crear_panel_nueva_tabla(self, info_tabla):

        if self.panel_tabla != None:
            self.panel_tabla.pack_forget()
        
        self.panel_tabla = ctk.CTkFrame(self.panel_1)
        self.panel_tabla.pack(padx=10, pady=10, fill="both", expand=True)

        fig = Figure(figsize=(5,3), dpi=100)
        axis = fig.add_subplot(111)

        boton_agrandar= ctk.CTkButton(self.panel_botones_1_1, text="Agrandar/guardar\n imagen",
                                    fg_color = ("#70AB94","#4D8871"), hover_color = ("#7FB9A2","#52987C"),
                                    command=lambda:self.gestor_etapas.agrandar_tabla(fig,1))
        boton_agrandar.grid(row=0,column=0, padx=5, pady=5)

        #  ------ Creamos el objeto tabla
        [id, nuevos_datos, nomColumn, existeSub, subconjunto] = info_tabla


        tabla = axis.table(cellText=nuevos_datos, colLabels=nomColumn, cellLoc='center', loc='center')
        axis.axis('off')

        # ------ Coloreamos las celdas de la nueva tabla
        # Pintamos las filas de la tabla
        for i in range(1,len(nuevos_datos)-1):
    
            cell = tabla[i,1]
            cell.set_facecolor('#FAFAD2')

            cell = tabla[i,2]
            cell.set_facecolor('#FAFAD2')


        # Fila asociada al valor K
        for i in range(0,3):
            cell = tabla[len(nuevos_datos)-1,i]
            if i == 2:
                cell.set_facecolor('#FAFAD2')
            else:
                cell.set_facecolor('#48D1CC')
            
        
        
        
        # Fila asociada al valor B
        for i in range(0,3):
            cell = tabla[len(nuevos_datos),i]
            if i == 1:
                cell.set_facecolor('#FAFAD2')
            else:
                cell.set_facecolor('#DDA0DD')


        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(fig, self.panel_tabla)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        
    
    
        
  
