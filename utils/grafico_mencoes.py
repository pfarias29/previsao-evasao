import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from .transform_df import mencao_map


def grafico_mencoes_agrupadas(df: pd.DataFrame):

    df_notas_mapeadas = df

    df_notas_mapeadas["valor_nota"] = df["nota"].map(mencao_map)

    df_medias = (df_notas_mapeadas.groupby(["nome_aluno", "ano_periodo"])["valor_nota"].mean().reset_index())

    figuras = []

    for nome, dados_aluno in df_medias.groupby("nome_aluno"):

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.plot(
            dados_aluno["ano_periodo"],
            dados_aluno["valor_nota"],
            marker="o"
        )

        ax.set_title(f"{nome}")
        ax.set_xlabel("Semestre")
        ax.set_ylabel("Média")

        figuras.append(fig)

    return figuras