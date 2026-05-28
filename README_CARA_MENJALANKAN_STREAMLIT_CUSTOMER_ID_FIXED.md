# README — Streamlit Customer ID FIX Recommendation

Dokumen ini menjelaskan cara menjalankan dashboard Streamlit versi **Customer ID FIX Recommendation**.

Versi ini adalah versi perbaikan dari dashboard sebelumnya yang sempat menghasilkan rekomendasi produk kurang relevan, misalnya customer dengan kategori favorit **Alat Tulis** tetapi mendapat rekomendasi produk **Makanan**. Pada versi FIX ini, logika rekomendasi sudah diperbaiki agar:

1. `recommended_product` utama mengikuti `favorite_category` customer terlebih dahulu.
2. Hasil Association Rule tetap digunakan, tetapi dipisahkan sebagai insight tambahan pada kolom `cross_sell_product_from_rule`.
3. Dashboard menampilkan alasan rekomendasi melalui kolom `recommendation_basis` dan `recommendation_reason`.

---

## 1. Struktur Folder yang Benar

Setelah file ZIP diekstrak, struktur folder harus seperti berikut:

```text
streamlit_customer_id_fixed/
├── app_customer_id_fixed.py
├── requirements.txt
└── outputs/
    ├── customer_monthly_summary.csv
    ├── customer_product_summary.csv
    ├── customer_rfm.csv
    ├── data_dictionary.csv
    ├── market_basket_rules.csv
    ├── next_best_action.csv
    ├── project_summary.json
    ├── segment_summary.csv
    ├── top_products.csv
    └── transaction_line_items.csv
```

File utama yang dijalankan adalah:

```text
app_customer_id_fixed.py
```

Folder `outputs/` tidak boleh dihapus karena dashboard membaca semua file hasil analisis dari folder tersebut.

---

## 2. Isi File Utama

### 2.1 `app_customer_id_fixed.py`

File ini adalah aplikasi dashboard Streamlit. Isinya menampilkan:

- segmentasi customer berbasis Customer RFM,
- market basket rules untuk cross-selling,
- next best action per customer,
- customer 360°,
- data dan panduan baca hasil rekomendasi.

### 2.2 `requirements.txt`

File ini berisi daftar library Python yang harus diinstall:

```text
streamlit
pandas
plotly
```

### 2.3 Folder `outputs/`

Folder ini berisi semua output dari notebook Colab, yaitu:

| File | Fungsi |
|---|---|
| `customer_rfm.csv` | Hasil perhitungan RFM per customer |
| `segment_summary.csv` | Ringkasan jumlah customer dan revenue per segment |
| `customer_monthly_summary.csv` | Tren bulanan customer dan revenue per segment |
| `customer_product_summary.csv` | Produk/kategori dominan per customer |
| `market_basket_rules.csv` | Hasil Association Rule untuk cross-selling |
| `next_best_action.csv` | Rekomendasi utama, cross-sell, nudge, dan action per customer |
| `top_products.csv` | Produk populer per kategori |
| `transaction_line_items.csv` | Data transaksi line item yang sudah diproses |
| `data_dictionary.csv` | Kamus data/penjelasan kolom |
| `project_summary.json` | Ringkasan jumlah customer, order, rules, dan output |

---

## 3. Cara Menjalankan Dashboard di VSCode

### Langkah 1 — Extract ZIP

Extract file ZIP sampai muncul folder:

```text
streamlit_customer_id_fixed
```

### Langkah 2 — Buka Folder di VSCode

Buka VSCode, lalu pilih:

```text
File → Open Folder → pilih folder streamlit_customer_id_fixed
```

Pastikan di panel kiri VSCode terlihat:

```text
app_customer_id_fixed.py
requirements.txt
outputs/
```

### Langkah 3 — Buka Terminal

Di VSCode, buka terminal:

```text
Terminal → New Terminal
```

Pastikan terminal sudah berada di folder:

```text
streamlit_customer_id_fixed
```

Jika belum, masuk dulu dengan command:

```bash
cd streamlit_customer_id_fixed
```

---

## 4. Install Library

Jalankan command berikut di terminal:

```bash
python -m pip install -r requirements.txt
```

Command ini berfungsi untuk menginstall library yang dibutuhkan dashboard, yaitu Streamlit, Pandas, dan Plotly.

Jika berhasil, terminal tidak menampilkan error.

---

## 5. Jalankan Dashboard Streamlit

Setelah library berhasil diinstall, jalankan dashboard dengan command:

```bash
python -m streamlit run app_customer_id_fixed.py
```

Jika berhasil, terminal akan menampilkan link seperti:

```text
Local URL: http://localhost:8501
```

Biasanya browser akan terbuka otomatis. Jika tidak terbuka otomatis, copy link tersebut dan paste di browser.

---

## 6. Cara Membaca Dashboard

Dashboard terdiri dari beberapa tab utama.

### 6.1 Overview RFM

Tab ini menampilkan segmentasi customer berdasarkan Customer RFM.

Cara membaca:

- `recency_days` menunjukkan jarak hari sejak transaksi terakhir customer.
- `frequency` menunjukkan jumlah transaksi/order customer.
- `monetary` menunjukkan total nilai belanja customer.
- `segment` menunjukkan kelompok customer, misalnya Champions, Loyal Customers, Potential Loyalist, dan lain-lain.

Tujuan tab ini adalah melihat kelompok customer mana yang paling bernilai bagi bisnis.

---

### 6.2 Market Basket Rules

Tab ini menampilkan hasil Association Rule.

Cara membaca:

- `antecedent` adalah produk/kategori awal.
- `consequent` adalah produk/kategori yang direkomendasikan sebagai cross-sell.
- `support` menunjukkan seberapa sering pola muncul dalam transaksi.
- `confidence` menunjukkan peluang consequent muncul ketika antecedent muncul.
- `lift` menunjukkan kekuatan hubungan antar produk/kategori.

Catatan penting:

Association Rule pada versi FIX tidak langsung dipaksakan menjadi rekomendasi utama customer. Hasil rules dipakai sebagai **cross-sell insight** agar rekomendasi tetap masuk akal.

---

### 6.3 Next Best Action FIX

Tab ini adalah bagian paling penting karena berisi rekomendasi per customer.

Kolom penting:

| Kolom | Makna |
|---|---|
| `customer_id` | ID pelanggan |
| `segment` | Segmen customer berdasarkan RFM |
| `favorite_category` | Kategori favorit customer |
| `favorite_product` | Produk favorit customer |
| `recommended_product` | Rekomendasi utama yang mengikuti kategori favorit |
| `recommended_category` | Kategori dari produk rekomendasi utama |
| `recommendation_basis` | Dasar logika rekomendasi |
| `recommendation_reason` | Alasan kenapa produk itu direkomendasikan |
| `cross_sell_product_from_rule` | Produk tambahan dari Association Rule |
| `cross_sell_category_from_rule` | Kategori produk cross-sell |
| `nudge_type` | Jenis pesan nudge |
| `action_recommendation` | Strategi/tindakan pemasaran yang disarankan |

Contoh interpretasi:

Jika customer memiliki `favorite_category = Alat Tulis`, maka `recommended_product` utama akan dipilih dari kategori **Alat Tulis**. Jika Association Rule menemukan peluang lintas kategori, hasilnya masuk ke `cross_sell_product_from_rule`, bukan menggantikan rekomendasi utama.

---

### 6.4 Customer 360°

Tab ini digunakan untuk melihat detail satu customer.

Fitur ini menampilkan:

- segment customer,
- skor RFM,
- frequency,
- monetary,
- pesan rekomendasi,
- action recommendation,
- produk cross-sell,
- riwayat transaksi customer,
- ringkasan produk customer.

Tab ini cocok digunakan saat demo untuk menunjukkan bahwa rekomendasi sudah berbasis customer.

---

### 6.5 Data dan Panduan Baca

Tab ini menampilkan semua data output yang digunakan dashboard.

Data yang bisa dibuka:

- `customer_rfm`
- `segment_summary`
- `market_basket_rules`
- `next_best_action`
- `transaction_line_items`
- `customer_product_summary`
- `top_products`

Tab ini berguna untuk mengecek data mentah hasil analisis jika dosen atau pembimbing bertanya.

---

## 7. Penjelasan Kenapa Hasil Sudah Diperbaiki

Masalah sebelumnya terjadi karena `recommended_product` diambil dari produk populer secara global/segment. Akibatnya, customer dengan kategori favorit **Alat Tulis** bisa mendapat rekomendasi produk **Makanan** jika produk makanan tersebut populer pada segment yang sama.

Pada versi FIX, logika rekomendasi diubah menjadi:

```text
Prioritas 1:
Cari produk rekomendasi dari kategori favorit customer.

Prioritas 2:
Jika tidak tersedia, gunakan produk populer dalam segment.

Prioritas 3:
Association Rule digunakan sebagai cross-sell insight, bukan rekomendasi utama.
```

Dengan alur ini, rekomendasi utama menjadi lebih relevan secara bisnis.

---

## 8. Jawaban Jika Ditanya Dosen

Jika dosen bertanya kenapa hasil sebelumnya aneh, jawab:

> Hasil sebelumnya terlihat kurang relevan karena logika rekomendasi masih mengambil produk populer pada level segment/global, sehingga produk lintas kategori dapat muncul sebagai rekomendasi utama. Pada versi perbaikan, rekomendasi utama diprioritaskan berdasarkan kategori favorit customer. Association Rule tetap digunakan, tetapi dipisahkan sebagai cross-sell insight agar rekomendasi utama tidak terlihat random dan tetap sesuai dengan preferensi customer.

Jika dosen bertanya kenapa Association Rule tidak dijadikan rekomendasi utama, jawab:

> Association Rule tetap digunakan untuk melihat peluang cross-selling. Namun, karena cross-selling bisa menghasilkan rekomendasi lintas kategori, hasil rule dipisahkan dari rekomendasi utama. Rekomendasi utama mengikuti kategori favorit customer, sedangkan Association Rule menjadi rekomendasi tambahan.

---

## 9. Error yang Sering Terjadi

### 9.1 Error: `streamlit is not recognized`

Gunakan command:

```bash
python -m streamlit run app_customer_id_fixed.py
```

Jangan gunakan:

```bash
streamlit run app_customer_id_fixed.py
```

jika Streamlit belum terdaftar di PATH.

---

### 9.2 Error: `ModuleNotFoundError`

Jalankan ulang:

```bash
python -m pip install -r requirements.txt
```

---

### 9.3 Error: file CSV tidak ditemukan

Pastikan struktur folder seperti ini:

```text
streamlit_customer_id_fixed/
├── app_customer_id_fixed.py
├── requirements.txt
└── outputs/
    ├── customer_rfm.csv
    ├── next_best_action.csv
    └── file output lainnya
```

Folder harus bernama:

```text
outputs
```

Jangan diubah menjadi:

```text
output
hasil
data
```

---

### 9.4 Error karena terminal salah folder

Pastikan terminal berada di folder `streamlit_customer_id_fixed`.

Cek dengan command:

```bash
pwd
```

atau pada Windows Command Prompt:

```bash
cd
```

Jika belum masuk folder, gunakan:

```bash
cd path_ke_folder/streamlit_customer_id_fixed
```

---

## 10. Command Ringkas

Jika folder sudah benar, cukup jalankan:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app_customer_id_fixed.py
```

---

## 11. Checklist Sebelum Dikirim ke Mahasiswa

Pastikan isi folder final seperti ini:

```text
[✓] app_customer_id_fixed.py
[✓] requirements.txt
[✓] outputs/customer_rfm.csv
[✓] outputs/next_best_action.csv
[✓] outputs/market_basket_rules.csv
[✓] outputs/transaction_line_items.csv
[✓] outputs/project_summary.json