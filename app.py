
import streamlit as st
import pandas as pd
import os
from datetime import date

# 📁 fichier de sauvegarde
FILE = "data.csv"

st.set_page_config(page_title="Finanzas Tequeños", layout="centered")

st.title("📊 Finanzas - Jeovanny Tequeños")

# ✅ Charger données existantes
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["tipo", "monto", "descripcion", "fecha"])

# ➕ Formulaire
st.subheader("➕ Nueva transacción")

tipo = st.selectbox("Tipo", ["Venta", "Gasto"])
monto = st.number_input("Monto (€)", min_value=0.0)
descripcion = st.text_input("Descripción")
fecha = st.date_input("Fecha", value=date.today())

if st.button("Agregar"):
    nueva = pd.DataFrame([{
        "tipo": tipo,
        "monto": monto,
        "descripcion": descripcion,
        "fecha": fecha
    }])

    df = pd.concat([df, nueva], ignore_index=True)
    df.to_csv(FILE, index=False)

    st.success("✅ Transacción guardada")

# 📋 Mostrar datos
if not df.empty:

    st.subheader("📋 Historial")
    st.dataframe(df)

    ingresos = df[df["tipo"] == "Venta"]["monto"].sum()
    gastos = df[df["tipo"] == "Gasto"]["monto"].sum()
    beneficio = ingresos - gastos

    st.subheader("📊 Resumen")

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Ingresos", f"{ingresos:.2f} €")
    col2.metric("💸 Gastos", f"{gastos:.2f} €")
    col3.metric("✅ Beneficio", f"{beneficio:.2f} €")

    st.bar_chart({
        "Ingresos": [ingresos],
        "Gastos": [gastos]
    })

# 🧹 bouton reset (optionnel)
if st.button("⚠️ Borrar todo"):
    df = pd.DataFrame(columns=["tipo","monto","descripcion","fecha"])
    df.to_csv(FILE, index=False)
    st.warning("Datos eliminados")
