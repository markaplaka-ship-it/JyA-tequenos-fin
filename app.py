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

# HEADER
st.markdown("<h1>🌮 Jeovanny Tequeños</h1>", unsafe_allow_html=True)
st.caption("📊 Gestión financiera profesional")

# PARAMÈTRES
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

# CLEAN DATA
df = df.dropna(how="all")

# 📂 IMPORT CSV
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📂 Cargar datos")

uploaded_file = st.file_uploader("Subir archivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.to_csv(FILE, index=False)
    st.success("Datos cargados correctamente ✅")

st.markdown("</div>", unsafe_allow_html=True)

# ➕ FORMULAIRE
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("➕ Nueva transacción")

tipo = st.selectbox("Tipo", ["Venta", "Gasto"])

producto = ""
cantidad = 0
precio = 0.0
monto = 0.0
costo = 0.0
beneficio = 0.0

# ✅ VENTAS
if tipo == "Venta":
    producto = st.selectbox("Producto", ["Tequeños", "Pasteles"])
    cantidad = st.number_input("Cantidad", min_value=1)

    precio = PRICES[producto]
    costo_unit = COSTS[producto]

    monto = cantidad * precio
    costo = cantidad * costo_unit
    beneficio = monto - costo

    st.info(f"💰 Ingreso: ${monto}")
    st.warning(f"💸 Costo producción: ${costo}")
    st.success(f"✅ Ganancia: ${beneficio}")

# ✅ GASTOS
elif tipo == "Gasto":
    producto = st.text_input("Material / Producto")
    cantidad = st.number_input("Cantidad", min_value=1)
    precio = st.number_input("Precio unitario ($)", min_value=0.0)

    monto = cantidad * precio
    costo = monto
    beneficio = -monto

    st.warning(f"💸 Gasto total: ${monto}")

fecha = st.date_input("Fecha", value=date.today())

# SAVE DATA
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

    st.success("✅ Guardado correctamente")

st.markdown("</div>", unsafe_allow_html=True)

# ✅ AFFICHAGE UNIQUEMENT SI DATA
if len(df) > 0:

    # 📊 RESUMEN
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📊 Resumen")

    ingresos = df[df["tipo"] == "Venta"]["monto"].sum()
    gastos = df["costo"].sum()
    beneficio_total = ingresos - gastos

    st.metric("💰 Ingresos", f"${ingresos:.2f}")
    st.metric("💸 Gastos", f"${gastos:.2f}")
    st.metric("✅ Beneficio", f"${beneficio_total:.2f}")

    st.markdown("</div>", unsafe_allow_html=True)

    # 📈 GRAPH
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📈 Evolución diaria")

    df["fecha"] = pd.to_datetime(df["fecha"])
    daily = df.groupby("fecha").sum(numeric_only=True)

    chart = pd.DataFrame({
        "Ingresos": daily["monto"],
        "Gastos": daily["costo"],
        "Beneficio": daily["beneficio"]
    })

    st.line_chart(chart)
    st.caption("🟢 Ingresos | 🔴 Gastos | 🔵 Beneficio")

    st.markdown("</div>", unsafe_allow_html=True)

    # 📋 HISTORIAL
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📋 Historial")
    st.dataframe(df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 📥 EXPORT CSV
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Descargar backup",
        csv,
        "backup_tequenos.csv",
        "text/csv"
    )

else:
    st.info("📭 No hay datos todavía - empieza añadiendo tu primera transacción")

# RESET
if st.button("⚠️ Borrar todo"):
    df = pd.DataFrame(columns=df.columns)
    df.to_csv(FILE, index=False)
    st.warning("Datos eliminados")
