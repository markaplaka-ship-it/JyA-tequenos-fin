import streamlit as st
import pandas as pd
from datetime import date
import os

FILE = "data.csv"

st.set_page_config(page_title="J&A Tequeños", layout="wide")

# 🎨 DESIGN PREMIUM + ANIMATIONS
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #020617, #0F172A);
    color: #E2E8F0;
}

/* LOGO */
.logo {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom:10px;
}

/* BANNER */
.banner {
    height: 200px;
    background-image: url('https://domesticfits.com/wp-content/uploads/2023/06/venezuelan-food-Tequenos.jpg');
    background-size: cover;
    background-position: center;
    border-radius: 15px;
    margin-bottom: 20px;
}

/* CARDS */
.card {
    background: #1E293B;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.3);
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.05);
    box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
}

/* VALUES */
.value {
    font-size: 30px;
    font-weight: bold;
    color: white;
}

/* COLORS */
.green { color: #22c55e; }
.red { color: #ef4444; }
.blue { color: #3b82f6; }

/* SECTION */
.section {
    background:#1E293B;
    padding:20px;
    border-radius:15px;
    margin-bottom:20px;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#22c55e,#15803d);
    color:white;
    border-radius:12px;
    height:45px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ✅ LOGO
st.markdown("<div class='logo'>J&amp;A Tequeños</div>", unsafe_allow_html=True)
st.caption("🔥 Gestión financiera profesional")

# ✅ BANNER
st.markdown("<div class='banner'></div>", unsafe_allow_html=True)

PRICES = {"Tequeños": 4, "Pasteles": 5}

# LOAD DATA
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["tipo","producto","cantidad","precio_unitario","monto","fecha"])

df = df.dropna(how="all")

# ➕ FORM
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("➕ Nueva transacción")

col1, col2 = st.columns(2)

tipo = col1.selectbox("Tipo", ["Venta", "Gasto"])

if tipo == "Venta":
    producto = col1.selectbox("Producto", ["Tequeños", "Pasteles"])
    cantidad = col2.number_input("Cantidad", min_value=1)

    precio = PRICES[producto]
    monto = cantidad * precio

    st.success(f"💰 Ingreso: ${monto}")

else:
    producto = col1.text_input("Material")
    cantidad = col2.number_input("Cantidad", min_value=1)
    precio = col2.number_input("Precio", min_value=0.0)

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

st.markdown("</div>", unsafe_allow_html=True)

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

    # 📋 HISTORIAL + DELETE
    st.subheader("📋 Historial")

    st.dataframe(df, use_container_width=True)

    st.subheader("🗑️ Eliminar una entrada")

    index_to_delete = st.number_input(
        "Número de fila a eliminar",
        min_value=0,
        max_value=len(df)-1,
        step=1
    )

    if st.button("Eliminar"):
        df = df.drop(index=index_to_delete)
        df.to_csv(FILE, index=False)
        st.success("✅ Entrada eliminada")

else:
    st.info("📭 Sin datos todavía")

# RESET TOTAL
if st.button("🗑️ Reset total"):
    if os.path.exists(FILE):
        os.remove(FILE)
    st.success("✅ Datos eliminados")
