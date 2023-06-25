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
    # 1º : demostramos que UHAMCYCLE es NP
    # 2º : realizamos la poli-reducción en sí
    # 3º : aplicaremos el Tercer Teorema de la Reducibilidad

    def lanzar_subetapa_0(self):

        # Panel con los pasos que se van a seguir
        self.panel_0_0 = ctk.CTkFrame(self.ventana)
        self.panel_0_0.pack(fill="both", expand=True, padx=10, pady=10)

        panel_0 = ctk.CTkFrame(self.panel_0_0)
        panel_0.pack(padx=10, pady=10)

        label = ctk.CTkLabel(panel_0, text="Poli-reducción HAMCYCLE -> UHAMCYCLE", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(padx=10, pady=(10,30))

        texto = "Realizaremos la poli-reducción de HAMCYCLE a UHAMCYCLE, así que probaremos\n que UHAMCYCLE es NP-Completo. Para ello, seguiremos los siguientes pasos:"
        label = ctk.CTkLabel(panel_0, text=texto, font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=(10,10))

        panel = ctk.CTkFrame(panel_0)
        panel.pack(padx=10, pady=10, fill="both",)
        texto="1º"
        label = ctk.CTkLabel(panel, fg_color="#6889B1", text=texto, font=ctk.CTkFont(size=13,weight="bold"))
        label.pack(padx=10, pady=10, fill="both")

        texto="Veremos que UHAMCYCLE pertence a la clase NP."
        label = ctk.CTkLabel(panel, text=texto, font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=(0,10), fill="both")

        panel = ctk.CTkFrame(panel_0)
        panel.pack(padx=10, pady=10, fill="both")
        texto="2º"
        label = ctk.CTkLabel(panel, text=texto, fg_color="#6889B1", font=ctk.CTkFont(size=13,weight="bold"))
        label.pack(padx=10, pady=10, fill="both")

        texto="Realizaremos la poli-reducción de HAMCYCLE (NP-Completo) a UHAMCYCLE:\n\n" \
                    "Dado un grafo dirigido G=(V,E), veremos cómo construir una\nfunción " \
                    "computable en tiempo polinomial que mapea el grafo G a otro grafo \n no dirigido G'=(V',E') "\
                    " de forma que: G' tiene un ciclo hamiltoniano no dirigido si y sólo si G tenía un ciclo hamiltoniano dirigido."
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
                    "En nuestro caso, L = HAMCYCLE y L'= UHAMCYCLE."
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

        label = ctk.CTkLabel(panel_titulo, text = "1º: UHAMCYCLE es NP", font=ctk.CTkFont(size=20,weight="bold"))
        label.pack(padx=50, pady=10)
        
        lista_texto = []
        texto = "Sabemos que UHAMCYCLE = {<G> | G es grafo no dirigido con ciclo hamiltoniano}"\
                "\nRecordemos que un grafo con ciclo hamiltoniano es aquel que contiene un " \
                "ciclo que pasa por todos los nodos\n exactamente una vez.\n\n" \
                "Para demostrar que UHAMCYCLE es un problema NP tenemos que probar que, dada una posible solución al problema,\npodemos constatar su validez en un tiempo polinomial.\n\n"\
                "Para ello, supongamos que tenemos un grafo no dirigido G'=(V',E') y un ciclo hamiltoniano C con n nodos. Para comprobar que esta solución es válida debemos "\
                "de comprobar que dicho ciclo es un subgrafo de G' que contiene a todos los vértices del grafo G' exactamente una vez. Una forma de comprobar esto sería:\n\n"\
                " 1) Verificar que el ciclo visite cada vértice exactamente una vez: Esto se puede hacer comprobando si el ciclo contiene\n  todos los vértices del grafo y si ningún vértice se repite.\n"\
                " 2) Verificar que haya una arista entre cada par de vértices adyacentes en el ciclo: Esto se puede hacer comprobando si\n   todas las aristas en el ciclo existen en el grafo.\n\n"\
                "Estas comprobaciones se pueden hacer en O(n+|V'|+n|E'|), por lo que podemos concluir que se hace un un tiempo\npolinomial."  

        lista_texto.append(texto)

        lista_texto.append(texto)
        self.gestor_etapas.crear_panel_pseudocodigo(self.panel_0_1, altura=300, anchura=800, num_pasos=1, lista_texto=lista_texto)

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

        label = ctk.CTkLabel(panel_titulo, text = "2º: HAMCYCLE ≤p UHAMCYCLE", fg_color="#6889B1",
                                font=ctk.CTkFont(size=20,weight="bold"))
        label.pack(padx=50, pady=(10,10))

        panel = ctk.CTkFrame(self.panel_0_2, fg_color=("#98B3D0","gray20"))
        panel.pack()

        # Panel selección grafo hamiltoniano de partida
        panel_seleccion_grafo = ctk.CTkFrame(panel)
        panel_seleccion_grafo.pack(padx=10, pady=(10,10), side='top')

        label = ctk.CTkLabel(panel_seleccion_grafo,text="Para comenzar la poli-reducción, necesitamos un grafo de partida.")
        label.pack(padx=10, pady=10)

        # Panel de botones para selección de grafo
        panel_botones_seleccion_grafo = ctk.CTkFrame(panel_seleccion_grafo)
        panel_botones_seleccion_grafo.pack(padx=10, pady=10)

        boton_crear_grafo = ctk.CTkButton(panel_botones_seleccion_grafo, text="Crear grafo", fg_color="#D79E12", hover_color="#F0B72D",
                                            command=lambda:self.escoger_grafo())
        boton_crear_grafo.grid(padx=10, pady=10, row=0, column=0)
        
        boton_escoger_grafo_hampath = ctk.CTkButton(panel_botones_seleccion_grafo, text="Escoger grafo \n generado anteriormente",
                                                        fg_color=("#70AB94","#4D8871"), hover_color=("#7FB9A2","#52987C"),
                                                        command=lambda:self.escoger_grafo_1())
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

    def escoger_grafo(self):

        ventana_seleccion_nuevo_grafo = VentanaPopUp(self.ventana)

        ventana_seleccion_nuevo_grafo.geometry("")
        ventana_seleccion_nuevo_grafo.configure(background="#9AA4B0")
        ventana_seleccion_nuevo_grafo.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana_seleccion_nuevo_grafo.title("Creación de nuevo grafo")

        panel = ctk.CTkFrame(ventana_seleccion_nuevo_grafo, corner_radius=0)
        panel.pack(fill="both", expand=True)

        label = ctk.CTkLabel(panel, text="Selecciona el grafo que deseas crear: ")
        label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        boton_grafo_sin_camino_hamiltoniano = ctk.CTkButton(panel, text="Sin ciclo\nhamiltoniano",  fg_color="#1D7841", hover_color="#269753", command=lambda:self.escoger_nuevo_grafo(ventana_seleccion_nuevo_grafo, con_camino=False))
        boton_grafo_sin_camino_hamiltoniano.grid(row=1, column=0, padx=10, pady=10)

        boton_grafo_con_camino_hamiltoniano = ctk.CTkButton(panel, text="Con ciclo\nhamiltoniano", fg_color="#299ACB",hover_color="#31A9DD", command=lambda:self.escoger_nuevo_grafo(ventana_seleccion_nuevo_grafo, con_camino=True))
        boton_grafo_con_camino_hamiltoniano.grid(row=1, column=1, padx=10, pady=10)

        ventana_seleccion_nuevo_grafo.center()


    # Funcion auxiliar que muestra el combobox que ilustra las opciones disponibles para
    # crear el nuevo grafo
    def escoger_nuevo_grafo(self, ventana, con_camino):

        ventana.destroy()

        self.gestor_etapas.set_grafo_dirigido_con_ch(con_camino)

        ventana_seleccion_nuevo_grafo = VentanaPopUp(self.ventana)

        ventana_seleccion_nuevo_grafo.geometry("")
        ventana_seleccion_nuevo_grafo.configure(background="#9AA4B0")
        ventana_seleccion_nuevo_grafo.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana_seleccion_nuevo_grafo.title("Creación de nuevo grafo")

        panel = ctk.CTkFrame(ventana_seleccion_nuevo_grafo, corner_radius=0)
        panel.pack(fill="both", expand=True)

        label = ctk.CTkLabel(panel, text="Selecciona el número de nodos que quieres que tenga el grafo: ")
        label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # tendría que crear un combobox que me pregunte el numero de nodos
        # la funcion controladora del combobox sería la responsable de crear dicho 
        # grafo (que por simplicidad será sencillamente un ciclo)
        lista_valores = ["---- Seleccionar Nº de nodos ----", "3","4","5","6","7","8"]
        combobox = ctk.CTkComboBox(panel, values=lista_valores, command=lambda value: self.establecer_numNodos(value), width=300)
        combobox.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        
        boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:self.crear_grafo_nuevo(ventana_seleccion_nuevo_grafo, con_camino))
        boton_aceptar.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        ventana_seleccion_nuevo_grafo.center()

    # Guardo el numero de nodos que he seleccionado en el combobox
    def establecer_numNodos(self, numNodos):
        if numNodos!="---- Seleccionar Nº de nodos ----":
            self.num_nodos = int(numNodos)

    # Funcion que crea un grafo nuevo en base al numero de nodos escogido en el combobox
    def crear_grafo_nuevo(self, ventana, con_camino):
        self.gestor_etapas.set_grafo_previo_escogido(False)

        if self.num_nodos != 0:

            # Destruimos ventana de selección num nodos del grafo
            ventana.destroy()

            if con_camino:
                # ----------------- CONSTRUYO EL GRAFO CICLO ---------------------
                grafo = nx.DiGraph()
                etiquetas = list(string.ascii_lowercase)

                # Agregar nodos al grafo
                for i in range(1, self.num_nodos + 1):
                    grafo.add_node(i, name=etiquetas[i-1])
                
                
                # Agregar aristas para formar un ciclo dirigido
                for i in range(1, self.num_nodos):
                    grafo.add_edge(i, i+1)

                # Agregar arista desde el último nodo al primer nodo para cerrar el ciclo
                grafo.add_edge(self.num_nodos, 1)

            else:
                # Construyo un grafo que no sea un ciclo
                grafo = nx.DiGraph()
                etiquetas = list(string.ascii_lowercase)

                # Agregar nodos al grafo
                for i in range(1, self.num_nodos + 1):
                    grafo.add_node(i, name=etiquetas[i-1])
                
                
                # Agregar aristas para formar un ciclo dirigido
                for i in range(1, self.num_nodos):
                    grafo.add_edge(i, i+1)


            # Guardamos el grafo de partida en la reduccion
            self.gestor_etapas.set_grafo_dirigido([grafo])
            
            
            
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
                                            command=lambda:self.crear_panel_grafo_nuevo(self.gestor_etapas.get_grafo_dirigido(), resetear = False))
        boton_repintar.grid(row=1, column=0, padx=5, pady=(5,5))"""

        color_map = ['#4188F3' for nodo in grafo.nodes()]
        # Crear un diccionario de atributos de nodos con los nombres
        node_labels = {node: data['name'] for node, data in grafo.nodes(data=True)}

        nx.draw_networkx(grafo, ax=axis, node_color = color_map, labels=node_labels)

        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(fig, self.panel_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    #####################################################################
    ################### RELATIVO AL GRAFO DE BD #########################
    #####################################################################

    # Pregunta que tipo de grafo quieres buscar en la BD
    def escoger_grafo_1(self):

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
    def escoger_grafo_previo(self, ventana, conCiclo):

        ventana.destroy()

        self.gestor_etapas.set_grafo_dirigido_con_ch(conCiclo)


        listaGrafos = Controlador.get_unica_instancia().get_base_datos().get_tabla_hamcycle().get_todas_filas_tabla_hamcycle()
        
        if listaGrafos==None:
            # Generar una ventana de error informando de esto
            ventana_error = VentanaPopUp(ventana_padre=None)
            ventana_error.title("No disponible")
            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')

            texto = 'No hay ningún grafo hamcycle almacenado en la BD.'
            self.mostrar_mensaje_error(ventana_error, texto)

            ventana_error.center()
        else:

            grafos = []
            if conCiclo:
                #Muestro solo los grafos con ciclo hamiltoniano
                for grafo in listaGrafos:
                    if grafo[7]==1:
                        grafos.append(grafo)

            else:
                # Muestro solo los grafos sin ciclo hamiltoniano
                for grafo in listaGrafos:
                    if grafo[7]==0:
                        grafos.append(grafo)

            if grafos == []:
                # Generar una ventana de error informando de esto
                ventana_error = VentanaPopUp(ventana_padre=None)
                ventana_error.title("No disponible")
                ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')

                texto = 'No hay ningún grafo dirigido '
                if conCiclo:
                    texto += 'con ciclo hamiltoniano almacenado en la base de datos.'
                else:
                    texto += 'sin ciclo hamiltoniano almacenado en la base de datos.'
                
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
                    # Recordar que el grafo hamcycle puede estar compuesto por dos grafos Hampath o no
                    id = fila[0]
                    id_hampath = fila[1]
                    grafo_3 = fila[2] # me quedo con el grafo_3
                    if id_hampath==-1:
                        # caso en el que el grafo hamcycle no depende del hampath
                        numNodos = grafo_3.number_of_nodes()
                    else:
                        numNodos = grafo_3.number_of_nodes()
                        grafoHampath = Controlador.get_unica_instancia().get_base_datos().get_tabla_hampath().get_fila_tabla_hampath_por_id(id_hampath)
                        numNodos += grafoHampath[2].number_of_nodes()

                    # Guardo la asociacion en el diccionario que contiene como valor la fila de la bd
                    asociacion_numNodos_fila[(id, numNodos)] = fila
                    lista_Combobox_pura.append((id,numNodos))
                    
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

        # Guardo la fila de la tabla_hamcycle
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

            # Representar el grafo hamcycle almacenado
            (id, id_hampath, grafo_3, posicion_grafo_3, colorMap_grafo_3, edgeMap_grafo_3, grososArcos_grafo_3, caminoHamiltoniano) = self.fila_bd[0:8]

            if caminoHamiltoniano==1:
                self.gestor_etapas.set_grafo_dirigido_con_ch(True)
            else:
                self.gestor_etapas.set_grafo_dirigido_con_ch(False)

            if id_hampath==-1:
                # Caso en el que solo pinto grafo_3
                nx.draw_networkx(grafo_3, ax=axis, node_color=colorMap_grafo_3, edge_color=edgeMap_grafo_3,   
                            width=grososArcos_grafo_3)
                
                # Establezco el grafo dirigido como el problema de inicio de la polli-reduccion
                grafo_inicial.append((grafo_3, posicion_grafo_3, colorMap_grafo_3, edgeMap_grafo_3, grososArcos_grafo_3))
                
                
            else:
                # Necesito el grafo hampath asociado
                fila_grafoHampath = Controlador.get_unica_instancia().get_base_datos().get_tabla_hampath().get_fila_tabla_hampath_por_id(id_hampath)

                # grafo_1
                (grafo, pos, etiquetas, color_map, edge_colors, posiciones_s_t) = fila_grafoHampath[2:8]
            
                nx.draw_networkx(grafo,ax=axis,labels=etiquetas, pos=pos, node_color=color_map, 
                                edge_color=edge_colors,node_size=190,font_size=6)
            
                grafo_inicial.append((grafo, pos, etiquetas, color_map, edge_colors, posiciones_s_t))
                
                # grafo_2
                (grafo, pos, etiquetas, color_map, edge_colors, posiciones_s_t) = fila_grafoHampath[8:14]

                nx.draw_networkx(grafo,ax=axis,labels=etiquetas, pos=pos, node_color=color_map, 
                                    edge_color=edge_colors,node_size=190,font_size=6, connectionstyle = 'arc3, rad=0.4')
            
                grafo_inicial.append((grafo, pos, etiquetas, color_map, edge_colors, posiciones_s_t))


                # grafo_3
                nx.draw_networkx(grafo_3, ax=axis, pos=posicion_grafo_3, node_color=colorMap_grafo_3, edge_color=edgeMap_grafo_3,
                            width=grososArcos_grafo_3, node_size=190, font_size=6)
            
                grafo_inicial.append((grafo_3, posicion_grafo_3, colorMap_grafo_3, edgeMap_grafo_3, grososArcos_grafo_3))

                
            # Pintamos en la figura
            canvas = FigureCanvasTkAgg(fig, self.panel_grafo)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # El grafo inicial está constituido por ambos grafos anteriores
            self.gestor_etapas.set_grafo_dirigido(grafo_inicial)