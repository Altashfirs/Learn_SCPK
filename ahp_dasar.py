import numpy as np

def normalize_comparation(M):
    sumCol = M.sum(axis = 0)
    norm = M / sumCol
    return norm

def weight(M):
    return np.mean(M, axis = 1)

def validity_check(M, W):
    n = len(M)
    RI = {
        2: 0.00,
        3: 0.58,
        4: 0.90,
        5: 1.12,
        6: 1.24,
        7: 1.32,
        8: 1.41,
        9: 1.45,
        10: 1.51,
        11: 1.53,
        12: 1.54,
        13: 1.56,
        14: 1.57,
    }
    
    CV = M @ W / W
    print(f"CV: {CV}\n")
    
    eigen = np.mean(CV)
    print(f"Eigen: {eigen}\n")
    
    print(f"RI: {RI[n]}\n")
    
    CI = (eigen - n) / (n - 1)
    print(f"CI: {CI}\n")
    
    CR = CI / RI[n]
    print(f"CR: {CR}\n")
    
    if CR <= 0.1:
        print("Bobot Valid\n\n")
    else:
        print("Bobot Tidak Valid\n\n")
        
A = ["Yamaha", "Honda", "Suzuki", "Kawasaki"]

print("=== Kriteria ===")

MPBk = np.array([
    [1, 1/2, 3, 1/2],
    [2, 1, 4, 3],
    [1/3, 1/4, 1, 2],
    [2, 1/3, 1/2, 1],
])

print(f"Matriks Perbandingan:\n {MPBk}\n")

MPBk_norm = normalize_comparation(MPBk)
print(f"Matriks Perbandingan Normalisasi:\n {MPBk_norm}\n")

Wk = weight(MPBk_norm)
print(f"Bobot Kriteria:\n {Wk}\n")

validity_check(MPBk, Wk)

print("=== Gaya ===")
MPBg = np.array([
    [1, 1/2, 2, 1/3],
    [2, 1, 3, 1/2],
    [1/2, 1/3, 1, 1/4],
    [3, 2, 4, 1]
])
print(f"Matriks Perbandingan: {MPBg}\n")

MPBg_norm = normalize_comparation(MPBg)
print(f"Matriks Perbandingan Setelah Normalisasi: {MPBg_norm}\n")

Wg = weight(MPBg_norm)
print(f"Bobot: {Wg}\n")

validity_check(MPBg,Wg)

print("=== Keandalan ===")

MPBa = np.array([
    [1, 1/2, 3, 2],
    [2, 1, 4, 3],
    [1/3, 1/4, 1, 1/2],
    [1/2, 1/3, 2, 1]
])

print(f"Matriks Perbandingan: {MPBa}\n")

MPBa_norm = normalize_comparation(MPBa)
print(f"Matriks Perbandingan Setelah Normalisasi: {MPBa_norm}\n")

Wa = weight(MPBa_norm)
print(f"Bobot: {Wa}\n")

validity_check(MPBa, Wa)

print("=== Keekonomisan ===")
MPBe = np.array([
    [1, 60/80, 1, 60/80],
    [80/60, 1, 80/60, 1],
    [1, 60/80, 1, 60/80],
    [80/60, 1, 80/60, 1],
])

print(f"Matriks Perbandingan: {MPBe}\n")

MPBe_norm = normalize_comparation(MPBe)
print(f"Matriks Perbandingan Setelah Normalisasi:\n {MPBe_norm}\n")

We = weight(MPBe_norm)
print(f"Bobot: {We}\n")

validity_check(MPBe, We)

print("=== Harga ===")
MPBh = np.array([
    [1, 16/30, 16/15, 16/40],
    [30/16, 1, 2, 30/40],
    [15/16, 1/2, 1, 15/40],
    [40/16, 40/30, 40/15, 1],
])

print(f"Matriks Perbandingan: {MPBh}\n")

MPBh_norm = normalize_comparation(MPBh)
print(f"Matriks Perbandingan Setelah Normalisasi:\n {MPBh_norm}\n")

Wh = weight(MPBh_norm)
print(f"Bobot: {Wh}\n")
validity_check(MPBh, Wh)

def final_weight(W_alt, W_crit):
    W_fin = W_alt.T @ W_crit
    return W_fin

W_total = np.array([Wg, Wa, We, Wh])

W_final = final_weight(W_total, Wk)
print(f"Bobot Akhir: {W_final}\n")

max_index = np.argmax(W_final)
print(f"Alternatif Terbaik: {A[max_index]} dengan nilai {W_final[max_index]:.2f}\n")