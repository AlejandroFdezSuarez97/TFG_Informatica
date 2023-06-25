import tkinter as tk
import customtkinter as ctk

import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import string

from ...interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp

from .etapa import Etapa
from controlador.controlador import Controlador
from PIL import Image

#####################################################################
# Clase que engloba la primera etapa a realizar en la poli-reducción. 
# Informamos al usuario qué se va a realizar.
#####################################################################
class Etapa0(Etapa):


    def __init__(self, ventana, gestor_etapas):
        
        super().__init__(ventana, gestor_etapas)

        self.panel_grafo = None
        self.fila_bd = None

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
    # 1º : demostramos que HAMCYCLE es NP
    # 2º : realizamos la poli-reducción en sí
    # 3º : aplicaremos el Tercer Teorema de la Reducibilidad

    def lanzar_subetapa_0(self):

        # Panel con los pasos que se van a seguir
        self.panel_0_0 = ctk.CTkFrame(self.ventana)
        self.panel_0_0.pack(fill="both", expand=True, padx=10, pady=10)

        panel_0 = ctk.CTkFrame(self.panel_0_0)
        panel_0.pack(padx=10, pady=10)

        label = ctk.CTkLabel(panel_0, text="Poli-reducción HAMPATH -> HAMCYCLE", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(padx=10, pady=(10,30))

        texto = "Realizaremos la poli-reducción de HAMPATH a HAMCYCLE, así que probaremos\n que HAMCYCLE es NP-Completo. Para ello, seguiremos los siguientes pasos:"
        label = ctk.CTkLabel(panel_0, text=texto, font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=(10,10))

        panel = ctk.CTkFrame(panel_0)
        panel.pack(padx=10, pady=10, fill="both",)
        texto="1º"
        label = ctk.CTkLabel(panel, fg_color="#6889B1", text=texto, font=ctk.CTkFont(size=13,weight="bold"))
        label.pack(padx=10, pady=10, fill="both")

        texto="Veremos que HAMCYCLE pertence a la clase NP."
        label = ctk.CTkLabel(panel, text=texto, font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=(0,10), fill="both")

        panel = ctk.CTkFrame(panel_0)
        panel.pack(padx=10, pady=10, fill="both")
        texto="2º"
        label = ctk.CTkLabel(panel, text=texto, fg_color="#6889B1", font=ctk.CTkFont(size=13,weight="bold"))
        label.pack(padx=10, pady=10, fill="both")

        texto="Realizaremos la poli-reducción de HAMPATH (NP-Completo) a HAMCYCLE:\n\n" \
                    "Para un grafo dirigido (con o sin cambino hamiltoniano) G, veremos cómo construir una\nfunción " \
                    "computable en tiempo polinomial que mapea el grafo G a otro grafo \ndirigido G' con un ciclo "\
                    "hamiltoniano si y sólo si G tiene camino hamiltoniano."
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
                    "En nuestro caso, L = HAMPATH y L'= HAMCYCLE."
        label = ctk.CTkLabel(panel, text=texto,font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=10, fill="both")

        panel_botones_0_0 = ctk.CTkFrame(panel_0, corner_radius = 0)
        panel_botones_0_0.pack(padx=10, pady=(0,10), side='bottom')

        boton_siguiente = ctk.CTkButton(panel_botones_0_0, text="Comenzar",
                                        command=lambda:self.gestor_etapas.siguiente(0.1))
    
        boton_siguiente.pack()

    ################# ETAPA 0.1 #################

    # Mostramos que HAMCYCLE es NP.

    def lanzar_subetapa_1(self):

        self.panel_0_1 = ctk.CTkFrame(self.ventana)
        self.panel_0_1.pack(padx=10, pady=10, fill="both", expand=True)

        panel_titulo = ctk.CTkFrame(self.panel_0_1, fg_color="#6889B1")
        panel_titulo.pack(padx=30, pady=(30,10), fill=tk.X)

        label = ctk.CTkLabel(panel_titulo, text = "1º: HAMCYCLE es NP", font=ctk.CTkFont(size=20,weight="bold"))
        label.pack(padx=50, pady=10)
        
        lista_texto = []
        texto = "Sabemos que HAMCYCLE = {<G> | G es grafo dirigido con ciclo hamiltoniano}."\
                "\nRecordemos que un grafo con ciclo hamiltoniano es aquel que contiene un \n" \
                "ciclo que pasa por todos los nodos exactamente una vez.\n\n" \
                "Para probar que lenguaje es NP, se comprueba a través de una MT que, dada  \n" \
                "una posible solución de HAMCYCLE, puede constatar su validez en tiempo polinomial. " \
                "Para ello, sea V el conjunto de vértices de G, E el conjunto de aristas y |V| \n" \
                "y |E| sus respectivos cardinales. Ahora, dada una lista de n vértices la MT \n" \
                "que constituyen un ciclo hamiltoniano, posible solución de HAMCYCLE,\n" \
                "comprueba si es válida:\n\n" \
                "1º: Comprueba que todos los vértices están en G y que todos los vértices\n" \
                "de G están en la lista.\n\n" \
                "2º: Verifica si, para cada par de vértices vi y v(i+1) existe una arista \n" \
                "que los une en G, comprobando además que el primer y el último nodo son\n" \
                "también adyacentes."

        lista_texto.append(texto)

        texto = "Por tanto, esta comprobación es O(n + |V| + n|E|), puesto que hay que chequear\n" \
                "n+|V| nodos y, por cada nodo de la lista, la comprobación de que existe una arista\n" \
                "que los une es O(|E|). Luego la validación es polinómica. " \
                "\n\n"\
                "Así, ya hemos probado que HAMCYCLE pertenece a la clase de complejidad NP."

        lista_texto.append(texto)
        self.gestor_etapas.crear_panel_pseudocodigo(self.panel_0_1, altura=110, anchura=470, num_pasos=2, lista_texto=lista_texto)

        panel_botones_0_1 = ctk.CTkFrame(self.panel_0_1)
        panel_botones_0_1.pack(padx=10, pady=30, side='bottom')
        
        boton_siguiente = ctk.CTkButton(panel_botones_0_1, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(0.2))
        boton_siguiente.pack()

    ################# ETAPA 0.2 #################

    # Procedemos a realizar la poli-reducción en sí.
    # Para ello, se pedirá al usuario que seleccione un
    # grafo entre unos ejemplos propuestos o uno almacenado
    # previamente en la base de datos.

    def lanzar_subetapa_2(self):

        self.etapa_realizada = True

        self.panel_0_2 = ctk.CTkFrame(self.ventana)
        self.panel_0_2.pack(padx=10, pady=10,fill="both",expand=True)

        panel_titulo = ctk.CTkFrame(self.panel_0_2, fg_color="#6889B1")
        panel_titulo.pack(padx=30,pady=30,fill=tk.X)

        label = ctk.CTkLabel(panel_titulo, text = "2º: HAMPATH ≤p HAMCYCLE", fg_color="#6889B1",
                                font=ctk.CTkFont(size=20,weight="bold"))
        label.pack(padx=50, pady=(10,10))

        panel = ctk.CTkFrame(self.panel_0_2, fg_color=("#98B3D0","gray20"))
        panel.pack()

        # Panel selección grafo hamiltoniano de partida
        panel_seleccion_grafo_hamiltoniano = ctk.CTkFrame(panel)
        panel_seleccion_grafo_hamiltoniano.pack(padx=10, pady=(10,10), side='top')

        label = ctk.CTkLabel(panel_seleccion_grafo_hamiltoniano,text="Para comenzar la poli-reducción, necesitamos un grafo de partida.")
        label.pack(padx=10, pady=10)

        # Panel de botones para selección de grafo
        panel_botones_seleccion_grafo = ctk.CTkFrame(panel_seleccion_grafo_hamiltoniano)
        panel_botones_seleccion_grafo.pack(padx=10, pady=10)

        boton_crear_grafo = ctk.CTkButton(panel_botones_seleccion_grafo, text="Crear grafo", fg_color="#D79E12", hover_color="#F0B72D",
                                            command=lambda:self.escoger_nuevo_grafo())
        boton_crear_grafo.grid(padx=10, pady=10, row=0, column=0)
        
        boton_escoger_grafo_hampath = ctk.CTkButton(panel_botones_seleccion_grafo, text="Escoger grafo \n generado anteriormente",
                                                        fg_color=("#70AB94","#4D8871"), hover_color=("#7FB9A2","#52987C"),
                                                        command=lambda:self.crear_panel_grafo_previo())
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
    
    def escoger_nuevo_grafo(self):

        ventana_seleccion_nuevo_grafo = VentanaPopUp(self.ventana)

        ventana_seleccion_nuevo_grafo.geometry("")
        ventana_seleccion_nuevo_grafo.configure(background="#9AA4B0")
        ventana_seleccion_nuevo_grafo.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana_seleccion_nuevo_grafo.title("Creación de nuevo grafo")

        panel = ctk.CTkFrame(ventana_seleccion_nuevo_grafo, corner_radius=0)
        panel.pack(fill="both", expand=True)

        label = ctk.CTkLabel(panel, text="Selecciona el grafo que deseas crear: ")
        label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        boton_grafo_sin_camino_hamiltoniano = ctk.CTkButton(panel, text="Sin camino\nhamiltoniano",  fg_color="#1D7841", hover_color="#269753", command=lambda:self.escoger_num_nodos(ventana_seleccion_nuevo_grafo, con_camino=False))
        boton_grafo_sin_camino_hamiltoniano.grid(row=1, column=0, padx=10, pady=10)

        boton_grafo_con_camino_hamiltoniano = ctk.CTkButton(panel, text="Con camino\nhamiltoniano", fg_color="#299ACB",hover_color="#31A9DD", command=lambda:self.escoger_num_nodos(ventana_seleccion_nuevo_grafo, con_camino=True))
        boton_grafo_con_camino_hamiltoniano.grid(row=1, column=1, padx=10, pady=10)

        ventana_seleccion_nuevo_grafo.center()

    #################################################
    ############ CASO CREAR NUEVO GRAFO  ############
    #################################################

    # Muestra al usuario una ventana en la que podrá seleccionar el número
    # de nodos que desea que tenga el grafo inicial de partida.
    def escoger_num_nodos(self, ventana_seleccion_nuevo_grafo, con_camino):

        # Destruimos la ventana anterior
        ventana_seleccion_nuevo_grafo.destroy()

        self.num_nodos = 0

        self.gestor_etapas.set_grafo_nuevo_con_camino(con_camino)

        ventana_seleccion_nodos_grafo = VentanaPopUp(self.ventana)

        ventana_seleccion_nodos_grafo.geometry("")
        ventana_seleccion_nodos_grafo.configure(background="#9AA4B0")
        ventana_seleccion_nodos_grafo.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana_seleccion_nodos_grafo.title("Escoge el número de nodos")

        panel = ctk.CTkFrame(ventana_seleccion_nodos_grafo, corner_radius=0)
        panel.pack(fill="both", expand=True)

        label = ctk.CTkLabel(panel, text="Selecciona el nº de nodos que quieres que contenga el grafo:")
        label.pack(padx=10, pady=10)

        lista_valores = ["------","5","10","15"]

        combobox = ctk.CTkComboBox(panel, values=lista_valores, command=self.establecer_num_nodos)
        combobox.pack(padx=10, pady=10, side="top")

        boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:self.crear_grafo_nuevo(ventana_seleccion_nodos_grafo, con_camino))
        boton_aceptar.pack(padx=10, pady=10)

        ventana_seleccion_nodos_grafo.center()

    # Establece el nº de nodos que tiene el grafo nuevo a crear.
    def establecer_num_nodos(self, num_nodos):
        if num_nodos != "------":
            self.num_nodos = int(num_nodos)

    

    # Crea el grafo inicial. Ya sea con camino hamiltoniano o no, según escoja
    # el usuario.
    def crear_grafo_nuevo(self, ventana_seleccion_nodos_grafo, con_camino):

        self.gestor_etapas.set_grafo_previo_escogido(False)

        if self.num_nodos != 0:

            # Destruimos ventana de selección num nodos del grafo
            ventana_seleccion_nodos_grafo.destroy()

            grafo = nx.DiGraph()

            # Creamos nodos del grafo
            for nodo in range (1, self.num_nodos + 1):
                grafo.add_node(list(string.ascii_lowercase)[nodo-1])
        
            # Si el grafo tiene camino hamiltoniano, unimos todos los 
            # nodos
            if con_camino:
                # Unimos los nodos anteriores
                for nodo in range(1, self.num_nodos):
                    grafo.add_edge(list(string.ascii_lowercase)[nodo-1], list(string.ascii_lowercase)[nodo])
        
            # Si el grafo no tiene camino hamiltoniano, dejamos un nodo
            # aislado, sin conectar
            else:
                # Unimos los nodos anteriores, menos el último
                for nodo in range(1, self.num_nodos-1):
                    grafo.add_edge(list(string.ascii_lowercase)[nodo-1], list(string.ascii_lowercase)[nodo])
        
            # Asignamos a la arista el grafo con el que vamos a trabajar
            self.gestor_etapas.set_grafo_inicial(grafo)
            self.gestor_etapas.set_grafo_inicial_con_ciclo(con_camino)
        
            self.crear_panel_grafo_nuevo(grafo, resetear = True)
        
        else:
            pass

    # Creamos panel del grafo para representarlo gráficamente.
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

        boton_repintar = ctk.CTkButton(panel_botones_0_2_1, text="Repintar grafo",
                                            fg_color = ("#8F61D4","#9A42D5"), hover_color=("#8041A9","#8041A9"),
                                            command=lambda:self.crear_panel_grafo_nuevo(self.gestor_etapas.get_grafo_inicial(), resetear = False))
        boton_repintar.grid(row=1, column=0, padx=5, pady=(5,5))

        color_map = ['#4188F3' for nodo in grafo.nodes()]

        nx.draw_networkx(grafo, ax=axis, node_color = color_map)

        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(fig, self.panel_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    ##################################################
    ############ CASO CARGAR GRAFO PREVIO ############
    ##################################################
    
    # Establece el valor del comobobox del grafo almacenado en la bd
    def establecer_grafo_bd(self, combobox, asociacion_numNodos_fila, value):
    
        # Calculo la tupla (id, numNodos)
        tupla_seleccionada = eval(combobox.get())

        if tupla_seleccionada in asociacion_numNodos_fila:
            self.fila_bd = asociacion_numNodos_fila[tupla_seleccionada]

    # Funcion que, muestra todos los grafos previos almacenados en la base de datos
    def crear_panel_grafo_previo(self):

        # Creo una ventana nueva en la que se pide escoger que tipo de grafo
        # se quiere buscar en la base de datos (con o sin camino hamiltoniano)
        # En cuanto se clicla la opcion deseada, aparece un combobox 
        # mostrando las diferentes opciones disponibles o una ventana de error
        # en el caso de no tener ningún grafo almacenado en la BD con dichas caracteristicas


        ventana_seleccion_grafo_bd = VentanaPopUp(self.ventana)

        ventana_seleccion_grafo_bd.geometry("")
        ventana_seleccion_grafo_bd.configure(background="#9AA4B0")
        ventana_seleccion_grafo_bd.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana_seleccion_grafo_bd.title("Seleección de un grafo en la BD")

        panel = ctk.CTkFrame(ventana_seleccion_grafo_bd, corner_radius=0)
        panel.pack(fill="both", expand=True)

        label = ctk.CTkLabel(panel, text="Selecciona el tipo de grafo que deseas buscar: ")
        label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        boton_grafo_sin_camino_hamiltoniano = ctk.CTkButton(panel, text="Sin camino\nhamiltoniano",  fg_color="#1D7841", hover_color="#269753", command=lambda:self.escoger_grafo_bd(ventana_seleccion_grafo_bd, 0))
        boton_grafo_sin_camino_hamiltoniano.grid(row=1, column=0, padx=10, pady=10)

        boton_grafo_con_camino_hamiltoniano = ctk.CTkButton(panel, text="Con camino\nhamiltoniano", fg_color="#299ACB",hover_color="#31A9DD", command=lambda:self.escoger_grafo_bd(ventana_seleccion_grafo_bd, 1))
        boton_grafo_con_camino_hamiltoniano.grid(row=1, column=1, padx=10, pady=10)

        ventana_seleccion_grafo_bd.center()


    # Funcion que escribe el texto de la pantalla de error en caso de no encontrar un grafo 
    # con las carcaterisristicas indicadas
    def mostrar_mensaje_error(self, ventana, con_camino):
        panel = ctk.CTkFrame(ventana, corner_radius=0) 
        panel.pack(fill = "both", expand=True)

        label = ctk.CTkLabel(panel, text='No se ha encontrado ningún grafo en la base de datos con la siguiente característica: ')
        label.grid(row=1,column=0, padx=10, pady=10)

        
        if con_camino==0:
            label = ctk.CTkLabel(panel, text='Grafo sin camino hamiltoniano')
        else:
            label = ctk.CTkLabel(panel, text='Grafo con camino hamiltoniano')
        label.grid(row=3,column=0, padx=10, pady=(0,10))


        boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:ventana.exit())
        boton_aceptar.grid(row=4, column=0, padx=10, pady=(0,10))

        # Imagen aviso
        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"), size=(50, 50))
        label = ctk.CTkLabel(panel, image=bg_image, text="")
        label.grid(row=0,column=0, padx=10, pady=10)



    # Funcion que representa el proceso de escoger los distintos grafos almacenados en la BD
    # Para ello, muestra una nueva ventana donde me solicita que tipo de grafo almacenado quiero buscar
    # Si quiero uno que contenga un camino hamiltoniano o no
    def escoger_grafo_bd(self, ventana, con_camino):
        # Destruimos la ventana anterior
        ventana.destroy()

        self.num_nodos = 0
        self.gestor_etapas.set_grafo_nuevo_con_camino(con_camino)
        
        # Hago una busqueda en la tabla Hampath en base al criterio de si se quiere un grafo con o sin camino
        # Si no hay grafos con esa caracteristica, informo con una ventana de error
        # En caso contrario creo una nueva ventana para seleccionar el grafo deseado 

        lista_Combobox_pura = []

        lista_valores = Controlador.get_unica_instancia().get_base_datos().get_tabla_hampath().get_grafos_por_caminoHamiltoniano(con_camino)
        
        if lista_valores == []:
            # No había grafos almacenados con esas caracteristicas
            # crear una pantalla de error
            
            ventana_error = VentanaPopUp(ventana_padre=None)

            ventana_error.title("No disponible")

            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        
            self.mostrar_mensaje_error(ventana_error,con_camino)

            ventana_error.center()

        else:

            ventana_seleccion_grafo = VentanaPopUp(self.ventana)

            ventana_seleccion_grafo.geometry("")
            ventana_seleccion_grafo.configure(background="#9AA4B0")
            ventana_seleccion_grafo.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
            ventana_seleccion_grafo.title("Escoge el grafo")

            panel = ctk.CTkFrame(ventana_seleccion_grafo, corner_radius=0)
            panel.pack(fill="both", expand=True)

            label = ctk.CTkLabel(panel, text="Selecciona el grafo almacenado que quieras en base al número de nodos:\n\n(id, numNodos)")
            label.pack(padx=10, pady=10)


            # Obtengo el numero de nodos de todos los grafos que he obtenido en la busqueda anterior
            asociacion_numNodos_fila = {}
            for id in lista_valores:
                
                fila = Controlador.get_unica_instancia().get_base_datos().get_tabla_hampath().get_fila_tabla_hampath_por_id(id)
                grafo = fila[2] # me quedo con uno de los dos grafos
                numNodos = grafo.number_of_nodes()
                
                # Guardo la asociacion en el diccionario que contiene como valor la fila de la bd
                asociacion_numNodos_fila[(id, numNodos)] = fila
                lista_Combobox_pura.append((id, numNodos))
                
            lista_Combobox = [str(item) for item in lista_Combobox_pura]    

            combobox = ctk.CTkComboBox(panel, values=lista_Combobox, command=lambda value: self.establecer_grafo_bd(combobox, asociacion_numNodos_fila, value))
            combobox.pack(padx=10, pady=10, side="top")


            boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:self.crear_panel_grafo_almacenado(asociacion_numNodos_fila))
            boton_aceptar.pack(padx=10, pady=10)

            ventana_seleccion_grafo.center()

    # Funcion que representa y selecciona el grafo almacenado en la base de datos para empezar la reduccion
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
            # Resto del código que utiliza fila_bd
            (grafo, pos, etiquetas, color_map, edge_colors, posiciones_s_t) = self.fila_bd[2:8]

            if pos=={}:
                nx.draw_networkx(grafo, ax=axis)

            else:
                nx.draw_networkx(grafo,ax=axis,labels=etiquetas, pos=pos, node_color=color_map, 
                                    edge_color=edge_colors,node_size=190,font_size=6)
            
                grafo_inicial.append((grafo, pos, etiquetas, color_map, edge_colors, posiciones_s_t))

                # 2º Grafo
                (grafo, pos, etiquetas, color_map, edge_colors, posiciones_s_t) = self.fila_bd[8:14]

                nx.draw_networkx(grafo,ax=axis,labels=etiquetas, pos=pos, node_color=color_map, 
                                    edge_color=edge_colors,node_size=190,font_size=6, connectionstyle = 'arc3, rad=0.4')
                grafo_inicial.append((grafo, pos, etiquetas, color_map, edge_colors, posiciones_s_t))

            # Pintamos en la figura
            canvas = FigureCanvasTkAgg(fig, self.panel_grafo)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # El grafo inicial está constituido por ambos grafos anteriores
            self.gestor_etapas.set_grafo_inicial(grafo_inicial)

