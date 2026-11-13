"""Periksa komentar TODO/FIXME, fungsi >30 baris, dan kesalahan sintaks Python."""
import argparse
import os
from pathlib import Path
import sys

import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, '(function_definition name: (identifier) @nama) @fungsi')


def error_pertama(node):
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        if child.has_error or child.is_missing:
            error = error_pertama(child)
            if error is not None:
                return error
    return None


def cek_file(path: Path) -> list[str]:
    # Predicate #match? mendecode capture sebelum hasil dikembalikan binding Python.
    source = path.read_bytes().decode('utf-8', errors='replace').encode('utf-8')
    tree = Parser(PY).parse(source)
    temuan = []
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get('c', []):
        teks = node.text.decode('utf-8', errors='replace').lstrip('#').strip()
        temuan.append((node.start_byte, f'{path}:{node.start_point[0] + 1}: {teks}'))
    for _, captures in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        node = captures['fungsi'][0]
        jumlah = node.end_point[0] - node.start_point[0] + 1
        if jumlah > 30:
            nama = captures['nama'][0].text.decode('utf-8', errors='replace')
            temuan.append((node.start_byte,
                           f'{path}:{node.start_point[0] + 1}: fungsi {nama} ({jumlah} baris)'))
    error = error_pertama(tree.root_node)
    if error is not None:
        temuan.append((error.start_byte, f'{path}:{error.start_point[0] + 1}: kesalahan sintaks'))
    return [laporan for _, laporan in sorted(temuan)]


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('folder', type=Path)
    args = cli.parse_args()
    def gagal(error):
        raise error

    try:
        if not args.folder.is_dir():
            cli.error(f'bukan folder yang dapat diperiksa: {args.folder}')
        files = []
        for directory, dirs, names in os.walk(args.folder, onerror=gagal):
            dirs[:] = sorted(set(dirs) - {'.git', '.venv', 'venv', 'node_modules'})
            files.extend(Path(directory) / name for name in names if name.endswith('.py'))
        for path in sorted(files):
            for laporan in cek_file(path):
                print(laporan)
    except OSError as error:
        print(f'tidak dapat membaca input: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
