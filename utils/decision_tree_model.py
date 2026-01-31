import joblib
import pandas as pd

def load_decision_tree():
    return joblib.load('utils/modelo_decision_tree.joblib')


def predict_student(student: pd.DataFrame):

    clf = load_decision_tree()
    model = clf["model"]
    columns = clf["columns"]

    student = transforma_colunas(student=student, codigos=columns) 

    student = student.reindex(
        columns=columns,
        fill_value=-1
    )

    prediction = model.predict(student)
    probability = model.predict_proba(student)[0]

    r = ["Formou", "Evadiu"]
    print(r[prediction[0]])
    print(f'{probability[prediction[0]] * 100}% de chance de {r[prediction[0]]}')

    return prediction[0]



DISCIPLINAS = {
    116301: ["CIC0088"],
    118001: ["IFD0171"],
    118010: ["IFD0173"],
    145971: ["LET0331"],
    140481: ["LIP0096"],
    113034: ["MAT0024", "MAT0025"],
    116319: ["CIC0089", "CIC0090"],
    129011: ["CIC0229"],
    129020: ["CIC0231"],
    115045: ["EST0022", "EST0023"],
    118028: ["IDF0175"],
    118036: ["IDF0177"],
    113042: ["MAT0026"],
    113956: ["CIC0008"],
    118044: ["IDF0179"],
    118052: ["IDF0181"],
    113051: ["MAT0027"],
    117366: ["CIC0182"],
    116327: ["CIC0092"],
    116416: ["CIC0101"],
    113123: ["MAT0039"],
    116343: ["CIC0093"],
    116378: ["CIC0097"],
    116394: ["CIC0098", "CIC0099"],
    113107: ["MAT0033", "MAT0034"],
    113115: ["MAT0037"],
    113417: ["MAT0053"],
    116726: ["CIC0142"],
    116432: ["CIC0104"],
    116441: ["CIC0105"],
    116882: ["CIC0161"],
    204315: ["CIC0235"],
    116459: ["CIC0106"],
    116467: ["CIC0108"],
    113930: ["MAT0080"],
    117536: ["CIC0189"],
    116530: ["CIC0117"],
    113468: ["CIC0003"],
    113476: ["CIC0004"],
    113450: ["CIC0002"],
    113093: ["MAT0031"],
    117889: ["CIC0197"],
    116572: ["CIC0124"],
    117897: ["CIC0198"],
    117901: ["CIC0199"],
    116653: ["CIC0135"],
    117935: ["CIC0202"],
    117943: ["CIC0203"],
    117960: ["CIC0205"],
    117927: ["CIC0201"],
    117919: ["CIC0200"],
    116912: ["CIC0249"],
    116921: ["CIC0250"],
    111813: ["ENE0320"],
    111821: ["ENE0291"],
    113018: ["MAT0022"],
    113301: ["MAT0048"],
    113913: ["CIC0007"],
    115011: ["EST0019"],
    115444: ["EST0061"],
    115924: ["EST0069"],
    115932: ["EST0070"],
    116068: ["CIC0030"],
    116351: ["CIC0094"],
    116424: ["CIC0103"],
    116785: ["CIC0151"],
    117251: ["CIC0177"],
    117358: ["MAT0119"],
    118061: ["IFD0183"],
    118079: ["IFD0185"],
    118192: ["IFD0213"],
    118206: ["IFD0217"],
    118214: ["IFD0177"],
    118222: ["IFD0224"],
    118231: ["IFD0227"],
    118338: ["IFD0254", "IFD0394"],
    121614: ["CIC0206"],
    121771: ["CIC0225"],
    142930: ["LET0252"],
    147389: ["LIP0153"],
    147397: ["ILD0074"],
    167037: ["ENE0177"],
    167720: ["ENE0243"],
    167983: ["ENE0277"],
    200107: ["MAT0137"],
    200271: ["MAT0374"],
    201600: ["CIC0234"]
}
def transforma_colunas(student: pd.DataFrame, codigos: list):

    for codigo_antigo in codigos:
        novos_codigos = DISCIPLINAS[int(codigo_antigo)]

        for novo_codigo in novos_codigos:
            if novo_codigo in student.columns.tolist():
                student = student.rename(columns={novo_codigo: codigo_antigo})

    return student