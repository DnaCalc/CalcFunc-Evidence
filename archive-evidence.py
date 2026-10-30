#!/usr/bin/env python3
"""Archive OxFunc's git-ignored oracle evidence into this repository as deterministic gzip blobs.

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
    python archive-evidence.py restore <dir> --sample 100 --seed 7  # restore a random manifest sample

A sample is drawn from the sorted manifest paths with ``random.Random(seed)``; without ``--seed`` a
seed is drawn and printed, so every sample can be drawn again. ``restore`` refuses a target
directory that already holds anything, so it never mixes with or overwrites other files.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import os
import random
import re
import sys
from pathlib import Path

ROOTS = ('cache', 'runs')
# Re-downloadable third-party material, about 300 MB: the Intel MKL wheel and its extracted DLLs.
EXCLUDED_PREFIXES = ('runs/w108a-reference-hunt/mkl_dl/',)
CHUNK = 1 << 20
GITHUB_BLOB_LIMIT = 100 * 1024 * 1024
# A blob larger than this is stored as numbered parts <path>.gz.part000, part001, ... (each at
# most PART_BYTES), whose concatenation is the gzip stream the manifest hashes.
PART_BYTES = 90 * 1024 * 1024

# The W109 set (DnaCalc dc-ymjf.1, 2026-10-30): OxFunc/smart-fuzzer/work/w109, the discovery,
# held-out and discriminator banks of the W109 algorithm identification campaigns. Only Excel
# answers, generated inputs, search state (scores, eliminated, leaders, survivors, checkpoints)
# and our own notes are stored. Everything else is listed in w109-excluded.tsv with its reason:
# cargo build output (one row per build folder), code (it may port or embed third-party code),
# archives of third-party sources, binary intermediates, logs, and any file whose name marks
# third-party material (Microsoft CRT outputs, Boost, Cephes, TOMS/CDFLIB, Numerical Recipes,
# AMD libm, Open64, AS algorithms, published coefficient sources). When unsure, a file is left out.
W109_CODE = {'.py', '.ps1', '.rs', '.c', '.h', '.hpp', '.f', '.sh', '.toml', '.lock', '.pyc',
             '.manifest', '.cpp', '.js'}
W109_ARCHIVES = {'.tgz', '.gz', '.zip'}
W109_BINARY = {'.npz', '.pkl', '.bin', '.o', '.rlib', '.rmeta', '.pdb', '.exe', '.d', '.dll',
               '.lib', '.timestamp', '.exp', '.a', '.tag'}
W109_NAME_BAN = re.compile(
    r'agentG_|agentH_|msvc|(^|[^a-z])crt|boost|cephes|toms|glibc|libm|open64|(^|[^a-z])amd|_asm|'
    r'disas|nmath|rmath|recipes|(^|[-_/])nr([-_]|$)|as63|as241|cdflib/|specfun|ndtr|public-erf/|'
    r'codyhillstrom|ucrt|ntdll|__pycache__/', re.I)


def w109_build_dir(rel: str) -> str | None:
    """The cargo build folder holding `rel` (a path relative to the W109 root), or None."""
    parts = rel.split('/')
    for i, part in enumerate(parts[:-1]):
        if part.startswith('target') or part.startswith('cargo-target') or part in ('.fingerprint', 'incremental', 'deps'):
            return '/'.join(parts[:i + 1]) + '/'
    return None


def w109_reason(rel: str) -> str | None:
    """Why a W109 file is left out, or None when it is stored."""
    ext = os.path.splitext(rel)[1].lower()
    if ext in W109_CODE:
        return 'code (may port or embed third-party code)'
    if ext in W109_ARCHIVES:
        return 'archive of third-party sources'
    if ext in W109_BINARY:
        return 'binary intermediate (numpy, pickle or op-tree bank), not answers or inputs'
    if ext in ('.log', '.pid'):
        return 'process log or pid'
    if W109_NAME_BAN.search(rel):
        return 'third-party name marker (CRT, Boost, Cephes, TOMS/CDFLIB, NR, AMD libm, Open64, AS, published source)'
    return None


class Set:
    def __init__(self, name, roots, source_sub, manifest, excluded):
        self.name, self.roots, self.source_sub = name, roots, source_sub
        self.manifest, self.excluded = manifest, excluded


SETS = {
    'oracle': Set('oracle', ROOTS, '', 'manifest.tsv', 'excluded.tsv'),
    'w109': Set('w109', ('work/w109',), '', 'w109-manifest.tsv', 'w109-excluded.tsv'),
}


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


class _Parts(io.RawIOBase):
    """The concatenation of a blob's part files, read in order."""

    def __init__(self, paths: list[Path]):
        self.paths = list(paths)
        self.fh = None

    def readable(self) -> bool:
        return True

    def readinto(self, buf) -> int:
        while True:
            if self.fh is None:
                if not self.paths:
                    return 0
                self.fh = self.paths.pop(0).open('rb')
            n = self.fh.readinto(buf)
            if n:
                return n
            self.fh.close()
            self.fh = None


def blob_files(dest: Path, rel: str) -> list[Path]:
    """The file or the ordered part files holding the blob of `rel`; empty when there is none."""
    single = dest / (rel + '.gz')
    if single.is_file():
        return [single]
    parts = sorted(single.parent.glob(single.name + '.part[0-9][0-9][0-9]'))
    return parts


def split_blob(blob: Path) -> int:
    """Splits a blob larger than PART_BYTES into numbered parts; returns the number of parts."""
    size = blob.stat().st_size
    for old in blob.parent.glob(blob.name + '.part[0-9][0-9][0-9]'):
        old.unlink()
    if size <= PART_BYTES:
        return 1
    count = 0
    with blob.open('rb') as fh:
        while True:
            block = fh.read(PART_BYTES)
            if not block:
                break
            (blob.parent / f'{blob.name}.part{count:03d}').write_bytes(block)
            count += 1
    blob.unlink()
    return count


def decompress_hash(blob, out: Path | None = None) -> tuple[int, str]:
    h = hashlib.sha256()
    size = 0
    sink = None
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        sink = out.open('wb')
    try:
        source = blob if isinstance(blob, Path) else (blob[0] if len(blob) == 1 else io.BufferedReader(_Parts(blob)))
        with gzip.open(source, 'rb') as gz:
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
    chosen = SETS[args.set]
    source = args.source.resolve()
    dest = args.dest.resolve()
    manifest_path = dest / chosen.manifest
    previous = read_manifest(manifest_path)
    rows: list[list[str]] = []
    excluded: list[list[str]] = []
    build_dirs: dict[str, list[int]] = {}
    written = skipped = 0
    raw_total = gz_total = 0
    largest: tuple[int, str] = (0, '')
    for root in chosen.roots:
        base = source / root
        if not base.is_dir():
            print(f'missing source directory: {base}', file=sys.stderr)
            return 2
        for path in sorted(p for p in base.rglob('*') if p.is_file()):
            inner = rel_posix(path, base)
            rel = root + '/' + inner
            if chosen.name == 'oracle':
                if any(rel.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
                    size, sha = sha256_of(path)
                    excluded.append([rel, str(size), sha])
                    continue
            else:
                build = w109_build_dir(inner)
                if build is not None:
                    tally = build_dirs.setdefault(root + '/' + build, [0, 0])
                    tally[0] += 1
                    tally[1] += path.stat().st_size
                    continue
                reason = w109_reason(inner) or (args.hold.get(rel) if args.hold else None)
                if reason is not None:
                    size, sha = sha256_of(path)
                    excluded.append([rel, str(size), sha, reason])
                    continue
            prev = previous.get(rel)
            if prev is not None and blob_files(dest, rel) and prev[0] == path.stat().st_size:
                size, sha = sha256_of(path)
                if sha == prev[1]:
                    rows.append([rel, str(prev[0]), prev[1], str(prev[2]), prev[3]])
                    skipped += 1
                    raw_total += prev[0]
                    gz_total += prev[2]
                    if prev[2] > largest[0]:
                        largest = (prev[2], rel)
                    continue
            blob = dest / (rel + '.gz')
            raw_size, raw_sha, gz_size, gz_sha = compress_and_hash(path, blob, args.level)
            if chosen.name != 'oracle':
                split_blob(blob)
            rows.append([rel, str(raw_size), raw_sha, str(gz_size), gz_sha])
            written += 1
            raw_total += raw_size
            gz_total += gz_size
            if gz_size > largest[0]:
                largest = (gz_size, rel)
    rows.sort()
    write_tsv(manifest_path, ['path', 'raw_bytes', 'raw_sha256', 'gz_bytes', 'gz_sha256'], rows)
    if chosen.name == 'oracle':
        excluded.sort()
        write_tsv(dest / chosen.excluded, ['path', 'raw_bytes', 'raw_sha256'], excluded)
    else:
        for folder, (count, size) in build_dirs.items():
            excluded.append([folder, str(size), '-', f'cargo build output ({count} files)'])
        excluded.sort()
        write_tsv(dest / chosen.excluded, ['path', 'raw_bytes', 'raw_sha256', 'reason'], excluded)
    # Blobs whose source file disappeared are reported, not deleted; delete them deliberately.
    current = {row[0] for row in rows}
    stale = [rel for rel in previous if rel not in current]
    print(f'files archived: {len(rows)} (written {written}, unchanged {skipped}); excluded: {len(excluded)}')
    print(f'raw bytes: {raw_total:,}; gzip bytes: {gz_total:,}; largest blob: {largest[0]:,} bytes ({largest[1]})')
    if chosen.name == 'oracle' and largest[0] > GITHUB_BLOB_LIMIT:
        print('WARNING: a blob exceeds 100 MB, which GitHub rejects', file=sys.stderr)
    if stale:
        print(f'stale blobs no longer in the source ({len(stale)}): ' + ', '.join(stale[:10]) + (' ...' if len(stale) > 10 else ''))
    return 0


def draw_sample(keys: list[str], size: int, seed: int | None) -> list[str]:
    """A random sample of the sorted manifest paths, printing the seed that draws it again."""
    if seed is None:
        seed = random.SystemRandom().randrange(1 << 32)
    print(f'sample seed: {seed}')
    rng = random.Random(seed)
    return sorted(rng.sample(sorted(keys), min(size, len(keys))))


def cmd_verify(args: argparse.Namespace) -> int:
    dest = args.dest.resolve()
    manifest = read_manifest(dest / SETS[args.set].manifest)
    if not manifest:
        print('empty or missing manifest', file=sys.stderr)
        return 2
    keys = sorted(manifest)
    if not args.all:
        keys = draw_sample(keys, args.sample, args.seed)
    bad = 0
    for rel in keys:
        raw_size, raw_sha, gz_size, gz_sha = manifest[rel]
        blob = blob_files(dest, rel)
        if not blob:
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
    manifest = read_manifest(dest / SETS[args.set].manifest)
    if not manifest:
        print('empty or missing manifest', file=sys.stderr)
        return 2
    if args.seed is not None and args.sample is None:
        print('--seed needs --sample', file=sys.stderr)
        return 2
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        print(f'refusing to restore into {target}: it exists and is not an empty directory', file=sys.stderr)
        return 2
    keys = sorted(manifest)
    if args.sample is not None:
        keys = draw_sample(keys, args.sample, args.seed)
    bad = 0
    for rel in keys:
        raw_size, raw_sha, _, _ = manifest[rel]
        blob = blob_files(dest, rel)
        if not blob:
            print(f'MISSING {rel}')
            bad += 1
            continue
        size, sha = decompress_hash(blob, target / rel)
        if size != raw_size or sha != raw_sha:
            print(f'MISMATCH {rel}')
            bad += 1
    print(f'restored {len(keys)} of {len(manifest)} files into {target}; failures: {bad}')
    return 1 if bad else 0


def main() -> int:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--source', type=Path, default=here.parent / 'OxFunc' / 'smart-fuzzer', help='directory holding cache/ and runs/')
    ap.add_argument('--dest', type=Path, default=here, help='this repository root')
    ap.add_argument('--set', choices=sorted(SETS), default='oracle',
                    help='oracle: cache/ and runs/ (manifest.tsv, the default); w109: work/w109 (w109-manifest.tsv)')
    sub = ap.add_subparsers(dest='command', required=True)
    a = sub.add_parser('archive')
    a.add_argument('--level', type=int, default=6)
    a.add_argument('--hold', type=Path, default=None,
                   help='w109 only: a TSV of path<TAB>reason for further files left out after a content review')
    a.set_defaults(func=cmd_archive)
    v = sub.add_parser('verify')
    v.add_argument('--sample', type=int, default=50)
    v.add_argument('--seed', type=int, default=None)
    v.add_argument('--all', action='store_true')
    v.set_defaults(func=cmd_verify)
    r = sub.add_parser('restore')
    r.add_argument('target', type=Path)
    r.add_argument('--sample', type=int, default=None)
    r.add_argument('--seed', type=int, default=None)
    r.set_defaults(func=cmd_restore)
    args = ap.parse_args()
    if getattr(args, 'hold', None) is not None:
        held = {}
        for line in args.hold.read_text(encoding='utf-8').splitlines()[1:]:
            if line.strip():
                path, reason = line.split('	', 1)
                held[path] = reason
        args.hold = held
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
