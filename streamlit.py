import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparador de Planilhas", layout="wide")
st.title("📊 Comparador de Planilhas")

st.write("Envie duas planilhas (Excel ou CSV) para comparar nomes. O app mostrará divergências, duplicados e nomes presentes em ambas.")

# Botão Novo (reseta uploads)
if st.button("🔄 Novo"):
    st.experimental_rerun()

# Upload das planilhas
file_a = st.file_uploader("📂 Enviar Planilha A", type=["xlsx", "csv"], key="a")
file_b = st.file_uploader("📂 Enviar Planilha B", type=["xlsx", "csv"], key="b")

if file_a and file_b:
    try:
        # Ler arquivos
        df_a = pd.read_csv(file_a, dtype=str) if file_a.name.endswith(".csv") else pd.read_excel(file_a, dtype=str)
        df_b = pd.read_csv(file_b, dtype=str) if file_b.name.endswith(".csv") else pd.read_excel(file_b, dtype=str)
    except Exception as e:
        st.error(f"Erro ao ler os arquivos: {e}")
        st.stop()

    st.success("Planilhas carregadas com sucesso ✅")

    # Seleção de colunas de nomes
    col_a = st.selectbox("Selecione a coluna de NOME da Planilha A:", df_a.columns)
    col_b = st.selectbox("Selecione a coluna de NOME da Planilha B:", df_b.columns)

    # Normalizar nomes
    df_a[col_a] = df_a[col_a].str.strip().str.upper()
    df_b[col_b] = df_b[col_b].str.strip().str.upper()

    # Comparações
    apenas_a = df_a[~df_a[col_a].isin(df_b[col_b])]
    apenas_b = df_b[~df_b[col_b].isin(df_a[col_a])]
    duplicados_a = df_a[df_a.duplicated(col_a, keep=False)]
    duplicados_b = df_b[df_b.duplicated(col_b, keep=False)]
    presentes_em_ambas = df_a[df_a[col_a].isin(df_b[col_b])]

    st.subheader("🔍 Resultados da Comparação")
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Só na A", "Só na B", "Duplicados A", "Duplicados B", "Presentes em ambas"
    ])

    with tab1:
        st.write("Nomes que estão **somente na Planilha A**:")
        st.dataframe(apenas_a)

    with tab2:
        st.write("Nomes que estão **somente na Planilha B**:")
        st.dataframe(apenas_b)

    with tab3:
        st.write("Nomes **duplicados na Planilha A**:")
        st.dataframe(duplicados_a)

    with tab4:
        st.write("Nomes **duplicados na Planilha B**:")
        st.dataframe(duplicados_b)

    with tab5:
        st.write("Nomes presentes em **ambas as planilhas**:")
        st.dataframe(presentes_em_ambas)

    # Botão para baixar resultados
    with pd.ExcelWriter("resultado_comparacao.xlsx", engine="xlsxwriter") as writer:
        apenas_a.to_excel(writer, sheet_name="Só na A", index=False)
        apenas_b.to_excel(writer, sheet_name="Só na B", index=False)
        duplicados_a.to_excel(writer, sheet_name="Duplicados A", index=False)
        duplicados_b.to_excel(writer, sheet_name="Duplicados B", index=False)
        presentes_em_ambas.to_excel(writer, sheet_name="Presentes em ambas", index=False)

    with open("resultado_comparacao.xlsx", "rb") as f:
        st.download_button("📥 Baixar Resultado em Excel", f, file_name="resultado_comparacao.xlsx")
