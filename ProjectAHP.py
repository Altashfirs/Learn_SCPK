import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AHP Manual - Pemilihan Rumah")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("dataset/top_100_per_location_with_distance.csv")
    df = df.rename(columns={"building_area (m2)": "building_area", "jarak_ke_kota_km": "distance"})
    return df

df = load_data()

# Kriteria
kriteria = [
    "land_area", "building_area", "carport_count", "bathroom_count", "bedroom_count", "price", "distance"
]
kriteria_labels = [
    "Luas Tanah", "Luas Bangunan", "Carport", "Kamar Mandi", "Kamar Tidur", "Harga", "Jarak"
]
benefit_criteria = ["land_area", "building_area", "carport_count", "bathroom_count", "bedroom_count"]
cost_criteria = ["price", "distance"]

st.title("AHP Manual - Pemilihan Rumah Berdasarkan Kriteria")
st.markdown("Isi perbandingan berpasangan antar kriteria (1 = sama penting, 9 = sangat lebih penting)")

# Matriks perbandingan berpasangan
pairwise = np.ones((7, 7))
for i in range(7):
    for j in range(i+1, 7):
        val = st.number_input(f"{kriteria_labels[i]} vs {kriteria_labels[j]}", min_value=1.0, max_value=9.0, step=1.0, value=1.0, key=f"{i}-{j}")
        pairwise[i][j] = val
        pairwise[j][i] = 1 / val

# Normalisasi dan eigenvector (bobot kriteria)
def normalize_comparation(M):
    sumCol = M.sum(axis=0)
    return M / sumCol

def weight(M):
    return np.mean(M, axis=1)

pairwise_norm = normalize_comparation(pairwise)
Wk = weight(pairwise_norm)

st.markdown("### Matriks Perbandingan Berpasangan")
st.dataframe(pd.DataFrame(pairwise, index=kriteria_labels, columns=kriteria_labels))

st.markdown("### Matriks Normalisasi")
st.dataframe(pd.DataFrame(pairwise_norm, index=kriteria_labels, columns=kriteria_labels))

st.markdown("### Eigenvector (Bobot Kriteria)")
st.dataframe(pd.DataFrame(Wk, index=kriteria_labels, columns=["Bobot"]))

# Normalisasi data rumah
st.markdown("## Skor Rumah")
df_norm = df[kriteria].copy()
for col in benefit_criteria:
    df_norm[col] = df[col] / df[col].max()
for col in cost_criteria:
    df_norm[col] = df[col].min() / df[col]

# Skor akhir berdasarkan bobot manual
scores = df_norm @ Wk
df_result = df[["house_name", "location"]].copy()
df_result["score"] = scores
df_result_sorted = df_result.sort_values(by="score", ascending=False).reset_index(drop=True)

st.markdown("### Top 10 Rumah Terbaik")
st.dataframe(df_result_sorted.head(10))

st.success(f"🏆 Rumah terbaik berdasarkan pembobotan manual AHP adalah: **{df_result_sorted.iloc[0]['house_name']}** "
           f"dengan skor {df_result_sorted.iloc[0]['score']:.4f}")
