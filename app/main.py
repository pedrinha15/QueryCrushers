import streamlit as st
import openai
import pandas as pd
import plotly.express as px
import psycopg2
from io import BytesIO

# Configurar Azure OpenAI
openai.api_type = "azure"
openai.api_base = st.secrets["AZURE_OPENAI_ENDPOINT"]
openai.api_version = st.secrets["AZURE_OPENAI_API_VERSION"]
openai.api_key = st.secrets["AZURE_OPENAI_KEY"]

def gerar_sql(prompt_usuario):
    resposta = openai.ChatCompletion.create(
        engine=st.secrets["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "Converte perguntas em linguagem natural para SQL PostgreSQL."},
            {"role": "user", "content": prompt_usuario}
        ]
    )
    return resposta["choices"][0]["message"]["content"].strip()

def executar_query(sql):
    conn = psycopg2.connect(
        host=st.secrets["DB_HOST"],
        dbname=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"]
    )
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

def recomendar_grafico(df):
    colunas = df.columns
    if df.shape[0] == 1 and df.shape[1] == 1:
        return "kpi"
    elif len(colunas) == 2:
        if pd.api.types.is_numeric_dtype(df[colunas[1]]):
            if pd.api.types.is_datetime64_any_dtype(df[colunas[0]]):
                return "linha"
            elif df[colunas[0]].nunique() < 20:
                return "barra"
        elif pd.api.types.is_numeric_dtype(df[colunas[0]]) and pd.api.types.is_numeric_dtype(df[colunas[1]]):
            return "scatter"
    return "tabela"

def mostrar_visualizacao(df):
    tipo = recomendar_grafico(df)
    st.subheader("Visualização sugerida")
    if tipo == "kpi":
        st.metric(label=df.columns[0], value=df.iloc[0, 0])
    elif tipo == "barra":
        st.plotly_chart(px.bar(df, x=df.columns[0], y=df.columns[1]))
    elif tipo == "linha":
        st.plotly_chart(px.line(df, x=df.columns[0], y=df.columns[1]))
    elif tipo == "scatter":
        st.plotly_chart(px.scatter(df, x=df.columns[0], y=df.columns[1]))
    else:
        st.dataframe(df)

def aplicar_filtros(df):
    st.sidebar.subheader("Filtros")
    for coluna in df.columns:
        if df[coluna].dtype == 'object' or df[coluna].nunique() < 20:
            valores = st.sidebar.multiselect(f"{coluna}", df[coluna].unique(), default=df[coluna].unique())
            df = df[df[coluna].isin(valores)]
    return df

def exportar_dados(df):
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    st.download_button(
        label="📥 Exportar para Excel",
        data=buffer.getvalue(),
        file_name="dados_exportados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- Streamlit UI ---
st.set_page_config(page_title="LLM SQL Dashboard", layout="wide")
st.title("🔍 Consultas Inteligentes com LLM + PostgreSQL")

prompt = st.text_input("Escreve a tua pergunta sobre os dados:")

if prompt:
    with st.spinner("A gerar SQL..."):
        sql_query = gerar_sql(prompt)
        st.code(sql_query, language="sql")

    if st.button("Executar consulta"):
        try:
            df = executar_query(sql_query)
            if df.empty:
                st.warning("A consulta não retornou resultados.")
            else:
                df_filtrado = aplicar_filtros(df)
                mostrar_visualizacao(df_filtrado)
                exportar_dados(df_filtrado)
        except Exception as e:
            st.error(f"Erro ao executar query: {e}")
