"""Jalankan query Python; pasangan @nama/@params dihitung sebagai parameter."""
import argparse
from pathlib import Path

import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor, QueryError


def jalankan(src: bytes, pola: str) -> list[str]:
    language = Language(tspython.language())
    tree = Parser(language).parse(src)
    cursor = QueryCursor(Query(language, pola))
    hasil = []
    for _, cap in cursor.matches(tree.root_node):
        if "nama" in cap and "params" in cap:
            nama = cap["nama"][0].text.decode("utf-8")
            jumlah = sum(child.type not in {
                "positional_separator", "keyword_separator", "comment"
            } for child in cap["params"][0].named_children)
            hasil.append(f"{nama}: {jumlah} parameter")
        else:
            for nama, nodes in cap.items():
                if nama.startswith("_"):
                    continue
                for node in nodes:
                    hasil.append(f"baris {node.start_point[0] + 1}: "
                                 f"{node.text.decode('utf-8')}")
    return hasil


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("file", type=Path)
    cli.add_argument("pola", type=Path)
    args = cli.parse_args()
    try:
        source = args.file.read_bytes()
        pattern = args.pola.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        cli.error(f"tidak dapat membaca input: {error}")
    try:
        hasil = jalankan(source, pattern)
    except QueryError as error:
        cli.error(f"pola tidak valid: {error}")
    for baris in hasil:
        print(baris)


if __name__ == "__main__":
    main()
