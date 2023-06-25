import json
from persistencia.tiposTablas.tabla import Tabla
import matplotlib.pyplot as plt

from interfaz_grafica.interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp
from PIL import Image
import customtkinter as ctk

##############################################################################
# Clase que engloba el tipo de tabla_Mochila
##############################################################################

class Tabla_mochila(Tabla):

    # Constructor
    def __init__(self, bd):
        
        super().__init__(bd)

        self.cargar_tabla_mochila()
    


    ###############################################
    ############ CREACIÓN DE LA TABLA  ############
    ###############################################

    # Funcion para crear/cargar la tabla_mochila
    def cargar_tabla_mochila(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS tabla_mochila (
                            id INTEGER PRIMARY KEY,
                            Datos TEXT,
                            NombreColumnas TEXT,
                            ExisteSubconjunto INTEGER,
                            FilasSeleccionadas TEXT
                            )
                    ''')

    ###############################################
    ######### ANADIR ENTRADAS A LA TABLA ##########
    ###############################################    

    # Funcion que almacena una entrada en la tabla_mochila
    # Debo serializar la mayoria de sus parametro, por lo que debo tener cuidado a la hora de 
    # sacarlos de la BD.
    def anadir_fila_tabla_mochila(self, id, datos, nomColum, existeSub, filasSelec):

        sql = "INSERT INTO tabla_mochila (id, Datos, NombreColumnas, ExisteSubconjunto,FilasSeleccionadas) VALUES (?, ?, ?, ?, ?)"    


        # Transformamos todos los datos para poder almacenarlos en la base de datos
        
        datos = json.dumps(datos)
        nomColum = json.dumps(nomColum)
        filasSelec = json.dumps(filasSelec)

        
        # Anado la fila a la tabla
        self.cursor.execute(sql, (id, datos, nomColum, existeSub, filasSelec))


        # Guardo los cambios en la base de datos
        self.conexion.commit()


    ###############################################
    ####### EXTRAER ENTRADAS DE LA TABLA ##########
    ###############################################

    # Funcion que sirve para extaer una entrada de la tabla_mochila
    def extaer_fila_tabla_mochila_por_id(self, id):
        sql =  "SELECT * FROM tabla_mochila WHERE id = ?"
        self.cursor.execute(sql,(id,) )
        fila = self.cursor.fetchone()

        filaSolucion = []
        if fila is not None:
            filaSolucion.append(fila[0])                   # id
            filaSolucion.append(json.loads(fila[1]))       # datos
            filaSolucion.append(json.loads(fila[2]))       # nomColumnas
            filaSolucion.append(fila[3])                   # ExisteSubcon
            filaSolucion.append(json.loads(fila[4]))       # FilasSeleccionadas
            
        else:
            print('No se ha encontrado ninguna fórmula con dicho id')

        return filaSolucion


    # Devuelve una lista con todas las filas(entradas) de la tabla_mochila
    def get_todas_filas_tabla_mochila(self):
        sql = "SELECT * FROM tabla_mochila"
        self.cursor.execute(sql)
        filas = self.cursor.fetchall()

        entradas = []
        for fila in filas:
            nueva_fila = []
            nueva_fila.append(fila[0])                   # id
            nueva_fila.append(json.loads(fila[1]))       # datos
            nueva_fila.append(json.loads(fila[2]))       # nomColumnas
            nueva_fila.append(fila[3])                   # ExisteSubcon
            nueva_fila.append(json.loads(fila[4]))       # FilasSeleccionadas
           
            entradas.append(nueva_fila)

        return entradas
            

    # Comprueba si una tabla esta almacenada en tabla_mochila
    # Lo hace en base a los datos que contiene y devuelve
    # el id en caso de encontrarse y -1 en caso contrario
    def is_tabla_in_tabla_mochila(self, d):
        sql = "SELECT id FROM tabla_mochila WHERE Datos = ?"

        self.cursor.execute(sql,(json.dumps(d),))
        fila = self.cursor.fetchone()

        if fila==None:
            return -1
        else:
            return fila[0]


    # Funcion que imprime toda la tabla_mochila en la terminal
    def imprime_tabla(self):
        
        self.cursor.execute("SELECT * FROM tabla_mochila")
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
    # en formato grafico la tabla_mochila
    def mostrar_tabla_mochila(self, ventana_antigua):

        ventana_antigua.destroy()
        
        # Obtener los datos de la tabla
        sql = "SELECT * FROM tabla_mochila"
        self.cursor.execute(sql)
        entradas = self.cursor.fetchall()


        if len(entradas)==0:
            # Caso de tabla vacia

            ventana_error = VentanaPopUp(ventana_padre=None)

            ventana_error.title("No disponible")

            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')

            panel = ctk.CTkFrame(ventana_error, corner_radius=0) 
            panel.pack(fill = "both", expand=True)

            label = ctk.CTkLabel(panel, text='La tabla MOCHILA se encuentra actualemente vacía.')
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
                
                # Obtener los datos del grafo
                datos = json.loads(entrada[1])
                nomColum = json.loads(entrada[2])
                existeSub = entrada[3]
                filasSelec = json.loads(entrada[4])
                
                num_filas = len(datos)
                
                # Compruebo si solo tengo una tabla que mostrar
                if len(entradas)==1:
                    ax1=axs
                else:
                    ax1 = axs[i]

                # Imprimo el titulo de la tabla
                ax1.set_title("Tabla: " + str(id))

                # Configuramos la tabla que queremos pintar
                tabla = ax1.table(cellText=datos, colLabels=nomColum, cellLoc='center', loc='center')
                ax1.axis('off')

                # ------ Coloreamos las celdas de la nueva tabla
                # Pintamos las filas de la tabla
                for i in range(1,len(datos)-1):
            
                    cell = tabla[i,1]
                    cell.set_facecolor('#FAFAD2')

                    cell = tabla[i,2]
                    cell.set_facecolor('#FAFAD2')


                # Fila asociada al valor K
                for i in range(0,3):
                    cell = tabla[len(datos)-1,i]
                    if i == 2:
                        cell.set_facecolor('#FAFAD2')
                    else:
                        cell.set_facecolor('#48D1CC')
                    
                
                # Fila asociada al valor B
                for i in range(0,3):
                    cell = tabla[len(datos),i]
                    if i == 1:
                        cell.set_facecolor('#FAFAD2')
                    else:
                        cell.set_facecolor('#DDA0DD')


                
                # Pintamos las filas seleccionadas para pertenecer al subconjunto
                for fila in filasSelec:
                    #Busco la posicion de la fila dentro de la tabla
                    for i in range(1,len(datos)):
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
                
            # Muestro los graficos
            plt.show()