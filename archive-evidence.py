#!/usr/bin/env python3
"""Archive OxFunc's untracked oracle evidence into this repository as deterministic gzip blobs.

Mirrors ``<source>/cache`` and ``<source>/runs`` (default source: ``../OxFunc/smart-fuzzer``)
into ``cache/`` and ``runs/`` here, one ``<path>.gz`` per file, with a ``manifest.tsv`` of raw and
compressed sizes and SHA-256 hashes. Blobs are written with an empty gzip name field and
``mtime=0`` (the ``gzip -n`` convention), so an unchanged file produces a byte-identical blob and
git stores nothing new for it. Third-party binaries listed in ``EXCLUDED_PREFIXES`` are hashed
into ``excluded.tsv`` but never copied.

    python archive-evidence.py archive            # refresh blobs and manifest from the source tree
    python archive-evidence.py verify --sample 50 # decompress a random manifest sample and compare hashes
    python archive-evidence.py verify --all       # decompress everything and compare hashes
    python archive-evidence.py restore <dir>      # decompress every blob into <dir>, verifying hashes
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import os
import random
import sys
from pathlib import Path

ROOTS = ('cache', 'runs')
# Re-downloadable third-party material, about 300 MB: the Intel MKL wheel and its extracted DLLs.
EXCLUDED_PREFIXES = ('runs/w108a-reference-hunt/mkl_dl/',)
CHUNK = 1 << 20
GITHUB_BLOB_LIMIT = 100 * 1024 * 1024


def rel_posix(path: Path, base: Path) -> str:
    return path.relative_to(base).as_posix()


def read_manifest(path: Path) -> dict[str, tuple[int, str, int, str]]:
    rows: dict[str, tuple[int, str, int, str]] = {}
    if not path.is_file():
        return rows
    with path.open(encoding='utf-8') as fh:
        header = fh.readline()
        for line in fh:
            parts = line.rstrip('\n').split('\t')
            if len(parts) == 5:
                rows[parts[0]] = (int(parts[1]), parts[2], int(parts[3]), parts[4])
    return rows


def write_tsv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    with path.open('w', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join(header) + '\n')
        for row in rows:
            fh.write('\t'.join(row) + '\n')


def sha256_of(path: Path) -> tuple[int, str]:
    h = hashlib.sha256()
    size = 0
    with path.open('rb') as fh:
        while True:
            block = fh.read(CHUNK)
            if not block:
                break
            size += len(block)
            h.update(block)
    return size, h.hexdigest()


def compress_and_hash(src: Path, dst: Path, level: int) -> tuple[int, str, int, str]:
    raw = hashlib.sha256()
    raw_size = 0
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + '.tmp')
    with src.open('rb') as fin, tmp.open('wb') as fout:
        with gzip.GzipFile(filename='', mode='wb', compresslevel=level, fileobj=fout, mtime=0) as gz:
            while True:
                block = fin.read(CHUNK)
                if not block:
                    break
                raw_size += len(block)
                raw.update(block)
                gz.write(block)
    os.replace(tmp, dst)
    gz_size, gz_sha = sha256_of(dst)
    return raw_size, raw.hexdigest(), gz_size, gz_sha


def decompress_hash(blob: Path, out: Path | None = None) -> tuple[int, str]:
    h = hashlib.sha256()
    size = 0
    sink = None
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        sink = out.open('wb')
    try:
        with gzip.open(blob, 'rb') as gz:
            while True:
                block = gz.read(CHUNK)
                if not block:
                    break
                size += len(block)
                h.update(block)
                if sink is not None:
                    sink.write(block)
    finally:
        if sink is not None:
            sink.close()
    return size, h.hexdigest()


def cmd_archive(args: argparse.Namespace) -> int:
    source = args.source.resolve()
    dest = args.dest.resolve()
    manifest_path = dest / 'manifest.tsv'
    previous = read_manifest(manifest_path)
    rows: list[list[str]] = []
    excluded: list[list[str]] = []
    written = skipped = 0
    raw_total = gz_total = 0
    largest: tuple[int, str] = (0, '')
    for root in ROOTS:
        base = source / root
        if not base.is_dir():
            print(f'missing source directory: {base}', file=sys.stderr)
            return 2
        for path in sorted(p for p in base.rglob('*') if p.is_file()):
            rel = root + '/' + rel_posix(path, base)
            if any(rel.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
                size, sha = sha256_of(path)
                excluded.append([rel, str(size), sha])
                continue
            blob = dest / (rel + '.gz')
            prev = previous.get(rel)
            if prev is not None and blob.is_file() and prev[0] == path.stat().st_size:
                size, sha = sha256_of(path)
                if sha == prev[1]:
                    rows.append([rel, str(prev[0]), prev[1], str(prev[2]), prev[3]])
                    skipped += 1
                    raw_total += prev[0]
                    gz_total += prev[2]
                    if prev[2] > largest[0]:
                        largest = (prev[2], rel)
                    continue
            raw_size, raw_sha, gz_size, gz_sha = compress_and_hash(path, blob, args.level)
            rows.append([rel, str(raw_size), raw_sha, str(gz_size), gz_sha])
            written += 1
            raw_total += raw_size
            gz_total += gz_size
            if gz_size > largest[0]:
                largest = (gz_size, rel)
    rows.sort()
    excluded.sort()
    write_tsv(manifest_path, ['path', 'raw_bytes', 'raw_sha256', 'gz_bytes', 'gz_sha256'], rows)
    write_tsv(dest / 'excluded.tsv', ['path', 'raw_bytes', 'raw_sha256'], excluded)
    # Blobs whose source file disappeared are reported, not deleted; delete them deliberately.
    current = {row[0] for row in rows}
    stale = [rel for rel in previous if rel not in current]
    print(f'files archived: {len(rows)} (written {written}, unchanged {skipped}); excluded: {len(excluded)}')
    print(f'raw bytes: {raw_total:,}; gzip bytes: {gz_total:,}; largest blob: {largest[0]:,} bytes ({largest[1]})')
    if largest[0] > GITHUB_BLOB_LIMIT:
        print('WARNING: a blob exceeds 100 MB, which GitHub rejects', file=sys.stderr)
    if stale:
        print(f'stale blobs no longer in the source ({len(stale)}): ' + ', '.join(stale[:10]) + (' ...' if len(stale) > 10 else ''))
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    dest = args.dest.resolve()
    manifest = read_manifest(dest / 'manifest.tsv')
    if not manifest:
        print('empty or missing manifest', file=sys.stderr)
        return 2
    keys = sorted(manifest)
    if not args.all:
        rng = random.Random(args.seed)
        keys = rng.sample(keys, min(args.sample, len(keys)))
    bad = 0
    for rel in keys:
        raw_size, raw_sha, gz_size, gz_sha = manifest[rel]
        blob = dest / (rel + '.gz')
        if not blob.is_file():
            print(f'MISSING {rel}')
            bad += 1
            continue
        size, sha = decompress_hash(blob)
        if size != raw_size or sha != raw_sha:
            print(f'MISMATCH {rel}: manifest {raw_size}/{raw_sha[:12]} vs blob {size}/{sha[:12]}')
            bad += 1
    print(f'verified {len(keys)} of {len(manifest)} entries; failures: {bad}')
    return 1 if bad else 0


def cmd_restore(args: argparse.Namespace) -> int:
    dest = args.dest.resolve()
    target = args.target.resolve()
    manifest = read_manifest(dest / 'manifest.tsv')
    bad = 0
    for rel, (raw_size, raw_sha, _, _) in sorted(manifest.items()):
        size, sha = decompress_hash(dest / (rel + '.gz'), target / rel)
        if size != raw_size or sha != raw_sha:
            print(f'MISMATCH {rel}')
            bad += 1
    print(f'restored {len(manifest)} files into {target}; failures: {bad}')
    return 1 if bad else 0


def main() -> int:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--source', type=Path, default=here.parent / 'OxFunc' / 'smart-fuzzer', help='directory holding cache/ and runs/')
    ap.add_argument('--dest', type=Path, default=here, help='this repository root')
    sub = ap.add_subparsers(dest='command', required=True)
    a = sub.add_parser('archive')
    a.add_argument('--level', type=int, default=6)
    a.set_defaults(func=cmd_archive)
    v = sub.add_parser('verify')
    v.add_argument('--sample', type=int, default=50)
    v.add_argument('--seed', type=int, default=None)
    v.add_argument('--all', action='store_true')
    v.set_defaults(func=cmd_verify)
    r = sub.add_parser('restore')
    r.add_argument('target', type=Path)
    r.set_defaults(func=cmd_restore)
    args = ap.parse_args()
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
