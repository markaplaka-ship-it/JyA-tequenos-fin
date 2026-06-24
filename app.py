import streamlit as st
import pandas as pd
from datetime import date
import os

FILE = "data.csv"

st.set_page_config(page_title="Tequeños Business", layout="centered")

# 🎨 UI
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

# ➕ FORM
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("➕ Nueva transacción")

tipo = st.selectbox("Tipo", ["Venta", "Gasto"])

producto = ""
cantidad = 0
precio = 0.0
monto = 0.0
costo = 0.0
beneficio = 0.0

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

elif tipo == "Gasto":
    producto = st.text_input("Material / Producto")
    cantidad = st.number_input("Cantidad", min_value=1)
    precio = st.number_input("Precio unitario ($)", min_value=0.0)

    monto = cantidad * precio
    costo = monto
    beneficio = -monto

    st.warning(f"💸 Gasto total: ${monto}")

fecha = st.date_input("Fecha", value=date.today())

# SAVE
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

# ✅ DISPLAY ONLY IF DATA
if len(df) > 0:

    # 📊 RESUMEN
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📊 Resumen")

    ingresos = df[df["tipo"] == "Venta"]["monto"].sum()
    gastos = df["costo"].sum()
    beneficio_total = ingresos - gastos

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Ingresos", f"${ingresos:.2f}")
    col2.metric("💸 Gastos", f"${gastos:.2f}")
    col3.metric("✅ Beneficio", f"${beneficio_total:.2f}")

    st.markdown("</div>", unsafe_allow_html=True)

    # 📈 GRAPH FIXED
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📈 Evolución diaria")

    try:
        df_copy = df.copy()

        df_copy["fecha"] = pd.to_datetime(df_copy["fecha"], errors="coerce")
        df_copy = df_copy.dropna(subset=["fecha"])

        if not df_copy.empty:
            daily = df_copy.groupby("fecha").agg({
                "monto": "sum",
                "costo": "sum",
                "beneficio": "sum"
            }).reset_index()

            daily = daily.set_index("fecha")
            daily.columns = ["Ingresos", "Gastos", "Beneficio"]

            st.line_chart(daily)
            st.caption("🟢 Ingresos | 🔴 Gastos | 🔵 Beneficio")

        else:
            st.info("No hay datos suficientes para graficar")

    except:
        st.warning("⚠️ No se puede generar el gráfico todavía")

    st.markdown("</div>", unsafe_allow_html=True)

    # 📋 HISTORIAL
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📋 Historial")
    st.dataframe(df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 📥 EXPORT
    csv = df.to_csv(index=False).encode("utf-8")
