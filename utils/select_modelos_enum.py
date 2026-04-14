from enum import Enum

class Modelos(Enum):
    ARVORE_DECISAO_ANTIGO = "Árvore de decisão (Currículo 2011.1)"
    ARVORE_DECISAO_MEIO = "Árvore de decisão (Currículo 2016.1)"
    ARVORE_DECISAO_NOVO = "Árvore de decisão (Currículo 2025.1)"
    REGRESSAO_LOGISTICA_ANTIGO = "Regressão logística (Currículo 2011.1)"
    REGRESSAO_LOGISTICA_MEIO = "Regressão logística (Currículo 2016.1)"
    REGRESSAO_LOGISTICA_NOVO = "Regressão logística (Currículo 2025.1)"
    RANDOM_FOREST_ANTIGO = "Random forest (Currículo 2011.1)"
    RANDOM_FOREST_MEIO = "Random forest (Currículo 2016.1)"
    RANDOM_FOREST_NOVO = "Random forest (Currículo 2025.1)"
    