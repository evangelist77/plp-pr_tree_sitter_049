# Tugas 4–5: grammar filter

Proyek ini sudah diinisialisasi sekali dengan `tree-sitter init` (CLI 0.25.10), nama bahasa `filter`, dan ekstensi `.filter`. Folder `test/corpus/` dan `queries/` yang telah disediakan tetap dipakai; query highlighting dikerjakan pada Tugas 5.

Dari folder ini, dengan CLI tersedia di `PATH`:

```sh
tree-sitter generate
tree-sitter test
tree-sitter parse contoh.filter
```

Hasil pemeriksaan Tugas 4: generate berhasil, **17/17 corpus lulus**, dan contoh diparse menjadi root `query` tanpa `ERROR`/`MISSING`. Corpus memeriksa string/angka/boolean, prioritas `or=1`, `and=2`, `not=3`, asosiativitas kiri `and`/`or`, kurung, label field, identifier berawalan keyword, `in` tiga nilai dan campuran tipe, serta input rusak. Contoh `status in ()` menghasilkan nilai yang `MISSING`; `a =` menghasilkan string yang `MISSING`, sehingga keduanya tetap ditolak sebagai input valid.

`comparison` memiliki field `field`, `operator`, dan `value`; operator berupa token anonim sehingga tidak ditampilkan pada pohon bernama default. `and_expression`/`or_expression` memiliki `left`/`right`, `not_expression` memiliki `operand`, `in_expression` memiliki `field`/`values` (`value_list`), dan `contains_expression` memiliki `field`/`value` string.

Grammar mengikuti nilai sederhana materi: string berpetik ganda tanpa pengolahan escape, angka nonnegatif dengan pecahan opsional, boolean `true`/`false`, dan identifier ASCII yang boleh berisi titik. `in` wajib memiliki sedikitnya satu nilai; `contains` hanya menerima string. Tidak ada evaluator maupun konversi SQL. Input tidak valid tetap dapat menghasilkan pohon pemulihan Tree-sitter; pemakai harus memeriksa `has_error` sebelum memakainya.

`src/parser.c`, `src/grammar.json`, `src/node-types.json`, dan header `src/tree_sitter/` adalah hasil generate; jangan edit manual. Scaffolding binding lintas bahasa dan build hasil init dihapus karena tugas ini memakai CLI. Metadata binding dinonaktifkan. CLI mungkin memperingatkan parser directory belum dikonfigurasi; parse dari folder grammar tetap berhasil. Konfigurasi penemuan grammar untuk highlighting dilengkapi pada Tugas 5.
