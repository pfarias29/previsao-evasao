from enum import Enum

class Modelos(Enum):
    ARVORE_DECISAO             = "utils/modelos/novo/modelo_decision_tree.joblib"
    REGRESSAO_LOGISTICA        = "utils/modelos/novo/modelo_logistic_regression.joblib"
    RANDOM_FOREST              = "utils/modelos/novo/modelo_random_forest.joblib"
    K_DEPENDENCE_BAYESIAN      = "utils/modelos/novo/modelo_k_dependence_bayesian.joblib"
    # REDE_BAYESIANA             = "utils/modelos/novo/modelo_rede_bayesiana.joblib"
    TREE_AUGMENTED_NAIVE_BAYES = "utils/modelos/novo/modelo_tree_augmented_naive_bayes.joblib"
    
NOMES_MODELOS = {
    Modelos.ARVORE_DECISAO: "Árvore de Decisão",
    Modelos.REGRESSAO_LOGISTICA: "Regressão Logística",
    Modelos.RANDOM_FOREST: "Random Forest",
    Modelos.K_DEPENDENCE_BAYESIAN: "Redes KDB (K-Dependence-Bayesian)",
    # Modelos.REDE_BAYESIANA: "Rede Bayesiana",
    Modelos.TREE_AUGMENTED_NAIVE_BAYES: "Tree Augmented Naive Bayes (TAN)",
}