import streamlit as st
import pandas as pd
from utils.read_file import read_file_pdf, read_file_csv
from utils.transform_df import transform_df
from utils.predict_student import predict_student_all_models
from utils.exceptions import EmtpyDocumentException
from utils.grafico_mencoes import grafico_mencoes_agrupadas

st.set_page_config(
    page_title="Área do Professor",
    page_icon="👨‍🏫",
    layout="centered"
)

st.page_link("app.py", label="⬅ Voltar")

if "analise_realizada" not in st.session_state:
    st.session_state.analise_realizada = False

if "graficos" not in st.session_state:
    st.session_state.graficos = None

if "resultado_previsao" not in st.session_state:
    st.session_state.resultado_previsao = None

def exibir_previsoes(previsao_dicionario):

    linhas = []

    for matricula, modelos in previsao_dicionario.items():

        linha = {
            "Matrícula": matricula
        }

        probabilidades = []

        for nome_modelo, dados in modelos.items():

            probabilidade = float(
                dados["probability"]
            )

            linha[nome_modelo] = f"{probabilidade * 100:.2f}%"

            probabilidades.append(probabilidade)

        linha["Risco Médio"] = (
            f"{sum(probabilidades)/len(probabilidades)*100:.2f}%"
        )

        linhas.append(linha)   # <- faltava isso

    df = pd.DataFrame(linhas)

    st.subheader("📊 Risco de Evasão")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

def apresentar_graficos():

    graficos = st.session_state.graficos

    if graficos is None:
        return

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

    aluno_selecionado = st.selectbox(
        "Selecione o aluno",
        list(graficos.keys())
    )

    for grafico in graficos[aluno_selecionado]:
        st.pyplot(grafico)

def executar_analise():

    result = {}

    transformed_data, matriculas = transform_df(
        st.session_state.df
    )

    for index, row in transformed_data.iterrows():

        dados_aluno = row.to_frame().T


        result[matriculas[index]] = (
            predict_student_all_models(
                dados_aluno
            )
        )

    st.session_state.resultado_previsao = result

    st.session_state.graficos = grafico_mencoes_agrupadas(
        st.session_state.df,
        True
    )

    st.session_state.analise_realizada = True


st.title("👨‍🏫 Área do Professor")

st.markdown("""
### 📌 O que você pode fazer aqui
- Enviar o histórico acadêmico de vários estudantes ou enviar um arquivo preenchido com as informações do histórico dos estudantes
- Obter uma **previsão de evasão** por estudante
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True, height="stretch"):
        st.subheader("📄 Envio dos históricos")
        uploaded_files_pdf = st.file_uploader(
            "Selecione os históricos em PDF",
            accept_multiple_files=True,
            type="pdf"
        )

with col2:
    with st.container(border=True, height="stretch"):
        st.subheader("🗃️ Baixar template")
        st.markdown(
            "<p style='font-size: 20px; font-weight:bold'>"
            "Obs.: Não remover o header."
            "</p>",
            unsafe_allow_html=True
        )   
        st.download_button(
            label="Baixar template",
            data="nome_aluno,matricula,ano_periodo,codigo,nome,carga_horaria,turma,frequencia,nota,situacao",
            file_name="template_alunos.csv",
            icon=":material/download:"
        )
    with st.container(border=True, height="stretch"):
        st.subheader("📄 Envio do template preenchido")
        uploaded_file_csv = st.file_uploader(
            "Selecione o arquivo em CSV",
            type="csv"
        )

if uploaded_files_pdf and "pdf_carregado" not in st.session_state:

    with st.spinner("📊 Coletando dados..."):

        st.session_state.df = pd.DataFrame()

        for uploaded_file in uploaded_files_pdf:
            df_pdf = read_file_pdf(uploaded_file)

            st.session_state.df = pd.concat(
                [st.session_state.df, df_pdf],
                ignore_index=True
            )

        st.session_state.pdf_carregado = True


    st.divider()
    
if "df" in st.session_state:

    st.subheader("✏️ Confira os dados e clique no botão abaixo")

    if st.button("📤 Enviar dados para análise"):

        try:
            executar_analise()

        except AttributeError:
            st.markdown(
                "<p style='color: red; font-size: 20px;'>"
                "Selecione algum documento para ser enviado!"
                "</p>",
                unsafe_allow_html=True
            )    
        except EmtpyDocumentException:
            st.markdown(
                "<p style='color: red; font-size: 20px;'>"
                "Não foram encontrados registros no documento enviado."
                "</p>",
                unsafe_allow_html=True
            ) 

    st.session_state.df = st.data_editor(
        st.session_state.df,
        num_rows="dynamic"
    )

    
if uploaded_file_csv:

    with st.spinner("📊 Coletando dados..."):
        try:
            st.session_state.df = read_file_csv(uploaded_file_csv)

            st.divider()

            st.subheader("✏️ Confira os dados e clique no botão abaixo")
            if st.button("📤 Enviar dados para análise", key="enviar_csv"):
            
              try:
                  executar_analise()

              except AttributeError:
                  st.markdown(
                      "<p style='color: red; font-size: 20px;'>"
                      "Selecione algum documento para ser enviado!"
                      "</p>",
                      unsafe_allow_html=True
                  )   
                  

            st.session_state.df = st.data_editor(
                st.session_state.df,
                num_rows="dynamic"
            )

        except EmtpyDocumentException:
            st.markdown(
                "<p style='color: red; font-size: 20px;'>"
                "Não foram encontrados registros no documento enviado."
                "</p>",
                unsafe_allow_html=True
            ) 


if st.session_state.analise_realizada:

    exibir_previsoes(
        st.session_state.resultado_previsao
    )

    apresentar_graficos()