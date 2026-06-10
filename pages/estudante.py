import streamlit as st
import pandas as pd
from utils.read_file import read_file_pdf
from utils.transform_df import transform_df
from utils.predict_student import predict_student_all_models
from utils.modelos import Modelos
from utils.exceptions import EmtpyDocumentException
from utils.grafico_mencoes import grafico_mencoes_agrupadas

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
    if st.button("📤 Enviar dados"):
        try:
            transformed_data, matriculas = transform_df(st.session_state.df)
            resultados = predict_student_all_models(transformed_data)
            exibir_previsoes_estudante(resultados)        
        
        except AttributeError:
            st.markdown(
                "<p style='color: red; font-size: 20px;'>"
                "Selecione algum documento para ser enviado!"
                "</p>",
                unsafe_allow_html=True
            ) 

def carrossel_graficos():
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

    alunos = list(graficos.keys())

    aluno_selecionado = st.selectbox(
        "Selecione o aluno",
        alunos
    )

    if "indice_grafico" not in st.session_state:
        st.session_state.indice_grafico = 0

    graficos = graficos[aluno_selecionado]

    if "ultimo_aluno" not in st.session_state:
        st.session_state.ultimo_aluno = aluno_selecionado

    if st.session_state.ultimo_aluno != aluno_selecionado:
        st.session_state.indice_grafico = 0
        st.session_state.ultimo_aluno = aluno_selecionado

    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        if st.button("⬅️", key="anterior"):
            st.session_state.indice_grafico = (
            st.session_state.indice_grafico - 1
            ) % len(graficos)

    with col3:
        if st.button("➡️", key="proximo"):
            st.session_state.indice_grafico = (
            st.session_state.indice_grafico + 1
            ) % len(graficos)

    indice = st.session_state.indice_grafico

    st.write(
        f"Gráfico {indice + 1} de {len(graficos)}"
    )

    st.pyplot(graficos[indice])

st.title("👨‍🎓 Área do Estudante")

st.markdown("""
### 📌 O que você pode fazer aqui
- Enviar seu histórico acadêmico
- Visualizar suas disciplinas
- Obter uma **previsão de evasão**
""")


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

            st.subheader("✏️ Edite seus dados")
            st.session_state.df = st.data_editor(
                st.session_state.df,
                num_rows="dynamic"
            )

            button_enviar_dados()

            carrossel_graficos()
            

        except EmtpyDocumentException:
            st.markdown(
                "<p style='color: red; font-size: 20px;'>"
                "Não foram encontradas matérias no documento enviado."
                "</p>",
                unsafe_allow_html=True
            ) 
    
