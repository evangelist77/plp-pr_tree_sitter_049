"""Cetak node bernama Python beserta kedalaman, field, dan posisi byte."""
import argparse
from pathlib import Path

import tree_sitter_python as tspython
from tree_sitter import Language, Node, Parser


def jelajah(node: Node, kedalaman: int = 0, field: str | None = None) -> None:
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
    for i, child in enumerate(node.children):
        if child.is_named:
            jelajah(child, kedalaman + 1, node.field_name_for_child(i))


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("file", type=Path)
    args = cli.parse_args()
    try:
        source = args.file.read_bytes()
    except OSError as error:
        cli.error(f"tidak dapat membaca {args.file}: {error}")
    parser = Parser(Language(tspython.language()))
    jelajah(parser.parse(source).root_node)


if __name__ == "__main__":
    main()
