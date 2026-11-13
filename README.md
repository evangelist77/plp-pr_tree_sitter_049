# Praktikum Tree-sitter

Praktikum berdasarkan `Part 1 - Tree-sitter.md`. Bukti parse Tugas 1 tersedia; bukti tulisan tangan pengguna masih pending. Tugas 2–6 belum dikerjakan.

## Setup

Prasyarat: Python 3.10+, Node.js, dan compiler C (Clang/GCC; di macOS dapat dipasang melalui `xcode-select --install`).

Jalankan dari root repo (contoh ini memakai `uv` untuk menyediakan Python 3.12):

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install --python .venv/bin/python -r requirements.txt
npm install -g tree-sitter-cli
tree-sitter --version
python scripts/cek_setup.py
```

Di Windows gunakan WSL sesuai saran materi. Paket Python menggunakan API seri 0.25 seperti contoh materi.

## Struktur dan status

- `tugas1-3/`: Tugas 1 tersedia di `t1.py`, `contoh/`, `perkiraan.md`, dan `output/t1.txt`; Tugas 2–3 belum dikerjakan.
- `tree-sitter-filter/`: grammar Tugas 4 dengan 17 corpus; query highlighting dilengkapi pada Tugas 5.
- `cek/`: tempat pemeriksa kode Tugas 6; belum diimplementasikan.
- `docs/catatan-ai.md`: catatan bantuan AI untuk diolah menjadi laporan.
- `laporan.pdf`: harus dibuat kemudian, maksimal 3 halaman.
- `proposal-draf.pdf`: harus dibuat kemudian, maksimal 1 halaman.

Panduan lengkap dan rubrik ada di `Part 1 - Tree-sitter.md`. Pengumpulan melalui satu repo GitHub atau ZIP, paling lambat satu minggu setelah Pertemuan 2. Nama repo dan visibilitasnya tidak ditentukan dalam materi.

## Memulai grammar (Tugas 4)

```bash
cd tree-sitter-filter
tree-sitter init
```

Isi nama bahasa `filter`. Ikuti langkah bertahap pada materi: mulai dari satu perbandingan, lalu tambah fitur dan kasus uji. Setelah menulis grammar dan contoh input:

```bash
tree-sitter generate
tree-sitter parse contoh.filter
tree-sitter test
```

`src/parser.c` merupakan hasil generate dan tidak diedit manual. Isi `test/corpus/` dengan tes dan `queries/highlights.scm` dengan query pada Tugas 4–5.

## Penggunaan AI

AI diperbolehkan, tetapi setiap tugas yang dibantu AI wajib dicatat: permintaan, kesalahan/kekurangan yang benar-benar ditemukan, serta bukti verifikasi. Jangan mengarang kesalahan atau hasil pengujian. Materi menyarankan Tugas 1 dan langkah 4a–4c dicoba tanpa AI terlebih dahulu.

## Menjalankan Tugas 1

```bash
source .venv/bin/activate
python scripts/cek_setup.py
python -m unittest discover -s tests -p test_tugas_awal.py -v
python tugas1-3/t1.py
```

Lingkungan verifikasi: Python 3.12.15 (Python sistem 3.9.6 terlalu lama), Node.js 26.12.0, Apple Clang 21.0.0, binding `tree-sitter` 0.25.2 serta grammar Python/JavaScript 0.25.0. Detail CLI lokal dan hasil aktual dicatat di `tugas1-3/README.md`.

Pengguna masih perlu menambahkan bukti perkiraan tulisan tangan sebelum checklist penyerahan Tugas 1 dapat ditutup.
