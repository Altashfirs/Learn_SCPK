# alternatif
a = []
for i in range(3):
    a.append(input("Masukkan lokasi gudang ke-{}: ".format(i+1)))

# matriks keputusan
x = []
for i in range(3):
    print("")
    x.append([])
    for j in range(5):
        x[i].append(float(input("Masukkan nilai alternatif {} kriteria {}: ".format(i+1,j+1))))

# penentuan benefit/cost tiap kriteria
# cost = -1, benefit = 1
k = [-1,-1,-1,1,-1]

# bobot dari tiap kriteria
w = [5,3,4,4,2]

# ambil dimensi dari matriks keputusan
# m = jumlah alternatif, n = jumlah kriteria
m = len(x)
n = len(x[0])

# normalisasi bobot
w_norm = [x/sum(w) for x in w]

# menghitung vektor S
s = [1]*m
for i in range(m):
    for j in range(n):
        s[i] = s[i]*x[i][j]**(k[j]*w_norm[j])
        
# menghitung vektor V
v = [x/sum(s) for x in s]

# ambil indeks nilai terbesar dari vektor V
max_index = v.index(max(v))

# tampilkan hasil vektor v dan alternatif terbaik
print("Hasil matriks V adalah {}".format(v))
print("Lokasi gudang terbaik berdasarkan metode WP adalah {}".format(a[max_index]))
