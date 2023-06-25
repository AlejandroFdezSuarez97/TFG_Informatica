import tkinter as tk
import customtkinter as ctk
import copy

import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .etapa import Etapa

##############################################################################
# Clase que engloba la etapa 4 a realizar en la poli-reducción. 
# En esta etapa, se comprueba si la fórmula introducida por el
# usuario es satisfacible o no; en caso de serlo, se muestra la
# seleccion de filas (elementos) del conjunto S que forman parte
# del subconjunto que suma t; y en caso contrario se indica que 
# no existe un subconjunto de forma que sume dicho valor.
# Por tanto, se prueba que existe un subconjunto que suma t si y solo si
# la fórmula es satisfacible, por lo que SAT3cnf se poli-reduce a SUBSET-SUM.
##############################################################################
class Etapa4(Etapa):

    def __init__(self, ventana, gestor_etapas):

        super().__init__(ventana, gestor_etapas)

        self.etapa_4_1_realizada = False
        self.etapa_4_2_realizada = False
        self.etapa_4_3_realizada = False

        self.panel_4_1 = None
    
    ### Getters y setters ###

    def get_panel_4(self):
        return self.panel_4
    
    def get_panel_4_1(self):
        return self.panel_4_1
    
    def resetear_panel_4_1(self):
        self.panel_4_1 = None

    def get_panel_4_2(self):
        return self.panel_4_2
    
    def get_panel_4_3(self):
        return self.panel_4_3
    
    def get_etapa_realizada_4_1(self):
        return self.etapa_4_1_realizada
    
    def set_etapa_realizada_4_1(self, valor):
        self.etapa_4_1_realizada = valor
    
    def get_etapa_realizada_4_2(self):
        return self.etapa_4_2_realizada
    
    def set_etapa_realizada_4_2(self, valor):
        self.etapa_4_2_realizada = valor
    
    def get_etapa_realizada_4_3(self):
        return self.etapa_4_3_realizada
    
    def set_etapa_realizada_4_3(self, valor):
        self.etapa_4_3_realizada = valor
    
    def get_lista_valores_literales(self):
        return copy.deepcopy(self.lista_valores_literales)
    
    def get_filas_seleccionadas(self):
        return self.filas_seleccionadas
    
    def is_formula_satisfacible(self):
        return self.satisfacible

    ### Lanzador de etapa ###

    ################# ETAPA 4.0 #################

    # Comprobamos que la fórmula introducida es satisfacible
    # o no. En caso de serlo, continuaremos con la reducción
    # hasta calcular el subconjunto que suma t.
    # Si no es satisfacbile, terminamos la reduccióon, afirmando que,
    # como no es satisfacible, entonces no existe dicho subconjunto.

    def lanzar_subetapa_0(self):

        # Realizamos etapa
        self.etapa_realizada = True

        # Creamos nuevo panel
        self.panel_4 = ctk.CTkFrame(self.ventana, corner_radius=0)
        self.panel_4.pack(fill="both", expand=True)

        # Ahora comprobamos la satisfaciblidad de la fórmula:
        satisfacible, lista_valores_literales = self.gestor_etapas.formula_satisfacible()
        self.lista_valores_literales = sorted(lista_valores_literales)
        self.satisfacible = satisfacible

        # Guardo si la formula es o no satisfacible y su asiganción de valores para guradar
        # esta info en la BD
        self.gestor_etapas.set_formula_is_satisfacible(satisfacible)
        self.gestor_etapas.set_lista_asignacion_satisfacible(self.lista_valores_literales)

        if satisfacible:

            lista_texto = []
            texto = "Ya hemos completado la tabla. Vamos a ver que cumple las condiciones\n"\
                    "para ser una reducción SAT3cnf ≤p SUBSET-SUM. \n\n"\
                    "Ahora veremos que, como nuestra fórmula booleana sí es satisfacible,\n" \
                    "sí existe un subconjunto de valores que suman t en la tabla \n" \
                    "anteriormente calculada en la Etapa 3."
                
            lista_texto.append(texto)

    
            self.gestor_etapas.crear_panel_informacion(panel=self.panel_4, altura=110, anchura=480, num_pasos=len(lista_texto), lista_texto=lista_texto,
                                                        mostrar_sol=False, mostrar_formula=True, num_etapa=4)

           


            panel_botones_4 = ctk.CTkFrame(self.panel_4)
            panel_botones_4.pack(padx=10, pady=(0,10), fill=tk.Y, side='bottom')

            boton_anterior = ctk.CTkButton(panel_botones_4, text="Anterior", command=lambda:self.gestor_etapas.anterior(3))
            boton_anterior.grid(row=0, column=0, padx=(10,20), pady=10)

            boton_siguiente = ctk.CTkButton(panel_botones_4, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(4.1))
            boton_siguiente.grid(row=0, column=1, padx=(20,10), pady=10)
        
        # Si la fórmula no es satisfacible, mostramos que no podemos construir el 
        # subconjunto.
        else:

            self.formula_es_satisfacible = False


            panel_botones_fin = ctk.CTkFrame(self.panel_4)
            panel_botones_fin.pack(padx=10, pady=(0,10), fill=tk.Y, side='bottom')

            lista_texto = []
            texto = "En nuestro conjunto S no existe un subconjunto que sume t\n" \
                    "puesto que la fórmula ϕ no es satisfacible, es decir, no hay ninguna\n " \
                    "asignación de valores a los literales que haga que la fórmula sea\n" \
                    "verdadera.\n\n" \
                    "Así que, como no es satisfacible no hay un subconjunto que sume t \n"\
                    "(solamente existirá dicho subconjunto si y sólo si la fórmula\n " \
                    "es satisfacible)."

            lista_texto.append(texto)
            self.gestor_etapas.crear_panel_informacion(panel=self.panel_4, altura=110, anchura=480, num_pasos=len(lista_texto), lista_texto=lista_texto,
                                                        mostrar_sol = False, mostrar_formula = True,num_etapa=4)


            # Guardo la info de la tabla en el gestor de etapas:
            [datos, nombreColumna,numFilas_tabla1, numFilas_tabla2] = self.gestor_etapas.get_etapa(3).solucion_reduccion
            self.gestor_etapas.set_solucion_reduccion([datos, nombreColumna,0,[],numFilas_tabla1, numFilas_tabla2])

            
            boton_anterior = ctk.CTkButton(panel_botones_fin, text="Anterior",command=lambda:self.gestor_etapas.anterior(3))
            boton_anterior.grid(row=0, column=0, padx=10, pady=10)

            boton_siguiente = ctk.CTkButton(panel_botones_fin, text="Siguiente",command=lambda:self.gestor_etapas.siguiente(5))
            boton_siguiente.grid(row=0, column=1, padx=10, pady=10)






    ################# ETAPA 4.1 #################

    # Informamos al usuario qué vamos a realizar ahora.

    def lanzar_subetapa_1(self):

        # Realizamos etapa
        self.etapa_4_1_realizada = True

        # Creamos nuevo panel
        self.panel_4_1 = ctk.CTkFrame(self.ventana, corner_radius=0)
        self.panel_4_1.pack(fill="both",expand=True)

        lista_texto = []
        texto = "Dada la asignación anterior de valores de verdad a los literales  \n " \
                "que satisface ϕ, el subconjunto que suma t se determina en  \n" \
                "base a dicha asignación de valores.\n\n" \
                "Empezamos escogiendo filas de la tabla de arriba a abajo; es decir\n"\
                "comenzamos por las filas yi y zi:\n\n"\
                "    si xi = True, entonces escogemos la fila yi\n"\
                "    si xi = False, entonces escogemos la fila zi"
                
        lista_texto.append(texto)

        # ------------------------------- SELECCION FILAS yi/zi ------------------------------
        texto = "Por tanto, vamos a ir viendo que filas se escogen: \n\n"
        self.filas_seleccionadas = []
        [datos,nombreColumn,numFilas_tabla1, numFilas_tabla2] = self.gestor_etapas.get_datos_tabla()
        


        for literal, valor_literal in self.lista_valores_literales:
            num_del_literal = literal.strip("x")

            # Itero solo sobre las filas de tabla1
            for i, fila in enumerate(datos[:numFilas_tabla1]):
                nombre_fila = fila[0]
                lista_izq = fila[1]
                lista_dch = fila[2]
                valor_decimal = fila[3]


                if valor_literal:

                    # El  literal vale TRUE -> debo guardar la fila yi
                    if nombre_fila=="y"+str(num_del_literal):
                        self.filas_seleccionadas.append(fila)
                        texto += " · Se ha añadido la fila y"+str(num_del_literal)+"\n" 
                        break

                else:

                    if nombre_fila=="z"+str(num_del_literal):
                        self.filas_seleccionadas.append(fila)
                        texto += " · Se ha añadido la fila z"+str(num_del_literal)+"\n"
                        break
            
        lista_texto.append(texto)

        # -------------------------------------------------------------------------------------------------
        

        texto = "Una vez seleccionadas las filas asociadas a los literales, vamos a ver\n" \
                "cuáles son las condiciones para seleccionar las filas gi y hi:\n\n"\
                "▶ Es posible que no se seleccione ninguna fila de este tipo.\n"\
                "▶ La idea es añadir las filas gi y hi de forma que la columna ci sume 3\n"\
                "   Esta suma sólo implica las filas seleccionadas en el paso anterior\n"\
                "   pertenecientes al sector (1,2) de la tabla.\n\n"\
                "  · Los dígitos de la columna ci suman un número entero entre 1 y 3\n"\
                "    (puesto que cada cláusula se satisface gracias a 1,2,o 3 literales)\n"\
                "  · Si la suma de la columna ci vale 3, no añadimos ni gi ni hi.\n"\
                "  · Si la suma de la columna ci vale 2, añadimos la fila gi.\n"\
                "  · Si la suma de la columna ci vale 1, añadimos las filas gi y hi."

        lista_texto.append(texto)

        # ------------------------------- SELECCION FILAS gi/hi ------------------------------
        texto = "Por tanto, vamos a ir viendo que filas se escogen: \n\n"  
        
        # Calculo una lista donde almaceno la suma de cada columna.
        lista_sumas_columnas = self.suma_columnas_seleccionadas(self.filas_seleccionadas, numFilas_tabla1,int(numFilas_tabla2/2))
        

        for i,valor_suma_columna in enumerate(lista_sumas_columnas):
            # Itero solo sobre las filas de tabla2
            for fila in enumerate(datos[numFilas_tabla1:len(datos)-1]):
                fila = fila[1]

                nombre_fila = fila[0]
                lista_izq = fila[1]
                lista_dch = fila[2]
                valor_decimal = fila[3]


                if valor_suma_columna==1:
                    if nombre_fila == "g"+str(i+1):
                        self.filas_seleccionadas.append(fila)
                        texto += " · Se ha añadido la fila g"+str(i+1)+"\n"
                    elif nombre_fila == "h"+str(i+1):
                        self.filas_seleccionadas.append(fila)
                        texto += " · Se ha añadido la fila h"+str(i+1)+"\n"
                elif valor_suma_columna==2:
                    if nombre_fila == "g"+str(i+1):
                        self.filas_seleccionadas.append(fila)
                        texto += " · Se ha añadido la fila g"+str(i+1)+"\n"

        lista_texto.append(texto)      

        # -------------------------------------------------------------------------------------------------
        

        self.gestor_etapas.crear_panel_informacion(panel=self.panel_4_1,altura=110,anchura=480,num_pasos=len(lista_texto),
                                                lista_texto=lista_texto,mostrar_sol = True, 
                                                mostrar_formula = True,num_etapa=4.1)

        panel_botones_4_1 = ctk.CTkFrame(self.panel_4_1)
        panel_botones_4_1.pack(padx=10,pady=(0,10),fill=tk.Y,side='bottom')

        boton_anterior = ctk.CTkButton(panel_botones_4_1, text="Anterior",command=lambda:self.gestor_etapas.anterior(4))
        boton_anterior.grid(row=0, column = 0,padx=(10,20), pady=10)

        boton_siguiente = ctk.CTkButton(panel_botones_4_1, text="Siguiente",command=lambda:self.gestor_etapas.siguiente(4.2))
        boton_siguiente.grid(row=0, column = 1, padx=(20,10), pady=10)



    # Devuelve una lista con las sumas de todas las columnas asociadas a clausulas de la tabla1
    def suma_columnas_seleccionadas(self, datos, numFilas_tabla1, numClausulas):
        suma = []

        # saco todas las filas derecha de la tabla1

        filaS_dch = []
        # Escojo solo filas de la tabla1
        for fila in enumerate(datos[:numFilas_tabla1]):
            
            fila = fila[1]
            lista_dch = fila[2].split('   ')
            filaS_dch.append(lista_dch)

        
        for c in range(numClausulas):
            valor = 0
            for fila_dch in filaS_dch:
                valor += int(fila_dch[c])
            suma.append(valor)

        return suma


    ################# ETAPA 4.2 #################

    # Mostramos la tabla seleccionando los valores
    # pertenecientes al subconjunto.

    def lanzar_subetapa_2(self):
        # Realizamos etapa
        self.etapa_4_2_realizada = True

        # Creamos nuevo panel
        self.panel_4_2 = ctk.CTkFrame(self.ventana, corner_radius=0)
        self.panel_4_2.pack(fill="both", expand=True)

        lista_texto = []
        texto = "Por tanto, siguiendo el paso anteriormente visto, vemos \n"\
            "los valores del conjunto que formaran parte del subconjunto (morado):"
        lista_texto.append(texto)

        self.gestor_etapas.crear_panel_informacion(panel=self.panel_4_2, altura=110, anchura=480, num_pasos=len(lista_texto), lista_texto=lista_texto,
                                                    mostrar_sol=False, mostrar_formula=True, num_etapa=4.2)



        # Creamos la tabla
        f = Figure(figsize=(5,3), dpi=100)
        a = f.add_subplot(111)

        panel_botones_4_2 = ctk.CTkFrame(self.panel_4_2)
        panel_botones_4_2.pack(padx=10, pady=(0,10), fill=tk.Y, side='bottom')

        self.panel_botones_4_2 = panel_botones_4_2


        # Representamos el grafo obtenido
        self.crear_panel_tabla(self.panel_4_2, f, a)

        boton_anterior = ctk.CTkButton(panel_botones_4_2, text="Anterior", command=lambda:self.gestor_etapas.anterior(4.1))
        boton_anterior.grid(row=0, column=0, padx=(10,20), pady=10)

        boton_siguiente = ctk.CTkButton(panel_botones_4_2, text="Siguiente",command=lambda:self.gestor_etapas.siguiente(4.3))
        boton_siguiente.grid(row=0, column=2, padx=(20,20), pady=10)

    

    # Pinta la tabla de la reducción (sin rellenar).
    def crear_panel_tabla(self, panel, figure, axis):

        panel_tabla = ctk.CTkFrame(panel)
        panel_tabla.pack(padx=20,pady=(30,10),side="top", fill="both", expand=True)

        boton_agrandar = ctk.CTkButton(self.panel_botones_4_2, text="Agrandar/guardar\n imagen",
                                        fg_color=("#70AB94","#4D8871"), hover_color=("#7FB9A2","#52987C"),
                                        command=lambda:self.gestor_etapas.agrandar_tabla(figure,4))
        boton_agrandar.grid(row=0,column=1,padx=10,pady=10)

        # Creamos el objeto tabla
        [datos,nombreColumn,numFilas_tabla1, numFilas_tabla2] = self.gestor_etapas.get_datos_tabla()
        tabla = axis.table(cellText=datos, colLabels=nombreColumn, cellLoc='center', loc='center')
        axis.axis('off')

        self.gestor_etapas.set_solucion_reduccion([datos, nombreColumn,1,self.filas_seleccionadas,numFilas_tabla1,numFilas_tabla2])

        #  ----------- Coloreo las celdas para que sean mas visibles las distintas zonas de la tabla --------

        # tabla_1
        for i in range(1,numFilas_tabla1+1):
            cell = tabla[i,1]
            cell.set_facecolor('#FFFFF0')

            cell = tabla[i,2]
            cell.set_facecolor('#FFFFE0')

            cell = tabla[i,3]
            cell.set_facecolor('#FFF8DC')

            
        # tabla_2
        for i in range(numFilas_tabla1+1, numFilas_tabla1+numFilas_tabla2+1):
        
            cell = tabla[i,1]
            cell.set_facecolor('#FFFAFA')
            
            cell = tabla[i,2]    
            cell.set_facecolor('#FFF0F5')

            cell = tabla[i,3]
            cell.set_facecolor('#FFE4E1')
            
        
        # tabla_3
        cell = tabla[numFilas_tabla1+numFilas_tabla2+1,1]
        cell.set_facecolor('#F0FFFF')
        cell = tabla[numFilas_tabla1+numFilas_tabla2+1,2]
        cell.set_facecolor('#E0FFFF')
        cell = tabla[numFilas_tabla1+numFilas_tabla2+1,3]
        cell.set_facecolor('#AFEEEE')

        # Pintamos las filas seleccionadas para pertenecer al subconjunto
        for fila in self.filas_seleccionadas:

            #Busco la posicion de la fila dentro de la tabla
            for i in range(1,numFilas_tabla1+numFilas_tabla2+1):
                if tabla[i,0].get_text().get_text() == fila[0]:
                    cell = tabla[i,3]
                    cell.set_facecolor('#DA70D6')
                    break


        # ----------------------------------------------------------------------------------
        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(figure, panel_tabla)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    ################# ETAPA 4.3 #################

    # Realizamos la última etapa de la poli-reducción.
    # Demostramos al ususario el recíproco del teorema; es decir,
    # que si existe el subconjunto de valores qeu suma t, entonces existe una
    # asignacion de valores que hace que fórmula sea satisfacible.

    def lanzar_subetapa_3(self):

        # Realizamos etapa
        self.etapa_4_3_realizada = True

        # Creamos nuevo panel
        self.panel_4_3 = ctk.CTkFrame(self.ventana, corner_radius=0)
        self.panel_4_3.pack(fill="both", expand=True)

        texto = "Hasta el momento hemos visto que si la fórmula es satisfacible, entonces \n"\
                "existe un subconjunto de valores de S cuya suma es t.\n"\
                " Para completar la poli-reducción nos falta probar el recíproco; es decir:\n\n"\
                "Si S contiene un subconjunto de valores que suma t, entonces existe una\n"\
                " asignación que hace que la fórmula sea satisfacible.\n\n"\
                "Veámos como obtener dicha asiganción:\n"\
                "▶ Todos los dígitos de los números que forman S son 0 o 1.\n"\
                "▶ Cada columna de la tabla tiene como mucho 5 dígitos.\n"\
                "▶ Por tanto, nunca al sumar los números del subconjunto se va a producir\n"\
                "   una llevada a la columna siguiente.\n"\
                "▶ Por tanto, la única manera de tener 1s en las primeras l columnas es tener,\n"\
                "   para cada i, un 1 en yi o un 1 en zi, pero no los dos y, por tanto,\n"\
                "   se encontraría la asignación de verdad que hace satisfacible a ϕ."
        panel = ctk.CTkFrame(self.panel_4_3)
        panel.pack(padx=10, pady=(100,10),fill="both")

        # Creamos panel con información
        canvas = tk.Canvas(panel, width=40, height=185)
        canvas.configure(bg='#63BCE9')
        canvas.pack(side="left", padx=(10,0), pady=10)
        canvas.create_text(20, 150, text="Etapa " + str(4.3), angle=90, anchor="w", font=('Arial', 15,'bold'))

        textbox = ctk.CTkTextbox(panel, width=485, height= 400)
        textbox.insert("1.0", texto)
        textbox.configure(state="disabled")
        textbox.pack(padx=10, pady=10)

        panel_botones_4_3 = ctk.CTkFrame(self.panel_4_3)
        panel_botones_4_3.pack(padx=10, pady=(0,10), fill=tk.Y, side='bottom')

        boton_anterior = ctk.CTkButton(panel_botones_4_3, text="Anterior", command=lambda:self.gestor_etapas.anterior(4.2))
        boton_anterior.grid(row=0, column = 0, padx=(10,20), pady=10)

        boton_siguiente = ctk.CTkButton(panel_botones_4_3, text="Siguiente",command=lambda:self.gestor_etapas.siguiente(5))
        boton_siguiente.grid(row=0, column = 1, padx=(20,10), pady=10)