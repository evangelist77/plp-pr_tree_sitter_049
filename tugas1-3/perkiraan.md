# Perkiraan pohon Tugas 1

## Perkiraan AI — dicatat sebelum parse contoh

Perkiraan ini dibuat AI, bukan bukti tulisan tangan pengguna. S-expression di bawah hanya memuat node bernama.

### Fungsi: `def sapa(nama): return nama`

```text
(module (function_definition name: (identifier) parameters: (parameters (identifier)) body: (block (return_statement (identifier)))))
```

### Kondisi: `if aktif: print("José") else: print("tidak aktif")`

```text
(module (if_statement condition: (identifier) consequence: (block (expression_statement (call function: (identifier) arguments: (argument_list (string))))) alternative: (else_clause body: (block (expression_statement (call function: (identifier) arguments: (argument_list (string)))))))))
```

Prediksi sengaja berhenti pada `(string)`; detail token isi string belum diprediksi.

### Kelas: `class Penyapa` dengan satu method `sapa(self, nama)`

```text
(module (class_definition name: (identifier) body: (block (function_definition name: (identifier) parameters: (parameters (identifier) (identifier)) body: (block (return_statement (identifier)))))))
```

`def`, `:`, `(`, `)` diperkirakan anonim, sehingga tersembunyi dari S-expression biasa. Fungsi tanpa `:` diperkirakan memiliki `ERROR` atau `MISSING`.

## Perkiraan tulisan tangan pengguna — BELUM DIISI

- [ ] Pengguna menggambar ketiga pohon sendiri di kertas, sebelum menjalankan contoh sendiri.
- [ ] Pengguna menambahkan foto/scan atau lokasi bukti tulisan tangan dan perbandingannya.

Tidak ada perkiraan tulisan tangan yang dibuat atau diklaim oleh AI.

## Perbandingan aktual

Dibandingkan sesudah run pertama (lihat `output/t1.txt`):

- Fungsi: susunan node bernama sesuai perkiraan.
- Kondisi: `if_statement`, `consequence`, dan `else_clause` sesuai. Prediksi AI kurang rinci: setiap `string` ternyata berisi `string_start`, `string_content`, dan `string_end`.
- Kelas: `class_definition` dengan satu method dan dua identifier parameter sesuai.
- Node anonim: `def` dan `:` muncul di `children` fungsi; `(` dan `)` ada di `children` parameters.
- Fungsi tanpa `:`: hasil aktual `(module (ERROR (identifier) (parameters (identifier)) (identifier)))`, `has_error=True`; bukan node `MISSING` pada versi ini.
