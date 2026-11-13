"""Kontrak checker: komentar, batas inklusif, recovery, dan kegagalan I/O."""
import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tree_sitter import Language, Parser
import tree_sitter_python as tspython

ROOT = Path(__file__).resolve().parents[1]


class CekTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('cek', ROOT / 'cek/cek.py')
        self.cek = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.cek)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)

    def source(self, text):
        path = self.folder / 'contoh.py'
        path.write_bytes(text if isinstance(text, bytes) else text.encode())
        return path

    def cli(self, *args):
        return subprocess.run([sys.executable, str(ROOT / 'cek/cek.py'), *map(str, args)],
                              capture_output=True, text=True)

    def test_todo_komentar_saja(self):
        path = self.source('s = "TODO FIXME"\n# TODO nanti\nx = 1 # FIXME ini\n')
        with contextlib.redirect_stdout(io.StringIO()) as output:
            hasil = self.cek.cek_file(path)
        self.assertEqual(output.getvalue(), '')
        self.assertEqual(hasil, [f'{path}:2: TODO nanti', f'{path}:3: FIXME ini'])

    def test_batas_fungsi(self):
        # Salah memakai body atau > 31 akan kehilangan fungsi kedua.
        path = self.source('def tiga_puluh():\n' + '    pass\n' * 29 +
                           'def lebih():\n' + '    pass\n' * 30)
        self.assertEqual(self.cek.cek_file(path), [f'{path}:31: fungsi lebih (31 baris)'])
        path = self.source('class K:\n    def metode(self):\n        def dalam():\n' +
                           '            pass\n' * 30)
        self.assertEqual(self.cek.cek_file(path), [
            f'{path}:2: fungsi metode (32 baris)', f'{path}:3: fungsi dalam (31 baris)'])

    def test_error_dan_missing(self):
        for text, kind in [('x =\n', 'ERROR'), ('def f(:\n    pass\n', 'MISSING')]:
            with self.subTest(kind=kind):
                path = self.source(text)
                tree = Parser(Language(tspython.language())).parse(path.read_bytes())
                self.assertIn(kind, str(tree.root_node))
                self.assertEqual(self.cek.cek_file(path), [f'{path}:1: kesalahan sintaks'])
        path = self.source('# TODO satu\nx =\ny =\n')
        self.assertEqual(self.cek.cek_file(path), [f'{path}:1: TODO satu',
                                                f'{path}:2: kesalahan sintaks'])

    def test_cli_path_dan_skip(self):
        for args in [(), (self.folder / 'hilang',), (self.source('pass\n'),)]:
            result = self.cli(*args)
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(result.stderr)
            self.assertNotIn('Traceback', result.stderr)
        for name in ['.git', '.venv', 'venv', 'node_modules']:
            hidden = self.folder / name / 'sub'
            hidden.mkdir(parents=True)
            (hidden / 'skip.py').write_text('# TODO jangan\n')
        (self.folder / 'z.py').write_text('# TODO z\n')
        (self.folder / 'a.py').write_text('# FIXME a\n')
        sub = self.folder / 'b'
        sub.mkdir()
        (sub / 'c.py').write_text('# TODO c\n')
        result = self.cli(self.folder)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.splitlines(), [f'{self.folder}/a.py:1: FIXME a',
                         f'{sub}/c.py:1: TODO c', f'{self.folder}/z.py:1: TODO z'])
        with patch.object(sys, 'argv', ['cek.py', str(self.folder)]), \
                patch.object(Path, 'read_bytes', side_effect=OSError('izin ditolak')), \
                contextlib.redirect_stderr(io.StringIO()) as error:
            self.assertNotEqual(self.cek.main(), 0)
        self.assertIn('izin ditolak', error.getvalue())
        with patch.object(sys, 'argv', ['cek.py', str(self.folder)]), \
                patch.object(self.cek.os, 'scandir', side_effect=OSError('direktori ditolak')), \
                contextlib.redirect_stderr(io.StringIO()) as error:
            self.assertNotEqual(self.cek.main(), 0)
        self.assertIn('direktori ditolak', error.getvalue())

    def test_cli_validasi_folder_gagal(self):
        with patch.object(sys, 'argv', ['cek.py', str(self.folder)]), \
                patch.object(Path, 'is_dir', side_effect=PermissionError('stat ditolak')), \
                contextlib.redirect_stderr(io.StringIO()) as error:
            self.assertEqual(self.cek.main(), 1)
        self.assertIn('tidak dapat membaca input', error.getvalue())
        self.assertIn('stat ditolak', error.getvalue())
        self.assertNotIn('Traceback', error.getvalue())

    def test_teks_rusak(self):
        path = self.source(b'# TODO \xff\n')
        self.assertEqual(self.cek.cek_file(path), [f'{path}:1: TODO \ufffd'])


if __name__ == '__main__':
    unittest.main()
