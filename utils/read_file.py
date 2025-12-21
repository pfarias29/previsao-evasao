import pdfplumber
import pandas as pd
import re
from .padroes import padroes

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
        for p in padroes:
            m = p.search(linha)
            if m:
                dados.append({
                    "matricula": matricula,
                    "ano_periodo": m.groupdict().get("ano"),
                    "codigo": m.groupdict().get("codigo"),
                    "carga_horaria": m.groupdict().get("ch"),
                    "turma": m.groupdict().get("turma"),
                    "frequencia": m.groupdict().get("freq"),
                    "nota": m.groupdict().get("nota"),
                    "situacao": m.groupdict().get("situacao")
                })
                break


    return pd.DataFrame(dados)

def read_file_csv(arq):
    df = pd.read_csv(arq)

    return df