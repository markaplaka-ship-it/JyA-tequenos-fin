import streamlit as st
import pandas as pd
from datetime import date
import os

FILE = "data.csv"

st.set_page_config(page_title="Tequeños Business", layout="wide")

# 🎨 DESIGN ULTRA PRO
st.markdown("""
<style>

body {
    background: linear-gradient(180deg, #020617, #0F172A);
    color: #E2E8F0;
}

/* HEADER */
h1 {
    text-align: center;
    font-size: 2.5em;
    background: linear-gradient(90deg, #22c55e, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* CARDS */
.card {
    background: #1E293B;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.3);
}

/* VALUE */
.value {
    font-size: 28px;
    font-weight: bold;
}

/* COLORS */
.green { color: #22c55e; }
.red { color: #ef4444; }
.blue { color: #3b82f6; }

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #22c55e, #15803d);
    color: white;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
    border: none;
}

/* TABLE */
[data-testid="stDataFrame"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<h1>🌮 Jeovanny Tequeños Dashboard</h1>", unsafe_allow_html=True)
st.caption("📊 Gestión financiera profesional")

PRICES = {"Tequeños": 4, "Pasteles": 5}

# LOAD
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["tipo","producto","cantidad","precio_unitario","monto","fecha"])

df = df.dropna(how="all")

# ➕ FORMULAIRE
st.subheader("➕ Nueva transacción")

colA, colB = st.columns(2)

tipo = colA.selectbox("Tipo", ["Venta", "Gasto"])

if tipo == "Venta":
    producto = colA.selectbox("Producto", ["Tequeños", "Pasteles"])
    cantidad = colB.number_input("Cantidad", min_value=1)

    precio = PRICES[producto]
    monto = cantidad * precio

    st.success(f"💰 Ingreso: ${monto}")

else:
    producto = colA.text_input("Material")
    cantidad = colB.number_input("Cantidad", min_value=1)
    precio = colB.number_input("Precio", min_value=0.0)

    monto = cantidad * precio

    st.warning(f"💸 Gasto: ${monto}")

fecha = st.date_input("Fecha", value=date.today())

if st.button("Guardar"):
    new = pd.DataFrame([{
        "tipo": tipo,
        "producto": producto,
        "cantidad": cantidad,
        "precio_unitario": precio,
        "monto": monto,
        "fecha": fecha
    }])

    df = pd.concat([df, new], ignore_index=True)
    df.to_csv(FILE, index=False)

    st.success("✅ Guardado")

# ✅ DASHBOARD
if len(df) > 0:

    ingresos = df[df["tipo"] == "Venta"]["monto"].sum()
    gastos = df[df["tipo"] == "Gasto"]["monto"].sum()
    beneficio = ingresos - gastos

    st.subheader("📊 Resumen")

    c1, c2, c3 = st.columns(3)

    c1.markdown(f"""
    <div class="card">
        <div class="blue">💰 Ingresos</div>
        <div class="value">${ingresos:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
    <div class="card">
        <div class="red">💸 Gastos</div>
        <div class="value">${gastos:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
    <div class="card">
        <div class="green">✅ Beneficio</div>
        <div class="value">${beneficio:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    # 📈 GRAPH
    st.subheader("📈 Evolución")

    try:
        df_copy = df.copy()
        df_copy["fecha"] = pd.to_datetime(df_copy["fecha"])

        daily = df_copy.groupby(["fecha","tipo"])["monto"].sum().unstack(fill_value=0)

        if "Venta" not in daily:
            daily["Venta"] = 0
        if "Gasto" not in daily:
            daily["Gasto"] = 0

        daily["Beneficio"] = daily["Venta"] - daily["Gasto"]

        daily = daily.rename(columns={"Venta":"Ingresos", "Gasto":"Gastos"})

        st.line_chart(daily)

    except Exception as e:
        st.error(e)

    # HISTORIAL
    st.subheader("📋 Historial")
    st.dataframe(df)

else:
    st.info("📭 Sin datos todavía")

# RESET
if st.button("🗑️ Reset"):
    if os.path.exists(FILE):
        os.remove(FILE)
    st.success("✅ Datos eliminados")
