# Tugas Tree-sitter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Menyelesaikan enam tugas wajib Tree-sitter, bukti pengujian yang dapat diulang, serta laporan dan draf proposal DOCX untuk ditinjau pengguna.

**Architecture:** Pertahankan tiga unit yang sudah ditentukan materi: skrip Python Tugas 1–3, grammar filter Tugas 4–5, dan CLI Python Tugas 6. Gunakan query untuk pencarian pola dan traversal untuk navigasi/error; tidak membuat framework bersama. Dokumen akhir dan repo bahan uji berada di luar repo tugas.

**Tech Stack:** Python 3.10+, tree-sitter dan grammar Python seri 0.25 sesuai requirements.txt, Tree-sitter CLI, Node.js, compiler C, unittest bawaan Python. Pembuatan DOCX mengikuti skill dokumen saat eksekusi.

**Spec:** `Part 1 - Tree-sitter.md`, terutama bagian 4, 8, 9; keputusan pengguna dalam percakapan tanggal 2026-11-13.

## Global Constraints

- Semua tugas wajib 1–6; pengayaan tidak dikerjakan.
- Materi: Python 3.10+; API Python gaya 0.25 (`Parser(LANG)`, `Query`, `QueryCursor`). Pertahankan batas versi requirements.txt.
- Tugas 2 memakai file Python nyata minimal 100 baris; Tugas 4 minimal 5 kasus uji; Tugas 6 diverifikasi pada repo nyata dan 2 file acak.
- Hasil tidak boleh diklaim sebelum perintah pengujian dijalankan dan outputnya dibaca.
- Tidak mengarang perkiraan tulisan tangan pengguna, screenshot, kesalahan AI, hasil manual, atau hasil uji.
- Pesan commit singkat berbahasa Indonesia, dimulai huruf lowercase; contoh: `tambah penjelajah pohon`.
- Implementasi baru dimulai sesudah pengguna meninjau dan menyetujui plan ini. Plan ini belum di-commit/push pada tahap penyusunan.
- Setelah disetujui, pakai dua peran subagent: pelaksana menulis solusi; reviewer memeriksa hasil dan mencatat kekurangan yang benar-benar ditemukan. Koordinator mengurus integrasi, waktu, commit, dan push.
- Laporan dan proposal hanya dibuat di `/Users/hafizfs/Documents/plp-pr_tree_sitter_049-laporan/`, tidak di-stage, di-commit, atau di-push oleh agent.
- Pengguna meminta `.docx`: hasil akhir `laporan.docx` maksimal 3 halaman dan `proposal-draf.docx` maksimal 1 halaman. Materi aslinya meminta PDF; pengguna bertanggung jawab atas ekspor PDF dan push manual saat pengumpulan. Jangan menyatakan DOCX memenuhi format PDF.
- Pekerjaan yang membutuhkan tindakan manusia tetap ditandai terbuka sampai ada buktinya.

## Review Focus

1. UTF-8: posisi kolom Tree-sitter adalah byte dan teks multibyte tidak boleh rusak saat ditampilkan — tes Tugas 1 dan 2.
2. Field child: indeks child anonim tidak boleh menggeser label `name`, `left`, `right` — tes Tugas 2.
3. Parameter default, anotasi, `*args`, `**kwargs`, `/`, dan `*`: hitung parameter sungguhan, bukan separator — tes Tugas 3.
4. Keyword dan prioritas DSL: `android`/`origin` tetap identifier, `and` mengikat lebih kuat daripada `or`, kurung dan `not` dihormati — corpus Tugas 4.
5. Batas fungsi dan error: fungsi 30 baris tidak dilaporkan, 31 dilaporkan; error dan missing node dilaporkan, TODO dalam string diabaikan — tes Tugas 6.

---

## Pembagian pekerjaan dan berkas

| Unit | Berkas | Tanggung jawab |
| --- | --- | --- |
| Bukti T1 | `tugas1-3/t1.py`, `tugas1-3/contoh/{fungsi,kondisi,kelas,rusak}.py`, `tugas1-3/perkiraan.md`, `tugas1-3/output/t1.txt` | Contoh, prediksi sebelum parse, pohon, node anonim, error |
| Traversal T2 | `tugas1-3/jelajah.py`, `tugas1-3/output/t2.txt` | Cetak pohon bernama beserta posisi dan field |
| Query T3 | `tugas1-3/q.py`, `tugas1-3/queries/{fungsi,print,import}.scm`, `tugas1-3/contoh/query.py`, `tugas1-3/output/t3.txt` | Tiga query wajib dan hasil pembanding |
| Grammar T4 | `tree-sitter-filter/grammar.js`, `tree-sitter-filter/tree-sitter.json`, `tree-sitter-filter/test/corpus/dasar.txt`, `tree-sitter-filter/contoh.filter`, artefak hasil init/generate | Grammar, metadata, corpus, contoh |
| Highlight T5 | `tree-sitter-filter/queries/highlights.scm`, `tree-sitter-filter/output/{captures.txt,highlight.html}` | Capture token dan bukti warna |
| CLI T6 | `cek/cek.py`, `cek/uji/{todo,panjang,rusak}.py`, `cek/output/{uji,repo-nyata}.txt`, `cek/verifikasi-manual.md` | Pemeriksaan direktori dan bukti |
| Verifikasi | `tests/test_tugas_awal.py`, `tests/test_cek.py` | unittest tanpa dependency baru |
| Dokumentasi | README root dan tiap unit, `docs/catatan-ai.md`, `docs/review-pengerjaan.md`, `docs/bahan-uji.md` | Petunjuk, sumber, temuan reviewer, bukti AI |
| Dokumen eksternal | `../plp-pr_tree_sitter_049-laporan/{laporan,proposal-draf}.docx`, subfolder `bukti/` | Dokumen siap ditinjau dan screenshot/render |

Hanya artefak init/generate yang diperlukan CLI disertakan; jangan mengedit `src/parser.c` manual. Jangan menyalin virtualenv, cache, build binary, atau clone bahan uji ke repo tugas.

## Protokol eksekusi, review, dan push

- Pelaksana membaca materi dan task aktif; reviewer membaca perubahan serta menjalankan pemeriksaan independen sesudah pelaksana selesai. Reviewer tidak mengedit implementasi.
- Reviewer mencatat di `docs/review-pengerjaan.md`: task, berkas/baris, masalah, reproduksi, dampak, rekomendasi, status, dan bukti uji ulang. Jika tidak ada temuan, tulis apa yang diperiksa tanpa mengarang kesalahan.
- Koordinator mengembalikan temuan ke pelaksana sampai selesai, lalu memeriksa diff dan menjalankan verifikasi task. Satu task aktif mengubah kode pada satu waktu.
- Saat mulai eksekusi, baca skill worktree dan subagent-driven-development. Jika memakai worktree, simpan di luar repo ini, pertahankan perubahan pengguna, dan catat branch serta path aktual. Semua perintah relatif dalam plan dijalankan di checkout implementasi.
- Target integrasi adalah `origin/main` yang sudah ada; jangan force-push. Periksa fetch/status terlebih dahulu; jika remote bergerak, integrasikan dengan aman dan ulangi pemeriksaan terdampak.
- Pilih jeda acak bilangan bulat **360–480 detik** setelah setiap pasangan commit+push berhasil; catat timestamp aktual dan jeda berikutnya. Pasangan pertama menunggu jeda sejak mulai eksekusi. Gunakan jam aktual, bukan backdate commit.
- Siapkan pekerjaan dan review selama menunggu; cek input pengguna dan beri update paling lambat setiap 60 detik. Jangan membuat background loop yang terus melakukan push setelah giliran berakhir.
- Saat jadwal tiba, commit hanya unit lengkap yang telah lolos review dan tes. Jika belum siap, tunda sampai siap dan jelaskan keterlambatan; rentang waktu bukan alasan mendorong hasil rusak atau membuat commit kosong.
- Gunakan `git add` dengan path eksplisit, commit pesan task, lalu `git push origin HEAD:main` setelah memastikan branch integrasi sesuai. Periksa kode keluar dan kecocokan SHA remote. Jika push gagal, selesaikan push commit yang sama sebelum membuat pasangan berikutnya.
- Beberapa task boleh digabung satu commit bila selesai dalam satu interval; satu task boleh memiliki beberapa commit hanya jika setiap bagian bermakna dan telah diuji. Nomor task bukan janji durasi.
- Jangan menyimpan credential/token dalam output atau dokumen.

### Task 1: Setup dan bukti membaca pohon

**Files:** buat berkas T1 dan `tests/test_tugas_awal.py` pada peta; ubah `tugas1-3/README.md`, `docs/catatan-ai.md`, README root; gunakan `scripts/cek_setup.py` dan requirements yang ada.

**Interfaces:** consumes contoh Python UTF-8 sebagai bytes; produces `python tugas1-3/t1.py` yang mencetak tiga pohon valid, klasifikasi node, dan contoh error. Skrip hanya berjalan lewat main guard.

- [ ] **Step 1:** Catat versi Python, Node, compiler dan CLI; buat venv, pasang requirements, jalankan `python scripts/cek_setup.py`. Hasil harus mencetak `module` tanpa error. Jika CLI belum ada, pasang dan catat versi aktual yang kompatibel dengan generator.
- [ ] **Step 2:** Sebelum menjalankan contoh, tulis perkiraan AI untuk ketiga pohon dalam `perkiraan.md`, beri label jelas sebagai perkiraan AI. Sediakan bagian terpisah untuk perkiraan tulisan tangan pengguna; jangan isi atas nama pengguna.
- [ ] **Step 3:** Rancang fixture `def sapa(nama): return nama`, `if aktif: ... else: ...`, kelas dengan satu method, dan fungsi kehilangan `:`; jangan buat berkas fixture dulu. Buat tes `test_contoh_pohon` yang mem-parse file itu dan mengassert tiga contoh tanpa error, satu contoh dengan error, serta contoh string `"José"` tetap utuh saat node didekode UTF-8.
- [ ] **Step 4:** Jalankan `python -m unittest discover -s tests -p test_tugas_awal.py -v`; sebelum berkas contoh ada, harus gagal karena berkas belum tersedia.
- [ ] **Step 5:** Buat keempat berkas fixture yang dirancang di Step 3, lalu implementasikan `main() -> None` dalam `t1.py`: cetak pohon dan perbandingan dengan perkiraan; tunjukkan `def`, `:`, `(`, `)` sebagai anonim melalui children dan children parameters. Jelaskan perbedaan children/named_children di README.
- [ ] **Step 6:** Jalankan tes dan `python tugas1-3/t1.py > tugas1-3/output/t1.txt`; cek output terhadap contoh, tandai selisih prediksi yang nyata. Minta pengguna menambahkan bukti tulisan tangan sebelum menutup checklist penyerahan.
- [ ] **Step 7:** Reviewer memeriksa output dan catatan AI; setelah koreksi, commit+push sesuai protokol dengan pesan `tambah contoh pohon python`.

### Task 2: Penjelajah node rekursif

**Files:** buat `tugas1-3/jelajah.py`, `tugas1-3/output/t2.txt`, `docs/bahan-uji.md`; tambah tes ke `tests/test_tugas_awal.py`, ubah README T1–3.

**Interfaces:** consumes bytes Python dari path CLI; produces `jelajah(node: Node, kedalaman: int = 0, field: str | None = None) -> None` dan `python tugas1-3/jelajah.py <file.py>`.

- [ ] **Step 1:** Tambah `test_jelajah_field` dengan sumber `x = 1\n`; assert output persis `module [1:0]\n  expression_statement [1:0]\n    assignment [1:0]\n      left: identifier [1:0]\n      right: integer [1:4]\n`. Tambah `test_posisi_utf8` pada `é = 1\n`, assert integer berada di `[1:5]` karena kolom byte.
- [ ] **Step 2:** Jalankan suite T1–3; tes baru harus gagal karena jelajah belum tersedia. Gunakan importlib untuk modul pada folder bernama `tugas1-3`, tanpa membuat paket baru.
- [ ] **Step 3:** Implementasikan traversal rekursif child bernama. Ambil field dengan indeks asli `children` dan `field_name_for_child`, bukan indeks hasil filter. CLI membaca bytes, menampilkan pesan kesalahan jika path tidak terbaca, dan tidak berjalan saat diimpor.
- [ ] **Step 4:** Clone `https://github.com/pallets/click.git` ke `/Users/hafizfs/Documents/plp-pr_tree_sitter_049-bahan-uji/click`; catat SHA, URL, lisensi dan perintah clone di `docs/bahan-uji.md`. Pilih `src/click/core.py`, pastikan jumlah baris aktual >=100; jangan menyalin sumber ke repo tugas.
- [ ] **Step 5:** Jalankan suite sampai PASS; jalankan jelajah pada file nyata itu ke `output/t2.txt`. Cocokkan satu fungsi, satu kelas dan satu field dengan parse sumber; catat lokasi yang dicek dan hasilnya.
- [ ] **Step 6:** Reviewer memeriksa field, indentasi dan sumber nyata. Commit+push sesuai protokol: `tambah penjelajah pohon`.

### Task 3: Tiga query wajib

**Files:** buat berkas T3 pada peta; tambah tes di `tests/test_tugas_awal.py`; ubah README T1–3.

**Interfaces:** consumes `python tugas1-3/q.py <file.py> <pola.scm>`; produces baris berisi nama fungsi dan jumlah parameter, pemanggilan print beserta barisnya, atau modul import beserta barisnya. `jalankan(src: bytes, pola: str) -> list[str]` menjadi fungsi yang diuji; CLI mencetak hasilnya.

- [ ] **Step 1:** Tambah `test_query_fungsi`, `test_query_print`, `test_query_import`. Fixture berisi `def f(a, /, b=1, *args, c: int=2, **kwargs): ...`, `def kosong(): ...`, `print("ya")`, `obj.print("bukan")`, string `"print(1)"`, `import os, sys as sistem`, `from pathlib import Path`, `from . import lokal`, `from ..paket import nama`. Assert f memiliki 5 parameter, kosong 0; hanya satu print langsung; modul persis os, sys, pathlib, `.`, `..paket`.
- [ ] **Step 2:** Jalankan suite, pastikan gagal karena q.py/query belum ada.
- [ ] **Step 3:** Tulis tiga query berdasarkan pohon fixture, bukan tebakan nama node. Untuk pasangan fungsi/parameters gunakan matches; hitung named child parameter dengan mengecualikan separator `/` dan `*`. Import alias dilaporkan sebagai modul asli, bukan nama alias. Parse pola tidak valid/path tidak terbaca menghasilkan pesan CLI dan status nonzero.
- [ ] **Step 4:** Jalankan suite sampai PASS. Simpan keluaran ketiga perintah dalam `output/t3.txt`; tulis tabel hitungan manual fixture di README, cocokkan setiap item dengan sumber.
- [ ] **Step 5:** Reviewer menguji hasil dan pembanding. Commit+push sesuai protokol: `tambah query kode python`.

### Task 4: Grammar DSL filter

**Files:** buat grammar, metadata, contoh dan corpus T4 pada peta; ubah README grammar; sertakan hasil generate yang diperlukan.

**Interfaces:** consumes `.filter` UTF-8; produces root `query`, `comparison` dengan field field/operator/value; `and_expression`/`or_expression` dengan left/right; `not_expression` dengan operand; `parenthesized`; `in_expression` dengan field dan values; `contains_expression` dengan field dan value string. Values in adalah node `value_list` berisi satu atau lebih string/number/boolean.

- [ ] **Step 1:** Jalankan `tree-sitter init` dalam folder yang sudah ada, nama filter, ekstensi filter. Simpan README yang sudah ada; catat file hasil init aktual. Jangan buat scaffold kedua.
- [ ] **Step 2:** Tambah corpus secara bertahap sebelum rule terkait: perbandingan string/angka/boolean; `a = 1 or b = 2 and c = 3`; `(a = 1 or b = 2) and c = 3`; `not a = 1 and b = 2`; `status in ("open", "pending", "closed")`; `title contains "invoice"`; `android = true or origin = false`; input rusak `status in ()` dan `a =` dengan ERROR/MISSING yang diharapkan. Tulis expected tree secara eksplisit untuk tiap kasus; jangan memakai test --update tanpa pemeriksaan.
- [ ] **Step 3:** Jalankan generate/test tiap penambahan; rekam kegagalan nyata rule yang belum didukung.
- [ ] **Step 4:** Bangun grammar berurutan: comparison → or → and → not → kurung → field → in → contains. Precedence or=1, and=2, not=3, and/or left associative; word menunjuk identifier; in tidak menerima daftar kosong; contains hanya menerima string. Tetap gunakan aturan nilai sederhana materi, tanpa ekspansi escape/angka negatif yang tidak diminta.
- [ ] **Step 5:** Jalankan `tree-sitter generate`, `tree-sitter test`, `tree-sitter parse contoh.filter`. Semua corpus harus PASS; contoh valid tanpa ERROR. Reviewer memastikan subtree kasus prioritas dan in tiga nilai secara langsung.
- [ ] **Step 6:** Simpan ringkasan tes dan keterbatasan grammar di README/catatan AI. Commit+push sesuai protokol: `tambah grammar filter`.

### Task 5: Highlight DSL

**Files:** buat highlights.scm dan output T5 pada peta; ubah tree-sitter.json dan README grammar bila diperlukan.

**Interfaces:** consumes node grammar T4; produces capture keyword, operator, string, number, constant.builtin, property untuk seluruh field comparison/in/contains, serta HTML hasil CLI.

- [ ] **Step 1:** Lengkapi contoh.filter sebagai satu ekspresi valid yang mengandung semua keyword, semua operator perbandingan, ketiga tipe nilai, dan ketiga bentuk field. Jalankan query highlight yang belum ada, pastikan gagal sebelum implementasi.
- [ ] **Step 2:** Buat highlights.scm; metadata menunjuk query dan file-types filter. Konfigurasi CLI menggunakan parser-directories folder induk checkout; jangan menimpa pengaturan pengguna lainnya.
- [ ] **Step 3:** Jalankan `tree-sitter query queries/highlights.scm contoh.filter > output/captures.txt` serta `tree-sitter highlight --html contoh.filter > output/highlight.html`. Pastikan capture mencakup and/or/not/in/contains, =/!=/>/</>=/<=, setiap tipe nilai dan nama field.
- [ ] **Step 4:** Buka HTML, periksa warna setiap kategori, ambil screenshot nyata ke folder bukti eksternal. Jika tema menyamakan warna keyword dan boolean, pilih tema lokal untuk demonstrasi dengan warna kategori berbeda; jangan mengubah tema global pengguna.
- [ ] **Step 5:** Reviewer memeriksa capture dan tampilan, ulangi corpus agar query tidak mengubah grammar. Commit+push sesuai protokol: `tambah highlight filter`.

### Task 6: CLI TODO, fungsi panjang dan error

**Files:** buat berkas T6 pada peta dan `tests/test_cek.py`; ubah `cek/README.md`.

**Interfaces:** `cek_file(path: Path) -> list[str]` dalam `cek/cek.py`, tidak mencetak sendiri; `main() -> int` mencetak laporan, memindai folder rekursif `.py`, melewati .git/.venv/venv/node_modules sebelum turun ke direktori itu. Output `path:baris: TODO/FIXME ...`, `path:baris: fungsi nama (N baris)`, `path:baris: kesalahan sintaks`. Posisi baris 1-based. Temuan tidak membuat exit gagal; argumen/path/I/O error menghasilkan status nonzero dan pesan jelas.

- [ ] **Step 1:** Tambah tes `test_todo_komentar_saja` dengan komentar TODO/FIXME dan string serupa (assert hanya 2 temuan); `test_batas_fungsi` dengan fungsi 30 dan 31 baris termasuk def (assert hanya 31), serta nested/method yang ikut terdeteksi; `test_error_dan_missing` dengan dua input berbeda yang benar-benar menghasilkan ERROR dan MISSING; `test_cli_path_dan_skip` untuk folder tak ada, argumen kosong, folder terlewati, dan file gagal dibaca memakai mock OSError. Tambah `test_teks_rusak` agar decode errors=replace tetap menghasilkan laporan.
- [ ] **Step 2:** Jalankan `python -m unittest discover -s tests -p test_cek.py -v`; pastikan gagal karena fungsi belum ada.
- [ ] **Step 3:** Implementasikan query comment + #match? TODO|FIXME, query pasangan fungsi/nama, dan pencarian rekursif error/missing pertama menurut urutan sumber. Untuk panjang ikuti langkah/rubrik materi: `end_point[0] - start_point[0] + 1` dari function_definition, termasuk def; dokumentasikan keputusan ini karena checklist menyebut body. Gunakan os.walk untuk pruning dan urutan path stabil, tanpa dependency baru.
- [ ] **Step 4:** Jalankan semua unittest sampai PASS, lalu `python cek/cek.py cek/uji > cek/output/uji.txt`. Cocokkan setiap temuan dengan fixture.
- [ ] **Step 5:** Jalankan CLI pada clone Click yang SHA-nya dicatat di Task 2, simpan `repo-nyata.txt`. Pilih 2 file Python acak memakai seed yang dicatat dan random.sample dari path terurut; simpan nama, seed, hitungan manual semua kategori, lokasi temuan/ketiadaan temuan dan selisih dalam `verifikasi-manual.md`. Jangan memakai hasil CLI sebagai satu-satunya pembanding manual.
- [ ] **Step 6:** Lengkapi README dengan instalasi, perintah, output nyata, definisi panjang fungsi, perlakuan nested function, direktori terlewati, dan exit code. Reviewer mengulang tes batas serta sampling.
- [ ] **Step 7:** Commit+push sesuai protokol: `tambah pemeriksa kode python`.

### Task 7: Dokumentasi, bukti AI dan verifikasi akhir repo

**Files:** ubah README root, seluruh README unit, `docs/catatan-ai.md`, `docs/review-pengerjaan.md`, `docs/bahan-uji.md`.

**Interfaces:** consumes output dan temuan T1–6; produces panduan reproduksi dari checkout bersih serta daftar kekurangan manusia/format yang belum terselesaikan.

- [ ] **Step 1:** Hapus status “belum diimplementasikan” hanya untuk bagian terbukti selesai. Dokumentasikan semua perintah dari root atau folder yang disebut jelas, versi aktual, SHA bahan uji, dan lokasi dokumen eksternal.
- [ ] **Step 2:** Untuk setiap tugas, isi permintaan AI, kesalahan/kekurangan yang benar-benar ditemukan, reproduksi, perbaikan, bukti uji. Bila tidak menemukan kesalahan, tulis apa adanya dan tandai kebutuhan rubrik sebagai belum terpenuhi; jangan sengaja membuat bug demi catatan.
- [ ] **Step 3:** Jalankan `python scripts/cek_setup.py`, `python -m unittest discover -s tests -v`, perintah T1–3, corpus grammar, parse dan query/highlight, CLI fixture dan repo nyata. Baca hasil; cek path dokumen eksternal tidak masuk git status/staging. Tidak memakai compileall atas fixture sintaks rusak sebagai syarat kelulusan.
- [ ] **Step 4:** Reviewer memetakan rubrik 10/15/15/20/10/20/10 ke bukti yang tersedia; koordinator memeriksa diff akhir dan daftar bagian yang masih butuh pengguna, khususnya perkiraan tulisan tangan dan demo pemahaman.
- [ ] **Step 5:** Setelah koreksi, commit+push sesuai protokol: `lengkapi bukti praktikum`. Catat SHA lokal dan remote yang sama.

### Task 8: Laporan dan proposal DOCX di luar repo

**Files:** hanya `/Users/hafizfs/Documents/plp-pr_tree_sitter_049-laporan/laporan.docx`, `proposal-draf.docx`, dan bahan/render dalam folder tersebut. Tidak mengubah repo pada task ini.

**Interfaces:** consumes bukti aktual T1–7; produces laporan <=3 halaman dan proposal <=1 halaman siap ditinjau, bukan dipublikasikan.

- [ ] **Step 1:** Baca skill DOCX/dokumen saat eksekusi; buat folder eksternal tanpa menimpa file pengguna yang sudah ada. Kumpulkan screenshot asli pohon, traversal/query, corpus/highlight, dan CLI ke subfolder bukti.
- [ ] **Step 2:** Susun laporan: identitas kosong yang jelas untuk diisi pengguna, ringkasan keenam tugas, screenshot terbaca, kendala/solusi dan catatan AI berdasarkan ledger. Jangan mengklaim tindakan pengguna yang belum dilakukan. Prioritaskan bukti inti agar muat 3 halaman.
- [ ] **Step 3:** Susun proposal “Pendeteksi console.log dan debugger pada JavaScript sebelum rilis”: pengguna developer/reviewer; dua aturan sintaks; target JavaScript Node.js/Express dengan tree-sitter-javascript. Scope proposal tidak mencakup implementasi proyek lanjut.
- [ ] **Step 4:** Isi kesembilan unsur template: judul; masalah; alasan determinisme/biaya dibanding review AI; bahasa/framework/grammar; contoh positif `console.log(user)` dan `debugger;`, negatif string/komentar serta `logger.info(user)`; rancangan query; output terminal path/baris/aturan; evaluasi satu repo JavaScript publik dengan SHA dicatat saat dipilih dan pemeriksaan manual 20 temuan atau seluruhnya jika kurang; rencana kerja 5 pertemuan dan risiko false positive akibat console yang di-shadow. Verifikasi query pada snippet dengan grammar JavaScript yang sudah ada, tanpa membangun tool proyek.
- [ ] **Step 5:** Render kedua DOCX, hitung halaman dan inspeksi setiap halaman sebagai gambar. Koreksi overflow, tabel/screenshot kecil, dan judul terpotong sampai laporan <=3 dan proposal <=1 halaman; render PDF sementara hanya untuk QA di folder eksternal jika dibutuhkan tool.
- [ ] **Step 6:** Reviewer mencocokkan klaim dokumen dengan bukti; koordinator menyampaikan link kedua DOCX, batasan yang belum beres, dan instruksi bahwa pengguna mengekspor PDF sesuai materi serta melakukan push manual. Tidak ada commit/push dokumen akhir oleh agent.

## Handoff dan pemeriksaan plan

Plan ini disusun untuk satu rangkaian praktikum dengan tiga unit yang dapat diuji terpisah, bukan satu aplikasi besar. Task 1–3, 4–5, dan 6 menjadi batas review; Task 7 dan 8 menggabungkan bukti.

Self-review koordinator sebelum diserahkan: seluruh tugas wajib dan syarat pengumpulan dipetakan; lima review focus memiliki tes; interface CLI konsisten; dependency baru untuk tes tidak diperlukan; pengayaan tidak masuk scope. Syarat PDF berbeda dari permintaan DOCX dicatat terang, begitu pula tindakan tulisan tangan pengguna yang tidak bisa digantikan agent.

**Status:** menunggu tinjauan pengguna; belum ada implementasi, instalasi, commit, atau push dari plan ini. Setelah plan disetujui, jalankan pelaksana dan reviewer sesuai metode dua subagent yang telah dipilih.
