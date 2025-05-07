gudang = {}

def cek_barang(id_barang):
    if id_barang in gudang:
        return True
    else:
        return False

def tambah_barang():
    id_barang = input("Masukkan ID Barang: ")
    if cek_barang(id_barang):
        print("Barang sudah terdaftar")
        return
    
    nama_barang = input("Masukkan Nama Barang: ")
    kategori_barang = input("Masukkan Kategori Barang: ")
    jumlah_stok = int(input("Masukkan Jumlah Stok: "))
    
    gudang[id_barang] = {
        'nama': nama_barang,
        'kategori': kategori_barang,
        'stok': jumlah_stok
    }
    print("Barang berhasil ditambahkan.")

def tampilkan_daftar_barang():
    if not gudang:
        print("Tidak ada barang dalam gudang.")
    else:
        print("Daftar Barang:")
        for id_barang, detail in gudang.items():
            print(f"ID: {id_barang}, Nama: {detail['nama']}, Kategori: {detail['kategori']}, Stok: {detail['stok']}")

def cari_barang():
    nama_cari = input("Masukkan nama barang yang ingin dicari: ").lower()
    ditemukan = False
    for id_barang, detail in gudang.items():
        if nama_cari in detail['nama'].lower():
            print(f"ID: {id_barang}, Nama: {detail['nama']}, Kategori: {detail['kategori']}, Stok: {detail['stok']}")
            ditemukan = True
    if not ditemukan:
        print("Barang tidak ditemukan.")

def hapus_barang():
    id_hapus = input("Masukkan ID Barang yang ingin dihapus: ")
    if id_hapus in gudang:
        del gudang[id_hapus]
        print("Barang berhasil dihapus.")
    else:
        print("Barang dengan ID tersebut tidak ditemukan.")

def main():
    while True:
        print("\nMenu Sistem Manajemen Gudang:")
        print("1. Tambah Barang")
        print("2. Tampilkan Daftar Barang")
        print("3. Cari Barang")
        print("4. Hapus Barang")
        print("5. Keluar")
        pilihan = input("Pilih menu (1/2/3/4/5): ")
        
        if pilihan == '1':
            tambah_barang()
        elif pilihan == '2':
            tampilkan_daftar_barang()
        elif pilihan == '3':
            cari_barang()
        elif pilihan == '4':
            hapus_barang()
        elif pilihan == '5':
            print("Terima kasih telah menggunakan Sistem Manajemen Gudang.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih menu yang tersedia.")

if __name__ == "__main__":
    main()
