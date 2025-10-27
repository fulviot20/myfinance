import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 📁 File CSV per salvare i dati
FILE = "storico_finanze.csv"

# 📊 Categorie predefinite
CATEGORIE = [
    "Alimentari", "Trasporti", "Casa", "Tempo libero",
    "Abbigliamento", "Salute", "Istruzione", "Lavoro", "Viaggi", "Altro"
]

# 🧾 Layout mobile-friendly
st.set_page_config(page_title="MyFinance", layout="centered")

st.title("💸 MyFinance - Gestione Entrate e Uscite")

# 📥 Inserimento dati
st.subheader("📌 Inserisci una nuova voce")

col1, col2 = st.columns(2)
with col1:
    data = st.date_input("Data", value=datetime.today())
with col2:
    tipo = st.selectbox("Tipo", ["Uscita", "Entrata"])

categoria = st.selectbox("Categoria", CATEGORIE)
descrizione = st.text_input("Descrizione")
importo = st.number_input("Importo (€)", min_value=0.0, step=0.5)

if st.button("Aggiungi"):
    nuova_voce = pd.DataFrame([{
        "Data": data.strftime("%Y-%m-%d"),
        "Tipo": tipo,
        "Categoria": categoria,
        "Descrizione": descrizione,
        "Importo": importo
    }])
    if os.path.exists(FILE):
        esistente = pd.read_csv(FILE)
        df = pd.concat([esistente, nuova_voce], ignore_index=True)
    else:
        df = nuova_voce
    df.to_csv(FILE, index=False)
    st.success("✅ Voce aggiunta correttamente!")

# 📊 Report
st.subheader("📅 Report Finanziario")

if os.path.exists(FILE):
    df = pd.read_csv(FILE)
    df["Data"] = pd.to_datetime(df["Data"])
    df["Mese"] = df["Data"].dt.to_period("M")
    df["Anno"] = df["Data"].dt.year

    mese_corrente = datetime.today().strftime("%Y-%m")
    anno_corrente = datetime.today().year

    # 🔍 Filtri
    filtro = st.radio("Visualizza report per:", ["Mese corrente", "Anno corrente"])
    if filtro == "Mese corrente":
        df_filtrato = df[df["Mese"] == mese_corrente]
    else:
        df_filtrato = df[df["Anno"] == anno_corrente]

    # 📈 Bilancio
    entrate = df_filtrato[df_filtrato["Tipo"] == "Entrata"]["Importo"].sum()
    uscite = df_filtrato[df_filtrato["Tipo"] == "Uscita"]["Importo"].sum()
    bilancio = entrate - uscite

    st.metric("Entrate totali", f"€{entrate:.2f}")
    st.metric("Uscite totali", f"€{uscite:.2f}")
    st.metric("Bilancio netto", f"€{bilancio:.2f}")

    # 📊 Grafico per categoria
    spese_per_categoria = df_filtrato[df_filtrato["Tipo"] == "Uscita"].groupby("Categoria")["Importo"].sum()
    if not spese_per_categoria.empty:
        st.bar_chart(spese_per_categoria)

    # 📥 Download del report filtrato
    st.download_button(
        label="📁 Scarica report CSV",
        data=df_filtrato.to_csv(index=False).encode("utf-8"),
        file_name=f"report_{filtro.replace(' ', '_')}.csv",
        mime="text/csv"
    )
else:
    st.info("ℹ️ Nessun dato disponibile. Inserisci una voce per iniziare.")


