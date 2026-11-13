# Catatan penggunaan AI

## Setup awal repositori

- Permintaan: membuat struktur awal sesuai materi, melakukan commit, dan menjelaskan hasilnya.
- Bantuan AI: kerangka folder, README, daftar dependensi, `.gitignore`, dan skrip cek setup dari contoh materi.
- Status saat setup awal: Tugas 1–6 belum dikerjakan. Kini implementasi dan bukti mesin tersedia pada catatan per tugas di bawah.
- Keterbatasan saat setup awal: CLI belum tersedia; kemudian CLI lokal 0.25.10 dipasang dan generate/parse/test berhasil pada Tugas 4–5.

Catatan ini melaporkan riwayat nyata; tes merah karena file belum dibuat bukan kesalahan hasil AI. Ringkasannya akan masuk dokumen Task 8 yang masih direncanakan. Tidak membuat kekurangan rekaan untuk memenuhi rubrik.

## Tugas 1 — setup dan membaca pohon

- Permintaan: menyiapkan lingkungan, membuat tiga contoh Python (fungsi, if/else, kelas), menulis prediksi sebelum parse, menampilkan node anonim dan pemulihan error, serta menyimpan output dan tes.
- Bantuan AI: `t1.py`, empat fixture, prediksi berlabel AI, unit test tanpa dependensi tambahan, output aktual, dan dokumentasi. AI tidak membuat bukti tulisan tangan pengguna.
- Lingkungan aktual: Python sistem 3.9.6 terlalu lama; dipakai Python 3.12.15 melalui uv, Node.js 26.12.0, Apple Clang 21.0.0, CLI lokal 0.25.10; binding `tree-sitter` 0.25.2 dan grammar Python/JavaScript 0.25.0.
- Kekurangan yang benar-benar ditemukan: prediksi AI untuk `(string)` belum memuat anak `string_start`, `string_content`, `string_end`. Prediksi awal tetap disimpan; perbandingan aktual menjelaskan selisihnya. npm melewati lifecycle installer CLI sehingga package terpasang belum cukup; installer resminya dijalankan secara eksplisit.
- Bukti TDD aktual: prediksi disimpan sebelum parse contoh; tes pertama gagal dengan empat `FileNotFoundError` sebelum fixture dibuat. Tes keluaran/main guard kemudian juga gagal karena `t1.py` belum ada (total lima error pada dua tes). Setelah implementasi, kedua tes lulus.
- Cara membuktikan: `python scripts/cek_setup.py` mencetak `module` tanpa error; `python -m unittest discover -s tests -p test_tugas_awal.py -v` lulus 2 tes; `python -m unittest discover -s tests -v` juga lulus 2 tes; `python tugas1-3/t1.py > tugas1-3/output/t1.txt` menghasilkan tiga `has_error: False`, klasifikasi anonim `def`, `:`, `(`, `)`, serta `ERROR`/`has_error: True` untuk fungsi tanpa `:`. Tes memastikan string `"José"` utuh saat slice byte didekode UTF-8 dan import skrip tidak mencetak output.
- Status: kode dan bukti mesin Tugas 1 tersedia; checklist tulisan tangan pengguna masih pending di `tugas1-3/perkiraan.md`. Playground dan pemahaman pribadi pengguna belum diverifikasi. Generate CLI kemudian dibuktikan pada Tugas 4–5.


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

## Tugas 4 — grammar DSL filter

- Permintaan: grammar bertahap dengan perbandingan, boolean, `or/and/not`, kurung, field, `in`, dan `contains`; minimal lima corpus dan sumber parser hasil generate.
- Bantuan AI: grammar, metadata, 17 corpus dengan expected tree eksplisit, generate parser, contoh dan dokumentasi. Scaffolding binding yang tidak diperlukan dihapus.
- Kekurangan hasil AI yang benar-benar ditemukan: ekspektasi pemulihan input rusak pada corpus awal tidak sama dengan parse aktual. `in ()` disangka menyisipkan number tetapi aktual boolean dengan MISSING true; perbandingan tanpa nilai aktual MISSING string; argumen contains yang salah berada sebagai number/identifier di ERROR, bukan UNEXPECTED.
- Reproduksi/bukti: jalankan `tree-sitter test` dari `tree-sitter-filter/`, baca expected tree empat kasus terakhir di `test/corpus/dasar.txt`; riwayat awal dan koreksi ada di review T4 dalam [riwayat review lengkap](review-pengerjaan.md) (laporan pelaksanaan lokal: `.superpowers/sdd/2026-11-13-tugas-tree-sitter/task-4-report.md`). Ekspektasi kemudian dikoreksi secara eksplisit setelah AI membaca pohon aktual, bukan perbaikan grammar produksi dan bukan pekerjaan manual pengguna. Pemeriksaan parser terkompilasi juga memastikan empat input memiliki `has_error`.
- Verifikasi: generate berhasil dan 17/17 corpus lulus, termasuk prioritas, asosiativitas, keyword-prefix, in nonkosong dan contains string. Warning parser-directory saat awal T4 ditangani dengan config lokal pada T5; warning slow parse rate tetap dicatat di laporan asli.

## Tugas 5 — query highlighting

- Permintaan: keyword, operator, string, number, boolean, dan property berwarna pada satu contoh lengkap; query/HTML dan screenshot nyata.
- Bantuan AI: delapan pola query, contoh lengkap, config demonstrasi lokal enam warna, output capture dan HTML, serta screenshot browser yang diperiksa reviewer.
- Kekurangan yang benar-benar ditemukan: percobaan discovery memakai induk checkout menghasilkan `dump-languages` kosong walau status 0. CLI tidak menemukan grammar yang bersarang di checkout itu. Path diubah menjadi root checkout, induk langsung `tree-sitter-filter/`. Ini koreksi konfigurasi operasional, bukan bug query atau bukti perubahan konfigurasi global.
- Reproduksi: `tree-sitter dump-languages --config-path ../.venv/filter-cli.json` dari folder grammar menampilkan `source.filter`, query, dan ekstensi filter bila direktori penemuan benar; ulangi query/highlight mengikuti [README grammar](../tree-sitter-filter/README.md). Riwayat discovery gagal dan koreksi tercatat di review T5 dalam [riwayat review lengkap](review-pengerjaan.md) (laporan pelaksanaan lokal: `.superpowers/sdd/2026-11-13-tugas-tree-sitter/task-5-report.md`).
- Verifikasi: 38 capture mencakup enam kategori dan semua operator/keyword, 17 corpus lulus; HTML ditampilkan di browser dan screenshot eksternal tersedia di path pada README root. Reviewer melihat screenshot langsung. Pembuatan config eksklusif menolak overwrite; pengulangan memakai file yang sudah ada.

## Tugas 6 — checker Python

- Permintaan: CLI komentar TODO/FIXME, fungsi >30 baris termasuk def, dan ERROR/MISSING pertama; uji folder dan repo nyata, lalu sampling dua file.
- Bantuan AI: checker, lima tes kontrak, tiga fixture, output CLI, README, dan pemeriksaan sumber bernomor serta pembanding AST/tokenize/compile. Tidak mengklaim pekerjaan manual pengguna.
- Bukti TDD: kelima tes pertama gagal dengan FileNotFoundError sebelum checker ada. Implementasi awal lulus empat tes tetapi tes byte rusak benar-benar menemukan UnicodeDecodeError di predicate `#match?`, sebelum decoding output; input lalu dinormalisasi UTF-8 dengan errors=replace sebelum parse.
- Verifikasi aktual sesudah perbaikan: `.venv/bin/python -m unittest discover -s tests -v` lulus 14 tes, termasuk sembilan tes T1–3. Fixture menghasilkan empat laporan. Clone Click SHA `e38188e9e205005d5af5f9e59df51904c984586a` menghasilkan 136 laporan.
- Sampling seed 20261113 dari 91 path terurut memilih `src/click/decorators.py` dan `examples/colors/colors.py`; sumber dibaca penuh oleh AI dan hitungan independen memberi selisih 0 pada ketiga kategori. Rincian ada di `cek/verifikasi-manual.md`. Pengayaan JavaScript tidak dikerjakan.
- Temuan reviewer T6 yang benar-benar terjadi: validasi folder awal `Path.is_dir()` masih di luar penanganan OSError; PermissionError dapat lolos sebagai traceback. Regresi baru dibuktikan merah (`PermissionError: stat ditolak`), validasi dipindahkan ke try yang sudah ada, lalu tes terfokus dan seluruh 15 tes lulus. Output/format laporan tidak berubah.

## Status akhir Tugas 7 dan celah rubrik

- Semua perintah setup-check, 15 tes Python, T1–3, generate/17 corpus/parse/query/highlight, serta CLI fixture dan Click diulang dan dibaca hasilnya pada 13 November 2026. Output T2, capture, HTML, dan pemindaian Click identik dengan artefak tersimpan. [Pemetaan rubrik dan riwayat review](review-pengerjaan.md#pemetaan-rubrik-dan-verifikasi-tugas-7) merinci bukti dan celahnya.
- **Tugas 2 dan Tugas 3 belum mempunyai kesalahan implementasi hasil AI yang ditemukan.** Keduanya tetap memenuhi perilaku mesin yang diuji, tetapi syarat catatan minimal satu kesalahan/kekurangan hasil AI per tugas belum terpenuhi untuk keduanya. Tidak mengubah keterbatasan yang sudah disengaja atau tes sebelum implementasi menjadi cerita bug.
- Perkiraan tulisan tangan, kegiatan Playground, pembanding/pemahaman pribadi, dan demo pengguna tetap pending. Hitungan/pembacaan sumber oleh AI diberi label dan tidak diklaim sebagai bukti pengguna.
- `laporan.docx` (maks. 3 halaman) dan `proposal-draf.docx` (maks. 1 halaman) pada direktori eksternal `.../plp-pr_tree_sitter_049-laporan/` masih direncanakan untuk Task 8, belum dibuat pada verifikasi Task 7. Format pengumpulan tetap PDF; pengguna mengekspor dan push dokumen secara manual.
