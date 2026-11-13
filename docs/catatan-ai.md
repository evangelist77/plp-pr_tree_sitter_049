# Catatan penggunaan AI

## Setup awal repositori

- Permintaan: membuat struktur awal sesuai materi, melakukan commit, dan menjelaskan hasilnya.
- Bantuan AI: kerangka folder, README, daftar dependensi, `.gitignore`, dan skrip cek setup dari contoh materi.
- Status: belum mengerjakan Tugas 1–6. Catatan setup ini bukan pengganti catatan per tugas.
- Keterbatasan: CLI Tree-sitter belum tersedia saat setup; inisialisasi grammar dan uji parse belum dijalankan.

## Template per tugas yang dibantu AI

- Tugas:
- Apa yang diminta kepada AI:
- Kesalahan/kekurangan hasil AI yang benar-benar ditemukan:
- Cara membuktikan (kasus uji, output, atau pengecekan manual):
- Perbaikan dan hasil verifikasi:

Pindahkan ringkasan ke `laporan.pdf` saat pengumpulan. Isi berdasarkan pengalaman nyata, bukan contoh rekaan.

## Tugas 1 — setup dan membaca pohon

- Permintaan: menyiapkan lingkungan, membuat tiga contoh Python (fungsi, if/else, kelas), menulis prediksi sebelum parse, menampilkan node anonim dan pemulihan error, serta menyimpan output dan tes.
- Bantuan AI: `t1.py`, empat fixture, prediksi berlabel AI, unit test tanpa dependensi tambahan, output aktual, dan dokumentasi. AI tidak membuat bukti tulisan tangan pengguna.
- Lingkungan aktual: Python sistem 3.9.6 terlalu lama; dipakai Python 3.12.15 melalui uv, Node.js 26.12.0, Apple Clang 21.0.0, CLI lokal 0.25.10; binding `tree-sitter` 0.25.2 dan grammar Python/JavaScript 0.25.0.
- Kekurangan yang benar-benar ditemukan: prediksi AI untuk `(string)` belum memuat anak `string_start`, `string_content`, `string_end`. Prediksi awal tetap disimpan; perbandingan aktual menjelaskan selisihnya. npm melewati lifecycle installer CLI sehingga package terpasang belum cukup; installer resminya dijalankan secara eksplisit.
- Bukti TDD aktual: prediksi disimpan sebelum parse contoh; tes pertama gagal dengan empat `FileNotFoundError` sebelum fixture dibuat. Tes keluaran/main guard kemudian juga gagal karena `t1.py` belum ada (total lima error pada dua tes). Setelah implementasi, kedua tes lulus.
- Cara membuktikan: `python scripts/cek_setup.py` mencetak `module` tanpa error; `python -m unittest discover -s tests -p test_tugas_awal.py -v` lulus 2 tes; `python -m unittest discover -s tests -v` juga lulus 2 tes; `python tugas1-3/t1.py > tugas1-3/output/t1.txt` menghasilkan tiga `has_error: False`, klasifikasi anonim `def`, `:`, `(`, `)`, serta `ERROR`/`has_error: True` untuk fungsi tanpa `:`. Tes memastikan string `"José"` utuh saat slice byte didekode UTF-8 dan import skrip tidak mencetak output.
- Status: kode dan bukti mesin Tugas 1 tersedia; checklist tulisan tangan pengguna masih pending di `tugas1-3/perkiraan.md`. Playground dan pemahaman pribadi pengguna belum diverifikasi. Generate CLI akan dibuktikan pada tugas grammar.
