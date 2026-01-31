import streamlit as st
import pandas as pd
from utils.read_file import read_file_pdf, read_file_csv
from utils.transform_df import transform_df
from utils.decision_tree_model import predict_student

st.set_page_config(
    page_title="Área do Professor",
    page_icon="👨‍🏫",
    layout="centered"
)

st.page_link("app.py", label="⬅ Voltar")

@st.dialog("Previsão")
def modal_previsao(previsao_dicionario: dict):

    total_alunos = len(previsao_dicionario)
    evasao = sum(list(previsao_dicionario.values()))
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
        new_row = pd.DataFrame([{"Matrícula": key, "Previsão": "⚠️ Risco de evasão" if value else "✅ Chance de formação"}])

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
            data="matricula,ano_periodo,codigo,nome,carga_horaria,turma,frequencia,nota,situacao",
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

    result = {}

    try:
        transformed_data, matriculas = transform_df(st.session_state.df)
        
        for index, row in transformed_data.iterrows():

            result[matriculas[index]] = predict_student(row.to_frame().T)

        modal_previsao(result)
    except AttributeError:
        st.markdown(
            "<p style='color: red; font-size: 20px;'>"
            "Selecione algum documento para ser enviado!"
            "</p>",
            unsafe_allow_html=True
        )   