import streamlit as st
import pandas as pd
import os
from datetime import date

FILE = "data.csv"

st.set_page_config(page_title="Jeovanny Tequeños", layout="centered")

# 🎨 DESIGN SIMPLE & LISIBLE
st.markdown("""
<style>
html, body {
    background-color: #0F172A;
    color: white;
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
    color: white;
}

.stButton>button {
