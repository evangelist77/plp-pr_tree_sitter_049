# Bahan uji nyata Tugas 2

- Proyek: Click, https://github.com/pallets/click.git.
- Clone aktual (13 November 2026), di luar repo tugas:

```bash
git clone https://github.com/pallets/click.git /Users/hafizfs/Documents/plp-pr_tree_sitter_049-bahan-uji/click
git -C /Users/hafizfs/Documents/plp-pr_tree_sitter_049-bahan-uji/click rev-parse HEAD
```

- SHA aktual: `e38188e9e205005d5af5f9e59df51904c984586a`.
- Lisensi: BSD-3-Clause; `LICENSE.txt` menyebut Copyright 2014 Pallets dan tiga syarat redistribusi. Sumber asli tetap di clone eksternal, tidak disalin ke repo tugas.
- Berkas: `src/click/core.py`, aktual 4018 baris (`wc -l`, dikonfirmasi `len(read_bytes().splitlines())`), memenuhi minimal 100 baris.

```bash
.venv/bin/python tugas1-3/jelajah.py /Users/hafizfs/Documents/plp-pr_tree_sitter_049-bahan-uji/click/src/click/core.py > tugas1-3/output/t2.txt
```

Output aktual berisi 15307 baris. Parse file yang sama memberi `has_error: False`.

## Pemeriksaan sumber dan output

Pengecekan berikut dilakukan dengan membaca baris sumber dan output, lalu mengonfirmasi node langsung melalui parser (bukan Playground):

| Sumber | Output aktual | Hasil |
|---|---|---|
| Baris 62, `def _complete_visible_commands(` | Baris output 329: dua spasi + `function_definition [62:0]`; 330: empat spasi + `name: identifier [62:4]` | Tipe, posisi fungsi, dan nama sesuai; node anak lebih dalam satu tingkat. |
| Baris 197, `class ParameterSource(enum.IntEnum):` | Baris output 942: dua spasi + `class_definition [197:0]`; 943: empat spasi + `name: identifier [197:6]` | Kelas dan field nama sesuai dengan teks sumber. |
| Baris 63, `ctx: Context, incomplete: str` | Baris output 334: delapan spasi + `type: type [63:9]`, kemudian `identifier [63:9]` di kedalaman berikutnya | Field `type` berada pada child sesudah token `:` anonim; label tetap benar karena indeks memakai semua `children`. |

Baris dimulai dari 1 dan kolom byte UTF-8 dari 0. Tes `é = 1` memverifikasi integer `[1:5]`. Pemeriksaan Playground dan bukti tulisan tangan/perbandingan pribadi pengguna masih pending; pemeriksaan mesin ini tidak menggantikannya.
