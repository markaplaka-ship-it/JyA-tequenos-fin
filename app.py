import streamlit as st
import pandas as pd
from datetime import date
import os

FILE = "data.csv"

st.set_page_config(page_title="Tequeños Business", layout="centered")

# 🎨 UI PRO
st.markdown("""
<style>
body {
    background-color: #0F172A;
    color: white;
}

h1 {
    text-align:center;
    color:#22c55e;
}

.section {
    background:#1E293B;
    padding:15px;
    border-radius:10px;
    margin-bottom:20px;
}

.stButton>button {
    background:#22c55e;
    color:white;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌮 Jeovanny Tequeños</h1>", unsafe_allow_html=True)

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

# CLEAN
df = df.dropna(how="all")
df = df[df["tipo"].notna()]

# ✅ IMPORT DATA (UPLOAD)
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📂 Cargar datos")

uploaded_file = st.file_uploader("Subir archivo CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.to_csv(FILE, index=False)
    st.success("Datos cargados correctamente ✅")
st.markdown("</div>", unsafe_allow_html=True)

# ✅ FORMULAIRE
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("➕ Nueva transacción")

tipo = st.selectbox("Tipo", ["Venta", "Gasto"])

if tipo == "Venta":
    producto = st.selectbox("Producto", ["Tequeños", "Pasteles"])
    cantidad = st.number_input("Cantidad", min_value=1)

    precio = PRICES[producto]
    costo_unit = COSTS[producto]

    monto = cantidad * precio
    costo = cantidad * costo_unit
    beneficio = monto - costo

    st.info(f"Ingreso: ${monto}")
    st.warning(f"Costo: ${costo}")
    st.success(f"Ganancia: ${beneficio}")

else:
    producto = st.text_input("Material")
    cantidad = st.number_input("Cantidad", min_value=1)
    precio = st.number_input("Precio unitario", min_value=0.0)

    monto = cantidad * precio
    costo = monto
    beneficio = -monto

    st.warning(f"Gasto: ${monto}")

fecha = st.date_input("Fecha", value=date.today())

if st.button("Guardar"):
    nueva = pd.DataFrame([{
        "tipo": tipo,
        "producto": producto,
        "cantidad": cantidad,
        "precio_unitario": precio,
        "monto": monto,
        "costo": costo,
        "beneficio": beneficio,
        "fecha": fecha
    }])

    df = pd.concat([df, nueva], ignore_index=True)
    df.to_csv(FILE, index=False)

    st.success("Guardado ✅")

st.markdown("</div>", unsafe_allow_html=True)

# ✅ SI DONNÉES
if len(df) > 0:

    # DASHBOARD
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📊 Resumen")

    ingresos = df[df["tipo"] == "Venta"]["monto"].sum()
    gastos = df["costo"].sum()
    beneficio_total = ingresos - gastos

    st.metric("Ingresos", f"${ingresos:.2f}")
    st.metric("Gastos", f"${gastos:.2f}")
    st.metric("Beneficio", f"${beneficio_total:.2f}")

    st.markdown("</div>", unsafe_allow_html=True)

    # GRAPH
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📈 Evolución")

    df["fecha"] = pd.to_datetime(df["fecha"])
    daily = df.groupby("fecha").sum(numeric_only=True)

    chart = pd.DataFrame({
        "Ingresos": daily["monto"],
        "Gastos": daily["costo"],
        "Beneficio": daily["beneficio"]
    })

    st.line_chart(chart)
    st.markdown("</div>", unsafe_allow_html=True)

    # HISTORIAL
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📋 Historial")
    st.dataframe(df)
    st.markdown("</div>", unsafe_allow_html=True)

    # ✅ EXPORT DATA
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Descargar backup",
        csv,
        "backup_tequenos.csv",
        "text/csv"
    )

else:
