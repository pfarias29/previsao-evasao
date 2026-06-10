from enum import Enum

class Modelos(Enum):
    ARVORE_DECISAO      = "utils/modelos/novo/modelo_decision_tree.joblib"
    REGRESSAO_LOGISTICA = "utils/modelos/novo/modelo_logistic_regression.joblib"
    RANDOM_FOREST       = "utils/modelos/novo/modelo_random_forest.joblib"
    
NOMES_MODELOS = {
    Modelos.ARVORE_DECISAO: "Árvore de Decisão",
    Modelos.REGRESSAO_LOGISTICA: "Regressão Logística",
    Modelos.RANDOM_FOREST: "Random Forest"
}