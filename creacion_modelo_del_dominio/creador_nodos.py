from .creador import Creador

from modelo_del_dominio.nodos.nodo import Nodo

#######################################################
# Clase que se encarga de la creación (fabricación) de
# de los nodos (problemas).
#######################################################
class CreadorNodos(Creador):

    _unica_instancia = None

    _lista_nodos_creados = []
    
    ### Getters ###

    # Devuelve la lista de nodos.
    def get_lista_nodos(self):
        return self._lista_nodos_creados

    # Instancia del creador.
    def get_unica_instancia():

        if CreadorNodos._unica_instancia == None:
            CreadorNodos._unica_instancia = CreadorNodos()

        return CreadorNodos._unica_instancia
    
    # Creación de nodos.
    def metodo_factoria(self):

        #### NODO SAT3ncf 
        texto_info = "Es el problema de la satisfacibilidad booleana (SAT) que se \nse presenta bajo la forma normal conjuntiva "\
            "(esto es, que la fórmula \nbooleana está formada por una conjunción (^) de cláusulas, " + "donde \ncada cláusula está formada por la disyunción (v) de máximo tres literales).\nPara el simulador implementado, se considerarán como literales las \nvariables x1,...,x9." + \
            "\n\nSAT3cnf es NP-Completo. Lo sabemos puesto que:\n\n ▶ SAT3cnf pertenece a la clase NP (existe un decisor en tiempo polinomial que, dada una solución encontrada, decreta si es válida o no. " + \
            "\n\n ▶ Existe el problema SAT, que es NP-Completo (por el Teorema\nde Cook-Levin), y que se poli-reduce a SAT3cnf."

        nodo_sat3cnf = Nodo(0, "SAT3cnf", "SAT3", "red", texto_info, "https://en.wikipedia.org/wiki/Boolean_satisfiability_problem")

        #### NODO HAMPATH
        texto_info = "Es el lenguaje de triplas, grafo dirigido G, vértice \"s\" y vértice \"t\", tal que \nexiste un camino de \"s\" a \"t\" que pasa por todos los vértices exactamente \nuna vez."\
            "\n\nEl lenguaje lo podemos expresar como: \n\n" + "HAMPATH = {< G, s, t >| G es g.d. con cam. hamiltoniano de \"s\" a \"t\"}.\n\n\n" + \
            "HAMPATH es NP-Completo. Lo sabemos puesto que:\n\n ▶ HAMPATH pertenece a la clase NP (existe un decisor en tiempo polinomial que, dada una solución encontrada, determina si es válida o no)." + \
            "\n\n ▶ Existe un problema, SAT3cnf, que es NP-Completo, y que se poli-\nreduce a HAMPATH. Dicha poli-reducción se puede simular en esta\naplicación."

        nodo_hampath = Nodo(1,"HAMPATH", "HAMP", "green", texto_info, "https://www.geeksforgeeks.org/proof-hamiltonian-path-np-complete/")

        #### NODO HAMCYCLE
        texto_info = "Es el lenguaje de 1-tuplas formadas por un grafo dirigido G tal que \nexiste un ciclo que pasa por todos los vértices exactamente \nuna vez."\
            "\n\nEl lenguaje lo podemos expresar como: \n\n" + "HAMCYCLE = {< G>| G es g.d. con ciclo. hamiltoniano}.\n\n\n" + \
            "HAMCYCLE es NP-Completo. Lo sabemos puesto que:\n\n ▶ HAMCYCLE pertenece a la clase NP (existe un decisor en tiempo polinomial que, dada una solución encontrada, determina si es válida o no)." + \
            "\n\n ▶ Existe un problema, HAMPATH, que es NP-Completo, y que se poli-\nreduce a HAMCYCLE. Dicha poli-reducción se puede simular en esta\naplicación."
        nodo_hamcycle = Nodo(2,"HAMCYCLE", "HAMC", "blue", texto_info, "https://www.geeksforgeeks.org/proof-that-hamiltonian-cycle-is-np-complete/")


        #### NODO UHAMCYCLE
        texto_info = "Representa el siguiente problema decisional:\n"\
            "Dado un grafo no dirigido, el problema decisional consiste en determinar si éste tiene o no un ciclo hamiltoniano; esto es un ciclo que pasa por todos los nodos del grafo una única vez."\
            "\n\nEl lenguaje lo podemos expresar como: \n\n" + "UHAMCYCLE = {< G>| G es g.n.d. con ciclo. hamiltoniano}.\n\n\n" + \
            "UHAMCYCLE es NP-Completo. Lo sabemos puesto que:\n\n ▶ UHAMCYCLE pertenece a la clase NP (existe un decisor en tiempo polinomial que, dada una solución encontrada, determina si es válida o no)." + \
            "\n\n ▶ Existe un problema, HAMCYCLE, que es NP-Completo, y que se poli-\nreduce a UHAMCYCLE. Dicha poli-reducción se puede simular en esta\naplicación."
        nodo_uhamcycle = Nodo(3,"UHAMCYCLE", "UHAMC", "purple", texto_info, "http://users.cms.caltech.edu/~umans/cs21/lec21.pdf")

        #### NODO TSP_DEC
        texto_info = "TSP: posiblemente, uno de los problemas de optimización más famosos que existen: el problema del viajante de comercio.\n\n"\
                "El problema se puede expresar mediante una 2-tupla formada por un grafo no dirigido y pesado G y un peso k tal que encontremos un ciclo hamiltoniano cuyo peso sea inferior a k.\n\n" \
                "Abreviadamente, podemos expresar su version decisional como: TSP-DEC={<G,K> | G es un g.n.d.c.p con un ciclo hamiltoniano cuyo peso sea inferior o igual a k}\n\n\n"\
                "TSP-DEC es NP-completo. Lo sabemos puesto que: \n\n ▶ TSP-DEC pertenece a la clase NP (existe un decisor en tiempo polinomial que, dada una solución encontrada, determina si es válida o no)." +\
                 "\n\n ▶ Existe un problema, UHAMCYCLE, que es NP-Completo, y que se poli-reduce a TSP-DEC. Dicha poli-reducción se puede simular en esta\naplicación."
        nodo_tspdec = Nodo(4,"TSP-DEC", "TSP", "coral", texto_info, "http://users.cms.caltech.edu/~umans/cs21/lec21.pdf")
        
        

        #### NODO SUBSET-SUM
        texto_info = "Es el lenguaje de 2-tuplas formadas por un multiconjunto S y un entero t de forma que encontremos algún subconjunto de S que sume exactamente t. (Recordar que multiconjunto es un conjunto que puede contener elementos repetidos)"\
            "\n\nEl lenguaje lo podemos expresar como: \n\n" + "SUBSET-SUM = {<S,t>| S ={x1, x2, . . . , xk} y para algún {y1, . . . , yl}\n  subconjuto de S se tiene la suma  y1+...+yl = t}.\n\n\n" + \
            "SUBSET-SUM es NP-Completo. Lo sabemos puesto que:\n\n ▶ SUBSET-SUM pertenece a la clase NP (existe un decisor en tiempo\n    polinomial que, dada una solución encontrada, determina\n    si es válida o no)." + \
            "\n\n ▶ Existe un problema, SAT3cnf, que es NP-Completo, y que se poli-\nreduce a SUBSET-SUM. Dicha poli-reducción se puede simular en esta\naplicación."
        nodo_subsetsum = Nodo(5,"SUBSET-SUM", "SUBSET", "fuchsia", texto_info, "https://www.geeksforgeeks.org/subset-sum-is-np-complete/")

        #### NODO MOCHILA
        texto_info = "El problema de la mochila (Knapsack 0-1) es un problema 'tipo' de \noptimización: (veremos su versión decisional)\n\n"\
                     "Dados dos enteros positivos b, k y un un conjunto finito U de forma que cualquier elemento u ∈ U tiene asociado un tamaño s(u) y un\nbeneficio v(u), "\
                     "el problema de la mochila (en su version decisional)\nconsiste en determinar si existe un subconjunto de elementos de U\nde forma que:\n\n"\
                     " · La suma del tamaño de cada elemento perteneciente a dicho\n   subconjunto sea menor o igual que k\n"\
                     " · La suma del beneficio de cada elemento perteneciente a dicho\n   subconjunto sea mayor o igual que b\n\n"\
                     "El problema MOCHILA es NP-completo. Lo sabemos puesto que:\n\n"\
                     "▶ MOCHILA pertenece a la clase NP (existe un decisor en tiempo\n   polinomial que, dada una solución encontrada, determina\n   si es válida o no)\n"\
                     "▶ Existe un problema, SUBSET-SUM, que es NP-Completo, y que se\n   poli-reduce a MOCHILA. Dicha poli-reducción se puede simular\n   en esta aplicación."
        nodo_mochila = Nodo(6,"MOCHILA", "MOCHILA", "#8B4513", texto_info, "https://www.baeldung.com/cs/knapsack-problem-np-completeness") 
        
        
        # Inserto todos los nodos creados
        self._lista_nodos_creados = [nodo_sat3cnf, nodo_hampath, nodo_hamcycle, nodo_uhamcycle, nodo_tspdec, nodo_subsetsum, nodo_mochila]

        # Devolvemos nodos creados
        return [nodo_sat3cnf, nodo_hampath, nodo_hamcycle, nodo_uhamcycle, nodo_tspdec, nodo_subsetsum, nodo_mochila]
    