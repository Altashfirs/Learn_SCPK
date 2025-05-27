import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Learn Streamlit")

st.markdown("## Tugas 3 - SPK dengan Metode WP")
st.markdown("### 123230062 - Muhamad Akbar Riziq")
st.markdown("#### Dataframe")

kriteria = []
bobot = []
keterangan = []

kriteriaTab, alternatifTab, matrixTab = st.tabs(["Kriteria", "Alternatif", "Matrix"])

with kriteriaTab:
    kriteriaTotal = st.number_input("Masukkan jumlah kriteria ", 1, 100, 1)
    for i in range(kriteriaTotal):
        col1, col2, col3 = st.columns(3)
        with col1:
            kriteriaName = st.text_input(f"Kriteria {i+1}")
            kriteria.append(kriteriaName)
        with col2:
            bobot.append(st.number_input(f"Bobot {kriteriaName}", 0, 5, 0, key=f"bobot_{i}"))
        with col3:
            keteranganName = st.selectbox(f"Keterangan {kriteriaName}", ["Benefit", "Cost"], key=f"keterangan_{i}")
            if keteranganName == "Benefit":
                keterangan.append(1)
            else:
                keterangan.append(-1)
    
alternatif = []
with alternatifTab:
    alternatifTotal = st.number_input("Masukkan jumlah alternatif ", 1, 100, 1)
    for i in range(alternatifTotal):
        alternatif.append(st.text_input(f"Alternatif {i+1}"))

with matrixTab:
    st.write("Matriks Alternatif")
    
    # Initialize matrix data in session state if not already present
    # if 'matrix_data' not in st.session_state:
    #     st.session_state['matrix_data'] = np.zeros((len(alternatif), len(kriteria)))
    
    # Collect matrix values
    matrix_data = []
    if kriteria and alternatif:
        for i, alt in enumerate(alternatif):
            row = []
            cols = st.columns(len(kriteria) + 1)
            with cols[0]:
                if i == 0:
                    st.write("\#")
                st.write(alt)
            for j, krit in enumerate(kriteria):
                with cols[j + 1]:
                    if i == 0:
                        st.write(f"{krit}({bobot[j]})")
                    value = st.number_input(f"{i},{j}", 0.0, None, 0.0, key=f"matrix_{i}_{j}")
                    row.append(value)
            matrix_data.append(row)
   
dataframeButton = st.button("Buat Dataframe")
if dataframeButton:
    # Create DataFrame from the matrix data
    df = pd.DataFrame(matrix_data, columns=kriteria, index=alternatif)
    st.write(df)

alternativeButton = st.button("Find Best Alternative")
if alternativeButton:
    if matrix_data and kriteria and alternatif and bobot and keterangan:
        # Use the same matrix_data as in the DataFrame
        m = len(matrix_data)  # Number of alternatives
        n = len(matrix_data[0])  # Number of criteria
        
        # Normalize weights
        if sum(bobot) == 0:
            st.error("Jumlah bobot tidak boleh nol.")
        else:
            w_norm = [x / sum(bobot) for x in bobot]
            
            # Create DataFrame for normalized weights
            w_norm_df = pd.DataFrame([w_norm], columns=kriteria, index=["Normalized Weight"])
            st.write("Normalized Weights:")
            st.write(w_norm_df)
            
            # Calculate S vector
            s = [1] * m
            for i in range(m):
                for j in range(n):
                    s[i] = s[i] * matrix_data[i][j] ** (keterangan[j] * w_norm[j])
            
            # Create DataFrame for S vector
            s_df = pd.DataFrame(s, columns=["S Score"], index=alternatif)
            st.write("S Vector:")
            st.write(s_df)
            
            # Calculate V vector
            if sum(s) == 0:
                st.error("Jumlah nilai S tidak boleh nol.")
            else:
                v = [x / sum(s) for x in s]
                # Create DataFrame for V vector
                v_df = pd.DataFrame(v, columns=["V Score"], index=alternatif)
                st.write("V Vector:")
                st.write(v_df)
                
                # Find the index of the maximum value in V
                max_index = v.index(max(v))
                
                # Display best alternative
                st.write(f"Alternatif terbaik berdasarkan metode WP adalah {alternatif[max_index]}")
    else:
        st.error("Pastikan semua kriteria, alternatif, bobot, keterangan, dan nilai matriks telah diisi dengan benar.")