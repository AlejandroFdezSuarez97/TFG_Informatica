import random
import tkinter as tk
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ...interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp
from PIL import Image

from .etapa import Etapa
from controlador.controlador import Controlador

#####################################################################
# Clase que engloba la primera etapa a realizar en la poli-reducción. 
# Informamos al usuario qué se va a realizar.
#####################################################################
class Etapa0(Etapa):

    # Constructor
    def __init__(self, ventana, gestor_etapas):
        
        super().__init__(ventana, gestor_etapas)

        self.panel_tabla = None
        self.panel_imprimir_tabla = None

    ### Getters y setters ###
    
    def get_panel_0_0(self):
        return self.panel_0_0
    
    def get_panel_0_1(self):
        return self.panel_0_1
    
    def get_panel_0_2(self):
        return self.panel_0_2
    
    
    ################# ETAPA 0.0 #################

    # Informamos al usuario de los pasos que se van a
    # realizar en la poli-reducción:
    # 1º : demostramos que MOCHILA es NP
    # 2º : realizamos la poli-reducción en sí
    # 3º : aplicaremos el Tercer Teorema de la Reducibilidad

    def lanzar_subetapa_0(self):

        # Panel con los pasos que se van a seguir
        self.panel_0_0 = ctk.CTkFrame(self.ventana)
        self.panel_0_0.pack(fill="both", expand=True, padx=10, pady=10)

        panel_0 = ctk.CTkFrame(self.panel_0_0)
        panel_0.pack(padx=10, pady=10)

        label = ctk.CTkLabel(panel_0, text="Poli-reducción SUBSET-SUM -> MOCHILA", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(padx=10, pady=(10,30))

        texto = "Realizaremos la poli-reducción de SUBSET-SUM a MOCHILA, así que probaremos\n que MOCHILA es NP-Completo. Para ello, seguiremos los siguientes pasos:"
        label = ctk.CTkLabel(panel_0, text=texto, font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=(10,10))

        panel = ctk.CTkFrame(panel_0)
        panel.pack(padx=10, pady=10, fill="both",)
        texto="1º"
        label = ctk.CTkLabel(panel, fg_color="#6889B1", text=texto, font=ctk.CTkFont(size=13,weight="bold"))
        label.pack(padx=10, pady=10, fill="both")

        texto="Veremos que MOCHILA pertence a la clase NP."
        label = ctk.CTkLabel(panel, text=texto, font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=(0,10), fill="both")

        panel = ctk.CTkFrame(panel_0)
        panel.pack(padx=10, pady=10, fill="both")
        texto="2º"
        label = ctk.CTkLabel(panel, text=texto, fg_color="#6889B1", font=ctk.CTkFont(size=13,weight="bold"))
        label.pack(padx=10, pady=10, fill="both")

        texto="Realizaremos la poli-reducción de SUBSET-SUM (NP-Completo) a MOCHILA:\n\n" \
                    "Dado un conjunto S y un valor T, crearemos una función que en tiempo\n"\
                    "polinomial que sea capaz de crear dos valores K,B y asignar un peso y un beneficio a cada elemento de S\n"\
                    "así como averiguar si existe un subconjunto de S de forma que\n"\
                    "la suma del peso de cada elemento sea inferior o igual a K y el beneficio obtenido sea mayor o igual que B."
        label = ctk.CTkLabel(panel, text=texto, font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=10, fill="both")

        panel = ctk.CTkFrame(panel_0)
        panel.pack(padx=10, pady=10, fill="both")
        texto="3º"
        label = ctk.CTkLabel(panel, text=texto, fg_color="#6889B1", font=ctk.CTkFont(size=13,weight="bold"))
        label.pack(padx=10, pady=10, fill="both")

        texto="Usaremos el Tercer Teorema de la Reducibilidad:\n\n" \
                    "Para cada par de lenguajes L, L' con L ≤p L', si L es NP-Completo y L' es NP,\n" \
                    "entonces L' es NP-Completo.\n" \
                    "En nuestro caso, L = SUBSET-SUM y L'= MOCHILA."
        label = ctk.CTkLabel(panel, text=texto,font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=10, fill="both")

        panel_botones_0_0 = ctk.CTkFrame(panel_0, corner_radius = 0)
        panel_botones_0_0.pack(padx=10, pady=(0,10), side='bottom')

        boton_siguiente = ctk.CTkButton(panel_botones_0_0, text="Comenzar",
                                        command=lambda:self.gestor_etapas.siguiente(0.1))
    
        boton_siguiente.pack()


    ################# ETAPA 0.1 #################

    # Mostramos que MOCHILA es NP.

    def lanzar_subetapa_1(self):

        self.panel_0_1 = ctk.CTkFrame(self.ventana)
        self.panel_0_1.pack(padx=10, pady=10, fill="both", expand=True)

        panel_titulo = ctk.CTkFrame(self.panel_0_1, fg_color="#6889B1")
        panel_titulo.pack(padx=30, pady=(30,10), fill=tk.X)

        label = ctk.CTkLabel(panel_titulo, text = "1º: MOCHILA es NP", font=ctk.CTkFont(size=20,weight="bold"))
        label.pack(padx=50, pady=10)
        
        lista_texto = []
        texto = "Para demostrar que MOCHILA es NP tenemos que demostrar que dada una posible solución al problema, podemos comprobar si es válida en un tiempo polinomial.\n\n"\
        "Supongamos entonces que para la tupla <S,b,k> se tiene una solución potencial, esto es un subconjunto C de elementos de S. Para verificar si dicha solución es correcta, podemos seguir los siguientes pasos:\n\n"\
        " 1) Verificamos si la suma de los pesos de C es menor o igual a la capacidad de la mochila; es decir,\n    es menor que k.\n"\
        " 2) Si la suma de pesos es menor o igual que k, calculamos la suma de los beneficios de los elementos de    C y verificamos si esta suma es mayor o igual que B.\n"\
        " 3) Si ambas condiciones anteriores se cumplen, entonces el subconjunto propuesto es válido para\n    MOCHILA y devolvemos True. De lo contrario, devolvemos False.\n\n"\
        "Este algoritmo de verificación polinomial tiene una complejidad de tiempo O(n), donde n es el número de\nelementos del conjunto S. Por lo tanto, el problema MOCHILA es un problema NP, ya que existe un\nalgoritmo de verificación polinomial para él."


        lista_texto.append(texto)

        lista_texto.append(texto)
        self.gestor_etapas.crear_panel_pseudocodigo(self.panel_0_1, altura=110, anchura=470, num_pasos=1, lista_texto=lista_texto)

        panel_botones_0_1 = ctk.CTkFrame(self.panel_0_1)
        panel_botones_0_1.pack(padx=10, pady=30, side='bottom')
        
        boton_siguiente = ctk.CTkButton(panel_botones_0_1, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(0.2))
        boton_siguiente.pack()


    ################# ETAPA 0.2 #################

    # Procedemos a realizar la poli-reducción en sí.
    # Para ello, se pedirá al usuario que seleccione una
    # tabla entre las almacenadas en la base de datos

    def lanzar_subetapa_2(self):

        self.etapa_realizada = True

        self.panel_0_2 = ctk.CTkFrame(self.ventana)
        self.panel_0_2.pack(padx=10, pady=10,fill="both",expand=True)

        panel_titulo = ctk.CTkFrame(self.panel_0_2, fg_color="#6889B1")
        panel_titulo.pack(padx=30,pady=30,fill=tk.X)

        label = ctk.CTkLabel(panel_titulo, text = "2º: SUBSET-SUM ≤p MOCHILA", fg_color="#6889B1",
                                font=ctk.CTkFont(size=20,weight="bold"))
        label.pack(padx=50, pady=(10,10))

        panel = ctk.CTkFrame(self.panel_0_2, fg_color=("#98B3D0","gray20"))
        panel.pack()

        # Panel selección tabla de partida
        panel_seleccion_tabla = ctk.CTkFrame(panel)
        panel_seleccion_tabla.pack(padx=10, pady=(10,10), side='top')

        label = ctk.CTkLabel(panel_seleccion_tabla,text="Para comenzar la poli-reducción, necesitamos una tabla de partida.")
        label.pack(padx=10, pady=10)


        # Creo un combobox que me permita escoger la tabla de partida
        texto_combobox = ["----------- INSERTAR NUEVO PROBLEMA ----------------------"]
        filas = Controlador.get_unica_instancia().get_base_datos().get_tabla_subset().get_todas_filas_tabla_subset()

        

        # Creo un diccionario para saber que conjunto escogo en el combobox
        self.diccionario = {}

        # Para ofertar las distintas tablas almacenadas en la BBDD lo hacemos con el mensaje:
        # Conjunto con X elementos que (no) contiene un subconjunto que suma t
        for fila in filas:
            [id,conjunto, valor_t, existeSub, subconjunto] = fila
            texto = "Conjunto de " + str(len(conjunto)) + " elementos que"
            if existeSub==0:
                texto += " no"
            texto += " tiene un subconjunto que suma " + str(valor_t)
            self.diccionario[texto] = fila
            texto_combobox.append(texto)
        
        combobox = ctk.CTkComboBox(panel_seleccion_tabla, values=texto_combobox, command=lambda entrada: self.escoger_tabla_inicial(entrada), width=300)
        combobox.pack(padx=10, pady=10)


        self.crear_panel_botones()


    # creo los botones anterior y siguiente propios del gestor de etapas
    def crear_panel_botones(self):

        # Paneles de botones
        self.panel_botones_0_2 = ctk.CTkFrame(self.panel_0_2)
        self.panel_botones_0_2.pack(padx=10, pady=10, side='bottom')

        boton_siguiente = ctk.CTkButton(self.panel_botones_0_2, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(1))
        boton_siguiente.grid(row=0, column=2, padx=10, pady=10)

        boton_anterior = ctk.CTkButton(self.panel_botones_0_2, text="Anterior", command=lambda:self.gestor_etapas.anterior(0.1))
        boton_anterior.grid(row=0, column=0, padx=10, pady=10)

    # Controlador del combobox
    def escoger_tabla_inicial(self, entrada):

        if self.panel_imprimir_tabla is not None:
            self.panel_imprimir_tabla.destroy()

        self.panel_imprimir_tabla =  ctk.CTkFrame(self.panel_0_2)
        self.panel_imprimir_tabla.pack(padx=0, pady=10, side='top')

        if self.panel_tabla is not None:
            self.panel_tabla.destroy()

        self.panel_tabla = ctk.CTkFrame(self.panel_imprimir_tabla)
        self.panel_tabla.pack(padx=0,pady=(30,10),side="top", fill="both", expand=True)

        boton_agrandar = ctk.CTkButton(self.panel_botones_0_2, text="Agrandar/guardar\n imagen",
                                            fg_color=("#70AB94","#4D8871"), hover_color=("#7FB9A2","#52987C"),
                                            command=lambda:self.gestor_etapas.agrandar_tabla(self.f,0))
        boton_agrandar.grid(row=0,column=1,padx=10,pady=10)

        # Imprimo el problema en el panel
        self.f = Figure(figsize=(20,4), dpi=100)
        self.axis = self.f.add_subplot(111)

        if entrada == "----------- INSERTAR NUEVO PROBLEMA ----------------------":
            
            # Vamos a crear una jerarquía de ventanas para crear un caso artificial

            self.gestor_etapas.set_problema_inicial_en_BD(False)
            
            self.ventana_crear_problema = VentanaPopUp(ventana_padre=None)

            self.ventana_crear_problema.title("Crear problema nuevo")

            self.ventana_crear_problema.iconbitmap('interfaz_grafica/interfaz_app/img/simulador.ico')

            
            label = ctk.CTkLabel(self.ventana_crear_problema, fg_color=("#A3B5CC","gray20"), text="¿Quieres que el problema tenga solución?",
                                font=ctk.CTkFont(size=15, weight="bold"))
            label.pack(padx=10, pady=10, side="top", fill=ctk.X)

            panel = ctk.CTkFrame(self.ventana_crear_problema, corner_radius=0) 
            panel.pack(fill = "both", expand=True)


            boton_si = ctk.CTkButton(panel, text="Sí", command=lambda: self.crear_problema_inicial(1))
            boton_si.grid(row=2, column=0, padx=10, pady=(10,10))

            boton_no = ctk.CTkButton(panel, text="No", command=lambda: self.crear_problema_inicial(0))
            boton_no.grid(row=2, column=1, padx=10, pady=(10,10))

            self.ventana_crear_problema.center()

        else:

            self.gestor_etapas.set_problema_inicial_en_BD(True)
            
            [id, conjunto, valor_t, existeSub, subconjunto] = self.diccionario[entrada]
            
            problema_inicial = [id, conjunto, valor_t, existeSub, subconjunto]
            self.gestor_etapas.set_tabla_inicial(problema_inicial)


            # ------------------ Pinto el problema inicial

            self.imprimir_problema_inicial(conjunto, valor_t, existeSub, subconjunto, self.axis)


            # Pintamos en la figura
            canvas = FigureCanvasTkAgg(self.f, self.panel_tabla)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)




    # Sistema de ventanas para configurar un problema inicial
    def crear_problema_inicial(self, con_subconjunto):

        self.ventana_crear_problema.destroy()


        ventana_nueva = VentanaPopUp(ventana_padre=None)

        ventana_nueva.title("Crear problema nuevo")

        ventana_nueva.iconbitmap('interfaz_grafica/interfaz_app/img/simulador.ico')

            
        label = ctk.CTkLabel(ventana_nueva, fg_color=("#A3B5CC","gray20"), text="Selecciona el tamaño del conjunto S",
                                font=ctk.CTkFont(size=15, weight="bold"))
        label.grid(row=1,column=0, padx=10, pady=10)

        panel = ctk.CTkFrame(ventana_nueva, corner_radius=0) 
        panel.grid(row=2, column=0, padx=10, pady=10)


        texto_combobox = [" "]
        lista = range(1,15)
        lista = [str(e) for e in range(1,16)]
        for e in lista:
            texto_combobox.append(e)
        
        combobox = ctk.CTkComboBox(panel, values=texto_combobox, command=lambda entrada: self.establecer_num_elem_conjunto(entrada, ventana_nueva, con_subconjunto), width=300)
        combobox.grid(row=3,column=0, padx=10, pady=10)

        ventana_nueva.center()

    # Creamos un panel que pregunte el rango de valores de los elementos que pertenezcan al subconjunto
    def establecer_num_elem_conjunto(self, entrada, ventana_antes, con_subconjunto):

        if entrada == " ":
            self.lanzar_ventana_error("Por favor, selecciona un número válido")
        else:

            ventana_antes.destroy()

            ventana_nueva = VentanaPopUp(ventana_padre=None)

            ventana_nueva.title("Crear problema nuevo")

            ventana_nueva.iconbitmap('interfaz_grafica/interfaz_app/img/simulador.ico')

            panel = ctk.CTkFrame(ventana_nueva, corner_radius=0) 
            panel.pack(fill = "both", expand=True)

            label = ctk.CTkLabel(panel, fg_color=("#A3B5CC","gray20"), text="Introduzca el valor t que debe sumar el subconjunto:",
                                font=ctk.CTkFont(size=15, weight="bold"))
            label.pack(padx=10, pady=10, side="top", fill=ctk.X)

            self.valor_t = tk.StringVar()
            entry_formula = ctk.CTkEntry(panel, textvariable=self.valor_t, width=300)
            entry_formula.pack(padx=10, pady=10, fill=ctk.X)

            

            boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:self.crear_datos_problema(con_subconjunto,entrada, ventana_nueva))
            boton_aceptar.pack(padx=10, pady=(0, 10))

            ventana_nueva.center()

    
    def crear_datos_problema(self, con_subconjunto, tam_conjunto, ventana):
        
        valor_t = self.valor_t.get()

        if valor_t=='':
            # Crear una ventana de error 
            self.lanzar_ventana_error("Introduzca un ENTERO POSITIVO que repesente el valor de t")
        else:
            try:
                if int(valor_t) < 0 or int(valor_t)==0:
                    self.lanzar_ventana_error("Introduzca un entero POSITIVO que repesente el valor de t")
                else:
                    ventana.destroy()

                    tam_conjunto = int(tam_conjunto)

                    # Vamos a crear un conjunto con tam_conjuntos elementos
                    if con_subconjunto==0:
                        # Creo un conjunto de nuemeros aleatorios
                        conjunto = []
                        for _ in range(tam_conjunto):
                            numero = random.randint(int(self.valor_t.get())+1, 10 * tam_conjunto)
                                    
                            conjunto.append(numero)
                        subconjunto = []

                    else:
                        # Necesito crear un subconjunto que sume valor_t
                        conjunto, subconjunto = self.generar_conjunto_subconjunto_aleatorio(tam_conjunto)
                    

                    # Guardo el problema inicial
                    self.gestor_etapas.set_tabla_inicial([0, conjunto, int(self.valor_t.get()), con_subconjunto, subconjunto])

                    self.imprimir_problema_inicial(conjunto, int(self.valor_t.get()), con_subconjunto, subconjunto, self.axis)


                    # Pintamos en la figura
                    canvas = FigureCanvasTkAgg(self.f, self.panel_tabla)
                    canvas.draw()
                    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            
            except ValueError:
                if float(valor_t):
                    self.lanzar_ventana_error("Introduza un entero (no float) positivo como valor de t")
                    
            

    # Genera el conjunto aleatorio que debe contener un subconjunto que sume t
    def generar_conjunto_subconjunto_aleatorio(self, tam_conjunto):
        valor_t = int(self.valor_t.get())
        conjunto = []
        subconjunto = []

        # Generar un subconjunto que sume exactamente valor_t
        suma_actual = 0
        while suma_actual < valor_t :
            numero = random.randint(1, valor_t - suma_actual)
            
            if len(subconjunto) == tam_conjunto-1:
                # Solo puedo meter un num más al subconjunto
                # meto lo que me queda para llegar a suma_actual
                numero = valor_t-suma_actual

            subconjunto.append(numero)
            suma_actual += numero

        # Llenar el resto del conjunto con números aleatorios
        while len(conjunto) < tam_conjunto:
            numero = random.randint(1, 2 * valor_t)
            conjunto.append(numero)

        # Combinar el subconjunto y el resto del conjunto
        conjunto[:len(subconjunto)] = subconjunto

        subconjunto.sort()

        return conjunto, subconjunto


    def lanzar_ventana_error(self, texto):

        ventana_error = VentanaPopUp(ventana_padre=None)

        ventana_error.title("No disponible")

        ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/info_ico.ico')

        panel = ctk.CTkFrame(ventana_error, corner_radius=0) 
        panel.pack(fill = "both", expand=True)

        label = ctk.CTkLabel(panel, text=texto)
        label.grid(row=1,column=0, padx=10, pady=10)

        boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:ventana_error.exit())
        boton_aceptar.grid(row=4, column=0, padx=10, pady=(0,10))

        # Imagen aviso
        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"), size=(50, 50))
        label = ctk.CTkLabel(panel, image=bg_image, text="")
        label.grid(row=0,column=0, padx=10, pady=10)

        ventana_error.center()


    # Impirme el problema inicial
    def imprimir_problema_inicial(self,conjunto, valor_t, existeSub, subconjunto, ax1):

        # Creo los datos:
        datos = ["<", "{"]
        for n in conjunto:
            datos.append(str(n))
                
        ultimo = datos.pop()
        datos.append(ultimo)
        datos.append("}")
        datos.append(", ")
        datos.append(str(valor_t))
        datos.append(">")
                
        subconjunto_str = [str(n) for n in subconjunto]


        tabla = ax1.table(cellText=[datos],  cellLoc='center', loc='center',bbox=[0, 0.5, 1, 0.2])
                

        #  ----------- Coloreo  --------

        # Pinto toda la fila de amarillo
        for i in range(0,len(datos)):
            cell = tabla[0,i]
            cell.set_facecolor('#FFFFF0')

        # pinto la celda del valor de t
        cell = tabla[0,len(datos)-2]
        cell.set_facecolor('#AFEEEE')

        # Si hay elementos en el subconjunto, los pinto
        if existeSub == 1:

            # Creo un diccionario que me servirá para ver que elementos del conjunto he pintado
            pintado = {}
            for i,elemento in enumerate(datos):
                pintado[i,elemento] = False


            for elemento in subconjunto:
                for i, elem_datos in enumerate(datos):
                    
                    if str(elem_datos) == str(elemento) and pintado[i,elem_datos]==False :
                        cell = tabla[0,i]
                        cell.set_facecolor("#DA70D6")
                        pintado[i,elem_datos] = True
                        break
                    
                
                        
        ax1.axis('off')