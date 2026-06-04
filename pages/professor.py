import streamlit as st
import pandas as pd
from utils.read_file import read_file_pdf, read_file_csv
from utils.transform_df import transform_df
from utils.decision_tree_model import predict_student
from utils.select_modelos_enum import Modelos
from utils.exceptions import EmtpyDocumentException, InvalidModelException
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

if "indice_grafico" not in st.session_state:
    st.session_state.indice_grafico = 0

if "ultimo_aluno" not in st.session_state:
    st.session_state.ultimo_aluno = None

if "mostrar_modal" not in st.session_state:
    st.session_state.mostrar_modal = False

@st.dialog("Previsão")
def modal_previsao(previsao_dicionario: dict):

    total_alunos = len(previsao_dicionario)
    evasao = sum(x[0] for x in list(previsao_dicionario.values()))
    formacao = total_alunos - evasao

    with st.container(border=True):
        st.markdown(
            "<h3 style='text-align:center;'>📌 Resumo Geral</h3>",
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("👥 Total", total_alunos)
        c2.metric("⚠️ Evasão", evasao)
        c3.metric("✅ Formação", formacao)
    
    st.divider()

    df = pd.DataFrame(columns=["Matrícula", "Previsão"])

    for key, value in previsao_dicionario.items():
        prediction = value[0]
        probability = value[1]

        new_row = pd.DataFrame([{"Matrícula": key, "Previsão": f"⚠️ {probability * 100:.2f} de risco de evasão" if prediction else f"✅ {probability * 100:.2f} de chance de formação"}])

        df = pd.concat([df, new_row], ignore_index=True)

    st.dataframe(
        df[["Matrícula", "Previsão"]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        "<p style='font-size:13px; color:gray; text-align:center;'>"
        "⚠️ As previsões são baseadas em modelos estatísticos e não representam decisões finais."
        "</p>",
        unsafe_allow_html=True
    )


def carrossel_graficos():

    graficos = st.session_state.graficos

    if graficos is None:
        return

    st.markdown(
        """
        <p style='font-size: 18px;'>
        O primeiro gráfico abaixo demonstra o desempenho do aluno ao longo do semestre
        a partir de uma média das menções obtidas.
        </p>
        """,
        unsafe_allow_html=True
    )

    alunos = list(graficos.keys())

    aluno_selecionado = st.selectbox(
        "Selecione o aluno",
        alunos
    )

    graficos_aluno = graficos[aluno_selecionado]

    if st.session_state.ultimo_aluno != aluno_selecionado:
        st.session_state.indice_grafico = 0
        st.session_state.ultimo_aluno = aluno_selecionado

    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        if st.button("⬅️", key="anterior"):
            st.session_state.indice_grafico = (
                st.session_state.indice_grafico - 1
            ) % len(graficos_aluno)

    with col3:
        if st.button("➡️", key="proximo"):
            st.session_state.indice_grafico = (
                st.session_state.indice_grafico + 1
            ) % len(graficos_aluno)

    indice = st.session_state.indice_grafico

    st.write(
        f"Gráfico {indice + 1} de {len(graficos_aluno)}"
    )

    st.pyplot(
        graficos_aluno[indice]
    )

def executar_analise():

    result = {}

    transformed_data, matriculas = transform_df(
        st.session_state.df
    )

    for index, row in transformed_data.iterrows():

        result[matriculas[index]] = predict_student(
            row.to_frame().T,
            option
        )

    st.session_state.resultado_previsao = result

    st.session_state.graficos = grafico_mencoes_agrupadas(
        st.session_state.df,
        True
    )

    st.session_state.analise_realizada = True
    st.session_state.mostrar_modal = True


st.title("👨‍🏫 Área do Professor")

st.markdown("""
### 📌 O que você pode fazer aqui
- Enviar o histórico acadêmico de vários estudantes ou enviar um arquivo preenchido com as informações do histórico dos estudantes
- Obter uma **previsão de evasão** por estudante
""")

option = st.selectbox(
    "Selecione o modelo que deseja utilizar",
    ("Selecione uma opção",
     Modelos.ARVORE_DECISAO_ANTIGO.value,
     Modelos.ARVORE_DECISAO_MEIO.value,
     Modelos.ARVORE_DECISAO_NOVO.value,
     Modelos.REGRESSAO_LOGISTICA_ANTIGO.value,
     Modelos.REGRESSAO_LOGISTICA_MEIO.value,
     Modelos.REGRESSAO_LOGISTICA_NOVO.value,
     Modelos.RANDOM_FOREST_ANTIGO.value,
     Modelos.RANDOM_FOREST_MEIO.value,
     Modelos.RANDOM_FOREST_NOVO.value)
)

match option:
    case Modelos.ARVORE_DECISAO_ANTIGO.value:
        st.write("""
-  Utiliza o currículo de 2011.1 para a construção do modelo de árvore de decisão;
-  95,71% de Verdadeiros Positivos (o modelo previu que os alunos evadiram e realmente evadiram);
-  97,70% de Verdadeiros Negativos (o modelo previu que os alunos não evadiram e realmente não evadiram).
""")
    case Modelos.ARVORE_DECISAO_MEIO.value:
        st.write("""
-  Utiliza o currículo de 2016.1 para a construção do modelo de árvore de decisão;
-  96,79% de Verdadeiros Positivos (o modelo previu que os alunos evadiram e realmente evadiram);
-  96,08% de Verdadeiros Negativos (o modelo previu que os alunos não evadiram e realmente não evadiram).
""")
    case Modelos.ARVORE_DECISAO_NOVO.value:
        st.write("""
-  Utiliza o currículo de 2025.1 para a construção do modelo de árvore de decisão;
-  98,60% de Verdadeiros Positivos (o modelo previu que os alunos evadiram e realmente evadiram);
-  92,95% de Verdadeiros Negativos (o modelo previu que os alunos não evadiram e realmente não evadiram).
""")
    case Modelos.REGRESSAO_LOGISTICA_ANTIGO.value:
        st.write("""
-  Utiliza o currículo de 2011.1 para a construção do modelo de regressão logística;
-  94,28% de Verdadeiros Positivos (o modelo previu que os alunos evadiram e realmente evadiram);
-  95,40% de Verdadeiros Negativos (o modelo previu que os alunos não evadiram e realmente não evadiram).
""")
    case Modelos.REGRESSAO_LOGISTICA_MEIO.value:
        st.write("""
-  Utiliza o currículo de 2016.1 para a construção do modelo de regressão logística;
-  94,95% de Verdadeiros Positivos (o modelo previu que os alunos evadiram e realmente evadiram);
-  92,15% de Verdadeiros Negativos (o modelo previu que os alunos não evadiram e realmente não evadiram).
""")
    case Modelos.REGRESSAO_LOGISTICA_NOVO.value:
        st.write("""
-  Utiliza o currículo de 2025.1 para a construção do modelo de regressão logística;
-  96,26% de Verdadeiros Positivos (o modelo previu que os alunos evadiram e realmente evadiram);
-  93,58% de Verdadeiros Negativos (o modelo previu que os alunos não evadiram e realmente não evadiram).
""")
    case Modelos.RANDOM_FOREST_ANTIGO.value:
        st.write("""
-  Utiliza o currículo de 2011.1 para a construção do modelo de random forest;
-  96,19% de Verdadeiros Positivos (o modelo previu que os alunos evadiram e realmente evadiram);
-  98,85% de Verdadeiros Negativos (o modelo previu que os alunos não evadiram e realmente não evadiram).
""")
    case Modelos.RANDOM_FOREST_MEIO.value:
        st.write("""
-  Utiliza o currículo de 2016.1 para a construção do modelo de random forest;
-  96,78% de Verdadeiros Positivos (o modelo previu que os alunos evadiram e realmente evadiram);
-  92,89% de Verdadeiros Negativos (o modelo previu que os alunos não evadiram e realmente não evadiram).
""")
    case Modelos.RANDOM_FOREST_NOVO.value:
        st.write("""
-  Utiliza o currículo de 2025.1 para a construção do modelo de random forest;
-  97,66% de Verdadeiros Positivos (o modelo previu que os alunos evadiram e realmente evadiram);
-  97,43% de Verdadeiros Negativos (o modelo previu que os alunos não evadiram e realmente não evadiram).
""")
    case _:
        pass


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


if uploaded_files_pdf:

    st.session_state.df = pd.DataFrame()

    with st.spinner("📊 Coletando os dados..."):
        for uploaded_file in uploaded_files_pdf:
            df_pdf = read_file_pdf(uploaded_file)

            st.session_state.df = pd.concat(
                [st.session_state.df, df_pdf],
                ignore_index=True
            )


    st.divider()
    st.subheader("✏️ Edite os dados")

    st.session_state.df = st.data_editor(
        st.session_state.df,
        num_rows="dynamic"
    )
    
    if st.button("📤 Enviar dados", key="enviar_pdf"):

        result = {}
            
        try:
            executar_analise()

        except AttributeError:
            st.markdown(
                "<p style='color: red; font-size: 20px;'>"
                "Selecione algum documento para ser enviado!"
                "</p>",
                unsafe_allow_html=True
            )   
            
        except InvalidModelException:
            st.markdown(
                "<p style='color: red; font-size: 20px;'>"
                "Selecione algum modelo para ser utilizado!"
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

    
if uploaded_file_csv:

    with st.spinner("📊 Coletando os dados..."):
        try:
            st.session_state.df = read_file_csv(uploaded_file_csv)

            st.divider()
            st.subheader("✏️ Edite os dados")

            st.session_state.df = st.data_editor(
                st.session_state.df,
                num_rows="dynamic"
            )

            if st.button("📤 Enviar dados", key="enviar_csv"):
            
              try:
                  executar_analise()

              except AttributeError:
                  st.markdown(
                      "<p style='color: red; font-size: 20px;'>"
                      "Selecione algum documento para ser enviado!"
                      "</p>",
                      unsafe_allow_html=True
                  )   
              except InvalidModelException:
                st.markdown(
                    "<p style='color: red; font-size: 20px;'>"
                    "Selecione algum modelo para ser utilizado!"
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

if st.session_state.mostrar_modal:

    modal_previsao(
        st.session_state.resultado_previsao
    )
    st.session_state.mostrar_modal = False
    
if st.session_state.analise_realizada:
    carrossel_graficos()