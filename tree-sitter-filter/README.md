# Tugas 4–5: grammar filter

Proyek ini sudah diinisialisasi sekali dengan `tree-sitter init` (CLI 0.25.10), nama bahasa `filter`, dan ekstensi `.filter`. Folder `test/corpus/` dan `queries/` yang telah disediakan tetap dipakai.

Siapkan Python/dependensi dan CLI lokal mengikuti [README root](../README.md#setup-dari-checkout-bersih). Dari folder `tree-sitter-filter/`, dengan CLI tersedia di `PATH`:

```sh
tree-sitter generate
tree-sitter test
tree-sitter parse contoh.filter
```

Hasil pemeriksaan Tugas 4: generate berhasil, **17/17 corpus lulus**, dan contoh diparse menjadi root `query` tanpa `ERROR`/`MISSING`. Corpus memeriksa string/angka/boolean, prioritas `or=1`, `and=2`, `not=3`, asosiativitas kiri `and`/`or`, kurung, label field, identifier berawalan keyword, `in` tiga nilai dan campuran tipe, serta input rusak. Contoh `status in ()` menghasilkan nilai yang `MISSING`; `a =` menghasilkan string yang `MISSING`, sehingga keduanya tetap ditolak sebagai input valid.

`comparison` memiliki field `field`, `operator`, dan `value`; operator berupa token anonim sehingga tidak ditampilkan pada pohon bernama default. `and_expression`/`or_expression` memiliki `left`/`right`, `not_expression` memiliki `operand`, `in_expression` memiliki `field`/`values` (`value_list`), dan `contains_expression` memiliki `field`/`value` string.

Grammar mengikuti nilai sederhana materi: string berpetik ganda tanpa pengolahan escape, angka nonnegatif dengan pecahan opsional, boolean `true`/`false`, dan identifier ASCII yang boleh berisi titik. `in` wajib memiliki sedikitnya satu nilai; `contains` hanya menerima string. Tidak ada evaluator maupun konversi SQL. Input tidak valid tetap dapat menghasilkan pohon pemulihan Tree-sitter; pemakai harus memeriksa `has_error` sebelum memakainya.

`src/parser.c`, `src/grammar.json`, `src/node-types.json`, dan header `src/tree_sitter/` adalah hasil generate; jangan edit manual. Scaffolding binding lintas bahasa dan build hasil init dihapus karena tugas ini memakai CLI. Metadata binding dinonaktifkan. Konfigurasi lokal di bawah mengatur penemuan grammar tanpa mengubah konfigurasi pengguna.

## Tugas 5: highlighting

`queries/highlights.scm` menangkap keyword `and/or/not/in/contains`, seluruh operator perbandingan, string, number, boolean sebagai `constant.builtin`, serta nama field (`property`) pada comparison, in, dan contains. `contoh.filter` adalah satu ekspresi multibaris yang memuat semuanya, termasuk kedua boolean. Metadata menunjuk query dan ekstensi `.filter`.

Dari folder grammar ini, buat konfigurasi demonstrasi lokal (Python dan CLI harus tersedia di `PATH`). Path penemuan harus **induk langsung `tree-sitter-filter/`**, yaitu root checkout ini; induk checkout tidak menjangkau grammar yang bersarang. Tema memberi enam warna berbeda, termasuk keyword dan boolean.

```sh
python - <<'PYCONFIG'
import json
from pathlib import Path
config = Path('../.venv/filter-cli.json')
config.parent.mkdir(exist_ok=True)
with config.open('x') as handle:
    handle.write(json.dumps({
    'parser-directories': [str(Path('..').resolve())],
    'theme': {
        'keyword': '#6f42c1', 'operator': '#d73a49',
        'string': '#176b24', 'number': '#005cc5',
        'constant.builtin': '#a24a00', 'property': '#006b73',
    },
    }, indent=2) + '\n')
PYCONFIG
tree-sitter dump-languages --config-path ../.venv/filter-cli.json
tree-sitter parse contoh.filter --config-path ../.venv/filter-cli.json
tree-sitter query queries/highlights.scm contoh.filter --config-path ../.venv/filter-cli.json > output/captures.txt
tree-sitter highlight --html contoh.filter --config-path ../.venv/filter-cli.json > output/highlight.html
tree-sitter test
```

Buka `output/highlight.html` di browser; `output/captures.txt` menunjukkan token dan rentangnya. Hasil Tugas 5: 38 capture, semua enam kategori berwarna, dan 17/17 corpus tetap lulus. Konfigurasi tersebut berada di `.venv/` yang diabaikan Git, tidak menimpa tema atau parser directory global. Pembuatan konfigurasi menolak menimpa file lokal yang sudah ada; gunakan konfigurasi yang ada atau pilih nama lain.


## Pengulangan dan bukti akhir

Potongan `config.open('x')` di atas khusus pembuatan pertama: bila `.venv/filter-cli.json` sudah ada, **lewati blok Python** dan langsung jalankan perintah `dump-languages`, parse, query, highlight, dan test dengan config tersebut. Pada lingkungan verifikasi Task 7, file ini sudah tersedia dan dipakai tanpa ditimpa. Bila pindah checkout, buat konfigurasi dengan nama lokal baru (ubah path pada blok dan seluruh `--config-path`), sehingga direktori penemuan sesuai dan konfigurasi lama tetap aman. Tidak perlu mengulang `tree-sitter init`.

Verifikasi ulang 13 November 2026: generate berhasil, 17/17 corpus lulus, parse tidak berisi ERROR/MISSING, query menghasilkan 38 capture, HTML dan capture identik byte demi byte dengan bukti tersimpan. Tes corpus sebelumnya pernah memberi peringatan slow parse rate untuk input pendek; hasilnya tetap lulus, bukan bukti kegagalan grammar atau regresi performa.

Screenshot browser nyata sudah diambil dan direview pada Tugas 5: `/Users/hafizfs/Documents/plp-pr_tree_sitter_049-laporan/bukti/tugas-5-highlight-20261113-102832.png`. Enam kategori terlihat berbeda warna. Bukti ini di luar repo dan tidak menggantikan pemeriksaan Playground/pemahaman pribadi pengguna yang masih terbuka.
