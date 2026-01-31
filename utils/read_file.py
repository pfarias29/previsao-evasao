import pdfplumber
import pandas as pd
import re
from .padroes import padroes, padrao_nome

def read_file_pdf(arq):
    text = ""

    with pdfplumber.open(arq) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    matricula_match = re.search(r"Matrícula:\s*(\d+)", text)
    matricula = matricula_match.group(1) if matricula_match else None

    linhas = text.splitlines()
    dados = []
    nome_atual = None

    for linha in linhas:
        linha = linha.strip()

        if (padrao_nome.match(linha)
            and not linha.startswith(("20", "--"))
            and not re.search(r"[A-Z]{3}\d{4}", linha)
        ):
            nome_atual = linha
            continue

        for p in padroes:
            m = p.search(linha)
            if m:
                dados.append({
                    "matricula": matricula,
                    "ano_periodo": m.groupdict().get("ano"),
                    "codigo": m.groupdict().get("codigo"),
                    "nome": nome_atual,
                    "carga_horaria": m.groupdict().get("ch"),
                    "turma": m.groupdict().get("turma"),
                    "frequencia": m.groupdict().get("freq"),
                    "nota": m.groupdict().get("nota"),
                    "situacao": m.groupdict().get("situacao")
                })
                nome_atual = None
                break


    return pd.DataFrame(dados)

def read_file_csv(arq):
    df = pd.read_csv(arq)

    return df