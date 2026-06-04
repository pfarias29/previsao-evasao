import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from .transform_df import mencao_map


def grafico_mencoes_agrupadas(df: pd.DataFrame, is_professor=False):

    ## DF gráfico média menções por semestre
    df_notas_mapeadas = df
    df_notas_mapeadas["valor_nota"] = df["nota"].map(mencao_map)
    df_medias = (df_notas_mapeadas.groupby(["nome_aluno", "ano_periodo"])["valor_nota"].mean().reset_index())

    df_media_geral = (
        df_medias
        .groupby("ano_periodo")["valor_nota"]
        .mean()
        .reset_index()
    )

    todos_semestres = sorted(df_medias["ano_periodo"].unique())


    resultado = {}

    for nome, dados_aluno in df_medias.groupby("nome_aluno"):

        graficos = []

        if is_professor:
            dados_plot = pd.DataFrame({
            "ano_periodo": todos_semestres
            })

            dados_plot = (
                dados_plot
                .merge(
                    dados_aluno[["ano_periodo", "valor_nota"]],
                    on="ano_periodo",
                    how="left"
                )
                .merge(
                    df_media_geral,
                    on="ano_periodo",
                    how="left",
                    suffixes=("_aluno", "_geral")
                )
            )

            fig, ax = plt.subplots(figsize=(8,4))

            x = range(len(todos_semestres))

            ax.plot(
                x,
                dados_plot["valor_nota_aluno"],
                marker="o",
                label="Aluno"
            )

            ax.plot(
                x,
                dados_plot["valor_nota_geral"],
                marker="s",
                linestyle="--",
                label="Média Geral"
            )

            ax.set_xticks(x)
            ax.set_xticklabels(todos_semestres, rotation=45)

            ax.legend()

        else:
            fig, ax = plt.subplots(figsize=(8, 4))

            # Média do aluno
            ax.plot(
                dados_aluno["ano_periodo"],
                dados_aluno["valor_nota"],
                marker="o",
                linewidth=2,
                label="Aluno"
            )

            ax.set_title("Média de Menções por Semestre")
            ax.set_xlabel("Semestre")
            ax.set_ylabel("Média")

            ax.legend()
            ax.grid(True, alpha=0.3)

        graficos.append(fig)

        ## Gráfico quantidade de menções

        ## DF histograma de menções
        dados_aluno = df[df["nome_aluno"] == nome]
        
        contagem = (
            dados_aluno["nota"]
            .value_counts()
            .reindex(["SR", "II", "MI", "MM", "MS", "SS"], fill_value=0)
        )

        fig_hist, ax_hist = plt.subplots(figsize=(8, 4))

        ax_hist.bar(
            contagem.index,
            contagem.values
        )

        ax_hist.set_title("Distribuição das Menções")
        ax_hist.set_xlabel("Menção")
        ax_hist.set_ylabel("Quantidade")

        graficos.append(fig_hist)

        
        ## Gráfico de taxa de aprovação por semestre

        ## DF taxa de aprovação
        dados_aluno = df[df["nome_aluno"] == nome]

        taxa_semestre = (
            dados_aluno
            .assign(
                aprovado=lambda x:
                x["nota"].isin(["MM", "MS", "SS"])
            )
            .groupby("ano_periodo")["aprovado"]
            .mean()
            .mul(100)
            .reset_index()
        )

        fig_taxa, ax_taxa = plt.subplots(figsize=(8,4))

        ax_taxa.plot(
            taxa_semestre["ano_periodo"],
            taxa_semestre["aprovado"],
            marker="o"
        )

        ax_taxa.set_ylim(0, 100)

        ax_taxa.set_title(
            "Taxa de Aprovação por Semestre"
        )

        ax_taxa.set_ylabel("% de Aprovação")

        graficos.append(fig_taxa)


        resultado[nome] = graficos

    return resultado
