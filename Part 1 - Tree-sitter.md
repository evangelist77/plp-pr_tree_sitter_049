# Materi & Tugas Awal: Memahami Tree-sitter

## 0. Sebelum mulai

Materi ini disusun untuk mahasiswa Sarjana Terapan Teknik Informatika semester 3 dan dirancang untuk 2 pertemuan, lalu dilanjutkan dengan proyek bertopik pilihan sendiri untuk 5 pertemuan (bagian 9).

**Prasyarat** yang diasumsikan sudah dikuasai dari mata kuliah sebelumnya:

| Dari mata kuliah | Yang dipakai di materi ini |
| --- | --- |
| Algoritma & Pemrograman | Python dasar: fungsi, perulangan, `list`, `dict`, membaca file |
| Struktur Data | Pohon (tree): node, parent, child, traversal rekursif (DFS) |
| Praktikum pemrograman | Menjalankan perintah di terminal, `pip`, `npm` |
| Regex (cukup dasar) | Pola sederhana seperti `\d+` dan `[a-z]+` |

**Capaian pembelajaran.** Setelah menyelesaikan materi dan tugas, mahasiswa mampu:

1. Menjelaskan apa itu syntax tree dan mengapa editor modern memakai tree-sitter.
2. Membaca pohon hasil parse dan membedakan node bernama, node anonim, dan field.
3. Menelusuri pohon secara rekursif dengan Python.
4. Menulis query sederhana untuk mencari pola kode.
5. Menulis grammar kecil beserta kasus ujinya.
6. Merancang dan membangun tool berbasis tree-sitter yang mendukung kegiatan pengembangan aplikasi web enterprise.
7. Memakai AI coding agent secara kritis: memverifikasi hasilnya dan menentukan kapan tool deterministik lebih tepat daripada AI.


## 1. Pengantar

Tree-sitter adalah generator parser sekaligus library parsing inkremental: dari satu file grammar, ia menghasilkan parser yang mengubah kode sumber menjadi pohon sintaks (syntax tree) dan memperbaruinya dengan cepat setiap kali kode diedit.

Awalnya dibuat oleh Max Brunsfeld di GitHub untuk editor Atom. Sekarang dipakai luas, misalnya di Neovim, Helix, Zed, Emacs (`treesit`), dan fitur navigasi kode GitHub.

Masalah yang dipecahkan:

- **Highlight berbasis regex rapuh.** Regex tidak paham struktur kode, jadi warna sering salah pada kode bersarang atau multi-baris. Tree-sitter memberi highlight berdasarkan pohon sintaks yang sebenarnya.
- **Parsing ulang seluruh file itu lambat.** Tree-sitter hanya mem-parse ulang bagian yang berubah, sehingga cukup cepat untuk dijalankan di setiap ketikan.
- **Kode yang sedang diketik sering belum valid.** Tree-sitter tetap menghasilkan pohon meski ada error, dengan menandai bagian yang rusak sebagai node `ERROR` atau `MISSING`.
- **Setiap bahasa butuh tool sendiri.** Dengan satu API yang seragam, satu tool (linter, refactoring, code search) bisa mendukung banyak bahasa cukup dengan mengganti grammar.

Tujuan belajar setelah materi ini: Anda bisa membaca pohon hasil parse, menulis grammar sederhana, menulis query untuk mencari pola kode, dan memakai parser dari program Python.

## 2. Konsep inti

Lima konsep ini muncul di hampir semua pekerjaan dengan tree-sitter; pahami dulu sebelum menulis grammar.

**Kaitan dengan Struktur Data.** Pohon tree-sitter adalah pohon biasa seperti di mata kuliah Struktur Data: setiap node punya satu parent dan nol atau lebih child, dan root-nya mewakili seluruh file. Bedanya, setiap node juga menyimpan potongan teks sumber yang diwakilinya. Menelusuri pohon ini sama dengan traversal preorder (DFS) yang sudah Anda pelajari.

| Konsep | Arti | Contoh |
| --- | --- | --- |
| Concrete Syntax Tree (CST) | Pohon yang menyimpan semua token, termasuk tanda kurung dan koma, dengan posisi byte dan baris/kolom | `(`, `)`, `,` tetap ada sebagai node |
| Node bernama (named) | Node dari rule yang diberi nama di grammar; inilah yang tampil di output `tree-sitter parse` | `function_definition`, `identifier` |
| Node anonim | Node dari string literal di grammar, disembunyikan dari tampilan S-expression default | `"def"`, `":"`, `"("` |
| Field | Label peran sebuah child di dalam parent-nya, agar Anda tidak bergantung pada urutan child | `name:`, `parameters:`, `body:` |
| Error recovery | Parser tetap jalan saat input tidak valid dan menyisipkan node khusus | `(ERROR ...)`, `(MISSING ")")` |

Contoh: kode Python `def halo(nama): return nama` di-parse menjadi pohon berikut (disingkat):

```
(module
  (function_definition
    name: (identifier)
    parameters: (parameters (identifier))
    body: (block
      (return_statement (identifier)))))
```

Perhatikan: `def`, `(`, `)`, dan `:` tidak tampil karena anonim, tetapi tetap ada di pohon dan bisa diakses lewat API.

**Parsing inkremental.** Setelah teks diedit, Anda memberi tahu pohon lama posisi edit (`tree.edit(...)`), lalu mem-parse lagi dengan pohon lama sebagai acuan. Tree-sitter memakai ulang subtree yang tidak terpengaruh, jadi biaya parse sebanding dengan besar perubahan, bukan besar file.

**Tree-sitter bukan compiler.** Ia hanya mengurus sintaks: tidak ada resolusi tipe, scope lintas file, atau makna program. Analisis semantik dibangun di atas pohonnya oleh tool Anda sendiri.

## 3. Arsitektur

Tree-sitter punya dua tahap: grammar diubah menjadi parser C satu kali, lalu runtime library memakai parser itu berulang kali untuk setiap file dan setiap edit.

&#91;embedded content: alur tree-sitter · tahap build dan runtime\]

Runtime-nya ditulis dalam C tanpa dependensi, sehingga mudah dibungkus. Binding resmi tersedia untuk Rust, Node.js, Python, Go, Swift, dan WebAssembly (dipakai oleh `tree-sitter playground`). Satu `Language` yang sama bisa dipakai dari binding mana pun.

## 4. Setup lingkungan

Anda butuh tiga hal: CLI untuk membuat dan menguji grammar, compiler C untuk membangun parser, dan binding Python untuk memakainya dari program.

1. **Prasyarat.** Node.js (untuk menjalankan `grammar.js`), compiler C (`gcc`/`clang`, atau MSVC di Windows), dan Python 3.10+.
2. **Pasang CLI.** Pilih salah satu: `npm install -g tree-sitter-cli` atau `cargo install tree-sitter-cli`. Cek dengan `tree-sitter --version`.
3. **Pasang binding Python dan grammar siap pakai:**

```bash
pip install tree-sitter tree-sitter-python tree-sitter-javascript
```

4. **Uji cepat** dengan skrip berikut. Jika pohon tercetak, lingkungan Anda siap.

```python
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

tree = parser.parse(b"def halo(nama):\n    return nama\n")
print(tree.root_node)  # mencetak S-expression pohon
```

**Tips untuk laptop Windows.** Pakai WSL (Windows Subsystem for Linux) dengan Ubuntu, lalu ikuti langkah Linux: `sudo apt install build-essential nodejs npm python3-pip`. Ini biasanya lebih cepat daripada memasang Build Tools for Visual Studio. Jika laptop bermasalah, Tugas 1–3 bisa dikerjakan di Google Colab karena hanya butuh `pip install`; Tugas 4–5 tetap butuh komputer dengan compiler C (misalnya komputer lab).

Struktur proyek grammar yang dibuat oleh `tree-sitter init` (di versi CLI lama, salin dari repo grammar resmi):

| Path | Isi |
| --- | --- |
| `grammar.js` | Definisi grammar; satu-satunya file yang Anda tulis manual |
| `src/parser.c` | Parser hasil generate, jangan diedit |
| `src/scanner.c` | Opsional, external scanner untuk token yang sulit (indentasi, heredoc) |
| `queries/highlights.scm` | Query untuk syntax highlighting |
| `test/corpus/*.txt` | Kasus uji: input kode dan pohon yang diharapkan |
| `bindings/` | Kode pembungkus untuk Node, Python, Rust, dan lainnya |
| `tree-sitter.json` | Metadata grammar: nama, ekstensi file, lokasi query |

Catatan versi: API binding Python berubah di 0.22 dan 0.24. Materi ini memakai gaya 0.25 (`Parser(LANG)`, `Query`, `QueryCursor`). Jika contoh lama memakai `parser.set_language(...)` atau `Language.build_library(...)`, itu API versi sebelumnya ([dokumentasi py-tree-sitter](https://tree-sitter.github.io/py-tree-sitter/)).

## 5. Menulis grammar

Grammar ditulis sebagai objek JavaScript di `grammar.js`; rule pertama di `rules` menjadi root pohon, dan setiap rule dibangun dari beberapa fungsi kombinator.

**Grammar dalam satu kalimat.** Grammar adalah daftar aturan yang menjelaskan bentuk kode yang sah dalam suatu bahasa. Misalnya aturan `comparison → identifier operator nilai` berarti sebuah perbandingan terdiri dari nama field, operator, lalu nilai, seperti `priority > 2`. Di `grammar.js`, aturan yang sama ditulis `seq($.identifier, choice('=', '>', '<'), $._value)`. Notasi panah seperti ini disebut BNF dan akan Anda temui lagi di mata kuliah Teori Bahasa & Automata.

| Fungsi | Arti | Contoh |
| --- | --- | --- |
| `seq(a, b, ...)` | Urutan berturut-turut | `seq($.identifier, '=', $._value)` |
| `choice(a, b, ...)` | Salah satu dari pilihan | `choice($.number, $.string)` |
| `repeat(x)` / `repeat1(x)` | Nol-atau-lebih / satu-atau-lebih | `repeat($.statement)` |
| `optional(x)` | Boleh ada, boleh tidak | `optional(';')` |
| `field('nama', x)` | Memberi label peran pada child | `field('value', $._expr)` |
| `prec.left(n, x)` / `prec.right(n, x)` | Prioritas dan asosiativitas operator | `prec.left(1, seq($._expr, '+', $._expr))` |
| `token(x)` | Gabungkan menjadi satu token leksikal | `token(seq('//', /.*/))` |
| `alias(x, nama)` | Tampilkan node dengan nama lain | `alias($.identifier, $.type_name)` |

Aturan penting lain:

- **Rule berawalan `_`** (misalnya `_expr`) disembunyikan dari pohon; pakai untuk rule pembungkus seperti `choice` antar-ekspresi.
- **`extras`** berisi hal yang boleh muncul di mana saja, biasanya spasi dan komentar.
- **`word`** menunjuk rule identifier, agar kata kunci seperti `and` tidak tertukar dengan nama field.
- **`conflicts`** \[Pengayaan\] dipakai saat ambiguitas memang disengaja; parser lalu mencoba kedua jalur (GLR). Utamakan `prec` dulu sebelum menambah conflict.

Contoh grammar mini untuk **DSL filter**, yaitu bahasa kecil untuk kotak pencarian lanjutan di halaman admin aplikasi enterprise, misalnya untuk menyaring tiket atau pesanan: `status = "open" and (priority > 2 or owner = "budi")`.

```javascript
module.exports = grammar({
  name: 'filter',
  extras: $ => [/\s/],
  word: $ => $.identifier,

  rules: {
    query: $ => $._expr,

    _expr: $ => choice(
      $.comparison, $.and_expression, $.or_expression,
      $.not_expression, $.parenthesized,
    ),

    comparison: $ => seq(
      field('field', $.identifier),
      field('operator', choice('=', '!=', '>', '<', '>=', '<=')),
      field('value', $._value),
    ),

    or_expression: $ => prec.left(1, seq(field('left', $._expr), 'or', field('right', $._expr))),
    and_expression: $ => prec.left(2, seq(field('left', $._expr), 'and', field('right', $._expr))),
    not_expression: $ => prec(3, seq('not', field('operand', $._expr))),
    parenthesized: $ => seq('(', $._expr, ')'),

    _value: $ => choice($.string, $.number, $.boolean),
    string: $ => /"[^"]*"/,
    number: $ => /\d+(\.\d+)?/,
    boolean: $ => choice('true', 'false'),
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
  }
});
```

Siklus kerjanya: edit `grammar.js` → `tree-sitter generate` → `tree-sitter parse contoh.filter` → `tree-sitter test`. Ulangi sampai semua tes lulus.

Format file tes di `test/corpus/dasar.txt`:

```
==================
and lebih kuat dari or
==================

status = "open" or priority > 2 and owner = "budi"

---

(query
  (or_expression
    left: (comparison
      field: (identifier)
      value: (string))
    right: (and_expression
      left: (comparison
        field: (identifier)
        value: (number))
      right: (comparison
        field: (identifier)
        value: (string)))))
```

Perhatikan bahwa `priority > 2 and owner = "budi"` menjadi satu subtree `and_expression` di sisi kanan, karena prioritas `and` (2) lebih tinggi dari `or` (1), sama seperti `*` lebih kuat dari `+` dalam aritmetika. Field `operator` tidak muncul karena isinya node anonim. Nama field dengan titik seperti `customer.city` juga diterima oleh rule `identifier`.

## 6. Query & pattern matching

Query adalah cara deklaratif mencari pola di pohon: Anda menulis bentuk pohon dalam S-expression, lalu menandai node yang ingin diambil dengan capture `@nama`.

| Sintaks | Arti | Contoh |
| --- | --- | --- |
| `(tipe)` | Cocok dengan node bernama bertipe itu | `(identifier)` |
| `(a (b))` | `b` adalah child (turunan langsung) dari `a` | `(call (identifier))` |
| `field: (x)` | Child dengan field tertentu | `name: (identifier)` |
| `@nama` | Capture node yang cocok | `(identifier) @var` |
| `"teks"` | Cocok dengan node anonim | `"return" @keyword` |
| `[a b]` | Alternatif | `["if" "else"] @keyword` |
| `*` `+` `?` | Kuantifier | `(comment)+ @doc` |
| `_` | Node apa saja (wildcard) | `(call function: _ @fn)` |
| `(#eq? @a "x")` | Predikat: teks capture sama dengan nilai | `(#eq? @fn "print")` |
| `(#match? @a "regex")` | Predikat: teks capture cocok regex | `(#match? @c "^[A-Z]")` |

Contoh: mencari semua pemanggilan `print(...)` di Python:

```scheme
(call
  function: (identifier) @fn
  arguments: (argument_list) @args
  (#eq? @fn "print"))
```

Coba langsung dari terminal dengan `tree-sitter query pola.scm contoh.py`, atau secara interaktif di `tree-sitter playground` (berjalan di browser dan menampilkan pohon serta hasil query saat Anda mengetik).

**Hubungan dengan highlight.** Editor membaca `queries/highlights.scm` dan memetakan nama capture ke warna. Nama capture mengikuti konvensi seperti `@function`, `@keyword`, `@string`, `@comment`, `@variable`. Contoh untuk grammar `filter`:

```scheme
["and" "or" "not"] @keyword
["=" "!=" ">" "<" ">=" "<="] @operator
(string) @string
(number) @number
(boolean) @constant.builtin
(comparison field: (identifier) @property)
```

Selain highlight, folder `queries/` sering berisi `locals.scm` (scope dan definisi), `injections.scm` (bahasa di dalam bahasa, misalnya SQL di string), `folds.scm`, dan `textobjects.scm` di editor seperti Neovim.

## 7. Menggunakan parser dari kode

Dari program, Anda bekerja dengan empat objek: `Parser` mengubah byte menjadi `Tree`, `Node` adalah titik di pohon, dan `TreeCursor` menelusuri pohon besar secara efisien.

**Navigasi node.** Properti yang paling sering dipakai:

| Properti / metode | Isi |
| --- | --- |
| `node.type` | Nama tipe, misalnya `"function_definition"` |
| `node.text` | Byte sumber yang dicakup node |
| `node.start_point`, `node.end_point` | Posisi `(baris, kolom)`, mulai dari 0 |
| `node.start_byte`, `node.end_byte` | Posisi byte |
| `node.children`, `node.named_children` | Semua child / hanya yang bernama |
| `node.child_by_field_name("name")` | Child berdasarkan field |
| `node.parent`, `node.next_sibling` | Naik ke parent / pindah ke saudara |
| `node.is_named`, `node.has_error`, `node.is_missing` | Status node |

**Contoh lengkap:** daftar fungsi beserta barisnya, dengan dua cara.

```python
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

src = b"""
def tambah(a, b):
    return a + b

def kali(a, b):
    print(a, b)
    return a * b
"""
tree = parser.parse(src)

# Cara 1: telusuri manual dengan rekursi
def cari_fungsi(node):
    if node.type == "function_definition":
        nama = node.child_by_field_name("name")
        print(nama.text.decode(), "baris", node.start_point[0] + 1)
    for child in node.named_children:
        cari_fungsi(child)

cari_fungsi(tree.root_node)

# Cara 2: pakai query
query = Query(PY, "(function_definition name: (identifier) @nama)")
captures = QueryCursor(query).captures(tree.root_node)
for node in captures["nama"]:
    print(node.text.decode())
```

**TreeCursor** \[Pengayaan\] lebih hemat untuk file besar karena tidak membuat objek `Node` untuk setiap langkah: `cursor = tree.walk()`, lalu `goto_first_child()`, `goto_next_sibling()`, dan `goto_parent()`, masing-masing mengembalikan `True` jika berhasil.

**Edit inkremental.** \[Pengayaan\] Setelah mengubah teks, beri tahu pohon lama apa yang berubah, lalu parse ulang dengan pohon lama:

```python
# ganti "tambah" (byte 5..11, baris 1) menjadi "jumlah" (panjang sama)
new_src = src.replace(b"tambah", b"jumlah")
tree.edit(
    start_byte=5, old_end_byte=11, new_end_byte=11,
    start_point=(1, 4), old_end_point=(1, 10), new_end_point=(1, 10),
)
new_tree = parser.parse(new_src, tree)
for r in tree.changed_ranges(new_tree):
    print("berubah:", r.start_point, r.end_point)
```

Jika `edit()` diberi posisi yang salah, pohon baru bisa tidak sesuai dengan teks. Saat belajar, bandingkan hasilnya dengan parse dari nol untuk memastikan.

## 8. Tugas awal

Kerjakan enam tugas ini berurutan; masing-masing membangun di atas tugas sebelumnya, dan setiap tugas punya kriteria selesai yang bisa Anda cek sendiri.

Setiap tugas punya **Langkah terpandu** yang naik sedikit demi sedikit, lengkap dengan kerangka kode dan contoh output, serta daftar **Jika macet**. Ikuti langkahnya berurutan; checklist di bawahnya adalah daftar hasil yang harus ada saat dikumpulkan. Kebiasaan terpenting di semua tugas: **lihat pohonnya dulu, baru tulis kode atau query.**

**Tentang AI coding agent.** Anda boleh memakai AI coding agent untuk semua tugas. Yang dinilai bukan siapa yang mengetik kodenya, tetapi apakah Anda bisa **membuktikan** hasilnya benar dan **menjelaskan** setiap bagiannya. Saran: kerjakan Tugas 1 dan langkah 4a–4c tanpa AI dulu, karena di situlah model mental "kode adalah pohon" terbentuk. Tanpa itu, Anda tidak akan bisa menilai apakah jawaban AI benar.

Selesaikan setup (bagian 4) di rumah sebelum Pertemuan 1, agar waktu di kelas tidak habis untuk instalasi. Tugas 1–5 dikerjakan di kelas, Tugas 6 dikerjakan mandiri dalam satu minggu, bersamaan dengan draf proposal proyek.

### Tugas 1 — Membaca pohon

Baca dulu: [2. Konsep inti](#m8fwzsjbzcq.1373) dan [4. Setup lingkungan](#m8fwzsjbzcq.3015).

Tulis 3 potongan kode Python pendek (fungsi, `if`/`else`, kelas dengan satu method), parse dengan skrip uji cepat, lalu cetak `tree.root_node`.

**Langkah terpandu**

1. Mulai dari yang paling kecil. Buka Playground di situs dokumentasi resmi tree-sitter, pilih bahasa Python, lalu ketik `x = 1`. Pohonnya langsung tampil dan berubah saat Anda mengetik. Coba ganti menjadi `x = 1 + 2`, lalu `print(x)`, dan perhatikan node apa yang bertambah.
2. Pindah ke Python. Buat folder `tugas1-3/` dan file `t1.py`:

```python
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode = b"x = 1\n"
tree = parser.parse(kode)
print(tree.root_node)
```

3. Jalankan `python t1.py`. Output yang benar:

```
(module (expression_statement (assignment left: (identifier) right: (integer))))
```

4. Ganti isi `kode` dengan potongan pertama Anda (fungsi). **Sebelum menjalankan**, tulis dulu di kertas pohon yang Anda perkirakan. Setelah itu jalankan dan bandingkan. Ulangi untuk `if`/`else` dan kelas.
5. Lihat node anonim. Tambahkan baris ini di akhir `t1.py`, lalu jalankan dengan potongan fungsi:

```python
for c in tree.root_node.children[0].children:
    print(c.type, "bernama" if c.is_named else "anonim")
```

Anda akan melihat `def` dan `:` tercetak sebagai anonim. Tanda `(` dan `)` ada satu tingkat lebih dalam, di dalam node `parameters`; coba cetak juga anak-anak node itu.

6. Rusak kodenya dengan sengaja, misalnya hapus `:` setelah `def sapa(nama)`. Jalankan lagi dan cari `ERROR` atau `MISSING` di output.

**Jika macet**

- **Output satu baris panjang sulit dibaca:** salin ke editor lalu rapikan indentasinya per tanda kurung, atau bandingkan dengan tampilan di Playground. Di Tugas 2 Anda akan membuat pencetak yang rapi.
- **`ModuleNotFoundError: tree_sitter_python`:** paket belum terpasang di Python yang sedang dipakai. Jalankan `python -m pip install tree-sitter tree-sitter-python`.
- **`TypeError` soal bytes:** `parser.parse()` menerima bytes. Pastikan string diawali `b"..."`, atau pakai `teks.encode()`.

* [ ] Untuk setiap potongan, tulis dengan tangan pohon yang Anda perkirakan, baru jalankan dan bandingkan.
* [ ] Tandai di pohon mana node bernama dan sebutkan minimal 3 node anonim yang tersembunyi.
* [ ] Hapus satu `:` atau `)` dari kode, parse lagi, dan cari node `ERROR` atau `MISSING`.

Selesai jika: Anda bisa menjelaskan perbedaan `children` dan `named_children` dengan contoh dari kode Anda sendiri.

### Tugas 2 — Penjelajah node

Baca dulu: [7. Menggunakan parser dari kode](#m8fwzsjbzcq.9300).

Buat skrip `jelajah.py` yang mencetak setiap node bernama dengan indentasi sesuai kedalaman, beserta tipe, posisi `baris:kolom`, dan nama field-nya (jika ada).

**Langkah terpandu**

1. Salin kerangka berikut ke `jelajah.py`. Fungsinya sudah bisa mencetak satu node; tugas Anda hanya mengisi bagian `TODO`.

```python
import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

def jelajah(node, kedalaman=0, field=None):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
    # TODO: untuk setiap child yang bernama, panggil jelajah() lagi
    #       dengan kedalaman + 1 dan nama field-nya.

with open(sys.argv[1], "rb") as f:
    tree = parser.parse(f.read())
jelajah(tree.root_node)
```

2. Buat `kecil.py` berisi satu baris `x = 1`, lalu jalankan `python jelajah.py kecil.py`. Karena TODO belum diisi, output hanya `module [1:0]`. Itu wajar.
3. Isi TODO. Petunjuk: telusuri `node.children` dengan `enumerate`, lewati yang `is_named` bernilai `False`, dan ambil nama field dengan `node.field_name_for_child(i)`. Output yang benar untuk `kecil.py`:

```
module [1:0]
  expression_statement [1:0]
    assignment [1:0]
      left: identifier [1:0]
      right: integer [1:4]
```

4. Naikkan ukurannya bertahap: file berisi satu fungsi, lalu file Tugas 1, lalu file nyata minimal 100 baris (misalnya tugas kuliah Anda sendiri).
5. Bandingkan beberapa bagian output dengan tampilan Playground untuk memastikan field dan kedalamannya benar.

**Jika macet**

- **Semua node tercetak tanpa field:** pastikan indeks `i` yang dikirim ke `field_name_for_child(i)` adalah indeks di `node.children` (semua child), bukan indeks di `named_children`.
- **Muncul `(` `)` `:` di output:** filter `is_named` belum dipasang.
- **Output terlalu panjang:** tambahkan `| head -50` di terminal (Linux/WSL/macOS) atau simpan ke file dengan `> hasil.txt`.

* [ ] Versi rekursif dengan `named_children`.
* [ ] &#91;Pengayaan\] Versi kedua dengan `TreeCursor` (petunjuk: `cursor.field_name` memberi nama field node saat ini).
* [ ] Jalankan pada file Python nyata (minimal 100 baris).

Selesai jika: semua node bernama tercetak dengan indentasi sesuai kedalamannya. Jika mengerjakan pengayaan, kedua versi harus menghasilkan output identik.

### Tugas 3 — Query pertama

Baca dulu: [6. Query & pattern matching](#m8fwzsjbzcq.7592).

Tulis query `.scm` dan jalankan dengan `tree-sitter query` atau `QueryCursor`.

**Langkah terpandu**

1. Siapkan penjalan query `q.py` agar Anda cukup mengedit file `.scm` tanpa mengubah kode Python:

```python
import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2]).read()
tree = parser.parse(kode)

hasil = QueryCursor(Query(PY, pola)).captures(tree.root_node)
for nama, nodes in hasil.items():
    for n in nodes:
        print(f"@{nama}  baris {n.start_point[0] + 1}: {n.text.decode()}")
```

2. Coba query paling sederhana. Tulis `(identifier) @id` ke `semua.scm`, lalu jalankan `python q.py contoh.py semua.scm`. Hasilnya banyak sekali, karena semua nama tertangkap.
3. Persempit selangkah. Ganti isinya menjadi `(function_definition name: (identifier) @nama)`. Sekarang hanya nama fungsi yang keluar.
4. Jumlah parameter: tangkap juga `parameters: (parameters) @params`. Karena Anda butuh pasangan nama fungsi dan parameternya, pakai `matches` alih-alih `captures`:

```python
for _, cap in QueryCursor(Query(PY, pola)).matches(tree.root_node):
    nama = cap["nama"][0].text.decode()
    jumlah = cap["params"][0].named_child_count
    print(nama, jumlah)
```

5. Pemanggilan `print`: salin contoh query dari 6. Query & pattern matching, lalu jalankan.
6. Import: **jangan menebak nama node.** Buat file berisi `import os` dan `from pathlib import Path`, lalu lihat pohonnya dengan `jelajah.py` dari Tugas 2. Dari situ Anda akan tahu nama node yang harus dipakai di query.

**Jika macet**

- **Error `Invalid node type` atau `Invalid field name`:** nama tipe atau field di query tidak ada di grammar. Cek ejaannya di output `jelajah.py`.
- **Query jalan tapi hasilnya kosong:** biasanya struktur bersarangnya salah. Mulai dari pola yang lebih longgar (hanya tipe node luarnya), lalu tambahkan child satu per satu.
- **`KeyError` di `cap["params"]`:** ada fungsi yang tidak cocok dengan seluruh pola. Pakai `cap.get("params", [])` dan cek isinya.

* [ ] Temukan semua nama fungsi dan jumlah parameternya.
* [ ] Temukan semua pemanggilan `print(...)`.
* [ ] Temukan semua `import` dan `from ... import ...`, lalu cetak nama modulnya.
* [ ] &#91;Pengayaan\] Temukan string yang menjadi baris pertama body fungsi (docstring).

Selesai jika: hasil query cocok dengan hitungan manual Anda pada satu file uji.

### Tugas 4 — Grammar DSL filter untuk halaman admin

Baca dulu: [5. Menulis grammar](#m8fwzsjbzcq.4752) dan [3. Arsitektur](#m8fwzsjbzcq.15770).

Banyak aplikasi enterprise punya kotak pencarian lanjutan di halaman admin, misalnya untuk menyaring tiket atau pesanan. Buat proyek grammar baru dengan `tree-sitter init`, salin grammar `filter` dari 5. Menulis grammar, lalu jalankan `tree-sitter generate` dan `tree-sitter parse`.

**Langkah terpandu**

Jangan langsung menyalin grammar lengkap. Bangun sedikit demi sedikit; setiap langkah hanya menambah satu hal, lalu dicek dengan `tree-sitter generate` dan `tree-sitter parse contoh.filter`. Grammar lengkap di bagian 5 dipakai sebagai kunci jawaban jika macet.

1. Buat proyek: `mkdir tree-sitter-filter`, `cd tree-sitter-filter`, lalu `tree-sitter init` dan isi nama bahasa `filter`.
2. Ganti isi `grammar.js` dengan versi paling kecil, yang hanya mengenali satu perbandingan:

```javascript
module.exports = grammar({
  name: 'filter',
  extras: $ => [/\s/],
  rules: {
    query: $ => $.comparison,
    comparison: $ => seq($.identifier, '=', $.string),
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
    string: $ => /"[^"]*"/,
  }
});
```

3. Buat `contoh.filter` berisi `status = "open"`, lalu generate dan parse. Output yang benar: `(query (comparison (identifier) (string)))`.
4. Tambahkan satu fitur per langkah, dan ulangi generate + parse setiap kali:

| Langkah | Yang ditambahkan | Contoh input untuk dicoba |
| --- | --- | --- |
| 4a | Operator `!=`, `>`, `<`, `>=`, `<=` dan rule `number` | `priority >= 2` |
| 4b | Rule `_expr` dan `and_expression`, serta `word: $ => $.identifier` | `a = 1 and b = 2` |
| 4c | `or_expression` tanpa `prec`; baca pesan conflict-nya, lalu tambahkan `prec.left` | `a = 1 or b = 2 and c = 3` |
| 4d | `parenthesized` | `(a = 1 or b = 2) and c = 3` |
| 4e | `not_expression` dan `boolean` | `not archived = true` |
| 4f | `field(...)` pada setiap child penting | Input sebelumnya, cek label field muncul |

5. Setiap selesai satu langkah dan hasilnya sudah benar, simpan sebagai satu kasus uji di `test/corpus/dasar.txt`. Setelah langkah 4f, Anda otomatis punya 5–6 tes.
6. Baru setelah semua tes lulus, tambahkan `in` dan `contains`. Petunjuk untuk `in`: daftar nilai bisa ditulis `seq('(', $._value, repeat(seq(',', $._value)), ')')`.

**Jika macet**

- **`Unresolved conflict`:** tree-sitter mencetak dua cara membaca input yang sama. Itu tanda perlu `prec.left` atau `prec` dengan angka yang membedakan prioritas. Ini memang sengaja dialami di langkah 4c.
- **`and` terbaca sebagai `identifier`:** `word: $ => $.identifier` belum dipasang.
- **Error saat generate setelah menambah rule:** rule baru belum dimasukkan ke `choice` di `_expr`, atau ada koma yang hilang. Bandingkan dengan grammar lengkap di bagian 5.
- **Tes gagal padahal hasil parse tampak benar:** bandingkan baris per baris; biasanya ada field yang lupa ditulis di hasil yang diharapkan. Jangan memakai `tree-sitter test --update` sebelum Anda yakin output-nya benar, karena perintah itu menimpa hasil yang diharapkan.

* [ ] Tulis minimal 5 kasus uji di `test/corpus/`, mencakup prioritas `and`/`or`, kurung, `not`, dan ketiga jenis nilai (string, angka, boolean).
* [ ] Tambahkan operator `in` untuk daftar nilai, misalnya `status in ("open", "pending")`, sebagai node baru `in_expression`.
* [ ] Tambahkan operator `contains` untuk pencarian teks, misalnya `title contains "invoice"`.
* [ ] &#91;Pengayaan\] Hapus semua `prec` sementara, jalankan `generate`, dan baca pesan conflict-nya; lalu pulihkan.
* [ ] &#91;Pengayaan\] Tulis skrip Python yang menelusuri pohon hasil parse dan menghasilkan klausa `WHERE` SQL yang setara, dengan nilai dikirim sebagai parameter (`?`), bukan digabung ke string. Inilah cara aman memakai DSL filter di backend.

Selesai jika: `tree-sitter test` lulus semua, termasuk tes `a = 1 or b = 2 and c = 3` yang mengelompok sebagai `a = 1 or (b = 2 and c = 3)`, dan tes `in` dengan tiga nilai.

### Tugas 5 — Highlight untuk DSL filter

Baca dulu: [6. Query & pattern matching](#m8fwzsjbzcq.7592), khususnya bagian highlight.

Buat `queries/highlights.scm` untuk grammar Anda.

**Langkah terpandu**

1. Siapkan CLI satu kali: jalankan `tree-sitter init-config`. Buka file konfigurasi yang dibuatnya, lalu pastikan `parser-directories` berisi folder **induk** dari `tree-sitter-filter/` (bukan folder itu sendiri).
2. Cek `tree-sitter.json` di proyek Anda: bagian `file-types` harus berisi `"filter"`, dan `highlights` harus menunjuk ke `queries/highlights.scm`.
3. Mulai dengan satu baris saja di `highlights.scm`, misalnya `(string) @string`, lalu jalankan `tree-sitter highlight contoh.filter`. Jika string berwarna, konfigurasinya sudah benar.
4. Tambahkan sisa contoh dari 6. Query & pattern matching satu per satu, jalankan lagi setiap kali.
5. Terakhir, tambahkan kata kunci `in` dan `contains` dari Tugas 4.

**Jika macet**

- **Tidak ada warna sama sekali:** biasanya konfigurasi di langkah 1–2. Cek dulu bahwa `tree-sitter parse contoh.filter` berjalan dari folder lain, misalnya folder rumah Anda. Jika gagal, `parser-directories` belum benar.
- **Sebagian token tidak berwarna:** jalankan `tree-sitter query queries/highlights.scm contoh.filter` untuk melihat capture mana yang benar-benar cocok.
- **Error `Invalid node type` saat highlight:** nama node di query tidak sama dengan nama rule di `grammar.js`, misalnya `and_expr` alih-alih `and_expression`.

* [ ] Beri capture untuk kata kunci (`and`, `or`, `not`, `in`, `contains`), operator perbandingan, string, angka, boolean, dan nama field.
* [ ] Jalankan `tree-sitter highlight contoh.filter` dan periksa warnanya (atur `tree-sitter.json` agar CLI mengenali ekstensi `.filter`).

Selesai jika: setiap jenis token di file contoh punya warna yang berbeda dan benar.

### Tugas 6 — Mini proyek: pendeteksi TODO dan fungsi panjang

Baca dulu: [6. Query & pattern matching](#m8fwzsjbzcq.7592) dan [7. Menggunakan parser dari kode](#m8fwzsjbzcq.9300).

Gabungkan semuanya menjadi CLI kecil `cek.py <folder>` untuk file Python.

**Langkah terpandu**

1. Salin kerangka `cek.py` berikut. Fitur pertama (TODO/FIXME) sudah jadi sebagai contoh; dua fitur lainnya Anda tulis dengan pola yang sama.

```python
import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')

def cek_file(path):
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME (sudah jadi)
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        print(f"{path}:{node.start_point[0] + 1}: {node.text.decode().strip()}")

    # Fitur 2 (TODO): fungsi yang lebih dari 30 baris
    # Fitur 3 (TODO): file yang pohonnya mengandung error

for path in Path(sys.argv[1]).rglob("*.py"):
    cek_file(path)
```

2. Buat folder `uji/` berisi dua atau tiga file kecil buatan sendiri: satu dengan komentar `# TODO`, satu dengan fungsi panjang, satu dengan sintaks rusak. Jalankan `python cek.py uji/` dan pastikan fitur 1 sudah melaporkan TODO.
3. Fitur 2. Buat query `(function_definition name: (identifier) @nama) @fungsi`, jalankan dengan `matches` seperti di Tugas 3, lalu hitung `end_point[0] - start_point[0] + 1` dari node `@fungsi`. Laporkan nama dan jumlah barisnya jika lebih dari 30.
4. Fitur 3. Ini cukup satu `if` dengan `tree.root_node.has_error`. Laporkan juga baris pertama yang bermasalah: cari node pertama yang `is_error` atau `is_missing` dengan fungsi rekursif seperti di Tugas 2.
5. Uji pada repositori nyata. Pilih proyek Python open source yang kecil di GitHub, `git clone`, lalu jalankan `cek.py` pada foldernya. Ambil 2 file acak dan cocokkan hasilnya secara manual.
6. Tulis `README.md`: cara memasang dependensi, cara menjalankan, dan contoh output.

**Jika macet**

- **`UnicodeDecodeError` saat mencetak:** ada file dengan encoding lain. Pakai `node.text.decode(errors="replace")`.
- **Hasil fitur 2 berlipat:** fungsi di dalam kelas dan fungsi bersarang ikut terhitung. Itu benar; cukup cantumkan di README bahwa semua fungsi dihitung.
- **Program lambat di repo besar:** wajar untuk tahap ini. Lewati folder `venv/`, `.git/`, dan `node_modules/` dengan memeriksa `path.parts` sebelum memanggil `cek_file`.

* [ ] Laporkan setiap komentar berisi `TODO` atau `FIXME` beserta file dan barisnya (query + `#match?`).
* [ ] Laporkan fungsi yang body-nya lebih dari 30 baris (pakai `start_point` dan `end_point`).
* [ ] Laporkan file yang pohonnya punya error (`root_node.has_error`).
* [ ] &#91;Pengayaan\] Dukung juga file JavaScript dengan `tree-sitter-javascript`, cukup ganti grammar dan query.

Selesai jika: skrip berjalan pada satu repo nyata dan outputnya cocok dengan pengecekan manual pada 2 file acak.

### Pengumpulan

Kumpulkan satu repositori GitHub (atau file `.zip`) paling lambat satu minggu setelah Pertemuan 2, dengan struktur:

| Folder / file | Isi |
| --- | --- |
| `tugas1-3/` | Skrip Python dan file `.scm`, beserta output-nya dalam `.txt` |
| `tree-sitter-filter/` | `grammar.js`, `test/corpus/`, `queries/highlights.scm` (Tugas 4–5) |
| `cek/` | `cek.py` dan `README.md` berisi cara menjalankan (Tugas 6) |
| `laporan.pdf` | Maksimal 3 halaman: tangkapan layar hasil, penjelasan singkat tiap tugas, kendala dan cara mengatasinya, serta catatan penggunaan AI |
| proposal-draf.pdf | Draf proposal proyek, maksimal 1 halaman, mengikuti template di bagian 9. Tidak dinilai, hanya diberi umpan balik |

**Penggunaan AI.** Boleh berdiskusi dengan teman atau memakai AI coding agent. Konsekuensinya, laporan wajib memuat **catatan penggunaan AI**: untuk setiap tugas yang dibantu AI, tulis apa yang Anda minta, minimal satu kesalahan atau kekurangan hasil AI yang Anda temukan, dan bagaimana Anda membuktikannya (kasus uji, output, atau pengecekan manual). Dosen/asisten dapat meminta demo singkat dan menanyakan baris kode mana pun.

### Rubrik penilaian

| Komponen | Bobot | Nilai penuh jika |
| --- | --- | --- |
| Tugas 1 | 10 | Pohon perkiraan dan hasil sebenarnya dibandingkan, node anonim dan `ERROR`/`MISSING` ditunjukkan |
| Tugas 2 | 15 | Penjelajah rekursif berjalan pada file ≥100 baris dengan indentasi, posisi, dan field yang benar |
| Tugas 3 | 15 | Tiga query wajib berjalan dan hasilnya cocok dengan hitungan manual |
| Tugas 4 | 20 | `tree-sitter test` lulus, minimal 5 tes, prioritas `and`/`or` benar, `in_expression` dan `contains` ada |
| Tugas 5 | 10 | Semua jenis token di file contoh berwarna dan benar |
| Tugas 6 | 20 | Tiga laporan (TODO, fungsi panjang, file error) berjalan pada repo nyata |
| Laporan dan catatan AI | 10 | Kendala dan solusinya jelas; untuk tugas yang dibantu AI, ada minimal satu kesalahan hasil AI yang ditemukan beserta bukti verifikasinya |
| **Total** | **100** |  |

Butir \[Pengayaan\] tidak menambah nilai, tetapi sangat disarankan bagi yang ingin mendalami topik ini sebelum mengambil mata kuliah Teknik Kompilasi.

## 9. Proyek: topik pilihan sendiri

Setelah Tugas 1–6, setiap mahasiswa menentukan topik proyek sendiri dengan tema **pemanfaatan tree-sitter untuk mendukung kegiatan pengembangan aplikasi web enterprise**. Tugas 6 adalah latihan pemanasan untuk proyek ini: polanya sama, yaitu parse kode, cari pola dengan query, lalu laporkan hasilnya.

**Mengapa relevan.** Aplikasi web enterprise biasanya punya basis kode besar, banyak developer, banyak bahasa sekaligus (TypeScript, Java, PHP, SQL, YAML), dan aturan internal tim yang harus dipatuhi. Tool berbasis tree-sitter bisa memeriksa aturan itu secara otomatis dan akurat, karena memahami struktur kode, bukan sekadar mencocokkan teks seperti `grep` atau regex.

### Tree-sitter di era AI coding agent

AI coding agent dan tree-sitter saling melengkapi, bukan saling menggantikan: AI menulis aturannya, tree-sitter menjalankannya di setiap commit.

|  | AI coding agent | Tool berbasis tree-sitter |
| --- | --- | --- |
| Sifat hasil | Probabilistik, bisa berbeda tiap kali dijalankan | Deterministik, selalu sama untuk input yang sama |
| Biaya per pengecekan | Token per file, mahal untuk jutaan baris kode | Hampir nol, ribuan file per detik |
| Cocok untuk | Menulis kode dan aturan, menjelaskan, refactoring | Menjalankan aturan di CI, mengindeks dan mencari struktur kode |

Tree-sitter juga banyak dipakai *di dalam* tool AI itu sendiri, misalnya untuk membuat peta struktur repositori sebagai konteks bagi model, atau memotong kode per fungsi sebelum dikirim ke model. Karena itu, topik proyek yang menggabungkan keduanya sangat dianjurkan.

### Contoh topik

Contoh berikut boleh dipakai langsung, dimodifikasi, atau hanya dijadikan inspirasi.

| Topik | Kegiatan yang didukung | Bahasa / berkas target |
| --- | --- | --- |
| Linter aturan internal tim, misalnya larangan `console.log` di kode produksi atau wajib `try/catch` di handler | Code review | JavaScript / TypeScript (Express, NestJS) |
| Pendeteksi potensi SQL injection: query yang dibentuk dengan penggabungan string | Keamanan aplikasi | PHP (Laravel), JavaScript, Python |
| Generator daftar endpoint API dari kode route, misalnya `app.get('/users', ...)` atau `@GetMapping` | Dokumentasi API | JavaScript, Java (Spring Boot) |
| Pemeriksa arsitektur berlapis: controller tidak boleh langsung meng-import repository | Menjaga arsitektur | TypeScript, Java |
| Pencari teks UI yang belum diterjemahkan, yaitu string di JSX yang tidak dibungkus `t(...)` | Internasionalisasi (i18n) | TSX / JSX (React) |
| Pendeteksi data sensitif di log, misalnya `logger.info(user.password)` | Keamanan dan kepatuhan data | Java, TypeScript, PHP |
| Pemeriksa konfigurasi deployment: image tanpa tag versi, secret ditulis langsung | DevOps / CI | YAML (docker-compose, GitHub Actions) |
| Laporan kualitas kode untuk CI: fungsi terlalu panjang, terlalu banyak cabang | Quality gate di pipeline | Bahasa apa pun yang punya grammar |
| Guardrail kode hasil AI di CI: memeriksa pull request buatan AI terhadap aturan tim sebelum di-merge | Code review, kepatuhan standar | TypeScript, Java, PHP |
| Pembuat peta repositori: daftar file, kelas, fungsi, dan signature-nya sebagai konteks ringkas untuk AI agent | Membantu AI memahami basis kode besar | Bahasa apa pun yang punya grammar |
| Pemotong kode per fungsi atau kelas untuk pencarian semantik (RAG) atas basis kode perusahaan | Onboarding developer baru, tanya-jawab tentang kode | Java, TypeScript, Python |
| Server MCP yang memberi AI agent akses ke struktur kode: cari definisi, daftar pemanggil sebuah fungsi | Navigasi kode oleh AI agent | Bahasa apa pun yang punya grammar |

### Kriteria topik yang baik

- **Masalah nyata.** Sebutkan siapa penggunanya (developer, reviewer, tim QA, tim DevOps) dan kegiatan apa yang dibantu.
- **Tree-sitter adalah inti solusinya.** Hasil utama didapat dari parse dan query, bukan dari regex atas teks mentah. Di laporan, jelaskan kenapa pendekatan regex akan gagal untuk kasus Anda.
- **Lebih tepat daripada "minta AI me-review saja".** Jelaskan keunggulan tool Anda dibanding meminta AI memeriksa kode setiap kali: konsistensi hasil, biaya, kecepatan, atau bisa dijalankan otomatis di CI. Jika topik Anda justru membantu AI agent, jelaskan apa yang tidak bisa dilakukan AI tanpa tool Anda.
- **Skop realistis.** Cukup 2–4 aturan atau fitur yang berjalan baik, bukan tool lengkap.
- **Bisa diuji pada kode nyata.** Pilih minimal satu repositori open source atau proyek kuliah Anda sebagai bahan uji.
- **Grammar tersedia.** Pastikan grammar bahasa target ada di PyPI (misalnya `tree-sitter-javascript`, `tree-sitter-typescript`, `tree-sitter-java`, `tree-sitter-php`) sebelum mengajukan topik.

### Template proposal (maksimal 1 halaman)

1. **Judul.**
2. **Masalah:** apa yang sulit atau sering salah dalam pengembangan web enterprise, dan siapa yang mengalaminya.
3. **Kenapa tidak cukup dengan AI saja:** satu paragraf sesuai kriteria di atas.
4. **Bahasa dan framework target**, beserta grammar tree-sitter yang dipakai.
5. **Contoh kode** yang harus terdeteksi, dan contoh kode yang tidak boleh ikut terdeteksi.
6. **Rancangan query** untuk minimal satu aturan, dalam bentuk S-expression.
7. **Bentuk output:** laporan di terminal, file JSON, komentar di pull request, halaman HTML, atau tool yang dipanggil AI agent.
8. **Cara evaluasi:** repositori uji yang dipakai, dan cara mengecek hasil (misalnya cek manual 20 temuan, berapa yang benar).
9. **Rencana kerja** per minggu dan risiko yang mungkin muncul.

**Draf proposal dikumpulkan bersama Tugas 6**, satu minggu setelah Pertemuan 2. Draf ini tidak dinilai, tetapi akan diberi umpan balik soal skop dan kelayakan topik. Saran: sambil mengerjakan Tugas 6, coba tulis satu query untuk kasus topik Anda sendiri, lalu masukkan ke poin 6 template. Jika query itu sulit ditulis, itu tanda topiknya perlu dipersempit.

Durasi proyek, format kelompok atau individu, dan rubrik proyek ditentukan oleh dosen pengampu.

## 10. Referensi dan langkah lanjutan

Setelah enam tugas selesai, langkah berikutnya yang paling berguna adalah membaca grammar nyata, misalnya `tree-sitter-python` atau `tree-sitter-javascript`, dan mencocokkan rule-nya dengan pohon yang Anda lihat di Tugas 1.

Topik lanjutan untuk dipelajari kemudian: external scanner (`src/scanner.c`) untuk bahasa berbasis indentasi, `locals.scm` dan `injections.scm`, integrasi grammar sendiri ke Neovim atau Helix, serta binding Rust untuk tool berperforma tinggi.

Sumber:

- [Dokumentasi resmi tree-sitter](https://tree-sitter.github.io/tree-sitter/) — grammar DSL, query syntax, CLI
- [Dokumentasi py-tree-sitter](https://tree-sitter.github.io/py-tree-sitter/) — API Python
- [Repo py-tree-sitter](https://www.github.com/tree-sitter/py-tree-sitter) — contoh `examples/walk_tree.py`
- [Organisasi tree-sitter di GitHub](https://github.com/tree-sitter) — grammar resmi sebagai bahan bacaan
