import pandas as pd

def get_metricas_modelos():
    return pd.DataFrame([
        {
            "Modelo": "Árvore de Decisão",
            "Acurácia": "88,65",
            "Precisão": "89,00",
            "Recall": "89,00",
            "F1-Score": "89,00",
        },
        {
            "Modelo": "Random Forest",
            "Acurácia": "97,73",
            "Precisão": "94,00",
            "Recall": "94,00",
            "F1-Score": "94,00",
        },
        {
            "Modelo": "Regressão Logística",
            "Acurácia": "90,75",
            "Precisão": "94,00",
            "Recall": "94,00",
            "F1-Score": "94,00",
        },
        {
            "Modelo": "Tree Augmented Naive Bayes",
            "Acurácia": "90.44",
            "Precisão": "90,00",
            "Recall": "91,00",
            "F1-Score": "90,00",
        },
        {
            "Modelo": "K-Dependence-Bayesian",
            "Acurácia": "92,83",
            "Precisão": "93,00",
            "Recall": "93,00",
            "F1-Score": "93,00",
        },
        {
            "Modelo": "Rede Bayesiana",
            "Acurácia": "92,83",
            "Precisão": "93,00",
            "Recall": "93,00",
            "F1-Score": "93,00",
        },
    ])