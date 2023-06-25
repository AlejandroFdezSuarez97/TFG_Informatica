import copy

from .etapa_0 import *
from .etapa_1 import *
from .etapa_2 import *

from ...interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp

from controlador.controlador import Controlador

###########################################################################
# Clase gestora de etapas de la poli-reducción HAMCYCLE a UHAMCYCLE.
# Se encarga de la gestión y de la comunicación entre las distintas etapas 
# a desarrollar en la poli-reducción. Además, engloba el uso de funciones
# comunes a todas las etapas a realizar.
###########################################################################
class GestorEtapas():

    def __init__(self, ventana, lista_resultados_previos):

        # Ventana sobre la que se lanzará la ventana
        # de la poli-reducción
        self.ventana = ventana

        # Etapa 0
        self.etapa_0 = Etapa0(ventana, self)

        # Etapa 1
        self.etapa_1 = Etapa1(ventana, self)

        # Etapa 2
        self.etapa_2 = Etapa2(ventana, self)

        # Grafo inicial con el que comenzará la poli-reducción
        # Será una lista de tuplas en la que cada una de ellas, 
        # almacenara el subgrafo pertinente (si es que existen)
        self.grafo_dirigido = []

        # Grafo obtenido en la poli-reducción
        # de igual forma, es una lista de tuplas
        self.grafo_noDirigido = []

        # variable que indica si uso un grafo almacenado en la BD
        self.grafo_previo_escogido = False

        self.grafo_dirigido_con_ch = False


    # ------------- GETTERs AND SETTERs ---------------------------

    def get_grafo_dirigido(self):
        return copy.deepcopy(self.grafo_dirigido)
    
    def get_grafo_noDirigido(self):
        return copy.deepcopy(self.grafo_noDirigido)
    
    def set_grafo_dirigido(self, lista):
        self.grafo_dirigido = lista

    def set_grafo_noDirigido(self, lista):
        self.grafo_noDirigido = lista

    def get_etapa(self, num_etapa):

        match num_etapa:
            
            case 0:
                return self.etapa_0
            
            case 1:
                return self.etapa_1

            case 2:
                return self.etapa_2

    def get_grafo_previo_escogido(self):
        return copy.deepcopy(self.grafo_previo_escogido)

    def set_grafo_previo_escogido(self, valor):
        self.grafo_previo_escogido = valor


    def set_grafo_dirigido_con_ch(self, valor):
        self.grafo_dirigido_con_ch = valor

    def get_grafo_dirigido_con_ch(self):
        return self.grafo_dirigido_con_ch
    

    # Reseteo de etapas.
    def resetear_etapas(self):

        self.etapa_1.set_etapa_realizada(False)
        self.etapa_2.set_etapa_realizada(False)
    
    ### Métodos comunes a todas las etapas ###

    # Función que vuelve a la etapa anterior en la poli-reducción.
    def anterior(self,etapa):
        match etapa:
            
            # Volvemos al panel HAMPATH es NP
            case 0.1: 

                # Olvidamos paneles siguientes
                self.etapa_0.get_panel_0_2().pack_forget()

                # Mostramos paneles anteriores
                self.etapa_0.get_panel_0_1().pack(padx=10, pady=10, fill="both", expand=True)

            # Volvemos al panel de introducción de fórmula
            case 0.2:

                # Olvidamos paneles siguientes
                self.etapa_1.get_panel_1().pack_forget()

                # Mostramos paneles anteriores
                self.etapa_0.get_panel_0_2().pack(padx=10, pady=10, fill="both", expand=True)
               
            case 1:
                
                # Olvidamos paneles siguientes
                self.etapa_2.get_panel_2().pack_forget()

                # Mostramos paneles anteriores
                self.etapa_1.get_panel_1().pack(fill="both", padx=10, pady=10, expand=True)
            
    # Función que vuelve a la etapa siguiente en la poli-reducción.
    def siguiente(self, etapa):
        match etapa:

            case 0.1: 
                self.etapa_0.get_panel_0_0().pack_forget()
                
                self.etapa_0.lanzar_subetapa_1()
            
            case 0.2:
                self.etapa_0.get_panel_0_1().pack_forget()
                
                if self.etapa_0.get_etapa_realizada():
                    self.etapa_0.get_panel_0_2().pack(padx=10, pady=10,fill="both",expand=True)
                   
                else:
                    self.etapa_0.lanzar_subetapa_2()

            case 1:
                
                self.etapa_1.lanzar_etapa()

            case 2:

                self.etapa_1.get_panel_1().pack_forget()

                if self.etapa_2.get_etapa_realizada():
                    self.etapa_2.get_panel_2().pack(fill="both",expand=True)

                else:
                    self.etapa_2.lanzar_etapa()

            # Terminamos de realizar la poli-reducción
            case 3:

                self.cerrar_simulacion()
    

    # Crea un panel con pseudocódigo, explicando los pasos a nivel
    # algorítmico de qué es lo que hay que realizar. Texto alineado 
    # a la izquierda.
    def crear_panel_pseudocodigo(self, panel, altura, anchura, num_pasos, lista_texto):

        panel_pasos = ctk.CTkTabview(panel, height=altura, width=anchura)
        panel_pasos.pack(side="top",padx=10, pady=10, fill="both")

        for paso in range (1, num_pasos+1):
            panel_pasos.add("Paso " + str(paso) + "º")

            textbox = ctk.CTkTextbox(panel_pasos.tab("Paso " + str(paso) + "º"), width=705, height= 300)
            textbox.insert("1.0", lista_texto[paso-1])
            textbox.configure(state="disabled")
            textbox.pack(padx=5, pady=10)
    
    # Función que se encargar de guardar un grafo en una imagen.
    def guardar_imagen(self, figure, etapa):

        archivo = "reduccion_Hamcycle_a_Uhamcycle_grafo_" + str(etapa) + ".png"
        figure.savefig(archivo, dpi=800, bbox_inches = 'tight')

        ventana = VentanaPopUp(self.ventana)
        ventana.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana.title("Grafo guardado")

        panel = ctk.CTkFrame(ventana, corner_radius=0)
        panel.pack(fill="both", expand=True)

        label = ctk.CTkLabel(panel, text="Imagen guardada en el archivo : \n\n" + archivo)
        label.pack(side="top", padx=10, pady=10)

        boton = ctk.CTkButton(panel,text="Aceptar", command=lambda:ventana.exit())
        boton.pack(side="bottom", padx=10, pady=10)

        ventana.center()

    # Función que abre una nueva ventana en la que ver más grande en grafo pasado por parámetro. 
    def agrandar_grafo(self, figure, etapa):
        
        # Reestablecemos dpi
        figure.set_dpi(100)

        # Aumentamos tamaño del grafo
        figure.set_figwidth(8)
        figure.set_figheight(6.5)

        # Creamos ventana
        ventana = VentanaPopUp(self.ventana)
        ventana.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana.title("Ampliar/guardar grafo")

        panel = ctk.CTkFrame(ventana, corner_radius=0)
        panel.pack(side="left",fill="both", expand=True)
        panel.grid_rowconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1)

        # Botones para guardar/cerrar
        boton = ctk.CTkButton(panel,text="Guardar imagen",command=lambda:self.guardar_imagen(figure,etapa))
        boton.grid(row=0, column=0, padx=10, pady=20, sticky="nswe")

        boton = ctk.CTkButton(panel, text="Cerrar", fg_color="red", hover_color="#D22121", command=lambda:ventana.exit(),height=50)
        boton.grid(row=1, column=0, padx=10, pady=(0,20), sticky="nswe")

        # Representamos el grafo el grafo
        canvas = FigureCanvasTkAgg(figure, ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        ventana.center()

    # Cierra la poli-reducción y la termina, indicando que se ha realizado.
    def cerrar_simulacion(self):

        # ---------------------------- GUARDO EN LA BD ---------------------------------------
        
        # Almacenar en la tabla_simulador solo si la reduccion no estaba ya almacenada
        numReduccionesBD = Controlador.get_unica_instancia().get_numReduccionesBD()
        numReduccionesBD += 1
        
        # Guardar simplemente el grafo uhamcycle creado
        [grafo, color_map]= self.get_grafo_noDirigido()

        # Compruebo si el grafo ya estaba almacenado en la base de datos
        id = Controlador.get_unica_instancia().get_base_datos().get_tabla_uhamcycle().is_grafo_in_tabla_uhamcycle(grafo)

        if id==-1:

            if self.get_grafo_dirigido_con_ch():
                con_ciclo = 1
                # Guardo el grafo uhamcycle indicando que SI que tiene un ciclo hamiltoniano
            else:
                con_ciclo = 0
                # Guardo el grafo uhamcycle indicando que NO que tiene un ciclo hamiltoniano

            # Si el grafo no dirigido no esta en la base de datos, lo guardarlo
            Controlador.get_unica_instancia().get_base_datos().get_tabla_uhamcycle().anadir_fila_tabla_uhamcycle(numReduccionesBD,grafo, color_map, con_ciclo)
            
            if self.grafo_previo_escogido:
                # Depende del hamcycle
                id_hamcycle =  self.get_etapa(0).fila_bd[0]
                Controlador.get_unica_instancia().get_base_datos().get_tabla_simulador().anadir_fila_tabla_simulador(numReduccionesBD, id_hamcycle, numReduccionesBD, "HAMCYCLE", "UHAMCYCLE")
            
            else:
                # El grafo no depende del hamcycle
                Controlador.get_unica_instancia().get_base_datos().get_tabla_simulador().anadir_fila_tabla_simulador(numReduccionesBD,0,numReduccionesBD, " ", "UHAMCYCLE")
            
                

        # Actualizo el numero de reducciones
        Controlador.get_unica_instancia().actualizar_numReduccionesBD()


        # Activamos flag indicando que se ha realizado la poli-reducción
        Controlador.get_unica_instancia().get_arista("HAMCYCLE->UHAMCYCLE").set_poli_reduccion_completada(True)
        
        self.ventana.exit()