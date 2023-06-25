import tkinter as tk
import customtkinter as ctk

from modulos_externos.formula_booleana_sat3cnf.formula_booleana_sat3cnf import FormulaBooleanaSat3cnf

from .etapa import Etapa

##############################################################################
# Clase que engloba la primera etapa a realizar en la poli-reducción. 
# Informamos al usuario qué se va a realizar y se pedirá una fórmula booleana
# para comenzar la reducción.
##############################################################################
class Etapa0(Etapa):

    def __init__(self, ventana, gestor_etapas):
        
        super().__init__(ventana, gestor_etapas)

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
    # 1º : demostramos que SUBSET-SUM es NP
    # 2º : realizamos la poli-reducción en sí
    # 3º : aplicaremos el Tercer Teorema de la Reducibilidad

    def lanzar_subetapa_0(self):

        # Panel con los pasos que se van a seguir
        self.panel_0_0 = ctk.CTkFrame(self.ventana)
        self.panel_0_0.pack(fill="both", expand=True, padx=10, pady=10)

        panel_0 = ctk.CTkFrame(self.panel_0_0)
        panel_0.pack(padx=10, pady=10)

        label = ctk.CTkLabel(panel_0, text="Poli-reducción SAT3cnf -> SUBSET-SUM", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(padx=10, pady=(10,30))

        texto = "Realizaremos la poli-reducción de SAT3cnf a SUBSET-SUM, así que probaremos\n que SUBSET-SUM es NP-Completo. Para ello, seguiremos los siguientes pasos:"
        label = ctk.CTkLabel(panel_0, text=texto,font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=(10,10))

        panel = ctk.CTkFrame(panel_0)
        panel.pack(padx=10, pady=10, fill="both",)
        texto="1º"
        label = ctk.CTkLabel(panel, fg_color="#6889B1", text=texto, font=ctk.CTkFont(size=13, weight="bold"))
        label.pack(padx=10, pady=10, fill="both")

        texto="Veremos que SUBSET-SUM pertence a la clase NP."
        label = ctk.CTkLabel(panel, text=texto,font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=(0,10),fill="both")

        panel = ctk.CTkFrame(panel_0)
        panel.pack(padx=10, pady=10, fill="both")
        texto="2º"
        label = ctk.CTkLabel(panel, text=texto, fg_color="#6889B1", font=ctk.CTkFont(size=13,weight="bold"))
        label.pack(padx=10, pady=10, fill="both")

        texto="Realizaremos la poli-reducción de SAT3cnf (NP-Completo) a SUBSET-SUM:\n\n" \
                    "Para una fórmula ϕ en 3cnf (elegida por el usuario), veremos cómo construir una\nfunción " \
                    "computable en tiempo polinomial que mapea la fórmula ϕ a una tabla con una\n"\
                    "determinada estructura; conteniendo un conjunto S y un valor t. \n\n"\
                    "Dicha tabla contendrá un subsconjunto de S que suma t si y sólo si ϕ es satisfacible."
        label = ctk.CTkLabel(panel, text=texto,font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=10, fill="both")

        panel = ctk.CTkFrame(panel_0)
        panel.pack(padx=10, pady=10, fill="both")
        texto="3º"
        label = ctk.CTkLabel(panel, text=texto, fg_color="#6889B1", font=ctk.CTkFont(size=13, weight="bold"))
        label.pack(padx=10, pady=10, fill="both")

        texto="Usaremos el Tercer Teorema de la Reducibilidad:\n\n" \
                    "Para cada par de lenguajes L, L' con L ≤p L', si L es NP-Completo y L' es NP,\n" \
                    "entonces L' es NP-Completo.\n" \
                    "En nuestro caso, L = SAT3cnf y L'= SUBSET-SUM."
        label = ctk.CTkLabel(panel, text = texto, font=ctk.CTkFont(size=13))
        label.pack(padx=10, pady=10, fill="both")

        panel_botones_0_0 = ctk.CTkFrame(panel_0, corner_radius = 0)
        panel_botones_0_0.pack(padx=10, pady=(0,10), side='bottom')

        boton_siguiente = ctk.CTkButton(panel_botones_0_0 , text="Comenzar",
                                        command=lambda:self.gestor_etapas.siguiente(0.1))
    
        boton_siguiente.pack()

    ################# ETAPA 0.1 #################

    # Mostramos que SUBSET-SUM es NP.
    
    def lanzar_subetapa_1(self):

        self.panel_0_1 = ctk.CTkFrame(self.ventana)
        self.panel_0_1.pack(padx=10, pady=10, fill="both", expand=True)

        panel_titulo = ctk.CTkFrame(self.panel_0_1, fg_color="#6889B1")
        panel_titulo.pack(padx=30, pady=(30,10), fill=tk.X)

        label = ctk.CTkLabel(panel_titulo, text = "1º: SUBSET-SUM es NP", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(padx=50, pady=10)
        
        lista_texto = []
        texto = "Comencemos recordando el problema SUBSET-SUM:\n\n\n"\
                "SUBSET-SUM = {<S,t> | S = {x1,...,xk} y para algun subconjunto {y1,...,yl} ⊆ S\n\t\tse cumple que ∑yi=t}\n\n\n"\
                "Para demostrar que SUBSET-SUM es NP tenemos que demostrar que dada una\nposible solución al problema, podemos comprobar si es válida\n en un tiempo polinomial.\n\n"\
                "Supongamos entonces que para un par dado <S,t> se tiene una solución potencial;\nesto es un subconjunto C. Para verificar si dicha solución es correcta,\npodemos seguir los siguientes pasos:\n\n"\
                " 1) Comprobar si C es una colección de números que suman k.\n"\
                " 2) Comprobar si C es un subconjunto del multiconjunto S.\n"\
                " 3) Si las dos condiciones anteriores se cumplen, entonces devolvemos True.\n   En caso contrario, devolvemos False.\n\n"\
                "Este algoritmo de verificación polinomial tiene una complejidad de tiempo O(n),\ndonde n es el tamaño del conjunto S. Por lo tanto, el problema SUBSET-SUM\nes un problema NP, ya que existe un algoritmo de verificación polinomial para él."

        lista_texto.append(texto)

        self.gestor_etapas.crear_panel_pseudocodigo(self.panel_0_1, altura=110, anchura=450, num_pasos=len(lista_texto), lista_texto=lista_texto)

        panel_botones_0_1 = ctk.CTkFrame(self.panel_0_1)
        panel_botones_0_1.pack(padx=10, pady=30, side='bottom')
        
        boton_siguiente = ctk.CTkButton(panel_botones_0_1, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(0.2))
        boton_siguiente.pack()

    ################# ETAPA 0.2 #################

    # Procedemos a realizar la poli-reducción en sí.
    # Para ello, se pedirá al usuario que introduzca una
    # fórmula booleana.
    
    def lanzar_subetapa_2(self):

        # Informamos de realización de etapa
        self.etapa_realizada = True

        self.panel_0_2 = ctk.CTkFrame(self.ventana)
        self.panel_0_2.pack(padx=10, pady=10, fill="both", expand=True)

        panel_titulo = ctk.CTkFrame(self.panel_0_2, fg_color="#6889B1")
        panel_titulo.pack(padx=30, pady=30, fill=tk.X)

        label = ctk.CTkLabel(panel_titulo, text = "2º: SAT3cnf ≤p SUBSET-SUM", fg_color="#6889B1",
                                font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(padx=50, pady=(10,10))

        # Asignamos al gestor_etapas la fórmula booleana que introduce el usuario
        # NOTA: La formula no se guarda hasta que dentro del panel asociado al objeto Formula se pulse el boton introducir
        self.gestor_etapas.set_formula(FormulaBooleanaSat3cnf(self.ventana, self.panel_0_2, ""))

        panel_botones_0_2 = ctk.CTkFrame(self.panel_0_2)
        panel_botones_0_2.pack(padx=10, pady=(20,25), side='bottom')
        
        boton_siguiente = ctk.CTkButton(panel_botones_0_2, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(1))
        boton_siguiente.grid(row=0, column=1, padx=10, pady=10)

        boton_anterior = ctk.CTkButton(panel_botones_0_2, text="Anterior", command=lambda:self.gestor_etapas.anterior(0.1))
        boton_anterior.grid(row=0, column=0, padx=10, pady=10)
