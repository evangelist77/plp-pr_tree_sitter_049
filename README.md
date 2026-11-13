# Praktikum Tree-sitter

Implementasi wajib Tugas 1–6 dan bukti mesin tersedia. Verifikasi ulang 13 November 2026: **15 tes Python dan 17 corpus grammar lulus**. Bukti tulisan tangan, Playground, pemahaman/demo pribadi, serta dokumen pengumpulan masih terbuka; implementasi selesai tidak berarti seluruh pengumpulan selesai.

## Setup dari checkout bersih

Prasyarat: Python 3.10+, Node.js, compiler C (Clang/GCC), Git, dan `uv` untuk contoh berikut. Di Windows gunakan WSL sesuai materi. Jalankan dari root repo:

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install --python .venv/bin/python -r requirements.txt
npm install --prefix .venv/tree-sitter-cli tree-sitter-cli@0.25.10
export PATH="$PWD/.venv/tree-sitter-cli/node_modules/.bin:$PATH"
tree-sitter --version
python scripts/cek_setup.py
```

Jika npm melewati lifecycle installer dan binary belum tersedia, jalankan installer resmi dari root lalu cek versi lagi:

```bash
(cd .venv/tree-sitter-cli/node_modules/tree-sitter-cli && node install.js)
tree-sitter --version
```

Lingkungan aktual: Python **3.12.15**, Node.js **26.12.0**, Apple Clang **21.0.0**, CLI **0.25.10** (`da6fe9beb4f7f67beb75914ca8e0d48ae48d6406`), binding `tree-sitter` **0.25.2**, grammar Python/JavaScript **0.25.0**. Python sistem 3.9.6 terlalu lama. Batas versi dependensi tetap `>=0.25,<0.26`; skrip memakai API `Parser(Language(...))`, `Query`, dan `QueryCursor`.

## Reproduksi Tugas 1–6

Semua perintah berikut dijalankan dari root dengan virtualenv dan PATH CLI di atas aktif. Siapkan clone Click pada SHA tetap mengikuti [bahan uji](docs/bahan-uji.md) sebelum Tugas 2/6. Path absolut di contoh mengikuti lingkungan pengujian ini; sesuaikan bila checkout/clone dipindah.

```bash
python scripts/cek_setup.py
python -m unittest discover -s tests -v
python tugas1-3/t1.py
python tugas1-3/jelajah.py tugas1-3/contoh/fungsi.py
python tugas1-3/jelajah.py /Users/hafizfs/Documents/plp-pr_tree_sitter_049-bahan-uji/click/src/click/core.py > tugas1-3/output/t2.txt
python tugas1-3/q.py tugas1-3/contoh/query.py tugas1-3/queries/fungsi.scm
python tugas1-3/q.py tugas1-3/contoh/query.py tugas1-3/queries/print.scm
python tugas1-3/q.py tugas1-3/contoh/query.py tugas1-3/queries/import.scm
python cek/cek.py cek/uji
python cek/cek.py /Users/hafizfs/Documents/plp-pr_tree_sitter_049-bahan-uji/click > cek/output/repo-nyata.txt
```

Untuk Tugas 4–5, pindah ke folder grammar. Buat konfigurasi lokal **sekali** memakai [potongan setup highlighting](tree-sitter-filter/README.md#tugas-5-highlighting), lalu jalankan:

```bash
cd tree-sitter-filter
tree-sitter generate
tree-sitter test
tree-sitter dump-languages --config-path ../.venv/filter-cli.json
tree-sitter parse contoh.filter --config-path ../.venv/filter-cli.json
tree-sitter query queries/highlights.scm contoh.filter --config-path ../.venv/filter-cli.json > output/captures.txt
tree-sitter highlight --html contoh.filter --config-path ../.venv/filter-cli.json > output/highlight.html
cd ..
```

Untuk pengulangan, gunakan `.venv/filter-cli.json` yang sudah ada dan lewati pembuatannya. Setelah checkout dipindah, pakai nama konfigurasi lokal baru dengan path induk grammar yang sesuai, lalu sesuaikan `--config-path`; jangan timpa konfigurasi pengguna. Jangan ulangi `tree-sitter init`: grammar sudah diinisialisasi dan sumber generate sudah tersedia. `src/parser.c` tidak diedit manual.

## Bukti dan batas pemeriksaan

| Tugas | Bukti yang tersedia |
| --- | --- |
| 1 | [Prediksi AI dan perbandingan](tugas1-3/perkiraan.md), [pohon aktual](tugas1-3/output/t1.txt), node anonim dan ERROR |
| 2 | [Penjelajah dan petunjuk](tugas1-3/README.md), Click `core.py` 4018 baris, output 15307 baris |
| 3 | [Tiga query dan pembanding sumber](tugas1-3/README.md#tugas-3--tiga-query-python), [output](tugas1-3/output/t3.txt): 2 fungsi, 1 print, 5 modul |
| 4 | [Grammar dan 17 corpus](tree-sitter-filter/README.md), prioritas, `in`, `contains`, input rusak |
| 5 | [38 capture](tree-sitter-filter/output/captures.txt), [HTML enam warna](tree-sitter-filter/output/highlight.html), screenshot eksternal |
| 6 | [Cara kerja CLI](cek/README.md), [4 laporan fixture](cek/output/uji.txt), [136 laporan Click](cek/output/repo-nyata.txt), [dua file acak dan pembanding sumber](cek/verifikasi-manual.md) |

Fixture sintaks rusak sengaja diparse sebagai data; jangan dijalankan atau dijadikan sasaran `compileall`. Temuan TODO, fungsi panjang, dan sintaks rusak dibuktikan pada fixture; pemindaian Click tidak harus menghasilkan ketiga kategori bila sumbernya tidak mengandung semuanya. Pemeriksaan sumber oleh AI bukan bukti manual pengguna.

[Catatan AI per tugas](docs/catatan-ai.md) menyimpan temuan yang benar-benar terjadi. [Review lengkap dan pemetaan rubrik 10/15/15/20/10/20/10](docs/review-pengerjaan.md#pemetaan-rubrik-dan-verifikasi-tugas-7) mempertahankan seluruh review independen, termasuk temuan dan persetujuan perbaikan Tugas 6. Tidak ada kesalahan implementasi yang ditemukan untuk Tugas 2/3; syarat catatan kesalahan per tugas tersebut tetap terbuka.

## Dokumen dan tindakan pengguna yang belum selesai

Dokumen Task 8 **direncanakan, belum dibuat pada verifikasi Task 7**:

- `/Users/hafizfs/Documents/plp-pr_tree_sitter_049-laporan/laporan.docx` — maksimal 3 halaman.
- `/Users/hafizfs/Documents/plp-pr_tree_sitter_049-laporan/proposal-draf.docx` — maksimal 1 halaman.

Screenshot Tugas 5 sudah tersedia di `/Users/hafizfs/Documents/plp-pr_tree_sitter_049-laporan/bukti/tugas-5-highlight-20261113-102832.png`. Dokumen dan bukti eksternal tidak di-stage/commit/push oleh agent. Materi meminta `laporan.pdf` dan `proposal-draf.pdf`; DOCX bukan pengganti PDF. Pengguna perlu melengkapi perkiraan tulisan tangan/perbandingan sendiri, kegiatan Playground, pemahaman/demo kode, memeriksa dokumen, mengekspor PDF, dan melakukan push dokumen secara manual saat pengumpulan. Pengayaan tidak dikerjakan.

Panduan dan tenggat relatif ada di [materi asli](Part%201%20-%20Tree-sitter.md): satu repo GitHub atau ZIP, satu minggu setelah Pertemuan 2. Tanggal pertemuan belum diberikan sehingga tanggal tenggat pasti belum ditetapkan.
