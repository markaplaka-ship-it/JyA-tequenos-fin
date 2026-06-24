import streamlit as st
import pandas as pd
import os
from datetime import date

FILE = "data.csv"

st.set_page_config(page_title="Jeovanny Tequeños", layout="centered")

# 🎨 DESIGN PREMIUM (lisible)
st.markdown("""
<style>
html, body {
    background-color: #0F172A;
    color: #E2E8F0;
}

h1 {
    text-align: center;
    color: #22c55e;
}

.card {
    background: #1E293B;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

/* Tableau lisible */
[data-testid="stDataFrame"] {
    background-color: #1E293B !important;
}

.stButton>button {
    background: #22c55e;
    color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# 🧾 TITRE
st.markdown("<h1>🌮 Jeovanny Tequeños</h1>", unsafe_allow_html=True)

# 💰 PRIX & COUTS
PRICES = {"Tequeños": 4, "Pasteles": 5}
COSTS = {"Tequeños": 2, "Pasteles": 3}

# 📂 LOAD
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=[
        "tipo","producto","cantidad","precio_unitario",
        "monto","costo","beneficio","fecha"
    ])

# ➕ FORM
st.subheader("➕ Nueva transacción")

tipo = st.selectbox("Tipo", ["Venta", "Gasto"])

producto = ""
cantidad = 0
precio_unitario = 0
monto = 0
costo = 0
beneficio = 0

if tipo == "Venta":
    producto = st.selectbox("Producto", ["Tequeños", "Pasteles"])
    cantidad = st.number_input("Cantidad", min_value=1)

    precio_unitario = PRICES[producto]
    costo_unitario = COSTS[producto]

    monto = cantidad * precio_unitario
    costo = cantidad * costo_unitario
    beneficio = monto - costo

    st.info(f"💵 Ingreso: ${monto}")
    st.info(f"💸 Costo producción: ${costo}")
    st.success(f"✅ Ganancia: ${beneficio}")

elif tipo == "Gasto":
    producto = st.text_input("Artículo / Material")
    cantidad = st.number_input("Cantidad", min_value=1)
    precio_unitario = st.number_input("Precio unitario ($)", min_value=0.0)

    monto = cantidad * precio_unitario
    costo = monto  # gasto ajouté aux coûts
    beneficio = -monto

    st.warning(f"💸 Gasto total: ${monto}")

fecha = st.date_input("Fecha", value=date.today())

# 💾 SAVE
if st.button("Agregar"):
    nueva = pd.DataFrame([{
        "tipo": tipo,
        "producto": producto,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "monto": monto,
        "costo": costo,
        "beneficio": beneficio,
        "fecha": fecha
    }])

    df = pd.concat([df, nueva], ignore_index=True)
    df.to_csv(FILE, index=False)

    st.success("✅ Guardado")

# 📊 DISPLAY
if not df.empty:

    st.subheader("📋 Historial")

    # ✅ TABLE LISIBLE
    st.dataframe(df, use_container_width=True)

    # ✅ CALCULS CORRECTS
    ingresos = df[df["tipo"] == "Venta"]["monto"].sum()
    gastos_produccion = df["costo"].sum()
    beneficio_total = ingresos - gastos_produccion

    st.subheader("📊 Resumen")

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div class='card'>💰 Ingreso<br><b>${ingresos:.2f}</b></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'>💸 Gastos<br><b>${gastos_produccion:.2f}</b></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card'>✅ Beneficio<br><b>${beneficio_total:.2f}</b></div>", unsafe_allow_html=True)
