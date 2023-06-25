import string
import tkinter as tk
import customtkinter as ctk
from matplotlib.figure import Figure
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ...interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp
import networkx as nx

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

        self.panel_grafo = None
        self.fila_bd = None
        self.num_nodos = 0

    ### Getters y setters ###
    
    def get_panel_0_0(self):
        return self.panel_0_0
    
    def get_panel_0_1(self):
        return self.panel_0_1
    
    def get_panel_0_2(self):
        return self.panel_0_2
    
    def get_num_nodos(self):
        return self.num_nodos
    
    def get_fila_bd(self):
        return self.fila_bd
    
    ################# ETAPA 0.0 #################

    # Informamos al usuario de los pasos que se van a
    # realizar en la poli-reducción:
    # 1º : demostramos que TSP-DEC es NP
    # 2º : realizamos la poli-reducción en sí
    # 3º : aplicaremos el Tercer Teorema de la Reducibilidad

    def lanzar_subetapa_0(self):

        # Panel con los pasos que se van a seguir
        self.panel_0_0 = ctk.CTkFrame(self.ventana)
        self.panel_0_0.pack(fill="both", expand=True, padx=10, pady=10)

        panel_0 = ctk.CTkFrame(self.panel_0_0)
        panel_0.pack(padx=10, pady=10)

        label = ctk.CTkLabel(panel_0, text="Poli-reducción UHAMCYCLE -> TSP-DEC", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(padx=10, pady=(10,30))

        texto = "Realizaremos la poli-reducción de UHAMCYCLE a TSP-DEC, así que probaremos\n que TSP-DEC es NP-Completo. Para ello, seguiremos los siguientes pasos:"
        label = ctk.CTkLabel(panel_0, text=texto, font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=(10,10))

        panel = ctk.CTkFrame(panel_0)
        panel.pack(padx=10, pady=10, fill="both",)
        texto="1º"
        label = ctk.CTkLabel(panel, fg_color="#6889B1", text=texto, font=ctk.CTkFont(size=13,weight="bold"))
        label.pack(padx=10, pady=10, fill="both")

        texto="Veremos que TSP-DEC pertence a la clase NP."
        label = ctk.CTkLabel(panel, text=texto, font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=(0,10), fill="both")

        panel = ctk.CTkFrame(panel_0)
        panel.pack(padx=10, pady=10, fill="both")
        texto="2º"
        label = ctk.CTkLabel(panel, text=texto, fg_color="#6889B1", font=ctk.CTkFont(size=13,weight="bold"))
        label.pack(padx=10, pady=10, fill="both")

        texto="Realizaremos la poli-reducción de UHAMCYCLE (NP-Completo) a TSP-DEC:\n\n" \
                    "Dado un grafo no dirigido G=(V,E), la reducción f construirá un nuevo\n " \
                    "grafo no dirigido, completo y pesado G'=(V',E',h) (donde h es una funcion que asigna a cada arista un peso)\n"\
                    "y genere un peso k, tal que G tiene un ciclo hamiltoniano si y sólo si, G' tiene un ciclo hamiltoniano con peso total ≤ k"
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
                    "En nuestro caso, L = UHAMCYCLE y L'= TSP-DEC."
        label = ctk.CTkLabel(panel, text=texto,font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=10, fill="both")

        panel_botones_0_0 = ctk.CTkFrame(panel_0, corner_radius = 0)
        panel_botones_0_0.pack(padx=10, pady=(0,10), side='bottom')

        boton_siguiente = ctk.CTkButton(panel_botones_0_0, text="Comenzar",
                                        command=lambda:self.gestor_etapas.siguiente(0.1))
    
        boton_siguiente.pack()


    ################# ETAPA 0.1 #################

    # Mostramos que UHAMCYCLE es NP.

    def lanzar_subetapa_1(self):

        self.panel_0_1 = ctk.CTkFrame(self.ventana)
        self.panel_0_1.pack(padx=10, pady=10, fill="both", expand=True)

        panel_titulo = ctk.CTkFrame(self.panel_0_1, fg_color="#6889B1")
        panel_titulo.pack(padx=30, pady=(30,10), fill=tk.X)

        label = ctk.CTkLabel(panel_titulo, text = "1º: TSP-DEC es NP", font=ctk.CTkFont(size=20,weight="bold"))
        label.pack(padx=50, pady=10)
        
        lista_texto = []
        texto = "Sabemos que TSP-DEC = {<G,K> | G es g.n.d.c.p. con c.h. con peso ≤ k}.\n\n"\
                "Para demostrar que TSP-DEC es un problema NP tenemos que probar que, dada una posible solución al problema,\npodemos constatar su validez en un tiempo polinomial.\n\n"\
                "Para ello, supongamos que tenemos un grafo no dirigido completo y pesado G'=(V',E') y un ciclo hamiltoniano C.\nPara comprobar que esta solución es válida debemos "\
                "de comprobar que dicho ciclo es un subgrafo de G' que\ncontiene a todos los vértices del grafo G' exactamente una vez y que su peso sea inferior a la constante k.\nUna forma de comprobar esto sería:\n\n"\
                " 1) Comprobar que es un ciclo hamiltoniano. Esto se puede hacer manteniendo un conjunto de nodos visitadas y\n   verificando que cada nodo se encuentre en el conjunto solo una vez.\n"\
                " 2) Comprobar que el peso de dicho ciclo es ≤ k. Para ello sumamos el peso de cada arista entre nodos\n   consecutivos en el ciclo.\n"\
                " 3) Si las condiciones anteriores se cumplen, estaremos ante una solución válida y devolveremos True; mientras\n    que si alguna falla devolveremos False.\n\n"\
                "Este algoritmo de verificación polinomial tiene una complejidad de tiempo O(n), donde n es el número de nodos del grafo, por lo que podemos afirmar que el problema TSP-DEC es NP."

                
        lista_texto.append(texto)

        lista_texto.append(texto)
        self.gestor_etapas.crear_panel_pseudocodigo(self.panel_0_1, altura=110, anchura=500, num_pasos=1, lista_texto=lista_texto)

        panel_botones_0_1 = ctk.CTkFrame(self.panel_0_1)
        panel_botones_0_1.pack(padx=10, pady=30, side='bottom')
        
        boton_siguiente = ctk.CTkButton(panel_botones_0_1, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(0.2))
        boton_siguiente.pack()


    ################# ETAPA 0.2 #################

    # Procedemos a realizar la poli-reducción en sí.
    # Para ello, se pedirá al usuario que seleccione un
    # grafo entre los almacenados en la base de datos

    def lanzar_subetapa_2(self):

        self.etapa_realizada = True

        self.panel_0_2 = ctk.CTkFrame(self.ventana)
        self.panel_0_2.pack(padx=10, pady=10,fill="both",expand=True)

        panel_titulo = ctk.CTkFrame(self.panel_0_2, fg_color="#6889B1")
        panel_titulo.pack(padx=30,pady=30,fill=tk.X)

        label = ctk.CTkLabel(panel_titulo, text = "2º: UHAMCYCLE ≤p TSP-DEC", fg_color="#6889B1",
                                font=ctk.CTkFont(size=20,weight="bold"))
        label.pack(padx=50, pady=(10,10))

        panel = ctk.CTkFrame(self.panel_0_2, fg_color=("#98B3D0","gray20"))
        panel.pack()

        # Panel selección grafo de partida
        panel_seleccion_grafo = ctk.CTkFrame(panel)
        panel_seleccion_grafo.pack(padx=10, pady=(10,10), side='top')

        label = ctk.CTkLabel(panel_seleccion_grafo,text="Para comenzar la poli-reducción, necesitamos un grafo de partida.")
        label.pack(padx=10, pady=10)

        # Panel de botones para selección de grafo
        panel_botones_seleccion_grafo = ctk.CTkFrame(panel_seleccion_grafo)
        panel_botones_seleccion_grafo.pack(padx=10, pady=10)

        boton_crear_grafo = ctk.CTkButton(panel_botones_seleccion_grafo, text="Crear grafo", fg_color="#D79E12", hover_color="#F0B72D",
                                            command=lambda:self.escoger_nuevo_grafo_segun_tipo())
        boton_crear_grafo.grid(padx=10, pady=10, row=0, column=0)
        
        boton_escoger_grafo_hampath = ctk.CTkButton(panel_botones_seleccion_grafo, text="Escoger grafo \n generado anteriormente",
                                                        fg_color=("#70AB94","#4D8871"), hover_color=("#7FB9A2","#52987C"),
                                                        command=lambda:self.escoger_grafo_previo_1())
        boton_escoger_grafo_hampath.grid(padx=10, pady=10, row=0, column=1)

        self.crear_panel_botones()



    def crear_panel_botones(self):

        # Paneles de botones
        self.panel_botones_0_2 = ctk.CTkFrame(self.panel_0_2)
        self.panel_botones_0_2.pack(padx=10, pady=10, side='bottom')

        boton_siguiente = ctk.CTkButton(self.panel_botones_0_2, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(1))
        boton_siguiente.grid(row=0, column=2, padx=10, pady=10)

        boton_anterior = ctk.CTkButton(self.panel_botones_0_2, text="Anterior", command=lambda:self.gestor_etapas.anterior(0.1))
        boton_anterior.grid(row=0, column=0, padx=10, pady=10)

    


    #####################################################################
    ################### RELATIVO AL NUEVO GRAFO #########################
    #####################################################################


    # Establece el numero de nodos del nuevo grafo
    def establecer_num_nodos(self, num_nodos):
         if num_nodos != "------":
            self.num_nodos = int(num_nodos)


    # Muestra al usuario una ventana en la que podrá seleccionar el número
    # de nodos que desea que tenga el grafo inicial de partida. (Combobox)
    def escoger_num_nodos(self, ventana_seleccion_nuevo_grafo, con_ciclo):

        # Destruimos la ventana anterior
        ventana_seleccion_nuevo_grafo.destroy()

        self.num_nodos = 0
        self.gestor_etapas.set_grafo_inicial_con_ch(con_ciclo)
        
        ventana_seleccion_nodos_grafo = VentanaPopUp(self.ventana)

        ventana_seleccion_nodos_grafo.geometry("")
        ventana_seleccion_nodos_grafo.configure(background="#9AA4B0")
        ventana_seleccion_nodos_grafo.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana_seleccion_nodos_grafo.title("Escoge el número de nodos")

        panel = ctk.CTkFrame(ventana_seleccion_nodos_grafo, corner_radius=0)
        panel.pack(fill="both", expand=True)

        label = ctk.CTkLabel(panel, text="Selecciona el nº de nodos que quieres que contenga el grafo:")
        label.pack(padx=10, pady=10)

        lista_valores = ["------","4","5","6","7","8","9","10","15"]

        combobox = ctk.CTkComboBox(panel, values=lista_valores, command=self.establecer_num_nodos)
        combobox.pack(padx=10, pady=10, side="top")

        boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:self.crear_grafo_nuevo(ventana_seleccion_nodos_grafo, con_ciclo))
        boton_aceptar.pack(padx=10, pady=10)

        ventana_seleccion_nodos_grafo.center()

    # Funcion que crea la ventana donde pregunta que tipo de grafo nuevo quieres crear, 
    # Si uno con ciclo o sin ciclo hamiltoniano.
    def escoger_nuevo_grafo_segun_tipo(self):
        ventana_seleccion_nuevo_grafo = VentanaPopUp(self.ventana)

        ventana_seleccion_nuevo_grafo.geometry("")
        ventana_seleccion_nuevo_grafo.configure(background="#9AA4B0")
        ventana_seleccion_nuevo_grafo.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana_seleccion_nuevo_grafo.title("Creación de nuevo grafo")

        panel = ctk.CTkFrame(ventana_seleccion_nuevo_grafo, corner_radius=0)
        panel.pack(fill="both", expand=True)

        label = ctk.CTkLabel(panel, text="Selecciona el grafo que deseas crear: ")
        label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        boton_grafo_sin_ciclo_hamiltoniano = ctk.CTkButton(panel, text="Sin ciclo\nhamiltoniano",  fg_color="#1D7841", hover_color="#269753", command=lambda:self.escoger_num_nodos(ventana_seleccion_nuevo_grafo, con_ciclo=False))
        boton_grafo_sin_ciclo_hamiltoniano.grid(row=1, column=0, padx=10, pady=10)

        boton_grafo_con_ciclo_hamiltoniano = ctk.CTkButton(panel, text="Con ciclo\nhamiltoniano", fg_color="#299ACB",hover_color="#31A9DD", command=lambda:self.escoger_num_nodos(ventana_seleccion_nuevo_grafo, con_ciclo=True))
        boton_grafo_con_ciclo_hamiltoniano.grid(row=1, column=1, padx=10, pady=10)

        ventana_seleccion_nuevo_grafo.center()



    # Funcion que crea un grafo nuevo no dirigido con ciclo o sin el en base al numero de nodos escogido en el combobox
    def crear_grafo_nuevo(self, ventana, con_ciclo):
        self.gestor_etapas.set_grafo_previo_escogido(False)

        if self.num_nodos != 0:

            # Destruimos ventana de selección num nodos del grafo
            ventana.destroy()

            grafo = nx.Graph()

            # Creamos los nodos
            for nodo in range (1, self.num_nodos + 1):
                grafo.add_node(list(string.ascii_lowercase)[nodo-1])

            # Creo aristas entre nodos (un camino)
            # Añadimos las aristas que solo forman un camino
            for nodo in range(1, self.num_nodos):
                grafo.add_edge(list(string.ascii_lowercase)[nodo-1], list(string.ascii_lowercase)[nodo])

            if con_ciclo==1:
                # Agregar arista desde el último nodo al primer nodo para cerrar el ciclo
                grafo.add_edge(list(string.ascii_lowercase)[grafo.number_of_nodes()-1], 'a')
                                

            # Guardamos el grafo de partida en la reduccion
            self.gestor_etapas.set_grafo_inicial([grafo])
        
            # Pintamos el grafo en el panel
            self.crear_panel_grafo_nuevo(grafo, resetear = True)
        
        else:
            pass
    
    # Funcion que grafica el grafo nuevo sobre el panel
    def crear_panel_grafo_nuevo(self, grafo, resetear):
        if self.panel_grafo != None:
            self.panel_grafo.pack_forget()

            self.panel_botones_0_2.pack_forget()
            self.crear_panel_botones() 

            if resetear:
                self.gestor_etapas.resetear_etapas()

        self.panel_grafo = ctk.CTkFrame(self.panel_0_2)
        self.panel_grafo.pack(padx=10, pady=(10,0), fill="both", expand=True)

        fig = Figure(figsize=(5,4), dpi=100)
        axis = fig.add_subplot(111)
        
        panel_botones_0_2_1 = ctk.CTkFrame(self.panel_botones_0_2, fg_color=("gray81", "gray20"))
        panel_botones_0_2_1.grid(row=0, column=1, padx=0, pady=5)

        boton_agrandar= ctk.CTkButton(panel_botones_0_2_1, text="Agrandar/guardar\n imagen",
                                    fg_color = ("#70AB94","#4D8871"), hover_color = ("#7FB9A2","#52987C"),
                                    command=lambda:self.gestor_etapas.agrandar_grafo(fig, 0))
        boton_agrandar.grid(row=0, column=0, padx=5, pady=5)

        """boton_repintar = ctk.CTkButton(panel_botones_0_2_1, text="Repintar grafo",
                                            fg_color = ("#8F61D4","#9A42D5"), hover_color=("#8041A9","#8041A9"),
                                            command=lambda:self.crear_panel_grafo_nuevo(self.gestor_etapas.get_grafo_inicial(), resetear = False))
        boton_repintar.grid(row=1, column=0, padx=5, pady=(5,5))"""

        color_map = ['#4188F3' for nodo in grafo.nodes()]
        
        nx.draw_networkx(grafo, ax=axis, node_color = color_map)

        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(fig, self.panel_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    #####################################################################
    ################### RELATIVO AL GRAFO DE BD #########################
    #####################################################################

    # Funcion que crea la ventana donde pregunta que tipo de grafo nuevo quieres cargar, 
    # Si uno con ciclo o sin ciclo hamiltoniano.
    def escoger_grafo_previo_1(self):
        ventana_seleccion_nuevo_grafo = VentanaPopUp(self.ventana)

        ventana_seleccion_nuevo_grafo.geometry("")
        ventana_seleccion_nuevo_grafo.configure(background="#9AA4B0")
        ventana_seleccion_nuevo_grafo.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana_seleccion_nuevo_grafo.title("Creación de nuevo grafo")

        panel = ctk.CTkFrame(ventana_seleccion_nuevo_grafo, corner_radius=0)
        panel.pack(fill="both", expand=True)

        label = ctk.CTkLabel(panel, text="Selecciona el grafo que deseas cargar: ")
        label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        boton_grafo_sin_ciclo_hamiltoniano = ctk.CTkButton(panel, text="Sin ciclo\nhamiltoniano",  fg_color="#1D7841", hover_color="#269753", command=lambda:self.escoger_grafo_previo(ventana_seleccion_nuevo_grafo, False))
        boton_grafo_sin_ciclo_hamiltoniano.grid(row=1, column=0, padx=10, pady=10)

        boton_grafo_con_ciclo_hamiltoniano = ctk.CTkButton(panel, text="Con ciclo\nhamiltoniano", fg_color="#299ACB",hover_color="#31A9DD", command=lambda:self.escoger_grafo_previo(ventana_seleccion_nuevo_grafo, True))
        boton_grafo_con_ciclo_hamiltoniano.grid(row=1, column=1, padx=10, pady=10)

        ventana_seleccion_nuevo_grafo.center()

    # Funcion que escribe el texto de la pantalla de error en caso de no encontrar un grafo 
    # con las carcaterisristicas indicadas
    def mostrar_mensaje_error(self, ventana, texto):
        panel = ctk.CTkFrame(ventana, corner_radius=0) 
        panel.pack(fill = "both", expand=True)

        label = ctk.CTkLabel(panel, text=texto)
        label.grid(row=1,column=0, padx=10, pady=10)

        boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:ventana.exit())
        boton_aceptar.grid(row=4, column=0, padx=10, pady=(0,10))

        # Imagen aviso
        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"), size=(50, 50))
        label = ctk.CTkLabel(panel, image=bg_image, text="")
        label.grid(row=0,column=0, padx=10, pady=10)

    # Funcion auxiliar que muestra el combobox que ilustra los diferentes grafos 
    # almacenados en la base de datos disponibles para este tipo de problema
    def escoger_grafo_previo(self,ventana, conCiclo):

        ventana.destroy()

        listaGrafos = Controlador.get_unica_instancia().get_base_datos().get_tabla_uhamcycle().get_todas_filas_tabla_uhamcycle()
        
        if listaGrafos==None:
            # Generar una ventana de error informando de esto
            ventana_error = VentanaPopUp(ventana_padre=None)
            ventana_error.title("No disponible")
            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')

            texto = 'No se ha encontrado ningún grafo no dirigido en la base de datos.'
            self.mostrar_mensaje_error(ventana_error, texto)

            ventana_error.center()
        else:

            grafos = []
            if conCiclo:
                for grafo in listaGrafos:
                    if grafo[3]==1:
                        grafos.append(grafo)
            else:
                for grafo in listaGrafos:
                    if grafo[3]==0:
                        grafos.append(grafo)

            if grafos==[]:
                # No hay ese tipo de grafo almacenado en la BD
                ventana_error = VentanaPopUp(ventana_padre=None)
                ventana_error.title("No disponible")
                ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')

                texto = 'No se ha encontrado ningún grafo no dirigido '
                if conCiclo:
                    texto += ' con ciclo hamiltoniano almacenado en la base de datos.'
                else:
                    texto += ' sin ciclo hamiltoniano almacenado en la base de datos.'
                self.mostrar_mensaje_error(ventana_error, texto)

                ventana_error.center()


            else:

                ventana_seleccion_grafo_previo = VentanaPopUp(self.ventana)

                ventana_seleccion_grafo_previo.geometry("")
                ventana_seleccion_grafo_previo.configure(background="#9AA4B0")
                ventana_seleccion_grafo_previo.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
                ventana_seleccion_grafo_previo.title("Seleccionar Grafo Previo")

                panel = ctk.CTkFrame(ventana_seleccion_grafo_previo, corner_radius=0)
                panel.pack(fill="both", expand=True)

                label = ctk.CTkLabel(panel, text="Selecciona el grafo que deseas: \n\n(id, numNodos)")
                label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

                # Obtengo el numero de nodos de todos los grafos que he obtenido en la busqueda anterior
                asociacion_numNodos_fila = {}
                lista_Combobox_pura = []
                for fila in grafos:
                    # Calculo el numero de nodos 
                    id = fila[0]
                    grafo = fila[1] 
                    
                    numNodos = grafo.number_of_nodes()

                    # Guardo la asociacion en el diccionario que contiene como valor la fila de la bd
                    asociacion_numNodos_fila[(id, numNodos)] = fila
                    lista_Combobox_pura.append((id, numNodos))
                    
                lista_Combobox = [str(item) for item in lista_Combobox_pura]

                
                combobox = ctk.CTkComboBox(panel, values=lista_Combobox, command=lambda value: self.establecer_grafo_bd(combobox, asociacion_numNodos_fila, value) )
                combobox.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
                
                boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda: self.crear_panel_grafo_almacenado(asociacion_numNodos_fila))
                boton_aceptar.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

                ventana_seleccion_grafo_previo.center()

    # Establece el valor del comobobox del grafo almacenado en la bd
    def establecer_grafo_bd(self, combobox, asociacion_numNodos_fila, value):
    
        # Calculo la tupla (id, numNodos)
        tupla_seleccionada = eval(combobox.get())

        # Guardo la fila de la tabla_uhamcycle
        if tupla_seleccionada in asociacion_numNodos_fila:
            self.fila_bd = asociacion_numNodos_fila[tupla_seleccionada]
    
    # Representa y selecciona el grafo almacenado en la base de datos para empezar la reduccion
    def crear_panel_grafo_almacenado(self, diccionario):

        self.gestor_etapas.set_grafo_previo_escogido(True)

        if self.panel_grafo != None:
            self.panel_grafo.pack_forget()

            self.panel_botones_0_2.pack_forget()
            self.crear_panel_botones() 

            self.gestor_etapas.resetear_etapas()

        self.panel_grafo = ctk.CTkFrame(self.panel_0_2)
        self.panel_grafo.pack(padx=10, pady=(10,0), fill="both", expand=True)

        fig = Figure(figsize=(5,4), dpi=100)
        axis = fig.add_subplot(111)

        panel_botones_0_2_1 = ctk.CTkFrame(self.panel_botones_0_2, fg_color=("gray81", "gray20"))
        panel_botones_0_2_1.grid(row=0, column=1, padx=0, pady=5)

        boton_agrandar= ctk.CTkButton(panel_botones_0_2_1, text="Agrandar/guardar\n imagen",
                                    fg_color = ("#70AB94","#4D8871"), hover_color = ("#7FB9A2","#52987C"),
                                    command=lambda:self.gestor_etapas.agrandar_grafo(fig,0))
        boton_agrandar.grid(row=0,column=0,padx=5,pady=5)

        grafo_inicial = []

        if self.fila_bd is not None:

            (id, grafo, colorMap, cicloHamiltoniano) = self.fila_bd[0:4]

            if cicloHamiltoniano==1:
                self.gestor_etapas.set_grafo_inicial_con_ch(True)
            else:
                self.gestor_etapas.set_grafo_inicial_con_ch(False)

            nx.draw_networkx(grafo, ax=axis, node_color=colorMap)

            grafo_inicial.append([id, grafo, colorMap, cicloHamiltoniano])

            # Pintamos en la figura
            canvas = FigureCanvasTkAgg(fig, self.panel_grafo)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # El grafo inicial está constituido por ambos grafos anteriores
            self.gestor_etapas.set_grafo_inicial(grafo_inicial)
            self.gestor_etapas.set_id_uhamcycle(id)
    