"""Cetak contoh pohon Python, node anonim, dan pemulihan sintaks rusak."""
from pathlib import Path

import tree_sitter_python as tspython
from tree_sitter import Language, Parser


def main() -> None:
    parser = Parser(Language(tspython.language()))
    contoh = Path(__file__).resolve().parent / "contoh"
    comparisons = {
        "fungsi": "Sesuai: function_definition, parameters, block, return_statement.",
        "kondisi": "Struktur if/else sesuai; prediksi (string) belum memuat string_start, string_content, string_end.",
        "kelas": "Sesuai: class_definition berisi satu function_definition di block.",
    }
    for name, comparison in comparisons.items():
        root = parser.parse((contoh / f"{name}.py").read_bytes()).root_node
        print(f"=== {name}.py ===")
        print(root)
        print(f"has_error: {root.has_error}")
        print(f"Perbandingan dengan perkiraan AI: {comparison}")
        if name == "fungsi":
            function = root.named_children[0]
            print("children fungsi:")
            for child in function.children:
                print(child.type, "bernama" if child.is_named else "anonim")
            print("children parameters:")
            for child in function.child_by_field_name("parameters").children:
                print(child.type, "bernama" if child.is_named else "anonim")
            print("named_children fungsi:", [child.type for child in function.named_children])
        print()

    broken = parser.parse((contoh / "rusak.py").read_bytes()).root_node
    print("=== rusak.py (kehilangan ':') ===")
    print(broken)
    print(f"has_error: {broken.has_error}")
    print("Perkiraan ERROR/MISSING: periksa penanda pemulihan pada pohon di atas.")


if __name__ == "__main__":
    main()
