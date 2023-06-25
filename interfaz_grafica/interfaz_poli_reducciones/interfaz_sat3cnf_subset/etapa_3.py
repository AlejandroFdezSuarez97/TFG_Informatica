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
# Clase que engloba la etapa 3 a realizar en la poli-reducción. 
# Se encarga de completar la tabla creada en la reducción. En particular
# añade una nueva columna mostrando el valor decimal de los numeros que
# componen el conjunto S así como el valor de t
#########################################################################
class Etapa3(Etapa):

    def __init__(self, ventana, gestor_etapas):
        
        super().__init__(ventana, gestor_etapas)

    ### Getters y setters ###

    def get_panel_3(self):
        return self.panel_3
    
    def get_tabla(self):
        return copy.deepcopy(self.tabla)

    ### Lanzador de etapa ###

    def lanzar_etapa(self):
        
       # Realizamos etapa
        self.etapa_realizada = True

        # Creamos nuevo panel
        self.panel_3 = ctk.CTkFrame(self.ventana, corner_radius = 0)
        self.panel_3.pack(fill="both",expand=True)
            
        lista_texto = []
        text = "Completamos la tabla anterior añadiendo una nueva columna.\n"\
               "Esta nueva columna almacenará el valor decimal de los numeros asociados\n a cada fila de la tabla.\n"\
               "La forma de rellenar esta nueva columna es: \n\n"\
               "A cada columna desde la ck hasta la x1, se le asocia una potencia de 10\n"\
               "(ck con 10^0, ck−1, con 10^1,. . . , xl con 10^k, . . . , x1 con 10^(k+l−1)"
               
        lista_texto.append(text)

        text =  "▶ ¿Donde está el conjunto S?\n\n "\
                "Los números decimales de esta nueva columna\n serán los números que componen el conjunto S.\n"\
                "   (sin contar la última fila; es decir, la fila t)"
        lista_texto.append(text)

        text =  "▶ ¿Dónde está el valor de t?\n\n"\
                "  El valor de t se encuentra en la nueva columna en la fila t.\n"
        lista_texto.append(text)
        

        self.gestor_etapas.crear_panel_informacion(panel=self.panel_3, altura=110, anchura=600, num_pasos=len(lista_texto), lista_texto=lista_texto,
                                                        mostrar_sol=False, mostrar_formula=True, num_etapa=3)

        # Creamos la tabla
        f = Figure(figsize=(5,3), dpi=100)
        a = f.add_subplot(111)

        panel_botones_1 = ctk.CTkFrame(self.panel_3)
        panel_botones_1.pack(padx=10, pady=(0,10), side='bottom', fill=tk.Y)
        self.panel_botones_1 = panel_botones_1

        self.tabla = self.crear_tabla()

        self.crear_panel_tabla(self.panel_3, self.tabla, f, a)

        boton_anterior= ctk.CTkButton(panel_botones_1, text="Anterior", command=lambda:self.gestor_etapas.anterior(2))
        boton_anterior.grid(row=0, column=0,padx=10, pady=10)

        boton_siguiente = ctk.CTkButton(panel_botones_1, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(4))
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
        nombreColumnas = [' ', col_labels1, col_labels2, 'S']

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
            
            
            matriz_izq = self.obtener_fila_identidad(i,l)
            lista_izq = ' '.join(matriz_izq)  # Convierte la matriz en una cadena

            matriz_dch = self.obtener_fila_derecha(i,k,nombre)
            lista_dch = '   '.join(matriz_dch)
            


















            
            valor_decimal = self.calcular_valor_decimal_tabla(matriz_izq,matriz_dch, i/2)

            fila.append(nombre)
            fila.append(lista_izq)
            fila.append(lista_dch)
            fila.append(valor_decimal)
            datos.append(fila)

        
        # ----------------------------------- TABLA2 ------------------------------

        # Rellenamos la tabla_2
        for i in range(self.num_filas_tabla2):
            fila = []
            lista_izq = '   '.join(' ' for _ in range(l))
            lista_dch = ''
            valor_decimal = 0
            if i % 2 == 0:
                nombre = f'g{i//2 + 1}'
            else:
                nombre = f'h{i//2 + 1}'
            

            matriz = self.obtener_fila_identidad(i,k)
            lista_dch = '   '.join(matriz)  # Convierte la matriz en una cadena

            valor_decimal = self.calcular_valor_decimal_tabla(matriz,[],i/2)

            fila.append(nombre)
            fila.append(lista_izq)
            fila.append(lista_dch)
            fila.append(valor_decimal)
            datos.append(fila)


        # ----------------------------------- TABLA3 ------------------------------

        # Rellenamos la tabla_3
        
        fila = []
        string_izq = ' '.join('1' for _ in range(l))
        string_dch = '   '.join('3' for _ in range(k))

        lista_izq = string_izq.split(' ')
        lista_dch = string_dch.split('   ')
        valor_decimal = self.calcular_valor_decimal_tabla(lista_izq, lista_dch,0)

        nombre = 't'

        fila.append(nombre)
        fila.append(string_izq)
        fila.append(string_dch)
        fila.append(valor_decimal)
        datos.append(fila)

        #############################################################################

        # Guardo esta info en el gestor de etapas 
        self.gestor_etapas.set_datos_tabla([datos,nombreColumnas,self.num_filas_tabla1, self.num_filas_tabla2])

        return [datos,nombreColumnas, self.num_filas_tabla1, self.num_filas_tabla2]
        
        
    # Calculo el valor decimal de cada fila
    def calcular_valor_decimal_tabla(self, lista_izq, lista_dch, empezar_en_lista_izq):
        valor = 0

        lista = lista_izq + lista_dch

        lista.reverse()

        for p in range(0,len(lista_dch)+len(lista_izq)-int(empezar_en_lista_izq)):
            valor += int(lista[p]) * (10**p)
 
        return valor




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
                                        command=lambda:self.gestor_etapas.agrandar_tabla(figure,3))
        boton_agrandar.grid(row=0,column=1,padx=10,pady=10)

        # Creamos el objeto tabla
        [datos, nombreColumna,numFilas_tabla1, numFilas_tabla2] = info_tabla
        tabla = axis.table(cellText=datos, colLabels=nombreColumna, cellLoc='center', loc='center')
        axis.axis('off')

        # Almaceno el valor para poder acceder a esto info desde otras etapas
        # Pero no lo guardo en el gestor de etapas porque no es la tabla definitiva.
        self.solucion_reduccion = [datos, nombreColumna,numFilas_tabla1, numFilas_tabla2]

        #  ----------- Coloreo las celdas para que sean mas visibles las distintas zonas de la tabla --------

        # tabla_1
        for i in range(1,self.num_filas_tabla1+1):
            cell = tabla[i,1]
            cell.set_facecolor('#FFFFF0')

            cell = tabla[i,2]
            cell.set_facecolor('#FFFFE0')

            cell = tabla[i,3]
            cell.set_facecolor('#FFF8DC')

            
        # tabla_2
        for i in range(self.num_filas_tabla1+1, self.num_filas):
        
            cell = tabla[i,1]
            cell.set_facecolor('#FFFAFA')
            
            cell = tabla[i,2]    
            cell.set_facecolor('#FFF0F5')

            cell = tabla[i,3]
            cell.set_facecolor('#FFE4E1')
            
        
        # tabla_3
        cell = tabla[self.num_filas,1]
        cell.set_facecolor('#F0FFFF')
        cell = tabla[self.num_filas,2]
        cell.set_facecolor('#E0FFFF')
        cell = tabla[self.num_filas,3]
        cell.set_facecolor('#AFEEEE')

        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(figure, panel_tabla)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)