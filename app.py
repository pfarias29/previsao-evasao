import streamlit as st

st.set_page_config(
    page_title="Sistema de Previsão de Evasão",
    page_icon="🎓",
    layout="centered"
)

st.markdown("<h1 style='text-align: center;'>🎓 Sistema de Previsão de Evasão Estudantil</h1>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align: center; font-size: 18px;'>"
    "Selecione o ambiente que deseja acessar"
    "</p>",
    unsafe_allow_html=True
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### 👨‍🎓 Área do Estudante")
        st.write("Envie seu histórico acadêmico e visualize sua previsão de evasão.")
        st.page_link(
            "pages/estudante.py",
            label="Acessar",
            icon=":material/school:"
        )

with col2:
    with st.container(border=True):
        st.markdown("### 👨‍🏫 Área do Professor")
        st.write("Envie o histórico de diversos estudantes e obtenha suas previsões de evasão.")
        st.page_link(
            "pages/professor.py",
            label="Acessar",
            icon=":material/admin_panel_settings:"
        )

st.divider()
st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "Projeto de Trabalho de Conclusão de Curso • Previsão de evasão estudantil"
    "</p>",
    unsafe_allow_html=True
)
