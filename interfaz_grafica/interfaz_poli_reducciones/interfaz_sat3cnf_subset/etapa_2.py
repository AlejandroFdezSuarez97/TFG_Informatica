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
# Clase que engloba la etapa 2 a realizar en la poli-reducción. 
# Se encarga de rellenar la tabla creada en la reducción, en base
# a la fórmula que ha introducido el usuario. Se indica además los pasos
# que se han seguido para que el usuario sea consciente de ellos.
#########################################################################
class Etapa2(Etapa):

    def __init__(self, ventana, gestor_etapas):
        
        super().__init__(ventana, gestor_etapas)

    ### Getters y setters ###

    def get_panel_2(self):
        return self.panel_2
    
    def get_tabla(self):
        return copy.deepcopy(self.tabla)

    ### Lanzador de etapa ###

    def lanzar_etapa(self):
        
       # Realizamos etapa
        self.etapa_realizada = True

        # Creamos nuevo panel
        self.panel_2 = ctk.CTkFrame(self.ventana, corner_radius = 0)
        self.panel_2.pack(fill="both",expand=True)
            
        lista_texto = []
        text = "Rellenamos la tabla anterior basándonos en la fórmula Φ. En particular,\n el relleno depende "\
                "de los literales.\n Veamos paso a paso como rellenarla."
        lista_texto.append(text)

        text =  "▶ Mitad izquierda en filas yi y zi:\n\n "\
                "  Se rellenan con 1 en pos i y después 0s."
        lista_texto.append(text)

        text =  "▶ Mitad derecha en filas gi y hi:\n\n"\
                "  Se rellenan con 1 en pos i y después 0s\n"\
                "      (en zona izquierda no se pone nada).\n"
        lista_texto.append(text)

        text =  "▶ Mitad derecha: se pone 1 en posición yi, cj si xi aparece en cj,y 0\n"\
                "  en caso de no aparecer. Se pone 1 en posición zi, cj si ¬xi aparece en cj\n"\
                "  y 0 en caso de no aparecer."
        lista_texto.append(text)

        text = "▶ Finalmente, la última fila se rellena:\n"\
                "  en su mitad izquierda con l unos\n"\
                "  en su mitad derecha con k treses."
        lista_texto.append(text)


        self.gestor_etapas.crear_panel_informacion(panel=self.panel_2, altura=110, anchura=600, num_pasos=len(lista_texto), lista_texto=lista_texto,
                                                        mostrar_sol=False, mostrar_formula=True, num_etapa=2)

        # Creamos la tabla
        f = Figure(figsize=(5,3), dpi=100)
        a = f.add_subplot(111)

        panel_botones_1 = ctk.CTkFrame(self.panel_2)
        panel_botones_1.pack(padx=10, pady=(0,10), side='bottom', fill=tk.Y)
        self.panel_botones_1 = panel_botones_1

        self.tabla = self.crear_tabla()

        self.crear_panel_tabla(self.panel_2, self.tabla, f, a)

        boton_anterior= ctk.CTkButton(panel_botones_1, text="Anterior", command=lambda:self.gestor_etapas.anterior(1))
        boton_anterior.grid(row=0, column=0,padx=10, pady=10)

        boton_siguiente = ctk.CTkButton(panel_botones_1, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(3))
        boton_siguiente.grid(row=0, column=2, padx=10, pady=10)

        

    # Creamos la tabla
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

        datos = []  # Lista para almacenar los datos

        # ----------------------------------- TABLA1 ------------------------------
        
        
        # Rellenamos la tabla_1
        for i in range(self.num_filas_tabla1):
            fila = []
            lista_izq = ''
            lista_dch = ''
            if i % 2 == 0:
                nombre = f'y{id_literales[i//2]}'
            else:
                nombre = f'z{id_literales[i//2]}'
            
            # -------------- Para crear lista_izq -------------------------------
            matriz_izq = self.obtener_fila_identidad(i,l)
            lista_izq = ' '.join(matriz_izq)  # Convierte la matriz en una cadena

            matriz_dch = self.obtener_fila_derecha(i,k,nombre)
            lista_dch = '   '.join(matriz_dch)
            # --------------------------------------------------------------------
            fila.append(nombre)
            fila.append(lista_izq)
            fila.append(lista_dch)
            datos.append(fila)

        


        # ----------------------------------- TABLA2 ------------------------------

        # Rellenamos la tabla_2
        for i in range(self.num_filas_tabla2):
            fila = []
            lista_izq = '   '.join(' ' for _ in range(l))
            lista_dch = ''
            if i % 2 == 0:
                nombre = f'g{i//2 + 1}'
            else:
                nombre = f'h{i//2 + 1}'
            
            # -------------- Para crear lista_dch -------------------------------
            matriz = self.obtener_fila_identidad(i,k)

            lista_dch = '   '.join(matriz)  # Convierte la matriz en una cadena

            # --------------------------------------------------------------------
            fila.append(nombre)
            fila.append(lista_izq)
            fila.append(lista_dch)
            datos.append(fila)




        # ----------------------------------- TABLA3 ------------------------------

        # Rellenamos la tabla_3
        
        fila = []
        lista_izq = ' '.join('1' for _ in range(l))
        lista_dch = '   '.join('3' for _ in range(k))
        nombre = 't'
        fila.append(nombre)
        fila.append(lista_izq)
        fila.append(lista_dch)
        datos.append(fila)

        #############################################################################


        return [datos,nombreColumnas]
        
        
    # Calcula las filas de la tabla que se asemejan a la matriz identidad
    def obtener_fila_identidad(self,numFila,posEnColumn):
        matriz = []  # Lista para almacenar la matriz de lista_(izq o dch)

        for m in range(posEnColumn):  # Bucle interno
            if numFila % 2 == 0:
                if m < numFila // 2:
                    elemento = ' '
                elif m == numFila // 2:
                    elemento = '1'
                else:
                    elemento = '0'
            else:
                if m < (numFila - 1) // 2:
                    elemento = ' '
                elif m == (numFila - 1) // 2:
                    elemento = '1'
                else:
                    elemento = '0'

            matriz.append(elemento)
        
        return matriz


    # Calcula la fila derecha de la tabla_1
    def obtener_fila_derecha(self, id_fila, numClausulas, nombreFila):
        matriz = []  # Lista para almacenar la matriz de lista_(izq o dch)

        for j in range(numClausulas):  # Bucle interno
            if id_fila % 2 == 0:    # Caso yi
                pertenece = self.literal_pertence_clausula(nombreFila,j)
                if pertenece:
                    elemento = '1'
                else:
                    elemento = '0'
            else:                   # Caso zi
                pertenece = self.literalNegado_pertenece_clausula(nombreFila,j)
                if pertenece:
                    elemento = '1'
                else:
                    elemento = '0'
            matriz.append(elemento)
        
        return matriz
    

    # Averigua si un literal pertenece o no a una clausula.
    # El literal lo identificamos por su id y la clausula tambien
    # En caso afirmativo, devuelve true; y en caso contrario false
    def literal_pertence_clausula(self, nombre_fila, id_clausula):
        
        lista_clausulas = self.gestor_etapas.get_clausulas_formula()

        literal = "x"+nombre_fila[-1]
        
        # Primero busco si esta su negado, porque si lo esta, no puede estar dicho literal
        # Por la definicion de formula en formato 3cnf.
        if ("!"+literal) in lista_clausulas[id_clausula]:
            return False
        elif literal in lista_clausulas[id_clausula]:
            return True
        else:
            return False

        

    # Averigua si el negado del literal pertenece o no a una clausula.
    # El literal lo identificamos por su id y la clausula tambien
    # En caso afirmativo, devuelve true; y en caso contrario false
    def literalNegado_pertenece_clausula(self, id_literal, id_clausula):
        
        lista_clausulas = self.gestor_etapas.get_clausulas_formula()
        
        literal = "x"+id_literal[-1]

        if ("!"+literal) in lista_clausulas[id_clausula]:
            return True
        else:
            return False


    # Pinta la tabla de la reducción (sin rellenar).
    def crear_panel_tabla(self, panel, info_tabla, figure, axis):

        panel_tabla = ctk.CTkFrame(panel)
        panel_tabla.pack(padx=20,pady=(30,10),side="top", fill="both", expand=True)

        boton_agrandar = ctk.CTkButton(self.panel_botones_1, text="Agrandar/guardar\n imagen",
                                        fg_color=("#70AB94","#4D8871"), hover_color=("#7FB9A2","#52987C"),
                                        command=lambda:self.gestor_etapas.agrandar_tabla(figure,2))
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