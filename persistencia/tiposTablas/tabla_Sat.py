import json
from persistencia.tiposTablas.tabla import Tabla
import tkinter as tk
from tkinter import ttk



##############################################################################
# Clase que engloba el tipo de tabla_sat.
##############################################################################

class Tabla_sat(Tabla):

    # Constructor
    def __init__(self, bd):
        
        super().__init__(bd)

        self.cargar_tabla_sat()



    ###############################################
    ############ CREACIÓN DE LA TABLA  ############
    ###############################################

    # Creo o cargo la tabla_sat en la base de datos
    def cargar_tabla_sat(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS tabla_sat (
                            id INTEGER PRIMARY KEY,
                            Formula TEXT,
                            Literales TEXT,
                            Clausulas TEXT,
                            NumLiterales INTEGER,
                            NumClausulas INTEGER,
                            isSatisfacible INTEGER,
                            asignacionSat TEXT
                            )
                    ''')

    ###############################################
    ######### ANADIR ENTRADAS A LA TABLA ##########
    ############################################### 

    # Función para añadir una entrada en la base de datos en la tabla_sat
    # Como literales, clausulas y asignacion son listas de string, debo serializarlas para poder introducilas
    # como texto plano en una columna de la base de datos. Para ello uso al libreria Json.
    # Por tanto, a la hora de extraer los datos de al base de datos debo 'deserializarlos' para
    # obtener de nuevo las listas.
    def anadir_fila_tabla_sat(self, id, formula, literales, clausulas, numLitereales, numClausulas, isSat, asignacion):

        sql = "INSERT INTO tabla_sat (id, Formula, Literales, Clausulas, NumLiterales, NumClausulas, isSatisfacible, asignacionSat) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"    


        # Serializamos las listas de datos para almacenarlas en la base de datos
        # Como literales es un set, debo transformarlo primero en list para poder serializarlo
        literealesSerializados = json.dumps(list(literales))

        clausulasSerializadas = json.dumps(clausulas)

        asignacion = str(asignacion)

        # Anado la fila a la tabla
        self.cursor.execute(sql, (id, formula, literealesSerializados, clausulasSerializadas, numLitereales, numClausulas, isSat, asignacion))


        # Guardo los cambios en la base de datos
        self.conexion.commit()


    ###############################################
    ####### EXTRAER ENTRADAS DE LA TABLA ##########
    ###############################################

    # Funcion que sirve para extaer una fila de la tabla_sat
    def extaer_fila_tabla_sat_por_id(self, id):
        sql =  "SELECT * FROM tabla_sat WHERE id = ?"
        self.cursor.execute(sql,(id,) )
        fila = self.cursor.fetchone()

        filaSolucion = []
        if fila is not None:
            filaSolucion.append(fila[0])                 # id
            filaSolucion.append(fila[1])                   # formula
            filaSolucion.append(set(json.loads(fila[2]))) # literales
            filaSolucion.append(json.loads(fila[3]))       # clausulas
            filaSolucion.append(fila[4])                   # numLiterales  
            filaSolucion.append(fila[5])                   # numClausulas
            filaSolucion.append(fila[6])                   # isSat
            filaSolucion.append(eval(fila[7]))             # asignacionSat
            

        return filaSolucion



    # Funcion que sirve para extaer una fila de la tabla_sat sabiendo su fórmula
    def extaer_fila_tabla_sat_por_formula(self, formula):
        sql =  "SELECT * FROM tabla_sat WHERE Formula = ?"
        self.cursor.execute(sql,(formula,) )
        fila = self.cursor.fetchone()

        filaSolucion = []
        if fila is not None:
            filaSolucion.append(fila[0])                 # id
            filaSolucion.append(fila[1])                   # formula
            filaSolucion.append(set(json.loads(fila[2]))) # literales
            filaSolucion.append(json.loads(fila[3]))       # clausulas
            filaSolucion.append(fila[4])                   # numLiterales  
            filaSolucion.append(fila[5])                   # numClausulas
            filaSolucion.append(fila[6])                   # isSat
            filaSolucion.append(eval(fila[7]))             # asignacionSat
            

        return filaSolucion


    # Funcion que devuelve todas las formulas almacenadas en la BD
    # SOLO LA FORMULA EN SI
    def get_todas_formulas_tabla_sat(self):
        self.cursor.execute("SELECT Formula FROM tabla_sat")
        formulas = self.cursor.fetchall()

        lista_formulas = [fila[0] for fila in formulas]

        return lista_formulas

    # Averigua si una formula está almacenada en tabla_sat. En caso afirmativo devuelve su primary key
    # y en caso contrario, devuelve -1.
    def is_formula_in_tabla_sat(self, formula):
        formulas_en_tabla_sat = self.get_todas_formulas_tabla_sat()
        id = -1

        for f in formulas_en_tabla_sat:
            if f == formula:
                id = self.extaer_fila_tabla_sat_por_formula(formula)[0]
                break

        return id
    
    # Comparador de formulas para evitar el caso de tener la misma formula
    # con distinto numero de espacios almacenada en la bd.
    def formula_in_tabla_por_clausulas(self,nueva_cl):
        self.cursor.execute("SELECT Formula,Clausulas FROM tabla_sat")
        filas_seleccionadas = self.cursor.fetchall()

        nueva_cl = json.dumps(nueva_cl)
        id = -1
        
        for fila in filas_seleccionadas:
            formula = fila[0]
            c = fila[1]
            if c == nueva_cl:
                id = self.extaer_fila_tabla_sat_por_formula(formula)[0]
                break

        return id

    # Funcion que devuelve toda la tabla_sat
    def imprime_tabla(self):
        
        self.cursor.execute("SELECT * FROM tabla_sat")
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
    # en formato grafico la tabla_simulador
    def mostrar_tabla_sat(self, ventana_antigua):

        ventana_antigua.destroy()
        
        ventana = tk.Tk()
        ventana.title("Tabla SAT") 

        # Obtener los datos de la tabla
        self.cursor.execute("SELECT * FROM tabla_sat")
        filas = self.cursor.fetchall()

        # Crear el TreeView
        treeview = ttk.Treeview(ventana)

        # Configurar las columnas
        treeview["columns"] = ("Formula", "Literales", "Clausulas", "NumLiterales", "NumClausulas", "isSatisfacible", "asignacionSat")
        treeview.column("#0", width=50)  # Columna para el ID
        treeview.column("Formula", width=200)
        treeview.column("Literales", width=200)
        treeview.column("Clausulas", width=200)
        treeview.column("NumLiterales", width=50)
        treeview.column("NumClausulas", width=50)
        treeview.column("isSatisfacible", width=30)
        treeview.column("asignacionSat", width=300)

        # Configurar las cabeceras de las columnas
        treeview.heading("#0", text="ID")
        treeview.heading("Formula", text="Formula")
        treeview.heading("Literales", text="Literales")
        treeview.heading("Clausulas", text="Clausulas")
        treeview.heading("NumLiterales", text="NumLit")
        treeview.heading("NumClausulas", text="NumCl")
        treeview.heading("isSatisfacible", text="isSat")
        treeview.heading("asignacionSat", text="asignacionSat")

        # Insertar los datos en el TreeView
        for fila in filas:
            treeview.insert("", "end", text=fila[0], values=fila[1:])

        # Añadir el TreeView a la ventana
        treeview.pack()