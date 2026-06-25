import streamlit as st
import pandas as pd
from datetime import date
import os
from io import BytesIO

from reportlab.pdfgen import canvas
from docx import Document

FILE = "data.csv"

st.set_page_config(page_title="J&A Tequeños", layout="wide")

# 🎨 DESIGN
st.markdown("""
<style>
body {background:#0F172A; color:white;}
.logo {
    text-align:center;
    font-size:40px;
    font-weight:bold;
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.banner {
    height:200px;
    background-image:url('https://domesticfits.com/wp-content/uploads/2023/06/venezuelan-food-Tequenos.jpg');
    background-size:cover;
    border-radius:15px;
    margin-bottom:20px;
}
.card {
    background:#1E293B;
    padding:20px;
    border-radius:15px;
    text-align:center;
}
.value {
    font-size:28px;
    font-weight:bold;
}
.stButton>button {
    background:#22c55e;
    color:white;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<div class='logo'>J&A Tequeños</div>", unsafe_allow_html=True)
st.markdown("<div class='banner'></div>", unsafe_allow_html=True)

PRICES = {"Tequeños": 4, "Pasteles": 5}

# LOAD
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["tipo","producto","cantidad","precio_unitario","monto","fecha"])

df = df.dropna(how="all")

# FORM
st.subheader("➕ Nueva transacción")

tipo = st.selectbox("Tipo", ["Venta","Gasto"])

if tipo == "Venta":
    producto = st.selectbox("Producto", ["Tequeños","Pasteles"])
    cantidad = st.number_input("Cantidad", min_value=1)

    precio = PRICES[producto]
    monto = cantidad * precio

else:
    producto = st.text_input("Material")
    cantidad = st.number_input("Cantidad", min_value=1)
    precio = st.number_input("Precio", min_value=0.0)

    monto = cantidad * precio

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
    df = pd.concat([df,new], ignore_index=True)
    df.to_csv(FILE,index=False)
    st.success("✅ Guardado")

# DASHBOARD
if len(df)>0:

    ingresos = df[df["tipo"]=="Venta"]["monto"].sum()
    gastos = df[df["tipo"]=="Gasto"]["monto"].sum()
    beneficio = ingresos - gastos

    c1,c2,c3 = st.columns(3)

    c1.metric("Ingresos", f"${ingresos:.2f}")
    c2.metric("Gastos", f"${gastos:.2f}")
    c3.metric("Beneficio", f"${beneficio:.2f}")

    st.subheader("📊 Historial")
    st.dataframe(df)

    # ✅ EXPORT EXCEL
    excel = BytesIO()
    df.to_excel(excel, index=False, engine='openpyxl')

    st.download_button(
        "📊 Descargar Excel",
        excel.getvalue(),
        "tequenos.xlsx"
    )

    # ✅ EXPORT PDF
    pdf_buffer = BytesIO()
    p = canvas.Canvas(pdf_buffer)

    y = 800
    for i, row in df.iterrows():
        text = f"{row['fecha']} - {row['tipo']} - {row['producto']} - ${row['monto']}"
        p.drawString(30, y, text)
        y -= 20

    p.save()

    st.download_button(
        "📄 Descargar PDF",
        pdf_buffer.getvalue(),
        "tequenos.pdf"
    )

    # ✅ EXPORT WORD
    doc = Document()
    doc.add_heading("Reporte J&A Tequeños")

    for i, row in df.iterrows():
        doc.add_paragraph(
            f"{row['fecha']} - {row['tipo']} - {row['producto']} - ${row['monto']}"
        )

    word_buffer = BytesIO()
    doc.save(word_buffer)

    st.download_button(
        "📝 Descargar Word",
        word_buffer.getvalue(),
        "tequenos.docx"
    )

else:
    st.info("No hay datos todavía")

# RESET
if st.button("🗑️ Borrar todo"):
    if os.path.exists(FILE):
        os.remove(FILE)
    st.success("Datos eliminados")
