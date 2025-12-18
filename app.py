import streamlit as st


st.title("Sistema de previsão de evasão estudantil")

st.write("Selecione o ambiente que deseja utilizar:")

st.page_link("pages/estudante.py", label="Área do estudante", icon=":material/school:")
st.page_link("pages/professor.py", label="Área do professor", icon=":material/admin_panel_settings:")