import streamlit as st
from utils.read_file import read_file_pdf

st.set_page_config(
    page_title="Área do Estudante",
    page_icon="👨‍🎓",
    layout="centered"
)

st.page_link("app.py", label="⬅ Voltar")

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
        if "df" not in st.session_state:
            st.session_state.df = read_file_pdf(uploaded_file)

        st.subheader("✏️ Edite seus dados")
        st.session_state.df = st.data_editor(
            st.session_state.df,
            use_container_width=True,
            num_rows="dynamic"
        )
