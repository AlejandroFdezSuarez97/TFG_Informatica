from .creador import Creador
from .creador_nodos import CreadorNodos

from modelo_del_dominio.aristas.arista import Arista

#######################################################
# Clase que se encarga de la creación (fabricación) de
# de las aristas.
#######################################################
class CreadorAristas(Creador):

    _unica_instancia = None

    _lista_aristas_creadas = []

    ### Getters ###
    
    # Devuelve la lista de aristas.
    def get_lista_aristas(self):
        return self._lista_aristas_creadas

    # Instancia del creador.
    def get_unica_instancia():

        if CreadorAristas._unica_instancia == None:
            CreadorAristas._unica_instancia = CreadorAristas()

        return CreadorAristas._unica_instancia
    
    # Creación de aristas.
    def metodo_factoria(self):

        nodo_sat3cnf = CreadorNodos.get_unica_instancia().get_lista_nodos()[0]
        nodo_hampath = CreadorNodos.get_unica_instancia().get_lista_nodos()[1]
        nodo_hamcycle = CreadorNodos.get_unica_instancia().get_lista_nodos()[2]
        nodo_uhamcycle = CreadorNodos.get_unica_instancia().get_lista_nodos()[3]
        nodo_tspdec = CreadorNodos.get_unica_instancia().get_lista_nodos()[4]
        nodo_subsetsum = CreadorNodos.get_unica_instancia().get_lista_nodos()[5]
        nodo_mochila = CreadorNodos.get_unica_instancia().get_lista_nodos()[6]

        #### ARISTA SAT3cnf A HAMPATH
        arista_sat3nf_a_hampath = Arista("SAT3cnf->HAMPATH", nodo_sat3cnf, nodo_hampath)

        #### ARISTA HAMPATH A HAMCYCLE
        arista_hampath_a_hamcycle = Arista("HAMPATH->HAMCYCLE", nodo_hampath, nodo_hamcycle)

        #### ARISTA HAMCYCLE A UHAMCYCLE
        arista_hamcycle_a_uhamcycle = Arista("HAMCYCLE->UHAMCYCLE", nodo_hamcycle, nodo_uhamcycle)

        #### ARISTA UHAMCYCLE A TSP-DEC
        arista_uhamcycle_a_tspdec = Arista("UHAMCYCLE->TSP", nodo_uhamcycle, nodo_tspdec)

        #### ARISTA SAT3NF A SUBSET-SUM
        arsita_sat3nf_a_subset_sum = Arista("SAT3cnf->SUBSET", nodo_sat3cnf, nodo_subsetsum)

        #### ARISTA SUBSET-SUM A MOCHILA
        arsita_subset_sum_a_mochila = Arista("SUBSET->MOCHILA", nodo_subsetsum, nodo_mochila)

        # Guardamos las aristas en la lista
        self._lista_aristas_creadas = [arista_sat3nf_a_hampath, arista_hampath_a_hamcycle, arista_hamcycle_a_uhamcycle, 
                                       arista_uhamcycle_a_tspdec, arsita_sat3nf_a_subset_sum, arsita_subset_sum_a_mochila]

        # Devolvemos lista de aristas
        return [arista_sat3nf_a_hampath, arista_hampath_a_hamcycle, arista_hamcycle_a_uhamcycle, arista_uhamcycle_a_tspdec, arsita_sat3nf_a_subset_sum, arsita_subset_sum_a_mochila]