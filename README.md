# OxFunc-Evidence

**Private** archive of the OxFunc smart-fuzzer oracle evidence that the [DnaCalc/OxFunc](https://github.com/DnaCalc/OxFunc) repository does not track (`smart-fuzzer/.gitignore` there excludes both directories' contents; only their two `README.md` files are tracked): `OxFunc/smart-fuzzer/cache` (Excel ground-truth captures per function and Excel build) and `OxFunc/smart-fuzzer/runs` (campaign runs with their logs, notes and minimized cases). Created 2026-10-14 as the raw half of bead `infra-m0.6` of the DNA Calc re-implementation plan. Kept separate from `OxFunc-History`, which archives session transcripts.

## Layout

- `cache/<path>.gz` and `runs/<path>.gz`: one deterministic gzip blob per source file, written with an empty name field and `mtime` 0 (the `gzip -n` convention), so an unchanged source file produces a byte-identical blob and git stores nothing new for it.
- `manifest.tsv`: path, raw bytes, raw SHA-256, gzip bytes, gzip SHA-256 for every archived file.
- `excluded.tsv`: third-party binaries hashed but not stored: the Intel MKL wheel and its extracted DLLs under `runs/w108a-reference-hunt/mkl_dl/`, which are re-downloadable.
- `archive-evidence.py`: archive, verify and restore.

## Removed for licence reasons (DnaCalc dc-96l.4, 2026-10-30)

Reference code is not kept here: the glibc 2.29 sources and the probe built from them under
`runs/w108a-reference-hunt/` (`g229_*.c/.h`, `e_exp_data_229.c`, `glibc229_probe.c`, `.exe`,
`.obj`; the probe's numeric output `glibc229_out.txt` stays) and the candidate copies of
OxFunc's `excel_numeric/x87.rs`, `mod.rs`, `discrete_dist_family.rs` and `normal_log_family.rs`
under `runs/w111-*-20260929/candidate/` were removed from the tree and from `manifest.tsv`. Their
sources still exist in the git-ignored `OxFunc/smart-fuzzer/runs`, so a later `archive` run would
add them again: delete them there, or remove them again after archiving.

## The W109 banks (DnaCalc dc-ymjf.1, 2026-10-30)

`work/w109/<path>.gz` holds `OxFunc/smart-fuzzer/work/w109`: the discovery, held-out and
discriminator banks of OxFunc's W109 algorithm identification campaigns, which existed only on the
owner's disk. It is a second set with its own manifest and the same blob layout:

- `w109-manifest.tsv`: path, raw bytes, raw SHA-256, gzip bytes, gzip SHA-256 per stored file.
- `w109-excluded.tsv`: every file of the source tree that is not stored, with its size, SHA-256 and
  reason (cargo build output is one row per build folder, without a hash).
- `w109-held.tsv`: the files left out after a content review, read by `archive --hold`.

Only Excel answers (`answers-*.json`, WitnessSet JSON with `capture_provenance` where the capture
recorded one), generated inputs (`batch-*`, `pool-*`, `meta-*`), search state (scores, eliminated,
leaders, survivors, checkpoints, predictions) and our own notes are stored. Left out: code of any
kind (it may port or embed third-party code), archives of third-party sources, binary intermediates
(numpy, pickle, the 225 MB op-tree bank), logs, files whose name marks third-party material
(Microsoft CRT outputs, Boost, Cephes, TOMS/CDFLIB, Numerical Recipes, AMD libm, Open64, AS
algorithms, a published coefficient paper), and five files a content review found to transcribe
published algorithms or quote third-party source. The selection rules are in
`archive-evidence.py` (`w109_reason`). At creation: 1,363 files stored, 2,086,703,406 raw bytes,
214,119,868 gzip bytes; 1,214 rows excluded (12 cargo build folders of about 8.2 GB).

A blob larger than 90 MB is stored as numbered parts `<path>.gz.part000`, `part001`, ... whose
concatenation is the gzip stream the manifest hashes (none at creation; the largest W109 blob is
79 MB).

```text
python archive-evidence.py --set w109 archive --hold w109-held.tsv
python archive-evidence.py --set w109 verify --sample 100
python archive-evidence.py --set w109 restore <target directory>
```

OxFunc's captures came from one Excel host, GOVERT-OMEN; every CPU recorded anywhere in its
evidence is "AMD Ryzen 7 4800H with Radeon Graphics" (Windows, 64-bit Excel). A bank whose
`capture_provenance` names a build was read on that build; a bank without the block has no
recorded build, and DnaCalc's witness judge labels it unknown rather than guessing one.

## The function-lane records (DnaCalc dc-ymjf.1, 2026-10-30)

`function-lane/` holds OxFunc's per-function bit-exact records as plain files, copied from OxFunc
`05196c39` (`docs/function-lane/`) and from the parent of `b2f4873e`:

- `ledgers/`: `EXCEL_PARITY_LEDGER.csv` (527 functions, 2026-09-29), `DISCREPANCY_RULED_OUT_LEDGER.csv`,
  `DISCREPANCY_CALCULATION_MAP.csv` and `W109_WALL_CLUES_LEDGER.md`.
- `notes/w109/`: 73 of OxFunc's 75 `W109_*.md` identification notes. Held back because they
  transcribe published code or coefficient tables: `W109_GAMMALN_PUBLISHED_COEFFICIENTS.md` (netlib
  SPECFUN coefficient tables) and `W109_ERF_GAUSS_NORMSDIST_THEORY_HANDOFF_20260821.md` (the TOMS
  654 branch as pseudo-code and the NSWC `gam1` coefficients).
- `notes/checkpoints-b2f4873e/`: the 8 racer checkpoint and partial reports that OxFunc
  `b2f4873e` (dc-96l.4) deleted, read with `git show b2f4873e^:<path>`. Each was checked: they
  name the public sources their candidates came from but hold no third-party code.

## Refresh

```text
python archive-evidence.py archive
git add -A
git commit -m "Refresh evidence archive"
git push
```

The source tree defaults to `../OxFunc/smart-fuzzer`. Archive a campaign run once it has finished rather than re-committing a growing one. Blobs whose source file disappeared are reported, not deleted. Any new commit here moves away from the commit DnaCalc pins: DnaCalc's `infra_m0_6__restore_roundtrip` fails until `migration/evidence/oxfunc-smart-fuzzer.json` names the new commit. After a refresh, that record's manifest hashes, counts and labels need updating too.

## Verify and restore

```text
python archive-evidence.py verify --sample 100
python archive-evidence.py verify --all
python archive-evidence.py --set w109 verify --all
python archive-evidence.py restore <target directory>
python archive-evidence.py restore <target directory> --sample 100 --seed 7
```

Verification decompresses blobs and compares size and SHA-256 with the manifest; restore does the same while writing each file under the target directory at its manifest path, so the relative layout of `cache/` and `runs/` is kept under one root. A sample is drawn from the sorted manifest paths with the given seed, or with a drawn seed that the script prints. Restore refuses a target that exists and is not an empty directory.

From a DnaCalc checkout, the same script runs as a repository command:

```text
cargo xtask evidence verify [--all | --sample N] [--seed S]
cargo xtask evidence restore <dir> [--sample N] [--seed S]
```

They find this checkout at `<legacy root>/OxFunc-Evidence`, where the legacy root is the DnaCalc checkout's parent directory or `DNACALC_LEGACY_ROOT`, run `archive-evidence.py` with `python` on Windows or `python3` on Linux, and exit with its exit code.

## Contents at creation (2026-10-14)

28,339 files (28,360 before the dc-96l.4 removals), 2.70 GB raw, 261 MB of gzip blobs; 32 excluded third-party files totalling 746 MB. A 100-file random sample decompressed to the manifest hashes with no failures.

## Provenance

The blobs are the files as found on the owner's machine on 2026-10-14. Acquisition metadata (Excel build, CPU, settings) is whatever each capture recorded itself. This GitHub repository is the one backup copy: by the owner's ruling of 2026-10-18 a copy on GitHub is enough, and the captures can be recreated from Excel. DnaCalc's `migration/evidence/oxfunc-smart-fuzzer.json` pins the commit of this repository that DnaCalc relies on and gives each cache subfolder, run folder and top-level file one acquisition label: a known Excel build with the place it was read from, or unknown. Legacy data without an Excel fingerprint remains investigation evidence and cannot certify a newly selected Exact target.


R16 scalar captures (2026-11-03) are retained under `probes/2026-11-03-r16/`:
the unchanged 250-call packet, 13 raw worker batches, frozen predictions,
requested/submitted/Value2 audits and the complete 151-file supplied hash map.
The original canonical reader exports are copied byte-for-byte to
`readings/excel-20527/r16-*.json`; their runtime ordering is preserved.
Three catalogue capture copies already equal the committed DnaCalc captures.
Independent verification rejects seven corrupted-input variants. Current
registered calculations match 70 of 250 readings and fail 180; both frozen
prediction lineages match 69. These are observations, not new product gains.
The 179 new distinct bank inputs add 42 matches and 137 failures; all shared
recorded answers and calculated outputs remain unchanged. The separate
round-18 YIELD correction gains two on the fixed pre-intake bank scope.
