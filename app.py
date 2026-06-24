import streamlit as st
import pandas as pd
import os
from datetime import date

FILE = "data.csv"

st.set_page_config(page_title="Jeovanny Tequeños", layout="centered")

# 🎨 DESIGN CORRIGÉ (lisible)
st.markdown("""
<style>
html, body {
    background-color: #0F172A;
    color: #FFFFFF;
}

/* TITRE */
h1 {
    text-align: center;
    color: #22c55e;
}

/* CARTES */
.card {
    background: #1E293B;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    color: white;
}

/* TABLE */
[data-testid="stDataFrame"] {
    color: white;
}

/* BOUTON */
.stButton>button {
    background: #22c55e;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<h1>🌮 Jeovanny Tequeños</h1>", unsafe_allow_html=True)

# PRICES
PRICES = {"Tequeños": 4, "Pasteles": 5}
COSTS = {"Tequeños": 2, "Pasteles": 3}

# LOAD DATA
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=[
        "tipo","producto","cantidad","precio_unitario",
        "monto","costo","beneficio","fecha"
    ])

# ✅ IMPORTANT : éviter ligne vide
df = df.dropna(how="all")

# FORM
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

    st.info(f"💰 Ingreso: ${monto}")
    st.warning(f"💸 Costo: ${costo}")
    st.success(f"✅ Ganancia: ${beneficio}")

elif tipo == "Gasto":
    producto = st.text_input("Material / Producto")
    cantidad = st.number_input("Cantidad", min_value=1)
    precio_unitario = st.number_input("Precio unitario ($)", min_value=0.0)

    monto = cantidad * precio_unitario
    costo = monto
    beneficio = -monto

    st.warning(f"💸 Gasto total: ${monto}")

fecha = st.date_input("Fecha", value=date.today())

# SAVE
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

# DISPLAY uniquement si DATA EXISTE
if not df.empty:

    st.subheader("📋 Historial")
    st.dataframe(df, use_container_width=True)

    # CALCULS CORRECTS
    ingresos = df[df["tipo"] == "Venta"]["monto"].sum()
    gastos = df["costo"].sum()
    beneficio_total = ingresos - gastos

    st.subheader("📊 Resumen")

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="card">
    💰 Ingresos<br><b>${ingresos:.2f}</b>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="card">
    💸 Gastos<br><b>${gastos:.2f}</b>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="card">
    ✅ Beneficio<br><b>${beneficio_total:.2f}</b>
    </div>
    """, unsafe_allow_html=True)

# RESET
if st.button("⚠️ Borrar todo"):
    df = pd.DataFrame(columns=df.columns)
    df.to_csv(FILE, index=False)
    st.warning("Datos eliminados")
