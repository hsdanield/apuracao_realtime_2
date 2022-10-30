import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import itertools
import altair as alt

urls = {
    "presidente": "https://resultados.tse.jus.br/oficial/ele2022/545/dados-simplificados/br/br-c0001-e000545-r.json",
    "sp": "https://resultados.tse.jus.br/oficial/ele2022/547/dados-simplificados/sp/sp-c0003-e000547-r.json",
}


def getUrlTSE(url):
    return json.loads(requests.get(url).text)


dados_tse_presidente = getUrlTSE(urls["presidente"])
dados_geral_presidente = dict(itertools.islice(dados_tse_presidente.items(), 64))
dados_presidente = dados_tse_presidente["cand"]

dados_sp = getUrlTSE(urls["sp"])
dados_geral_sp = dict(itertools.islice(dados_sp.items(), 64))
dados_governador = dados_sp["cand"]


st.header("Totalização de Votos Para Presidente 2º Turno")
st.write("Porcentagem de  Totalizadas: ", dados_geral_presidente["pst"])
st.write("Última atualização: ", dados_geral_presidente["ht"])
st.write("Total de Votos Válidos: ", dados_geral_presidente["tv"])

rename_columns = {
    "nm": "Nome",
    "n": "Numero",
    "nv": "Vice",
    "e": "Eleito",
    "pvap": "Porcentagem",
    "vap": "Votos",
}

df = pd.DataFrame(dados_presidente, columns=["nm", "n", "pvap", "vap"]).rename(
    columns=rename_columns
)

df_sp = pd.DataFrame(dados_governador, columns=["nm", "n", "pvap", "vap"]).rename(
    columns=rename_columns
)
df["Porcentagem"] = df["Porcentagem"].apply(lambda x: x.replace(",", ".")).astype(float)
df_sp["Porcentagem"] = df_sp["Porcentagem"].apply(lambda x: x.replace(",", ".")).astype(float)

st.sidebar.header("Opções")
df_checkbox = st.sidebar.checkbox("Mostrar Tabela Dados Presidente")

st.sidebar.text("Totalização Governador")
df_checkbox_sp = st.sidebar.checkbox("SP")

chart_presidente = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("Nome:N", title="Nome", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Porcentagem", title="Porcentagem (%)"),
        color= alt.Color("Nome:N", scale=alt.Scale(scheme="category10")),
        tooltip= ["Nome:N", "Porcentagem:Q"]
    ).properties(width=800, height=600)
)

chart_governador = (
    alt.Chart(df_sp)
    .mark_bar()
    .encode(
        x=alt.X("Nome:N", title="Nome", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Porcentagem:Q", title="Porcentagem (%)"),
        color= alt.Color("Nome:N", scale=alt.Scale(scheme="category10")),
        tooltip= ["Nome:O", "Porcentagem:Q"]
    ).properties(width=800, height=600)
)

st.altair_chart(chart_presidente, use_container_width=True)

if df_checkbox:
    st.table(df)

if df_checkbox_sp:
    st.header("SP: Totalização de Votos Para Governador")
    st.write("Porcentagem de  Totalizadas: ", dados_geral_sp["pst"])
    st.write("Última atualização: ", dados_geral_sp["ht"])
    st.write("Total de Votos Válidos: ", dados_geral_sp["tv"])
    st.altair_chart(chart_governador, use_container_width=True)
    st.table(df_sp)
    


