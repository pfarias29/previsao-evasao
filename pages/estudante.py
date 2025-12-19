import streamlit as st
import pdfplumber
import re
import pandas as pd
from io import StringIO
import utils.padroes as padroes

st.page_link("app.py", label="Voltar", icon=":material/keyboard_return:")

st.title("Área do estudante")

st.write("##### Aqui você poderá inserir seu histórico para conseguir uma previsão de evasão.",)
st.write("Baixe um exemplo do arquivo de entrada ou insira seu histórico para analisarmos.")

uploaded_file = st.file_uploader("Selecionar histórico (PDF)", type="pdf")

def read_file_pdf(arq):
    text = ""

    with pdfplumber.open(arq) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    matricula_match = re.search(r"Matrícula:\s*(\d+)", text)
    matricula = matricula_match.group(1) if matricula_match else None

    linhas = text.splitlines()
    dados = []

    for linha in linhas:
        for p in padroes.padroes:
            m = p.search(linha)
            if m:
                dados.append({
                    "matricula": matricula,
                    "ano_periodo": m.groupdict().get("ano"),
                    "codigo": m.groupdict().get("codigo"),
                    "nome": m.groupdict().get("nome"),
                    "carga_horaria": m.groupdict().get("ch"),
                    "turma": m.groupdict().get("turma"),
                    "frequencia": m.groupdict().get("freq"),
                    "nota": m.groupdict().get("nota"),
                    "situacao": m.groupdict().get("situacao")
                })
                break


    df = pd.DataFrame(dados)

    print(df) 

if uploaded_file:
    read_file_pdf(uploaded_file)