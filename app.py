import streamlit as st
import pandas as pd
from datetime import date
import os

FILE = "data.csv"

st.set_page_config(page_title="Tequeños Business", layout="centered")

# 🎨 UI
st.markdown("""
<style>
body {background-color:#0F172A; color:white;}
h1 {text-align:center; color:#22c55e;}
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
st.caption("📊 Gestión financiera simple")

# 💰 PRICES (uniquement pour calcul ventes)
PRICES = {"Tequeños": 4, "Pasteles": 5}

# ✅ LOAD DATA
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=[
        "tipo","producto","cantidad","precio_unitario",
        "monto","fecha"
    ])

# ✅ CLEAN
df = df.dropna(how="all")

if "tipo" in df.columns:
    df = df[df["tipo"].notna()]

if "monto" in df.columns:
    df = df[df["monto"] != 0]

# 📂 IMPORT CSV
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📂 Cargar datos")

uploaded_file = st.file_uploader("Subir archivo CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.to_csv(FILE, index=False)
    st.success("✅ Datos cargados correctamente")

st.markdown("</div>", unsafe_allow_html=True)

# ➕ FORM
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("➕ Nueva transacción")

tipo = st.selectbox("Tipo", ["Venta", "Gasto"])

producto = ""
cantidad = 0
precio = 0.0
monto = 0.0

# ✅ VENTA (juste calcul revenu)
if tipo == "Venta":
    producto = st.selectbox("Producto", ["Tequeños", "Pasteles"])
    cantidad = st.number_input("Cantidad", min_value=1)

    precio = PRICES[producto]
    monto = cantidad * precio

    st.info(f"💰 Ingreso: ${monto}")

# ✅ GASTO (tout est manuel maintenant)
else:
    producto = st.text_input("Material / Producto")
    cantidad = st.number_input("Cantidad", min_value=1)
    precio = st.number_input("Precio unitario ($)", min_value=0.0)

    monto = cantidad * precio

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
        "fecha": fecha
    }])

    df = pd.concat([df, nueva], ignore_index=True)
    df.to_csv(FILE, index=False)

    st.success("✅ Guardado correctamente")

st.markdown("</div>", unsafe_allow_html=True)

# ✅ DISPLAY
if len(df) > 0:

    # 📊 RESUMEN
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📊 Resumen")

    ingresos = df[df["tipo"] == "Venta"]["monto"].sum()
    gastos = df[df["tipo"] == "Gasto"]["monto"].sum()
    beneficio = ingresos - gastos

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Ingresos", f"${ingresos:.2f}")
    col2.metric("💸 Gastos", f"${gastos:.2f}")
    col3.metric("✅ Beneficio", f"${beneficio:.2f}")

    st.markdown("</div>", unsafe_allow_html=True)

    # 📈 GRAPH PRO
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📈 Evolución diaria")

    try:
        df_copy = df.copy()

        df_copy["fecha"] = pd.to_datetime(df_copy["fecha"], errors="coerce")
        df_copy = df_copy.dropna(subset=["fecha"])

        if not df_copy.empty:

            daily = df_copy.groupby(["fecha","tipo"])["monto"].sum().unstack(fill_value=0)

            # ✅ garantir colonnes
            if "Venta" not in daily:
                daily["Venta"] = 0
            if "Gasto" not in daily:
                daily["Gasto"] = 0

            # ✅ calcul bénéfice
            daily["Beneficio"] = daily["Venta"] - daily["Gasto"]

            # rename pour affichage
            daily = daily.rename(columns={
                "Venta":"Ingresos",
                "Gasto":"Gastos"
            })

            st.line_chart(daily)

            st.caption("🟢 Ingresos | 🔴 Gastos | 🔵 Beneficio")

        else:
            st.info("No hay datos suficientes")

    except Exception as e:
        st.error(f"Error gráfico: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

    # 📋 HISTORIAL
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📋 Historial")
    st.dataframe(df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 📥 EXPORT
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Descargar backup",
        csv,
        "backup_tequenos.csv",
        "text/csv"
    )

else:
    st.info("📭 No hay datos todavía")

# RESET
if st.button("🗑️ Borrar todos los datos"):
    if os.path.exists(FILE):
        os.remove(FILE)
    st.success("✅ Datos eliminados completamente")
