import tkinter as tk
import customtkinter as ctk

from matplotlib.figure import Figure
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ...interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp

from .etapa import Etapa

#########################################################################
# Clase que engloba la etapa 2 a realizar en la poli-reducción. 
# Se encarga determinar si la instancia del problema MOCHILA tiene o no
# solución en base a si la tenía su problema asociado SUBSET-SUM.
#########################################################################
class Etapa2(Etapa):

    
    def __init__(self, ventana, gestor_etapas):
        
        super().__init__(ventana, gestor_etapas)
        self.panel_tabla = None



    ### Getters ###

    def get_panel_2(self):
        return self.panel_2

    ### Lanzador de etapa ###

    def lanzar_etapa(self):

        # Si no hay tabla, mostramos mensaje de error
        if self.gestor_etapas.get_tabla_inicial() == []:

            ventana_error = VentanaPopUp(self.ventana)
            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
            ventana_error.title(" ")

            panel_error = ctk.CTkFrame(ventana_error, corner_radius = 0)
            panel_error.pack()

            # Imagen error
            imagen_error = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"),size=(50, 50))
            label = ctk.CTkLabel(panel_error, image=imagen_error, text="")
            label.grid(row=0,column=0, padx=10, pady=10)

            label = ctk.CTkLabel(panel_error, text = 'Selecciona una tabla para comenzar \n la poli-reducción.')
            label.grid(row=1, column=0, padx=10, pady=10)

            boton_aceptar = ctk.CTkButton(panel_error, text="Aceptar", command=lambda:ventana_error.exit())
            boton_aceptar.grid(row=2, column=0, padx=10, pady=10)

            ventana_error.center()

        else:

            self.gestor_etapas.get_etapa(1).get_panel_1().pack_forget()

            self.etapa_realizada = True

            self.panel_2 = ctk.CTkFrame(self.ventana, corner_radius = 0)
            self.panel_2.pack(fill="both", expand=True)


            lista_texto = []
            texto = "El objetivo de esta nueva etapa es determinar si la instancia actual del problema de la mochila\n"\
                    "tiene o no solución. Ahora bien, determinar esto es sencillo gracias a:\n\n"\
                    "La instancia actual del problema de la MOCHILA (Knapsack 0-1) tiene solución si y sólo si, el\n"\
                    "problema subset-sum asociado la tenía.\n\n"\
            
            [id, conjunto, valor_t, existeSub, subconjunto] = self.gestor_etapas.get_tabla_inicial()

            if subconjunto==[]:
                texto = texto + "En este caso, como el problema asociado no tenía solución, el problema de la mochila\n"\
                        "tampoco tendrá solución."
                lista_texto.append(texto)

                texto = "En este caso, no se selecciona ningún objeto de la mochila porque no se cumplirían los\nrequisitos"\
                        " de peso mínimo ni de beneficio máximo."
                lista_texto.append(texto)
            else:
                texto = texto + "En este caso, como el problema asociado sí que tenía solución, el problema de la mochila\n"\
                                "también tendrá solución."
                lista_texto.append(texto)
      
                texto = "En este caso, se seleccionan los siguientes objetos:\n\n"
                tabla = self.gestor_etapas.get_tabla_final()
                filasSelec = tabla[4]

                for fila in filasSelec:
                    nombre = fila[0]
                    texto = texto + " · Se ha añadido el objeto " + nombre + " a la mochila.\n"

                lista_texto.append(texto)


            panel_info = ctk.CTkFrame(self.panel_2)
            panel_info.pack(padx=10, pady=(10,0))

            canvas = tk.Canvas(panel_info, width=40, height=185)
            canvas.configure(bg='#63BCE9')
            canvas.pack(side="left", padx=(10,0), pady=10)
            canvas.create_text(20, 150, text="Etapa " + str(2) ,angle=90, anchor="w", font=('Arial', 15,'bold'))


            panel_pasos = ctk.CTkTabview(panel_info, height=50, width=500)
            panel_pasos.pack(side="top", padx=10, pady=10, fill="both")

            for paso in range (1, len(lista_texto)+1):
                panel_pasos.add("Paso " + str(paso) + "º")

                textbox = ctk.CTkTextbox(panel_pasos.tab("Paso " + str(paso) + "º"), width=600, height=150)
                textbox.insert("1.0", lista_texto[paso-1])
                textbox.configure(state="disabled")
                textbox.pack(padx=5, pady=10)


            panel_botones_2 = ctk.CTkFrame(self.panel_2)
            panel_botones_2.pack(padx=10, pady=(5,10), fill=tk.Y, side='bottom')

            panel_botones_2_2 = ctk.CTkFrame(panel_botones_2, fg_color=("gray81", "gray20"))
            panel_botones_2_2.grid(row=0, column=1, padx=0, pady=5)

            self.panel_botones_2_2 = panel_botones_2_2

            # Imprimimos la nueva tabla
            self.crear_panel_nueva_tabla()

            boton_anterior= ctk.CTkButton(panel_botones_2, text="Anterior", command=lambda:self.gestor_etapas.anterior(1))
            boton_anterior.grid(row=0, column=0, padx=10, pady=10)

            boton_siguiente = ctk.CTkButton(panel_botones_2, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(3))
            boton_siguiente.grid(row=0, column=2, padx=10, pady=10)


    
    # Crea el panel donde imprimir la nueva tabla
    def crear_panel_nueva_tabla(self):

        if self.panel_tabla is not None:
            self.panel_tabla.destroy()
        
        self.panel_tabla = ctk.CTkFrame(self.panel_2)
        self.panel_tabla.pack(padx=10, pady=10, fill="both", expand=True)

        fig = Figure(figsize=(5,3), dpi=100)
        axis = fig.add_subplot(111)

        boton_agrandar= ctk.CTkButton(self.panel_botones_2_2, text="Agrandar/guardar\n imagen",
                                    fg_color = ("#70AB94","#4D8871"), hover_color = ("#7FB9A2","#52987C"),
                                    command=lambda:self.gestor_etapas.agrandar_tabla(fig,2))
        boton_agrandar.grid(row=0,column=0, padx=5, pady=5)

        #  ------ Creamos el objeto tabla
        [id, nuevos_datos, nomColumn, existeSub, filasSelec] = self.gestor_etapas.get_tabla_final()

        
        tabla = axis.table(cellText=nuevos_datos, colLabels=nomColumn, cellLoc='center', loc='center')
        axis.axis('off')

        # ------ Coloreamos las celdas de la nueva tabla
        # Pintamos las filas de la tabla
        for i in range(1,len(nuevos_datos)-1):
    
            cell = tabla[i,1]
            cell.set_facecolor('#FAFAD2')

            cell = tabla[i,2]
            cell.set_facecolor('#FAFAD2')


        # Fila asociada al valor K
        for i in range(0,3):
            cell = tabla[len(nuevos_datos)-1,i]
            if i == 2:
                cell.set_facecolor('#FAFAD2')
            else:
                cell.set_facecolor('#48D1CC')
            
        
        # Fila asociada al valor B
        for i in range(0,3):
            cell = tabla[len(nuevos_datos),i]
            if i == 1:
                cell.set_facecolor('#FAFAD2')
            else:
                cell.set_facecolor('#DDA0DD')


        
        # Pintamos las filas seleccionadas para pertenecer al subconjunto
        for fila in filasSelec:
            #Busco la posicion de la fila dentro de la tabla
            for i in range(1,len(nuevos_datos)):
                if tabla[i,0].get_text().get_text() == fila[0]:
                    # Nombre del objeto
                    cell = tabla[i,0]
                    cell.set_facecolor('#FFA07A')
                    # Fila asociada al peso
                    cell = tabla[i,1]
                    cell.set_facecolor('#ADD8E6')
                    # Fila asociada al beneficio
                    cell = tabla[i,2]
                    cell.set_facecolor('#D8BFD8')
                    break

        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(fig, self.panel_tabla)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        
    
    
        
  
