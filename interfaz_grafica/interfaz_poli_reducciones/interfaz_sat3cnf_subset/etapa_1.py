import tkinter as tk
import customtkinter as ctk
import copy

from PIL import Image
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from interfaz_grafica.interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp

from .etapa import Etapa

#########################################################################
# Clase que engloba la etapa 1 a realizar en la poli-reducción. 
# Se encarga de realizar la estructura de la tabla en la reducción, en base
# a la fórmula que ha introducido el usuario. Se indica además los pasos
# que se han seguido para que el usuario sea consciente de ellos.
#########################################################################
class Etapa1(Etapa):

    def __init__(self, ventana, gestor_etapas):
        
        super().__init__(ventana, gestor_etapas)

    ### Getters y setters ###

    def get_panel_1(self):
        return self.panel_1
    
    def get_tabla(self):
        return copy.deepcopy(self.tabla)

    ### Lanzador de etapa ###

    def lanzar_etapa(self):
        
        # Si la fórmula es correcta, pasamos a la siguiente ventana
        if self.gestor_etapas.get_formula_correcta() == True:
            
            # Si introducimos más fórmulas, reseteamos las etapas para que las realicemos 
            # con los nuevos datos introducidos
            if self.gestor_etapas.get_num_formulas_introducidas() > 1:
                self.gestor_etapas.set_num_formulas_introducidas(1)
                self.gestor_etapas.resetear_etapas()

            self.gestor_etapas.get_etapa(0).get_panel_0_2().pack_forget()

            # Realizamos etapa
            self.etapa_realizada = True
 
            self.panel_1 = ctk.CTkFrame(self.ventana, corner_radius = 0)
            self.panel_1.pack(fill="both", expand=True)

            lista_texto = []
            text = "Creamos una tabla cuya estructura está basada en la fórmula Φ. En particular,\n la estructura depende "\
                   "del número de literales (l) y del número de claúsulas (k).\n En este caso, tenemos:\n\n"\
                   "l = " + str(self.gestor_etapas.get_num_literales_formula())+"\n"\
                   "k = " + str(self.gestor_etapas.get_num_clausulas_formula())+"\n\n"\
                   "Teniendo en cuenta esto, los pasos para el diseño de la estructura de la tabla\nson los siguientes."
            lista_texto.append(text)

            text = " · Para la mitad izquierda: Añadimos una columna i por cada proposición xi.\n"\
                   " · Para la mitad derecha: Añadimos una columna por cada claúsula cj.\n"\
                   " · Por cada proposición xi: añadimos las filas yi y zi.\n"\
                   " · Por cada claúsula ci: Añadimos las filas gi y hi."
            lista_texto.append(text)

            self.gestor_etapas.crear_panel_informacion(panel=self.panel_1, altura=110, anchura=600, num_pasos=len(lista_texto), lista_texto=lista_texto,
                                                        mostrar_sol=False, mostrar_formula=True, num_etapa=1)

            # Para crear la tabla (estructura)
            f = Figure(figsize=(5,3), dpi=100)
            a = f.add_subplot(111)

            panel_botones_1 = ctk.CTkFrame(self.panel_1)
            panel_botones_1.pack(padx=10, pady=(0,10), side='bottom', fill=tk.Y)
            self.panel_botones_1 = panel_botones_1

            self.tabla = self.crear_tabla()

            self.crear_panel_tabla(self.panel_1, self.tabla, f, a)

            boton_anterior= ctk.CTkButton(panel_botones_1, text="Anterior", command=lambda:self.gestor_etapas.anterior(0.2))
            boton_anterior.grid(row=0, column=0,padx=10, pady=10)

            boton_siguiente = ctk.CTkButton(panel_botones_1, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(2))
            boton_siguiente.grid(row=0, column=2, padx=10, pady=10)

        # Si la fórmula booleana es incorrecta (o no se ha introducido aún), no podremos pasar a la 
        # siguiente etapa. Mostramos mensaje de error 
        else:
            ventana_error = VentanaPopUp(self.ventana)
            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
            ventana_error.title(" ")

            panel_error = ctk.CTkFrame(ventana_error, corner_radius=0)
            panel_error.pack()

            # Imagen error
            imagen_error = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"), size=(50,50))
            label = ctk.CTkLabel(panel_error, image=imagen_error, text="")
            label.grid(row=0,column=0, padx=10, pady=10)

            label = ctk.CTkLabel(panel_error, text='Fórmula booleana incorrecta')
            label.grid(row=1, column=0, padx=10, pady=10)

            boton_aceptar = ctk.CTkButton(panel_error, text="Aceptar", command=lambda:ventana_error.exit())
            boton_aceptar.grid(row=2, column=0, padx=10, pady=10)

            ventana_error.center()

    # Creamos la estructura de la tabla (sin rellenar)
    # Devuelve una lista  [datos,nombreColumnas] porque es la informacion que necesito para crear la tabla
    # NOTA: no devuelve la propia tabla porque no existen funciones en la libreria para poder extaer informacion de ella.
    def crear_tabla(self):

        # La tabla la creo como si fueran 3 tablas
        #   tabla1 es la tabla cuyas filas estan asociadas al numero de literales
        #   tabla2 es la tabla cuyas filas estan asociadas al número de claúsulas
        #   tabla3 es la tabla con una única fila asociada al valor t

        # Establezco el valor de l y k
        l = self.gestor_etapas.get_num_literales_formula()
        k = self.gestor_etapas.get_num_clausulas_formula()

        literales = self.gestor_etapas.get_literales_formula()
        id_literales = []
        for literal in literales:
            id_literal = literal[-1]
            id_literales.append(id_literal)


        id_literales.sort()

        # Nombre de las columnas
        col_labels1 = ' '.join(str(i) for i in id_literales)
        col_labels2 = ' '.join(f'c{i}' for i in range(1, k+1))
        nombreColumnas = [' ', col_labels1, col_labels2]

        self.num_filas_tabla1 = 2*l
        self.num_filas_tabla2 = 2*k
        self.num_filas_tabla3 = 1
        self.num_filas = self.num_filas_tabla1 + self.num_filas_tabla2 + self.num_filas_tabla3

        # Lista donde se almacenan los datos de la tabla
        datos = []

        ##########################################################################
        ############################# RELLENAR TABLA #############################
        ##########################################################################

        # ----------------------------------- TABLA1 ------------------------------
        
        # Rellenamos la tabla_1
        contador = 0
        for i in range(self.num_filas_tabla1):
            fila = []
            lista_a = ' '.join(' ' for _ in range(l))
            lista_b = '   '.join(' ' for _ in range(k))
            if i % 2 == 0:
                nombre = f'y{id_literales[i//2]}'
            else:
                nombre = f'z{id_literales[i//2]}'

            fila.append(nombre)
            fila.append(lista_a)
            fila.append(lista_b)
            datos.append(fila)
            
            if contador==1:
                contador=0
            else:
                contador+=1

        # ----------------------------------- TABLA2 ------------------------------

        # Rellenamos la tabla_2
        for i in range(self.num_filas_tabla2):
            fila = []
            lista_a = ' '.join(' ' for _ in range(l))
            lista_b = '   '.join(' ' for _ in range(k))
            if i % 2 == 0:
                nombre = f'g{i//2 + 1}'
            else:
                nombre = f'h{i//2 + 1}'
            fila.append(nombre)
            fila.append(lista_a)
            fila.append(lista_b)
            datos.append(fila)
        # ----------------------------------- TABLA3 ------------------------------

        # Rellenamos la tabla_3
        
        fila = []
        lista_a = ' '.join(' ' for _ in range(l))
        lista_b = '   '.join(' ' for _ in range(k))
        nombre = 't'
        fila.append(nombre)
        fila.append(lista_a)
        fila.append(lista_b)
        datos.append(fila)

        #############################################################################


        return [datos,nombreColumnas]
        
        
    
    # Pinta la tabla de la reducción (sin rellenar).
    def crear_panel_tabla(self, panel, info_tabla, figure, axis):

        panel_tabla = ctk.CTkFrame(panel)
        panel_tabla.pack(padx=20,pady=(30,10),side="top", fill="both", expand=True)

        boton_agrandar = ctk.CTkButton(self.panel_botones_1, text="Agrandar/guardar\n imagen",
                                        fg_color=("#70AB94","#4D8871"), hover_color=("#7FB9A2","#52987C"),
                                        command=lambda:self.gestor_etapas.agrandar_tabla(figure,1))
        boton_agrandar.grid(row=0,column=1,padx=10,pady=10)

        # Creamos el objeto tabla
        [datos, nombreColumna] = info_tabla
        tabla = axis.table(cellText=datos, colLabels=nombreColumna, cellLoc='center', loc='center')
        axis.axis('off')


        #  ----------- Coloreo las celdas para que sean mas visibles las distintas zonas de la tabla --------

        # tabla_1
        for i in range(1, self.num_filas_tabla1+1):
            cell = tabla[i,1]
            cell.set_facecolor('#FFFFF0')

            cell = tabla[i,2]
            cell.set_facecolor('#FFFFE0')

        # tabla_2
        for i in range(self.num_filas_tabla1+1, self.num_filas):
        
            cell = tabla[i,1]
            cell.set_facecolor('#FFFAFA')
            
            cell = tabla[i,2]    
            cell.set_facecolor('#FFF0F5')
            
        
        # tabla_3
        cell = tabla[self.num_filas,1]
        cell.set_facecolor('#F0FFFF')
        cell = tabla[self.num_filas,2]
        cell.set_facecolor('#E0FFFF')

        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(figure, panel_tabla)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)