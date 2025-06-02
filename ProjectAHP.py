import streamlit as st
import pandas as pd
import numpy as np

# Fungsi-fungsi dasar AHP
def normalize_comparation(M):
    return M / M.sum(axis=0)

def weight(M):
    return np.mean(M, axis=1)

def final_weight(W_alt, W_crit):
    return W_alt.T @ W_crit

def value_to_ahp_scale(val1, val2, is_lower_better=False):
    try:
        if val1 == val2:
            return 1.0

        if is_lower_better:
            val1, val2 = val2, val1  # Tukar agar val1 selalu "lebih baik"

        if val2 == 0:  # Cegah pembagian dengan nol
            return 9.0

        ratio = val1 / val2

        if ratio <= 1:
            return round(1 / max(1.0, ratio), 2)  # untuk amankan jika ratio < 1
        elif ratio <= 1.5:
            return 2.0
        elif ratio <= 2:
            return 3.0
        elif ratio <= 3:
            return 5.0
        else:
            return 9.0
    except:
        return 1.0

# Konfigurasi halaman
st.set_page_config(page_title="AHP Housing Bandung", layout="wide")
st.title("🏠 AHP - Pemilihan Rumah Terbaik di Bandung")

try:
    df = pd.read_csv("dataset/balanced_top_500.csv")
    kolom_dibutuhkan = ['house_name', 'price', 'land_area', 'building_area', 'jarak_ke_kota_km',
                        'bedroom_count', 'bathroom_count', 'carport_count']
    df = df[kolom_dibutuhkan].dropna()
    for col in kolom_dibutuhkan[1:]:
        df[col] = pd.to_numeric(df[col], errors='raise')

    if df['house_name'].duplicated().any():
        df['house_name'] += '_' + df.index.astype(str)

    alternatif = df['house_name'].tolist()
    kriteria = ["Harga", "Luas Tanah", "Luas Bangunan", "Jarak ke Kota",
                "Jumlah Kamar Tidur", "Jumlah Kamar Mandi", "Jumlah Carport"]

    st.subheader("🧮 Input Matriks Perbandingan Kriteria")
    st.info("Isi perbandingan antar kriteria. Contoh: Jika Harga lebih penting daripada Luas Tanah, isi > 1.")
    
    matrix_data = []
    cols = st.columns(len(kriteria) + 1)
    for j, kol in enumerate(kriteria):
        with cols[j + 1]:
            st.markdown(f"**{kol}**")
    
    for i, row_krit in enumerate(kriteria):
        row = []
        cols = st.columns(len(kriteria) + 1)
        with cols[0]:
            st.markdown(f"**{row_krit}**")
        for j in range(len(kriteria)):
            with cols[j + 1]:
                if i == j:
                    st.markdown(":blue-background[1.0]")
                    row.append(1.0)
                elif i < j:
                    val = st.number_input(f"{row_krit} vs {kriteria[j]}", key=f"c_{i}_{j}", min_value=0.1, value=1.0)
                    row.append(val)
                else:
                    row.append(None)
        matrix_data.append(row)

    # Matriks Kriteria AHP Lengkap
    MPBk = np.ones((len(kriteria), len(kriteria)))
    for i in range(len(kriteria)):
        for j in range(len(kriteria)):
            if i < j:
                MPBk[i][j] = matrix_data[i][j]
                MPBk[j][i] = 1 / matrix_data[i][j]
            elif i > j:
                MPBk[i][j] = 1 / matrix_data[j][i]

    # Tampilkan hasil kriteria
    with st.expander("📊 Matriks Kriteria dan Perhitungan"):
        st.write("**Matriks Perbandingan Kriteria**")
        st.dataframe(pd.DataFrame(MPBk, index=kriteria, columns=kriteria))
        MPBk_norm = normalize_comparation(MPBk)
        st.write("**Normalisasi Matriks**")
        st.dataframe(pd.DataFrame(MPBk_norm, index=kriteria, columns=kriteria))
        Wk = weight(MPBk_norm)
        st.write("**Bobot/Eigenvector**")
        st.dataframe(pd.DataFrame(Wk, index=kriteria, columns=["Eigenvector"]))

    criteria_mapping = {
        "Harga": ("price", True),
        "Luas Tanah": ("land_area", False),
        "Luas Bangunan": ("building_area", False),
        "Jarak ke Kota": ("jarak_ke_kota_km", True),
        "Jumlah Kamar Tidur": ("bedroom_count", False),
        "Jumlah Kamar Mandi": ("bathroom_count", False),
        "Jumlah Carport": ("carport_count", False),
    }

    st.subheader("🏘️ Alternatif Rumah per Kriteria")
    w_total = []
    for crit in kriteria:
        column, is_lower_better = criteria_mapping[crit]
        values = df[column].values
        matrix = np.ones((len(alternatif), len(alternatif)))
        for i in range(len(alternatif)):
            for j in range(len(alternatif)):
                if i != j:
                    matrix[i][j] = value_to_ahp_scale(values[i], values[j], is_lower_better)
        norm = normalize_comparation(matrix)
        w = weight(norm)
        w_total.append(w)

        with st.expander(f"📑 Detail: {crit}"):
            st.write("**Matriks Perbandingan (5x5 pertama)**")
            st.dataframe(pd.DataFrame(matrix[:50, :50], index=alternatif[:50], columns=alternatif[:50]))
            st.write("**Normalisasi Matriks (5x5 pertama)**")
            st.dataframe(pd.DataFrame(norm[:50, :50], index=alternatif[:50], columns=alternatif[:50]))
            st.write("**Eigenvector (semua rumah)**")
            st.dataframe(pd.DataFrame(w, index=alternatif, columns=["Eigenvector"]))

    w_total = np.array(w_total)
    W_final = final_weight(w_total, Wk)

    # Hasil akhir
    st.subheader("🏁 Hasil Akhir")
    tab1, tab2 = st.tabs(["📈 Vector Keputusan", "🏅 Rumah Terbaik"])
    with tab1:
        st.write("**Matrix Eigenvector Alternatif**")
        st.dataframe(pd.DataFrame(w_total.T, index=alternatif, columns=kriteria))
        st.write("**Nilai Akhir Setiap Rumah**")
        st.dataframe(pd.DataFrame(W_final, index=alternatif, columns=["Skor Akhir"]))
    
    with tab2:
        best_idx = np.argmax(W_final)
        best_house = alternatif[best_idx]
        best_score = W_final[best_idx]
        st.success(f"🏆 Rumah terbaik adalah **{best_house}** dengan skor akhir **{best_score:.4f}**")

except Exception as e:
    st.error(f"Kesalahan: {str(e)}")
