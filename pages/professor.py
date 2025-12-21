import streamlit as st
import pandas as pd
from utils.read_file import read_file_pdf, read_file_csv
from utils.transform_df import transform_df

st.set_page_config(
    page_title="Área do Professor",
    page_icon="👨‍🏫",
    layout="centered"
)

st.page_link("app.py", label="⬅ Voltar")

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
            data="matricula,ano_periodo,codigo,carga_horaria,turma,frequencia,nota,situacao",
            file_name="template_alunos.csv",
            icon=":material/download:"
        )
    with st.container(border=True, height="stretch"):
        st.subheader("📄 Envio do template preenchido")
        uploaded_file_csv = st.file_uploader(
            "Selecione o arquivo em CSV",
            type="csv"
        )

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if uploaded_files_pdf:

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
    
if uploaded_file_csv:

    with st.spinner("📊 Coletando os dados..."):
        st.session_state.df = read_file_csv(uploaded_file_csv)

    st.divider()
    st.subheader("✏️ Edite os dados")

    st.session_state.df = st.data_editor(
        st.session_state.df,
        num_rows="dynamic"
    )

if st.button("📤 Enviar dados"):
    if not st.session_state.df.empty:
        st.session_state.df = transform_df(st.session_state.df)
        print(st.session_state.df)
    else:
        st.markdown(
            "<p style='color: red; font-size: 20px;'>"
            "Selecione algum documento para ser enviado!"
            "</p>",
            unsafe_allow_html=True
        )   