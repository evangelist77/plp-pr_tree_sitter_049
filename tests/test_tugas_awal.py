"""Bukti contoh Tugas 1 dapat diparse, termasuk UTF-8 dan pemulihan error."""
from pathlib import Path
import unittest
import subprocess
import sys

import tree_sitter_python as tspython
from tree_sitter import Language, Parser

ROOT = Path(__file__).resolve().parents[1]
CONTOH = ROOT / "tugas1-3" / "contoh"


class TugasAwalTests(unittest.TestCase):
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
