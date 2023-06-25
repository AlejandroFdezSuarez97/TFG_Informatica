import json
from persistencia.tiposTablas.tabla import Tabla
import matplotlib.pyplot as plt

from interfaz_grafica.interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp
from PIL import Image
import customtkinter as ctk


##############################################################################
# Clase que engloba el tipo de tabla_Subset
##############################################################################

class Tabla_subset(Tabla):

    # Constructor
    def __init__(self, bd):
        
        super().__init__(bd)

        self.cargar_tabla_subset()
    


    ###############################################
    ############ CREACIÓN DE LA TABLA  ############
    ###############################################

    # Funcion para crear/cargar la tabla_subset
    def cargar_tabla_subset(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS tabla_subset (
                            id INTEGER PRIMARY KEY,
                            Conjunto TEXT,
                            valor_t TEXT,
                            ExisteSubconjunto INTEGER,
                            Subconjunto TEXT
                            )
                    ''')

    ###############################################
    ######### ANADIR ENTRADAS A LA TABLA ##########
    ###############################################    

    # Funcion que almacena una entrada en la tabla_subset
    # Debo serializar la mayoria de sus parametro, por lo que debo tener cuidado a la hora de 
    # sacarlos de la BD.
    def anadir_fila_tabla_subset(self, id, elementos_conjunto, valor_t, existeSub, elemento_subconjunto):

        sql = "INSERT INTO tabla_subset (id, Conjunto, valor_t, ExisteSubconjunto, Subconjunto) VALUES (?, ?, ?, ?, ?)"    


        # Transformamos todos los datos para poder almacenarlos en la base de datos
        
        elementos_conjunto = json.dumps(elementos_conjunto)
        elemento_subconjunto = json.dumps(elemento_subconjunto)

        
        # Anado la fila a la tabla
        self.cursor.execute(sql, (id, elementos_conjunto, valor_t, existeSub, elemento_subconjunto))


        # Guardo los cambios en la base de datos
        self.conexion.commit()


    ###############################################
    ####### EXTRAER ENTRADAS DE LA TABLA ##########
    ###############################################

    # Funcion que sirve para extaer una entrada de la tabla_subset
    def extaer_fila_tabla_subset_por_id(self, id):
        sql =  "SELECT * FROM tabla_subset WHERE id = ?"
        self.cursor.execute(sql,(id,) )
        fila = self.cursor.fetchone()

        filaSolucion = []
        if fila is not None:
            filaSolucion.append(fila[0])                   # id
            filaSolucion.append(json.loads(fila[1]))       # elementos_conjunto
            filaSolucion.append(fila[2])                   # valor_t
            filaSolucion.append(fila[3])                   # existeSub
            filaSolucion.append(json.loads(fila[4]))       # elememntos_subconjunto
            
        else:
            print('No se ha encontrado ninguna fórmula con dicho id')

        return filaSolucion


    # Devuelve una lista con todas las filas(entradas) de la tabla_subset
    def get_todas_filas_tabla_subset(self):
        sql = "SELECT * FROM tabla_subset"
        self.cursor.execute(sql)
        filas = self.cursor.fetchall()

        entradas = []
        for fila in filas:
            nueva_fila = []
            nueva_fila.append(fila[0])                   # id
            nueva_fila.append(json.loads(fila[1]))       # elementos_conjunto
            nueva_fila.append(fila[2])                   # valor_t
            nueva_fila.append(fila[3])                   # existeSub
            nueva_fila.append(json.loads(fila[4]))       # elememntos_subconjunto
            entradas.append(nueva_fila)

        return entradas
            

    # Comprueba si una tabla esta almacenada en tabla_subset
    # Lo hace en base a los datos que contiene
    def is_conjunto_in_tabla_subset(self, d, t):
        sql = "SELECT id FROM tabla_subset WHERE Conjunto = ? and valor_t = ?"

        self.cursor.execute(sql,(json.dumps(d),t,))
        fila = self.cursor.fetchone()

        if fila==None:
            return -1
        else:
            return fila[0]


    # Funcion que imprime toda la tabla_subset en la terminal
    def imprime_tabla(self):
        
        self.cursor.execute("SELECT * FROM tabla_subset")
        filas = self.cursor.fetchall()

        # Obtener los nombres de las columnas de la tabla
        nombres_columnas = [descripcion[0] for descripcion in self.cursor.description]

        # Imprimir los nombres de las columnas
        print(" | ".join(nombres_columnas))

        # Imprimir los registros de la tabla
        for registro in filas:
            print(" | ".join(str(valor) for valor in registro))


    ###############################################
    ######### ELIMINAR ENTRADAS DE LA TABLA #######
    ###############################################
    

    ###############################################
    ######### MOSTRAR TABLA EN VENTANA ############
    ###############################################


    # Funcion que crea una ventana grafica y muestra en ella
    # en formato grafico la tabla_subset
    def mostrar_tabla_subset(self, ventana_antigua):

        ventana_antigua.destroy()
        
        # Obtener los datos de la tabla
        sql = "SELECT * FROM tabla_subset"
        self.cursor.execute(sql)
        entradas = self.cursor.fetchall()


        if len(entradas)==0:
            # Caso de tabla vacia

            ventana_error = VentanaPopUp(ventana_padre=None)

            ventana_error.title("No disponible")

            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/info_ico.ico')

            panel = ctk.CTkFrame(ventana_error, corner_radius=0) 
            panel.pack(fill = "both", expand=True)

            label = ctk.CTkLabel(panel, text='La tabla SUBSET-SUM se encuentra actualemente vacía.')
            label.grid(row=1,column=0, padx=10, pady=10)

            boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:ventana_error.exit())
            boton_aceptar.grid(row=4, column=0, padx=10, pady=(0,10))

            # Imagen aviso
            bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"), size=(50, 50))
            label = ctk.CTkLabel(panel, image=bg_image, text="")
            label.grid(row=0,column=0, padx=10, pady=10)

            ventana_error.center()

        else:

            # Crear una ventana para mostrar los gráficos
            fig, axs = plt.subplots(len(entradas), 1, figsize=(20, 5*len(entradas)))

            # Recorrer las entradas y mostrar los gráficos
            for i, entrada in enumerate(entradas):

                # Obtengo la info de una fila de la tabla_subset
                id = entrada[0]
                
                conjunto = json.loads(entrada[1])
                valor_t = entrada[2]
                existeSub = entrada[3]
                subconjunto = json.loads(entrada[4])

                
                # Compruebo si solo tengo una tabla que mostrar
                if len(entradas)==1:
                    ax1=axs
                else:
                    ax1 = axs[i]

                # Imprimo el titulo de la tabla
                ax1.set_title("<S, t>: " + str(id))

                
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
                

                #  ----------- Coloreo las celdas para que sean mas visibles las distintas zonas de la tabla --------

                for i in range(0,len(datos)):
                    cell = tabla[0,i]
                    cell.set_facecolor('#FFFFF0')

                # pinto la celda del valor de t
                cell = tabla[0,len(datos)-2]
                cell.set_facecolor('#AFEEEE')

                # Si hay elementos en el subconjunto, los pinto
                if existeSub == 1:

                    frecuencia = {}
                    pintado = {}
                    # Obtener la frecuencia de cada elemento en la segunda lista
                    for elemento in subconjunto_str:
                        frecuencia[elemento] = frecuencia.get(elemento, 0) + 1
                        pintado[elemento] = False

                    for i, valor in enumerate(datos):
                        if valor in frecuencia and not pintado[valor]:
                            
                            count = frecuencia[valor]
                            
                            for j in range(count):
                                celda = tabla[0, i+j]
                                celda.set_facecolor("#DA70D6")

                            pintado[valor] = True
                        
                ax1.axis('off')
                
                
            # Muestro los graficos
            plt.show()