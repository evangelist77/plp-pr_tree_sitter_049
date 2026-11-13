# Tugas 1–3

## Tugas 1 — membaca pohon

Jalankan dari root repo dengan virtualenv aktif:

```bash
python scripts/cek_setup.py
python -m unittest discover -s tests -p test_tugas_awal.py -v
python tugas1-3/t1.py > tugas1-3/output/t1.txt
```

- `contoh/fungsi.py`: fungsi `sapa(nama)` yang mengembalikan `nama`.
- `contoh/kondisi.py`: if/else dengan string UTF-8 `"José"`.
- `contoh/kelas.py`: kelas dengan satu method.
- `contoh/rusak.py`: fungsi tanpa `:`, sengaja tidak valid; diparse sebagai data, bukan dijalankan sebagai Python.
- `perkiraan.md`: prediksi AI yang ditulis sebelum parse, perbandingan aktual, serta bagian tulisan tangan pengguna yang masih kosong.
- `output/t1.txt`: keluaran aktual, termasuk penanda `ERROR` pada contoh rusak.

`children` mencakup semua anak langsung: pada fungsi ada `def`, `identifier`, `parameters`, `:`, dan `block`. `named_children` hanya memuat `identifier`, `parameters`, dan `block`; `def` serta `:` anonim. Tanda `(` dan `)` juga anonim, tetapi berada satu tingkat lebih dalam, di `children` dari `parameters`. Jadi S-expression node bernama menyembunyikan token tersebut, bukan membuangnya dari pohon.

Prediksi struktur fungsi/kelas sesuai. Prediksi kondisi kurang rinci: `(string)` aktual memuat `string_start`, `string_content`, dan `string_end`. Parser versi ini memberi node `ERROR` untuk `:` yang hilang, dengan `has_error=True`.

## Lingkungan yang benar-benar diuji

- Python sistem 3.9.6; eksekusi menggunakan Python 3.12.15 dari `uv venv --python 3.12 .venv`.
- Dependensi dipasang dengan `uv pip install --python .venv/bin/python -r requirements.txt`: `tree-sitter` 0.25.2, `tree-sitter-python` 0.25.0, `tree-sitter-javascript` 0.25.0.
- Node.js 26.12.0 dan Apple Clang 21.0.0 (arm64).

## Checklist penyerahan Tugas 1

- [x] Tiga contoh valid, pohon aktual, prediksi AI, dan perbandingan aktual tersedia.
- [x] Node bernama dan minimal tiga node anonim ditunjukkan.
- [x] Contoh rusak menunjukkan `ERROR`.
- [ ] Pengguna menambahkan bukti perkiraan tulisan tangan dan perbandingan sendiri; AI tidak mengisi atau mengklaim bukti ini.

Tugas 2–3 belum dikerjakan.

CLI lokal yang teruji: `tree-sitter 0.25.10` (`da6fe9beb4f7f67beb75914ca8e0d48ae48d6406`). Instalasi berada di `.venv/` yang diabaikan Git:

```bash
npm install --prefix .venv/tree-sitter-cli tree-sitter-cli@0.25.10
# npm versi lingkungan ini melewati lifecycle install; jalankan installer resmi:
(cd .venv/tree-sitter-cli/node_modules/tree-sitter-cli && node install.js)
export PATH="$PWD/.venv/tree-sitter-cli/node_modules/.bin:$PATH"
tree-sitter --version
```

Generator CLI belum diuji pada Tugas 1; Tugas 4 akan menguji generate dan corpus dengan CLI ini.
