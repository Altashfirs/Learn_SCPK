import streamlit as st
import pandas as pd
import sklearn as datasets

st.set_page_config(page_title="Learn Streamlit")

st.title("Aplikasi Streamlit Sederhana")
st.write("Selamat Datang di Pertemuan SPCK")

# FITUR INTERAKTIF
# Button
if st.button("Button"):
    st.write("Tombol Diklik")
    
# Slider
nilai = st.slider("Pilih Nilai", 5, 100, 0, 5)
st.write(f"Nilai yang dipilih : {nilai}")

# Selectbox
negara = st.selectbox("Pilih Negara", ["USA", "China", "Singapore", "Canada"])
st.write(f"Negara yang dipilih: {negara}")

# Number Input
st.number_input("Masukkan angka ", 0, 100, 0)

# Text Input
text = st.text_input("Masukkan Text", 
              placeholder='Ketik disini...',
              type='password')

# Text Area
st.text_area("Masukkan deskripsi", 
             placeholder="Ketik disini...")

# Expander
with st.expander("Lihat Detail"):
    st.write("Ini merupakan detailnya")
    
# Tabs
informasi, visualisasi, kontak = st.tabs(["Informasi", "Visualisasi", "Kontak"])

with informasi:
    st.write("Ini menu informasi")
    
with visualisasi:
    st.write("Ini menu visualisasi")

with kontak:
    st.write("Ini menu kontak")
    
