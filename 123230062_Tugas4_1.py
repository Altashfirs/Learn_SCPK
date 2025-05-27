import streamlit as st
import pandas as pd
import numpy as np

def normalize_comparation(M):
    sumCol = M.sum(axis = 0)
    norm = M / sumCol
    return norm

def weight(M):
    return np.mean(M, axis = 1)

def final_weight(W_alt, W_crit):
    W_fin = W_alt.T @ W_crit
    return W_fin
    
Motor = ["Yamaha", "Honda", "Suzuki", "Kawasaki"]
Kriteria = ["Gaya", "Keandalan", "Keekonomisan", "Biaya"]


st.set_page_config(page_title="Tugas 4")
st.markdown("## Tugas 4 - SPK dengan Metode AHP")

st.markdown("#### Kriteria")
with st.expander("Details"):
    MPBk = np.array([
        [1, 1/2, 3, 1/2],
        [2, 1, 4, 3],
        [1/3, 1/4, 1, 2],
        [2, 1/3, 1/2, 1],
    ])
    
    
    st.write("Matriks Perbandingan Berpasangan pada Kriteria")
    df = pd.DataFrame(MPBk, index=Kriteria, columns=Kriteria)
    st.dataframe(df)

    st.write("Normalisasi Matriks")
    MPBk_norm = normalize_comparation(MPBk)
    df = pd.DataFrame(MPBk_norm, index=Kriteria, columns=Kriteria)
    st.dataframe(df)
    
    st.write("Eigenvector")
    Wk = weight(MPBk_norm)
    df = pd.DataFrame(Wk, index=Kriteria, columns=["Eigenvektor"])
    st.dataframe(df)
    
st.markdown("#### Alternatif - Gaya")
with st.expander("Details"):
    MPBg = np.array([
        [1, 1/2, 2, 1/3],
        [2, 1, 3, 1/2],
        [1/2, 1/3, 1, 1/4],
        [3, 2, 4, 1]
    ])
    
    st.write("Matriks Perbandingan Berpasangan pada Gaya")
    df = pd.DataFrame(MPBg, index=Motor, columns=Motor)
    st.dataframe(df)

    st.write("Normalisasi Matriks")
    MPBg_norm = normalize_comparation(MPBg)
    df = pd.DataFrame(MPBg_norm, index=Motor, columns=Motor)
    st.dataframe(df)
    
    st.write("Eigenvector")
    Wg = weight(MPBg_norm)
    df = pd.DataFrame(Wg, index=Motor, columns=["Eigenvektor"])
    st.dataframe(df)
    
st.markdown("#### Alternatif - Keandalan")
with st.expander("Details"):
    MPBa = np.array([
        [1, 1/2, 3, 2],
        [2, 1, 4, 3],
        [1/3, 1/4, 1, 1/2],
        [1/2, 1/3, 2, 1]
    ])
    
    st.write("Matriks Perbandingan Berpasangan pada Keandalan")
    df = pd.DataFrame(MPBa, index=Motor, columns=Motor)
    st.dataframe(df)

    st.write("Normalisasi Matriks")
    MPBa_norm = normalize_comparation(MPBa)
    df = pd.DataFrame(MPBa_norm, index=Motor, columns=Motor)
    st.dataframe(df)
    
    st.write("Eigenvector")
    Wa = weight(MPBa_norm)
    df = pd.DataFrame(Wa, index=Motor, columns=["Eigenvektor"])
    st.dataframe(df)
    
st.markdown("#### Alternatif - Keekonomisan")
with st.expander("Details"):
    MPBe = np.array([
        [1, 60/80, 1, 60/80],
        [80/60, 1, 80/60, 1],
        [1, 60/80, 1, 60/80],
        [80/60, 1, 80/60, 1]
    ])
    
    st.write("Matriks Perbandingan Berpasangan pada Keekonomisan")
    df = pd.DataFrame(MPBe, index=Motor, columns=Motor)
    st.dataframe(df)

    st.write("Normalisasi Matriks")
    MPBe_norm = normalize_comparation(MPBe)
    df = pd.DataFrame(MPBe_norm, index=Motor, columns=Motor)
    st.dataframe(df)
    
    st.write("Eigenvector")
    We = weight(MPBe_norm)
    df = pd.DataFrame(We, index=Motor, columns=["Eigenvektor"])
    st.dataframe(df)
    
st.markdown("#### Alternatif - Biaya")
with st.expander("Details"):
    MPBh = np.array([
        [1, 16/30, 16/15, 16/40],
        [30/16, 1, 2, 30/40],
        [15/16, 1/2, 1, 15/40],
        [40/16, 40/30, 40/15, 1],
    ])

    
    st.write("Matriks Perbandingan Berpasangan pada Biaya")
    df = pd.DataFrame(MPBh, index=Motor, columns=Motor)
    st.dataframe(df)

    st.write("Normalisasi Matriks")
    MPBh_norm = normalize_comparation(MPBh)
    df = pd.DataFrame(MPBh_norm, index=Motor, columns=Motor)
    st.dataframe(df)
    
    st.write("Eigenvector")
    Wb = weight(MPBh_norm)
    df = pd.DataFrame(Wb, index=Motor, columns=["Eigenvektor"])
    st.dataframe(df)
    
st.markdown("## Jawaban Akhir dan Vector Keputusan")

st.write("Eigenvektor")
w_total = np.array([Wg, Wa, We, Wb])
df = pd.DataFrame(w_total.T, index=Motor, columns=Kriteria)
st.dataframe(df)

st.write("Nilai AKhir")
W_final = final_weight(w_total, Wk)
df = pd.DataFrame(W_final, index=Motor, columns=["Nilai Akhir"])
st.dataframe(df)

st.write(f"Motor terbaik terpilih berdasarkan kriteria adalah {Motor[np.argmax(W_final)]} dengan nilai {W_final.max():.4f}")
