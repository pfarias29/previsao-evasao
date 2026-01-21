import pandas as pd


mencao_map = {
    'SR': 0.0,
    'II': 1.0,
    'MI': 2.0,
    'MM': 3.0,
    'MS': 4.0,
    'SS': 5.0,
    'TR': 0.0, # trancamento r. (SR 0.0)
    'CC': 3.0, # credito concedido (3.0 MM)
    'AP': 3.0, # aproveitamento (3.0 MM)
    'DP': 3.0, # dispensado (3.0 MM)
    'TJ': 0.0, # trancamento justificado (SR 0.0)
    'Não cursado': -1.0,
}

def transform_df(df: pd.DataFrame):
    df_transformed = pd.pivot_table(data=df, index='matricula', columns="codigo", values='nota', aggfunc="max", fill_value="Não cursado").reset_index()


    colunas_materias = df_transformed.columns.difference(["matricula"])
    df_transformed[colunas_materias] = df_transformed[colunas_materias].replace(mencao_map)

    return df_transformed.drop(columns=['matricula'])