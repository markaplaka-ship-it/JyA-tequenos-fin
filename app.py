import streamlit as st
import pandas as pd
import os
from datetime import date

FILE = "data.csv"

st.set_page_config(page_title="Jeovanny Tequeños", layout="centered")

# 🎨 DESIGN PREMIUM
st.markdown("""
<style>
html, body, [class*="css"] {
    background: linear-gradient(180deg, #020617, #0F172A);
    color: #E2E8F0;
}

.block-container {
    padding-top: 2rem;
}

h1 {
    text-align: center;
    font-size: 2.2em;
    background: linear-gradient(90deg, #22c55e, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.card {
    background: #1E293B;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    text-align: center;
}

.value {
    font-size: 24px;
    font-weight: bold;
}

.green { color: #22c55e; }
.red { color: #ef4444; }
.blue { color: #3b82f6; }

.stButton>button {
    background: linear-gradient(90deg, #22c55e, #15803d);
    color: white;
    border-radius: 12px;
    height: 48px;
    font-size: 16px;
    font-weight: bold;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<h1>🌮 Jeovanny Tequeños Dashboard</h1>", unsafe_allow_html=True)
st.caption("📊 Control financiero simple y profesional")

# 💰 PRIX & COÛTS
PRICES = {
    "Tequeños": 4,
    "Pasteles": 5
}

COSTS = {
    "Tequeños": 2,
    "Pasteles": 3
}

# 📂 CHARGEMENT DATA
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["tipo","producto","cantidad","precio_unitario","monto","costo","beneficio","fecha"])

# ➕ FORMULAIRE
st.subheader("➕ Nueva transacción")

tipo = st.selectbox("Tipo", ["Venta", "Gasto"])

producto = "N/A"
cantidad = 0
precio_unitario = 0
monto = 0
costo = 0
beneficio = 0

if tipo == "Venta":
    producto = st.selectbox("Producto", ["Tequeños", "Pasteles"])
    cantidad = st.number_input("Cantidad vendida", min_value=1, step=1)

    precio_unitario = PRICES[producto]
    costo_unitario = COSTS[producto]

    monto = cantidad * precio_unitario
    costo = cantidad * costo_unitario
    beneficio = monto - costo

    st.info(f"💵 Total: ${monto}")
    st.info(f"💸 Costo: ${costo}")
    st.success(f"✅ Ganancia: ${beneficio}")

else:
    monto = st.number_input("Monto gasto ($)", min_value=0.0)

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

# 📊 AFFICHAGE
if not df.empty:
    st.subheader("📋 Historial")
    st.dataframe(df)

    ingresos = df[df["tipo"] == "Venta"]["monto"].sum()
    gastos = df[df["tipo"] == "Gasto"]["monto"].sum()
    beneficio_total = df["beneficio"].sum()

    st.subheader("📊 Resumen")

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="card">
        <div class="blue">💰 Ingresos</div>
        <div class="value">${ingresos:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="card">
        <div class="red">💸 Gastos</div>
        <div class="value">${gastos:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="card">
        <div class="green">✅ Beneficio</div>
        <div class="value">${beneficio_total:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    # 📈 GRAPH
    st.subheader("📈 Ventas por producto")
    ventas_producto = df[df["tipo"] == "Venta"].groupby("producto")["monto"].sum()
    st.bar_chart(ventas_producto)

# RESET
if st.button("⚠️ Borrar todo"):
    df = pd.DataFrame(columns=df.columns)
    df.to_csv(FILE, index=False)
    st.warning("Datos eliminados")


Internal Use Only - Only for Proximus business use. See more on https://www.proximus.com/confidentiality
