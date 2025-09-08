import pandas as pd

def comparar_planilhas(arquivo_a, arquivo_b):
    # Carregar planilhas (aceita .xlsx ou .csv)
    df_a = pd.read_excel(arquivo_a)
    df_b = pd.read_excel(arquivo_b)

    # Padronizar colunas principais
    df_a['NOME'] = df_a['NOME'].str.strip().str.upper()
    df_b['NOME'] = df_b['NOME'].str.strip().str.upper()

    # Encontrar diferenças
    apenas_a = df_a[~df_a['NOME'].isin(df_b['NOME'])]
    apenas_b = df_b[~df_b['NOME'].isin(df_a['NOME'])]
    duplicados_a = df_a[df_a.duplicated('NOME', keep=False)]
    duplicados_b = df_b[df_b.duplicated('NOME', keep=False)]

    return {
        "apenas_a": apenas_a.to_dict(orient="records"),
        "apenas_b": apenas_b.to_dict(orient="records"),
        "duplicados_a": duplicados_a.to_dict(orient="records"),
        "duplicados_b": duplicados_b.to_dict(orient="records"),
    }
