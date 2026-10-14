# OxFunc-Evidence

**Private** archive of the OxFunc smart-fuzzer oracle evidence that the [DnaCalc/OxFunc](https://github.com/DnaCalc/OxFunc) repository does not track: `OxFunc/smart-fuzzer/cache` (Excel ground-truth captures per function and Excel build) and `OxFunc/smart-fuzzer/runs` (campaign runs with their logs, notes and minimized cases). Created 2026-10-14 as the raw half of bead `infra-m0.6` of the DNA Calc re-implementation plan. Kept separate from `OxFunc-History`, which archives session transcripts.

## Layout

- `cache/<path>.gz` and `runs/<path>.gz`: one deterministic gzip blob per source file, written with an empty name field and `mtime` 0 (the `gzip -n` convention), so an unchanged source file produces a byte-identical blob and git stores nothing new for it.
- `manifest.tsv`: path, raw bytes, raw SHA-256, gzip bytes, gzip SHA-256 for every archived file.
- `excluded.tsv`: third-party binaries hashed but not stored: the Intel MKL wheel and its extracted DLLs under `runs/w108a-reference-hunt/mkl_dl/`, which are re-downloadable.
- `archive-evidence.py`: archive, verify and restore.

## Refresh

```text
python archive-evidence.py archive
git add -A
git commit -m "Refresh evidence archive"
git push
```

The source tree defaults to `../OxFunc/smart-fuzzer`. Archive a campaign run once it has finished rather than re-committing a growing one. Blobs whose source file disappeared are reported, not deleted.

## Verify and restore

```text
python archive-evidence.py verify --sample 100
python archive-evidence.py verify --all
python archive-evidence.py restore <target directory>
```

Verification decompresses blobs and compares size and SHA-256 with the manifest.

## Contents at creation (2026-10-14)

28,360 files, 2.70 GB raw, 261 MB of gzip blobs; 32 excluded third-party files totalling 746 MB. A 100-file random sample decompressed to the manifest hashes with no failures.

## Provenance

The blobs are the files as found on the owner's machine on 2026-10-14. Acquisition metadata (Excel build, CPU, settings) is whatever each capture recorded itself; the plan's `infra-m0.6` adds content addressing and a second backup on another medium, and legacy data without an Excel fingerprint remains investigation evidence rather than certification for a newly selected Exact target.
