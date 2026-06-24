import streamlit as st
import pandas as pd
import os
from datetime import date

FILE = "data.csv"

st.set_page_config(page_title="Finanzas Tequeños", layout="centered")

st.title("📊 Finanzas - Jeovanny Tequeños")

# Charger données
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["tipo", "producto", "monto", "descripcion", "fecha"])

# ➕ FORMULAIRE
st.subheader("➕ Nueva transacción")

tipo = st.selectbox("Tipo", ["Venta", "Gasto"])

# ✅ NOUVEAU : PRODUIT
producto = "N/A"
if tipo == "Venta":
    producto = st.selectbox("Producto", ["Tequeños", "Pasteles"])

monto = st.number_input("Monto ($)", min_value=0.0)
descripcion = st.text_input("Descripción")
fecha = st.date_input("Fecha", value=date.today())

if st.button("Agregar"):
    nueva = pd.DataFrame([{
        "tipo": tipo,
        "producto": producto,
        "monto": monto,
        "descripcion": descripcion,
        "fecha": fecha
    }])

    df = pd.concat([df, nueva], ignore_index=True)
    df.to_csv(FILE, index=False)

    st.success("✅ Transacción guardada")

# 📋 HISTORIAL
if not df.empty:

    st.subheader("📋 Historial")
    st.dataframe(df)

    ingresos = df[df["tipo"] == "Venta"]["monto"].sum()
    gastos = df[df["tipo"] == "Gasto"]["monto"].sum()
    beneficio = ingresos - gastos

    st.subheader("📊 Resumen")

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Ingresos", f"${ingresos:.2f}")
    col2.metric("💸 Gastos", f"${gastos:.2f}")
    col3.metric("✅ Beneficio", f"${beneficio:.2f}")

    # ✅ CA DÉTAIL PAR PRODUIT
    st.subheader("📈 Ventas por producto")

    ventas_producto = df[df["tipo"] == "Venta"].groupby("producto")["monto"].sum()

    st.bar_chart(ventas_producto)

# 🧹 RESET
if st.button("⚠️ Borrar todo"):
    df = pd.DataFrame(columns=["tipo","producto","monto","descripcion","fecha"])
    df.to_csv(FILE, index=False)
    st.warning("Datos eliminados")
