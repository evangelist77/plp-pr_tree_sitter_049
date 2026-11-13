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

## Tugas 2 — penjelajah rekursif

```bash
python tugas1-3/jelajah.py tugas1-3/contoh/fungsi.py
python tugas1-3/jelajah.py /Users/hafizfs/Documents/plp-pr_tree_sitter_049-bahan-uji/click/src/click/core.py > tugas1-3/output/t2.txt
```

`jelajah(node, kedalaman=0, field=None)` mencetak node bernama dengan dua spasi per tingkat, field bila tersedia, dan posisi `[baris:kolom]`. Baris dimulai dari 1; kolom adalah offset byte UTF-8 mulai dari 0. Anak ditelusuri rekursif melalui `children` dan difilter `is_named`; `field_name_for_child(i)` menggunakan indeks asli sehingga token anonim tidak menggeser label field.

`output/t2.txt` merupakan hasil aktual Click `src/click/core.py` (4018 baris), dengan asal, SHA, lisensi, dan pemeriksaan sampel di [bahan uji](../docs/bahan-uji.md). Lima tes Tugas 1–2 lulus, termasuk output persis `x = 1`, kolom UTF-8, CLI, kegagalan membaca path, dan import tanpa output.

- [x] Traversal rekursif, indentasi, posisi dan field teruji.
- [x] File nyata minimal 100 baris dan hasil output tersedia.
- [ ] Pengguna memeriksa Playground dan menambahkan bukti pribadi/tulisan tangan yang masih pending pada Tugas 1.

## Tugas 3 — tiga query Python

```bash
python tugas1-3/q.py tugas1-3/contoh/query.py tugas1-3/queries/fungsi.scm
python tugas1-3/q.py tugas1-3/contoh/query.py tugas1-3/queries/print.scm
python tugas1-3/q.py tugas1-3/contoh/query.py tugas1-3/queries/import.scm
python -m unittest discover -s tests -v
```

`q.py` membaca sumber sebagai bytes dan pola UTF-8. `jalankan(src, pola)` mengembalikan daftar baris; CLI mencetaknya. `QueryCursor.matches()` menjaga pasangan `@nama` dan `@params` dalam satu fungsi. Parameter dihitung dari anak bernama dengan mengecualikan `positional_separator` (`/`), `keyword_separator` (`*`), dan komentar. `*args` dan `**kwargs` masing-masing tetap satu parameter. Capture berawalan `_` dipakai untuk predicate dan tidak dicetak; capture lain di luar pasangan fungsi dicetak dengan baris mulai dari 1. Pola tidak valid dan path tidak terbaca menghasilkan pesan di stderr dan status nonzero tanpa traceback.

Query `print.scm` membatasi target panggilan ke `identifier` bernama `print`; `obj.print(...)` dan teks di dalam string tidak cocok. Query ini mencari bentuk sintaksis, sehingga `print` yang didefinisikan ulang tetap terdeteksi. Query import memakai field `name` untuk import biasa dan `module_name` untuk from-import. Alias diambil dari `aliased_import.name`; nama objek yang diimpor tidak dilaporkan sebagai modul.

Pembanding manual berikut dibuat AI dengan membaca [fixture](contoh/query.py), bukan bukti tulisan tangan pengguna:

| Baris sumber | Item yang dibaca langsung | Hasil yang diharapkan | Hasil aktual |
| --- | --- | --- | --- |
| 1 | `f(a, /, b=1, *args, c: int=2, **kwargs)` | `f`: 5 parameter (`a`, `b`, `args`, `c`, `kwargs`); `/` bukan parameter | `f: 5 parameter` |
| 2 | `kosong()` | `kosong`: 0 parameter | `kosong: 0 parameter` |
| 3 | `print("ya")` | 1 panggilan print langsung, baris 3 | `baris 3: print("ya")` |
| 4 | `obj.print("bukan")` | 0 panggilan print langsung | tidak tercetak |
| 5 | `"print(1)"` | 0 panggilan | tidak tercetak |
| 6 | `import os, sys as sistem` | 2 modul: `os`, `sys`; alias `sistem` diabaikan | `baris 6: os`, `baris 6: sys` |
| 7 | `from pathlib import Path` | 1 modul: `pathlib` | `baris 7: pathlib` |
| 8 | `from . import lokal` | 1 modul: `.` | `baris 8: .` |
| 9 | `from ..paket import nama` | 1 modul: `..paket` | `baris 9: ..paket` |

Total: 2 fungsi, 5 parameter, 1 panggilan print langsung, dan 5 modul. Ketiga perintah beserta keluaran aktual tersimpan di [output/t3.txt](output/t3.txt). Fixture adalah masukan parser dan tidak dijalankan: `obj` sengaja tidak didefinisikan dan import relatif hanya untuk query. Sembilan tes Tugas 1–3 lulus; kasus tambahan menguji separator `*`, nama fungsi UTF-8, error CLI, dan import skrip tanpa output.

- [x] Tiga query wajib dan pembanding setiap item tersedia.
- [x] Alias, import relatif, separator parameter, dan pengecualian string/attribute teruji.
- [ ] Pengguna memeriksa hasil dan pemahaman pribadi; bukti tulisan tangan Tugas 1 masih pending.


CLI lokal yang teruji: `tree-sitter 0.25.10` (`da6fe9beb4f7f67beb75914ca8e0d48ae48d6406`). Instalasi berada di `.venv/` yang diabaikan Git:

```bash
npm install --prefix .venv/tree-sitter-cli tree-sitter-cli@0.25.10
# npm versi lingkungan ini melewati lifecycle install; jalankan installer resmi:
(cd .venv/tree-sitter-cli/node_modules/tree-sitter-cli && node install.js)
export PATH="$PWD/.venv/tree-sitter-cli/node_modules/.bin:$PATH"
tree-sitter --version
```

Generator CLI belum diuji pada Tugas 1; Tugas 4 akan menguji generate dan corpus dengan CLI ini.
