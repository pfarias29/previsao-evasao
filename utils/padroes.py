import re

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
]