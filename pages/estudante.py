import streamlit as st
import pandas as pd
from utils.read_file import read_file_pdf
from utils.transform_df import transform_df
from utils.predict_student import predict_student_all_models
from utils.modelos import Modelos
from utils.exceptions import EmtpyDocumentException
from utils.grafico_mencoes import grafico_mencoes_agrupadas
from utils.metricas_modelos import get_metricas_modelos

st.set_page_config(
    page_title="Área do Estudante",
    page_icon="👨‍🎓",
    layout="centered"
)

st.page_link("app.py", label="⬅ Voltar")

def exibir_previsoes_estudante(resultados):

    linhas = []

    probabilidades = []

    for nome_modelo, dados in resultados.items():

        probabilidade = float(
            dados["probability"]
        )

        probabilidades.append(probabilidade)

        linhas.append({
            "Modelo": nome_modelo,
            "Risco de evasão": f"{probabilidade * 100:.2f}%"
        })

    df = pd.DataFrame(linhas)

    st.subheader("📊 Risco de Evasão")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    risco_medio = (
        sum(probabilidades)
        / len(probabilidades)
    )

    st.metric(
        "Risco Médio de Evasão",
        f"{risco_medio*100:.2f}%"
    )

def button_enviar_dados():
    if st.button("📤 Enviar dados para análise"):
        try:
            transformed_data, matriculas = transform_df(st.session_state.df)
            st.session_state.resultados = (
                predict_student_all_models(transformed_data)
            )
            st.session_state.mostrar_resultados = True
        
        except AttributeError:
            st.markdown(
                "<p style='color: red; font-size: 20px;'>"
                "Selecione algum documento para ser enviado!"
                "</p>",
                unsafe_allow_html=True
            ) 
        

def apresentar_desempenho_modelos():

    st.subheader("Desempenho dos Modelos")

    st.markdown(
        """
        Os modelos abaixo foram avaliados utilizando uma base de dados histórica
        de estudantes. As métricas apresentadas permitem comparar o desempenho
        de cada algoritmo utilizado para prever o risco de evasão. Para as métricas
        de precisão, recall e F1-score foi utilizada a média entre as predições de formação e evasão.
        """
    )

    df = get_metricas_modelos()

    df["Acurácia"] = df["Acurácia"].map("{:.2}%".format)
    df["Precisão"] = df["Precisão"].map("{:.2}%".format)
    df["Recall"] = df["Recall"].map("{:.2}%".format)
    df["F1-Score"] = df["F1-Score"].map("{:.2}%".format)

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )

def apresentar_graficos():
    st.markdown(
        """
        <p style='font-size: 18px;'>
        O primeiro gráfico abaixo demonstra o desempenho do aluno ao longo do semestre a partir de uma média das menções obtidas. Para o cálculo, foi utilizada a seguinte correspondência de notas:
        </p>
        <ul>
            <li> SR: 0.0 </li>
            <li> II: 1.0 </li>
            <li> MI: 2.0 </li>
            <li> MM: 3.0 </li>
            <li> MS: 4.0 </li>
            <li> SS: 5.0 </li>
        </ul>
        """,
        unsafe_allow_html=True
    )
            
    graficos = grafico_mencoes_agrupadas(st.session_state.df)

    for lista in graficos.values():
        for grafico in lista:
            st.pyplot(grafico)



st.title("👨‍🎓 Área do Estudante")

st.markdown("""
### O que você pode fazer aqui
- Enviar seu histórico acadêmico
- Visualizar suas disciplinas
- Obter uma **previsão de evasão**
""")


st.divider()

apresentar_desempenho_modelos()

st.divider()

with st.container(border=True):
    st.subheader("📄 Envio do histórico")
    uploaded_file = st.file_uploader(
        "Selecione seu histórico em PDF",
        type="pdf"
    )

if uploaded_file:

    with st.spinner("📊 Coletando os dados..."):
        try:
            st.session_state.df = read_file_pdf(uploaded_file)

            
            st.subheader("✏️ Confira os dados e clique no botão abaixo")
            button_enviar_dados()
            st.session_state.df = st.data_editor(
                st.session_state.df,
                num_rows="dynamic"
            )
            

        except EmtpyDocumentException:
            st.markdown(
                "<p style='color: red; font-size: 20px;'>"
                "Não foram encontradas matérias no documento enviado."
                "</p>",
                unsafe_allow_html=True
            ) 

if st.session_state.get("mostrar_resultados", False):
    exibir_previsoes_estudante(
        st.session_state.resultados
    )
    apresentar_graficos()
    
