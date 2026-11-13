# Bahan uji nyata Tugas 2 dan 6

- Proyek: Click, https://github.com/pallets/click.git.
- Clone aktual (13 November 2026), di luar repo tugas. Untuk checkout baru, jalankan dari root repo tugas; clone hanya bila tujuan belum ada. Jangan checkout ulang clone yang berisi perubahan pengguna. Pin SHA diperlukan karena HEAD proyek dapat berubah:

```bash
git clone https://github.com/pallets/click.git /Users/hafizfs/Documents/plp-pr_tree_sitter_049-bahan-uji/click
git -C /Users/hafizfs/Documents/plp-pr_tree_sitter_049-bahan-uji/click checkout --detach e38188e9e205005d5af5f9e59df51904c984586a
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


## Pemakaian Tugas 6 dan verifikasi ulang

Dari root repo tugas, setelah setup virtualenv pada README root:

```bash
source .venv/bin/activate
python cek/cek.py cek/uji
python cek/cek.py /Users/hafizfs/Documents/plp-pr_tree_sitter_049-bahan-uji/click > cek/output/repo-nyata.txt
```

Hasil aktual: empat laporan fixture (dua komentar, satu fungsi panjang, satu sintaks rusak) dan 136 laporan untuk Click. Repo nyata tidak wajib mengandung semua jenis temuan; fixture memastikan ketiga kategori. [Verifikasi dua file acak](../cek/verifikasi-manual.md) menyimpan algoritme sampling, seed 20261113, 91 kandidat, path terpilih, hitungan sumber dan pembanding independen AST/tokenize/compile. Compile tersebut hanya untuk dua file Click valid, bukan fixture sintaks rusak.

Verifikasi ulang Task 7 memeriksa SHA di atas, 4018 baris sumber, 15307 baris output T2, dan 136 laporan Click. Output T2 dan Click identik byte demi byte dengan hasil tersimpan. Path absolut adalah lokasi aktual pengujian; bila memakai direktori clone lain, ganti seluruh argumen sumber secara konsisten. Tidak perlu memasang dependensi Click karena sumber hanya dibaca dan diparse.
