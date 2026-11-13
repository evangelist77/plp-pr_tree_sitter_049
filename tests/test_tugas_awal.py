"""Bukti contoh Tugas 1 dapat diparse, termasuk UTF-8 dan pemulihan error."""
from pathlib import Path
import unittest
import contextlib
import importlib.util
import io
import subprocess
import sys
import tempfile

import tree_sitter_python as tspython
from tree_sitter import Language, Parser

ROOT = Path(__file__).resolve().parents[1]
CONTOH = ROOT / "tugas1-3" / "contoh"


class TugasAwalTests(unittest.TestCase):
    def load_query(self):
        spec = importlib.util.spec_from_file_location(
            "q", ROOT / "tugas1-3" / "q.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def query(self, name, source=None):
        module = self.load_query()
        if source is None:
            source = (CONTOH / "query.py").read_bytes()
        pattern = (ROOT / "tugas1-3" / "queries" / f"{name}.scm").read_text()
        return module.jalankan(source, pattern)

    def test_query_fungsi(self):
        # Salah menghitung separator atau memasangkan capture antarfungsi gagal di sini.
        self.assertEqual(self.query("fungsi"), ["f: 5 parameter", "kosong: 0 parameter"])
        self.assertEqual(self.query("fungsi", "def café(*, x: int): ...\n".encode()),
                         ["café: 1 parameter"])

    def test_query_print(self):
        # Attribute dan teks string tidak boleh menjadi pemanggilan print langsung.
        self.assertEqual(self.query("print"), ['baris 3: print("ya")'])

    def test_query_import(self):
        # Nama alias dan objek yang diimpor tidak boleh menggantikan modul asal.
        self.assertEqual(self.query("import"), [
            "baris 6: os", "baris 6: sys", "baris 7: pathlib",
            "baris 8: .", "baris 9: ..paket"])

    def test_query_cli(self):
        command = [sys.executable, str(ROOT / "tugas1-3" / "q.py")]
        fixture = str(CONTOH / "query.py")
        pattern = str(ROOT / "tugas1-3" / "queries" / "fungsi.scm")
        result = subprocess.run(command + [fixture, pattern],
                                capture_output=True, text=True, check=True)
        self.assertEqual(result.stdout, "f: 5 parameter\nkosong: 0 parameter\n")
        with tempfile.TemporaryDirectory() as directory:
            invalid = Path(directory) / "invalid.scm"
            invalid.write_text("(tidak_ada) @x")
            bad_utf8 = Path(directory) / "invalid-utf8.scm"
            bad_utf8.write_bytes(b"\xff")
            for args, message in (
                ([str(CONTOH / "tidak-ada.py"), pattern], "tidak dapat membaca"),
                ([fixture, str(Path(directory) / "hilang.scm")], "tidak dapat membaca"),
                ([fixture, str(invalid)], "pola tidak valid"),
                ([fixture, str(bad_utf8)], "tidak dapat membaca"),
            ):
                with self.subTest(args=args):
                    result = subprocess.run(command + args, capture_output=True, text=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(message, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
        imported = subprocess.run(
            [sys.executable, "-c", "import runpy; runpy.run_path('tugas1-3/q.py')"],
            cwd=ROOT, capture_output=True, text=True, check=True)
        self.assertEqual(imported.stdout, "")

    def load_jelajah(self):
        spec = importlib.util.spec_from_file_location(
            "jelajah", ROOT / "tugas1-3" / "jelajah.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_jelajah_field(self):
        module = self.load_jelajah()
        root = Parser(Language(tspython.language())).parse(b"x = 1\n").root_node
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            module.jelajah(root)
        self.assertEqual(output.getvalue(),
                         "module [1:0]\n"
                         "  expression_statement [1:0]\n"
                         "    assignment [1:0]\n"
                         "      left: identifier [1:0]\n"
                         "      right: integer [1:4]\n")

    def test_posisi_utf8(self):
        module = self.load_jelajah()
        root = Parser(Language(tspython.language())).parse("é = 1\n".encode()).root_node
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            module.jelajah(root)
        self.assertIn("      right: integer [1:5]\n", output.getvalue())

    def test_jelajah_cli_and_quiet_import(self):
        self.load_jelajah()
        result = subprocess.run(
            [sys.executable, str(ROOT / "tugas1-3" / "jelajah.py"),
             str(CONTOH / "fungsi.py")], capture_output=True, text=True, check=True)
        self.assertIn("name: identifier [1:4]", result.stdout)
        missing = subprocess.run(
            [sys.executable, str(ROOT / "tugas1-3" / "jelajah.py"),
             str(CONTOH / "tidak-ada.py")], capture_output=True, text=True)
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("tidak dapat membaca", missing.stderr)
        self.assertNotIn("Traceback", missing.stderr)
        imported = subprocess.run(
            [sys.executable, "-c",
             "import runpy; runpy.run_path('tugas1-3/jelajah.py')"],
            cwd=ROOT, capture_output=True, text=True, check=True)
        self.assertEqual(imported.stdout, "")

    def test_contoh_pohon(self):
        parser = Parser(Language(tspython.language()))
        for filename, expected_type in (
            ("fungsi.py", "function_definition"),
            ("kondisi.py", "if_statement"),
            ("kelas.py", "class_definition"),
        ):
            with self.subTest(filename=filename):
                root = parser.parse((CONTOH / filename).read_bytes()).root_node
                self.assertFalse(root.has_error)
                self.assertEqual(root.named_children[0].type, expected_type)
        broken = parser.parse((CONTOH / "rusak.py").read_bytes()).root_node
        self.assertTrue(broken.has_error)
        source = (CONTOH / "kondisi.py").read_bytes()
        root = parser.parse(source).root_node
        stack = [root]
        strings = []
        while stack:
            node = stack.pop()
            if node.type == "string":
                strings.append(source[node.start_byte:node.end_byte].decode("utf-8"))
            stack.extend(node.children)
        self.assertIn('"José"', strings)

    def test_t1_output_and_quiet_import(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tugas1-3" / "t1.py")],
            capture_output=True, text=True, check=True,
        )
        for token in ("function_definition", "if_statement", "class_definition",
                      "def anonim", ": anonim", "( anonim", ") anonim"):
            self.assertIn(token, result.stdout)
        self.assertRegex(result.stdout, r"\((?:ERROR|MISSING)")
        imported = subprocess.run(
            [sys.executable, "-c",
             "import runpy; runpy.run_path('tugas1-3/t1.py')"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        self.assertEqual(imported.stdout, "")


if __name__ == "__main__":
    unittest.main()
