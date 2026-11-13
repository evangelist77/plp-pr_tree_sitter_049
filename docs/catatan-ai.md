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


## Tugas 2 — penjelajah node

- Permintaan: traversal rekursif node bernama, field, posisi, CLI file bytes, dan uji pada Python nyata minimal 100 baris.
- Bantuan AI: `jelajah.py`, tiga tes tambahan, output aktual Click, dan dokumentasi sumber/SHA/lisensi di `bahan-uji.md`.
- Bukti TDD aktual: sebelum implementasi, tiga tes baru gagal dengan `FileNotFoundError` karena `jelajah.py` belum ada, sedangkan dua tes Tugas 1 tetap lulus. Setelah implementasi, `python -m unittest discover -s tests -v` lulus semua lima tes.
- Verifikasi: output tepat untuk `x = 1`, integer UTF-8 `[1:5]`, CLI berhasil, path hilang menampilkan kesalahan tanpa traceback, import diam. Click `src/click/core.py` 4018 baris menghasilkan 15307 baris output dan `has_error: False`; fungsi baris 62, kelas baris 197, dan field `type` baris 63 dicocokkan dengan sumber dan parser.
- Kekurangan hasil AI yang benar-benar ditemukan: belum ada kesalahan implementasi yang ditemukan pada pemeriksaan ini; tidak dibuat contoh kesalahan rekaan.
- Batas: belum ada pemeriksaan Playground oleh pengguna. Bukti tulisan tangan/perbandingan pribadi pengguna tetap pending; AI tidak mengklaimnya selesai. Pengayaan TreeCursor tidak dikerjakan.

## Tugas 3 — query Python

- Permintaan: tiga query wajib untuk fungsi/parameter, pemanggilan print langsung, dan modul import, dengan penjalan CLI dan pembanding fixture.
- Bantuan AI: `q.py`, tiga pola `.scm`, `contoh/query.py`, empat tes tambahan, output aktual, dan tabel pembanding berdasarkan pembacaan sumber oleh AI. Tabel bukan tulisan tangan pengguna.
- Bukti TDD: sebelum `q.py` dan query dibuat, suite berisi sembilan tes menghasilkan empat error pada tes T3 karena skrip belum tersedia; lima tes T1–2 tetap lulus. Sesudah implementasi, `.venv/bin/python -m unittest discover -s tests -v` lulus sembilan tes.
- Verifikasi: fixture menghasilkan `f: 5 parameter`, `kosong: 0 parameter`, satu print langsung pada baris 3, serta modul `os`, `sys`, `pathlib`, `.`, `..paket` pada baris 6–9. Tes tambahan menguji `*` sebagai separator, nama UTF-8, path sumber/pola hilang, pola invalid, pola bukan UTF-8, dan import skrip tanpa output.
- Kekurangan hasil AI yang benar-benar ditemukan: belum ditemukan kesalahan implementasi pada pemeriksaan ini; tidak mengarang kesalahan untuk memenuhi rubrik. Contoh hitungan `named_child_count` dalam materi tidak cukup untuk `/` dan `*` bernama; implementasi mengecualikannya berdasarkan pohon fixture aktual.
- Batas: query print bersifat sintaksis dan tidak menyelesaikan binding nama. Fixture hanya diparse, tidak dieksekusi. Docstring sebagai pengayaan tidak dikerjakan; pemeriksaan pribadi pengguna masih terbuka.
