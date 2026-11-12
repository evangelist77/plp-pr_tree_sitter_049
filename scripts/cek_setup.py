"""Uji cepat lingkungan dari bagian 4 materi."""
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))
tree = parser.parse(b"def halo(nama):\n    return nama\n")
print(tree.root_node)
if tree.root_node.has_error:
    raise SystemExit("Setup gagal: hasil parse mengandung error")
