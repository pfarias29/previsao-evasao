import streamlit as st
import pandas as pd
from utils.read_file import read_file_pdf

st.set_page_config(
    page_title="Área do Professor",
    page_icon="👨‍🏫",
    layout="centered"
)

st.page_link("app.py", label="⬅ Voltar")

st.title("👨‍🏫 Área do Professor")

st.markdown("""
### 📌 O que você pode fazer aqui
- Enviar o histórico acadêmico de vários estudantes ou Enviar um arquivo preenchido com as informações do histórico dos estudantes
- Obter uma **previsão de evasão** por estudante
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("📄 Envio dos históricos")
        uploaded_files = st.file_uploader(
            "Selecione os históricos em PDF",
            accept_multiple_files=True,
            type="pdf"
        )

with col2:
    with st.container(border=True, height="stretch"):
        st.subheader("🗃️ Baixar template")
        st.download_button(
            label="Baixar template",
            data="matricula;ano_periodo;codigo;carga_horaria;turma;frequencia;nota;situacao",
            file_name="template_alunos.csv",
            icon=":material/download:"
        )

if uploaded_files and "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if uploaded_files:

    with st.spinner("📊 Coletando os dados..."):
        for uploaded_file in uploaded_files:
            df_pdf = read_file_pdf(uploaded_file)
            st.session_state.df = pd.concat(
                [st.session_state.df, df_pdf],
                ignore_index=True
            )

    st.divider()
    st.subheader("✏️ Edite os dados")

    st.session_state.df = st.data_editor(
        st.session_state.df,
        use_container_width=True,
        num_rows="dynamic"
    )
