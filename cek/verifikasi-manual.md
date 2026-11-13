# Verifikasi sumber Tugas 6

Pemeriksaan ini dilakukan AI pada 13 November 2026 dengan membaca sumber bernomor
(`nl -ba`), menghitung rentang inklusif, dan membandingkan laporan aktual.
Ini bukan klaim pekerjaan manual pengguna.

## Repo dan sampling yang dapat diulang

Click eksternal: `/Users/hafizfs/Documents/plp-pr_tree_sitter_049-bahan-uji/click`,
SHA aktual `e38188e9e205005d5af5f9e59df51904c984586a` (dicek ulang dengan
`git rev-parse HEAD`). Asal dan lisensi: [bahan uji](../docs/bahan-uji.md).
Seed **20261113**, **91** kandidat, pemilihan tanpa mengganti seed:

```python
from pathlib import Path
import random
root = Path('/Users/hafizfs/Documents/plp-pr_tree_sitter_049-bahan-uji/click')
files = sorted(p.relative_to(root).as_posix() for p in root.rglob('*.py')
               if not {'.git', '.venv', 'venv', 'node_modules'}
               & set(p.relative_to(root).parts))
print(random.Random(20261113).sample(files, 2))
```

Urutan hasil: `src/click/decorators.py`, `examples/colors/colors.py`.
Kedua sumber dibaca penuh. Pembanding independen memakai `ast.parse`,
`ast.walk` pada FunctionDef/AsyncFunctionDef dan `end_lineno - lineno + 1`;
komentar diperiksa dengan `tokenize.generate_tokens`, dan `compile(..., 'exec')`
berhasil untuk keduanya tanpa menjalankan kodenya. Pembanding tidak mengimpor
checker atau menggunakan query Tree-sitter. Hitungan sumber berikut menjadi
acuan, lalu dibandingkan dengan `output/repo-nyata.txt`.

## decorators.py (621 baris)

Tidak ada komentar TODO/FIXME; komentar penjelas varian overload, type-ignore,
dan metadata dibaca pada sumber. Tidak ada kesalahan sintaks; compile berhasil.
Fungsi panjang yang terlihat pada sumber:

| Nama | Rentang def–akhir | Hitungan inklusif | CLI | Selisih |
|---|---|---:|---:|---:|
| make_pass_decorator | 47–93 | 47 | 47 | 0 |
| pass_meta_key | 96–126 | 31 | 31 | 0 |
| command (implementasi) | 164–251 | 88 | 88 | 0 |
| decorator (nested command) | 213–246 | 34 | 34 | 0 |
| version_option | 417–552 | 136 | 136 | 0 |
| callback (nested version_option) | 495–542 | 48 | 48 | 0 |
| custom_version_option | 555–594 | 40 | 40 | 0 |

Semua fungsi lainnya juga diperiksa; format berikut `nama: awal–akhir = N`.
Def di dalam docstring baris 59/61 bukan fungsi sumber.

```text
pass_context: 24–32 = 9; new_func: 29–30 = 2
pass_obj: 35–44 = 10; new_func: 41–42 = 2
decorator: 72–91 = 20; new_func: 73–89 = 17
decorator: 111–117 = 7; new_func: 112–115 = 4
command overload: 134–134 = 1; 140–144 = 5; 149–154 = 6; 159–161 = 3
group overload: 259–259 = 1; 265–269 = 5; 274–279 = 6; 284–286 = 3
group: 289–307 = 19; _param_memo: 310–317 = 8
argument: 320–345 = 26; decorator: 341–343 = 3
option: 348–373 = 26; decorator: 369–371 = 3
confirmation_option: 376–397 = 22; callback: 385–387 = 3
password_option: 400–414 = 15
show_version: 579–584 = 6
help_option: 597–621 = 25; show_help: 606–610 = 5
```

Ada 35 fungsi nyata (7 panjang, 28 tidak panjang). CLI mengeluarkan tepat 7
baris pada file ini, semuanya nama/baris/panjang sesuai tabel.

## examples/colors/colors.py (39 baris)

Sumber berisi daftar warna baris 4–21, dekorator baris 24, dan satu fungsi
`cli` pada 25–39: **39 − 25 + 1 = 15** baris. Tidak melebihi 30.
Tidak ada komentar TODO/FIXME atau sintaks rusak, compile berhasil.
CLI tidak mengeluarkan baris untuk file ini; tepat sesuai sumber.

| File | TODO/FIXME sumber / CLI | Fungsi panjang sumber / CLI | Error sumber / CLI | Selisih total |
|---|---|---|---|---:|
| src/click/decorators.py | 0 / 0 | 7 / 7 | 0 / 0 | 0 |
| examples/colors/colors.py | 0 / 0 | 0 / 0 | 0 / 0 | 0 |

Pemindaian seluruh clone menghasilkan **136** baris laporan; angka ini bukan
klaim bahwa semua file repo telah diperiksa manual.

## Fixture lokal

- `uji/todo.py`: baris 1 string TODO diabaikan; komentar TODO di 2 dan FIXME di 3
  cocok dengan dua laporan.
- `uji/panjang.py`: `tepat_batas` 1–30 = 30 tidak dilaporkan;
  `terlalu_panjang` 33–63 = 31 dilaporkan di 33.
- `uji/rusak.py`: assignment tanpa nilai di baris 1 menghasilkan ERROR dan
  satu laporan sintaks di 1.
- Unit test terpisah memakai `def f(:\n    pass\n`, yang pohonnya benar-benar
  mempunyai `MISSING ")"`; laporan di 1. Unit test juga menguji nested/method,
  dua error dalam file (hanya yang pertama), dan byte komentar invalid.
