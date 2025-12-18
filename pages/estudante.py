import streamlit as st
import pdfplumber
import re
import pandas as pd

padrao_normal = re.compile(
    r"(?P<ano>\d{4}\.\d|--)\s+"
    r"(?P<flag>[\*\#\&\@\§]?)\s*"
    r"(?P<codigo>[A-Z]{3}\d{4})\s+"
    r"(?P<ch>\d+)\s+"
    r"(?P<turma>[A-Z0-9]{1,2}|--)\s+"
    r"(?P<freq>\d{2,3},\d|--)\s+"
    r"(?P<nota>[A-Z]{2}|-)\s+"
    r"(?P<situacao>[A-Z]{3,4})"
)

padrao_com_nome = re.compile(
    r"(?P<ano>\d{4}\.\d|--)\s+"
    r"(?P<flag>[\*\#\&\@\§]?)\s*"
    r"(?P<codigo>[A-Z]{3}\d{4})\s+"
    r"(?P<nome>.+?)\s+"
    r"(?P<ch>\d+)\s+"
    r"(?P<turma>[A-Z0-9]{1,2}|--)\s+"
    r"(?P<freq>\d{2,3},\d|--)\s+"
    r"(?P<nota>[A-Z]{2}|-)\s+"
    r"(?P<situacao>[A-Z]{3,4})"
)

padrao_nome_antes = re.compile(
    r"(?P<ano>\d{4}\.\d)\s+"
    r"(?P<codigo>[A-Z]{3}\d{4})\s+"
    r"(?P<nome>.+?)\s+"
    r"(?P<ch>\d+)\s+"
    r"(?P<turma>[A-Z0-9]{1,2})\s+"
    r"(?P<freq>\d{2,3},\d)\s+"
    r"(?P<nota>[A-Z]{2})\s+"
    r"(?P<situacao>[A-Z]{3})"
)

padrao_enade = re.compile(
    r"(?P<ano>\d{4}\.\d)\s+"
    r"(?P<codigo>ENADE)\s+"
    r"(?P<ch>\d+)\s+--\s+--\s+---\s+--"
)

padroes = [
    padrao_normal,
    padrao_com_nome,
    padrao_nome_antes,
    padrao_enade
]




st.page_link("app.py", label="Voltar", icon=":material/keyboard_return:")

st.title("Área do estudante")

st.write("##### Aqui você poderá inserir seu histórico para conseguir uma previsão de evasão.",)
st.write("Baixe um exemplo do arquivo de entrada ou insira seu histórico para analisarmos.")


def read_file_pdf(path = "historico_211055577.pdf"):
    text = ""

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    matricula_match = re.search(r"Matrícula:\s*(\d+)", text)
    matricula = matricula_match.group(1) if matricula_match else None

    linhas = text.splitlines()
    dados = []

    for linha in linhas:
        for p in padroes:
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

read_file_pdf()