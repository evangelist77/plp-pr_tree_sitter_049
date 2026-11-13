# Tugas 6: pemeriksa kode Python

Dari root repo, gunakan Python 3.10+ (pengujian aktual Python 3.12.15):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python cek/cek.py cek/uji
python -m unittest discover -s tests -v
```

Dependensi mengikuti `requirements.txt`: binding dan grammar Tree-sitter 0.25.x.
API menggunakan `Parser(Language(...))`, `Query`, dan `QueryCursor`.
CLI menerima satu **folder**, memindai `.py` rekursif dengan `os.walk`, dan
memangkas `.git`, `.venv`, `venv`, `node_modules` sebelum turun ke subfolder.
Symlink direktori tidak diikuti. Path diurutkan leksikografis, lalu temuan per
file menurut posisi sumber; baris dimulai dari 1. Import tidak menjalankan CLI.

Output aktual fixture (juga tersimpan di [uji.txt](output/uji.txt)):

```text
cek/uji/panjang.py:33: fungsi terlalu_panjang (31 baris)
cek/uji/rusak.py:1: kesalahan sintaks
cek/uji/todo.py:2: TODO lengkapi contoh
cek/uji/todo.py:3: FIXME cek nilai
```

Komentar dicari lewat query `#match?` dengan pola case-sensitive `TODO|FIXME`;
string dan docstring diabaikan. Teks komentar ditampilkan tanpa `#` pembuka.
Byte yang bukan UTF-8 diganti U+FFFD sebelum parse agar predicate query dan
pencetakan tetap bekerja, bukan menebak encoding sumber.

Panjang fungsi adalah **`end_point[0] - start_point[0] + 1` pada
`function_definition`**, termasuk baris `def`, docstring, dan baris kosong
internal; dekorator dan baris kosong setelah akhir fungsi tidak dihitung.
Definisi ini mengikuti langkah/rubrik materi meskipun checklist menyebut body.
Fungsi 30 baris tidak dilaporkan, 31 dilaporkan. Method, async function, dan
nested function ikut dihitung masing-masing; fungsi luar juga mencakup rentang
fungsi dalamnya. Sintaks rusak dilaporkan sekali per file pada node ERROR atau
MISSING pertama menurut urutan sumber, melalui traversal rekursif.

`cek_file(Path) -> list[str]` mengembalikan laporan tanpa mencetak dan membiarkan
OSError diteruskan ke pemanggil. `main() -> int` mencetak laporan; status **0**
berarti pemindaian berhasil walaupun ada temuan, **1** berarti I/O gagal,
**2** berarti argumen salah atau path bukan folder. Pesan kegagalan ke stderr.
Kegagalan I/O dapat terjadi setelah laporan beberapa file sudah tercetak.

Uji repo nyata memakai clone Click eksternal yang sama dengan Tugas 2:

```bash
python cek/cek.py /Users/hafizfs/Documents/plp-pr_tree_sitter_049-bahan-uji/click > cek/output/repo-nyata.txt
```

SHA `e38188e9e205005d5af5f9e59df51904c984586a`, 136 baris laporan aktual di
[repo-nyata.txt](output/repo-nyata.txt). [Verifikasi sumber](verifikasi-manual.md)
mencatat seed 20261113, dua file acak dari daftar terurut, semua hitungan
kategori, rentang fungsi, serta pembanding independen AST/tokenize/compile.
Pemeriksaan sumber dilakukan AI dan tidak diklaim sebagai kerja manual pengguna.
Pengayaan JavaScript tidak dikerjakan.
