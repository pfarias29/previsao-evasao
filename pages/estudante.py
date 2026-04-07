import streamlit as st
from utils.read_file import read_file_pdf
from utils.transform_df import transform_df
from utils.decision_tree_model import predict_student
from utils.select_modelos_enum import Modelos
from utils.exceptions import InvalidModelException, EmtpyDocumentException


st.set_page_config(
    page_title="Área do Estudante",
    page_icon="👨‍🎓",
    layout="centered"
)

st.page_link("app.py", label="⬅ Voltar")

@st.dialog("Previsão")
def modal_previsao(previsao):
    with st.container(border=True):
        st.markdown(
            "<h3 style='text-align: center;'>🎓 Análise do Histórico Acadêmico</h3>",
            unsafe_allow_html=True
        )

        st.divider()

        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown(
                "<p style='font-size: 40px; text-align: center;'>"
                f"{'⚠️' if previsao else '✅'}"
                "</p>",
                unsafe_allow_html=True
            )

        with col2:
            if previsao:
                st.markdown(
                    """
                    <p style='font-size: 18px;'>
                    Com base no histórico informado, o estudante apresenta
                    <b style='color:#e74c3c;'>maior risco de evasão</b>.
                    </p>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <p style='font-size: 18px;'>
                    Com base no histórico informado, o estudante apresenta
                    <b style='color:#2ecc71;'>maior chance de formação</b>.
                    </p>
                    """,
                    unsafe_allow_html=True
                )

        st.divider()

        st.markdown(
            "<p style='text-align: center; font-size: 14px; color: gray;'>"
            "⚠️ Esta previsão é baseada em modelos estatísticos e não representa uma decisão final."
            "</p>",
            unsafe_allow_html=True
        )

def button_enviar_dados():
    if st.button("📤 Enviar dados"):
        try:
            transformed_data, matriculas = transform_df(st.session_state.df)
            prediction = predict_student(transformed_data, option)

            modal_previsao(previsao=prediction)

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

st.title("👨‍🎓 Área do Estudante")

st.markdown("""
### 📌 O que você pode fazer aqui
- Enviar seu histórico acadêmico
- Visualizar suas disciplinas
- Obter uma **previsão de evasão**
""")

option = st.selectbox(
    "Selecione o modelo que deseja utilizar",
    ("Selecione uma opção",
     Modelos.ARVORE_DECISAO_ANTIGO.value,
     Modelos.ARVORE_DECISAO_NOVO.value,
     Modelos.REGRESSAO_LOGISTICA.value,
     Modelos.RANDOM_FOREST.value)
)

match option:
    case Modelos.ARVORE_DECISAO_ANTIGO.value:
        st.write("""
-  Divide os dados de forma que os subconjuntos sejam o mais "puros" possíveis;
-  98,60% de Verdadeiros Positivos (o modelo previu que os alunos evadiram e realmente evadiram)
-  92,89% de Verdadeiros Negativos (o modelo previu que os alunos não evadiram e realmente não evadiram)
-  utiliza o um currículo mais antigo como base para as matérias do curso;
""")
    case Modelos.ARVORE_DECISAO_NOVO.value:
        st.write("""
-  Divide os dados de forma que os subconjuntos sejam o mais "puros" possíveis;
-  98,60% de Verdadeiros Positivos (o modelo previu que os alunos evadiram e realmente evadiram)
-  92,89% de Verdadeiros Negativos (o modelo previu que os alunos não evadiram e realmente não evadiram)
-  utiliza o um currículo mais atualizado como base para as matérias do curso;
""")
    case Modelos.REGRESSAO_LOGISTICA.value:
        st.write("""
-  Prevê a probabilidade de ocorrência de um evento específico;
-  96,26% de Verdadeiros Positivos (o modelo previu que os alunos evadiram e realmente evadiram);
-  93,58% de Verdadeiros Negativos (o modelo previu que os alunos não evadiram e realmente não evadiram);
""")
    case Modelos.RANDOM_FOREST.value:
        st.write("""
- Divide os dados de forma que os subconjuntos sejam o mais "puros" possíveis;
-  97,66% de Verdadeiros Positivos (o modelo previu que os alunos evadiram e realmente evadiram)
-  97,43% de Verdadeiros Negativos (o modelo previu que os alunos não evadiram e realmente não evadiram)
""")
    case _:
        pass

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

        except EmtpyDocumentException:
            st.markdown(
                "<p style='color: red; font-size: 20px;'>"
                "Não foram encontradas matérias no documento enviado."
                "</p>",
                unsafe_allow_html=True
            ) 
    
