import streamlit as st
from utils.read_file import read_file_pdf
from utils.transform_df import transform_df
from utils.decision_tree_model import predict_student

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
        num_rows="dynamic"
    )

if st.button("📤 Enviar dados"):
    if not st.session_state.df.empty:
        transformed_data = transform_df(st.session_state.df)
        predict_student(transformed_data)
    else:
        st.markdown(
            "<p style='color: red; font-size: 20px;'>"
            "Selecione algum documento para ser enviado!"
            "</p>",
            unsafe_allow_html=True
        )   

