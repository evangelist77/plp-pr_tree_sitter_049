# Praktikum Tree-sitter

Kerangka awal Tugas 1–6 berdasarkan `Part 1 - Tree-sitter.md`. Tugas belum dikerjakan.

## Setup

Prasyarat: Python 3.10+, Node.js, dan compiler C (Clang/GCC; di macOS dapat dipasang melalui `xcode-select --install`).

Jalankan dari root repo:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
npm install -g tree-sitter-cli
tree-sitter --version
python scripts/cek_setup.py
```

Di Windows gunakan WSL sesuai saran materi. Paket Python menggunakan API seri 0.25 seperti contoh materi.

## Struktur dan status

- `tugas1-3/`: tempat skrip Python, query `.scm`, dan output `.txt` Tugas 1–3.
- `tree-sitter-filter/`: tempat proyek grammar Tugas 4–5; belum diinisialisasi.
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
