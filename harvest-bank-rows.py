#!/usr/bin/env python3
"""Retain study discrepancies and exact regression rows from finished lanes."""

import argparse
import ast
import csv
from collections import Counter, defaultdict
from functools import lru_cache
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile

STUDIES = Path("readings/excel-20527/studies")
DISCREPANCIES = Path("readings/excel-20527/discrepancies")
DISCREPANCY_MANIFEST = "discrepancies-manifest.tsv"
LEGACY_LANES = "cb1 cb2 cb3 cb4 cb5 cb6 cb7 cb8 cb9 cb10 nx1 nx2 nx3 nx4 nx5 nx6 nx7 sx1 nc1 fx1 fx2 fx3 ax1 ax2 ax3 nt1".split()
AMD = "AMD Ryzen 7 4800H with Radeon Graphics"
WORD = re.compile(r"(?:0x)?([0-9a-f]{16})\Z", re.I)
FUNCTION = re.compile(r"[A-Z][A-Z0-9]*(?:\.[A-Z0-9]+)*\Z")
ERRORS = dict(zip(
    ("#NULL!", "#DIV/0!", "#VALUE!", "#REF!", "#NAME?", "#NUM!", "#N/A", "#SPILL!", "#CALC!", "#GETTING_DATA"),
    ("Null", "Div0", "Value", "Ref", "Name", "Num", "Na", "Spill", "Calc", "GettingData"),
))
FORMAT = "dnacalc-study-bank/1"
MANIFEST = "studies-manifest.tsv"
KODERBOT = {
    "eb6": "20261121-eb6-witness-replay",
    "fix3e": "20261113-fix3e-163255z",
    "fix3f": "20261114-fix3f-ets-prehistory-0340z",
}


def dump(obj):
    return json.dumps(obj, ensure_ascii=True, separators=(",", ":"), sort_keys=True, allow_nan=False)


def read(path):
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8-sig") as f:
            return json.load(f)
    with path.open(encoding="utf-8-sig") as f:
        if path.suffix == ".jsonl":
            return [json.loads(line) for line in f if line.strip()]
        return json.load(f)


def word(value):
    match = WORD.fullmatch(value) if isinstance(value, str) else None
    if match is None:
        raise ValueError("missing binary64 word")
    return "0x" + match[1].lower()


def scalar(value, bare_hex=False):
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return "0x" + struct.pack(">d", value).hex()
    if isinstance(value, str):
        value.encode("utf-8")
        if bare_hex and value.startswith("-0x") and WORD.fullmatch(value[1:]):
            return f"0x{int(value[3:],16) ^ (1 << 63):016x}"
        if value.startswith("0x") and WORD.fullmatch(value) or bare_hex and WORD.fullmatch(value):
            return word(value)
        return value
    if isinstance(value, list):
        if not value or any(isinstance(v, list) for v in value) and (
            not all(isinstance(v, list) and len(v) == len(value[0]) for v in value)
        ):
            raise ValueError("invalid array shape")
        return [scalar(item, bare_hex) for item in value]
    if not isinstance(value, dict):
        raise ValueError("unsupported value")
    kind = value.get("type", value.get("kind"))
    if kind in ("number", "num"):
        return word(value.get("bits", value.get("bits_hex")))
    if kind in ("boolean", "bool", "logical") and isinstance(value.get("value"), bool):
        return value["value"]
    if kind in ("text", "string") and isinstance(value.get("value"), str):
        if re.fullmatch(r"0x[0-9a-f]{16}", value["value"]):
            raise ValueError("text indistinguishable from a binary64 word")
        return value["value"]
    if kind in ("blank", "empty"):
        return None
    if kind == "error" or set(value) == {"error"}:
        error = value.get("code", value.get("error", value.get("value")))
        if isinstance(error, str):
            name = ERRORS.get(error, error)
            if name in ERRORS.values():
                return {"error": name}
    if kind in ("array", "range", "mixed_array") and isinstance(value.get("values"), list):
        values = value["values"]
        rows, cols = value.get("rows"), value.get("cols")
        # Touchstone v1 echoes request shapes as nested lists with no dimensions.
        if rows is None and cols is None and values and isinstance(values[0], list):
            rows, cols = len(values), len(values[0])
        if isinstance(rows, int) and isinstance(cols, int) and rows > 0 and cols > 0:
            if len(values) == rows * cols and not any(isinstance(v, list) for v in values):
                values = [values[i:i + cols] for i in range(0, len(values), cols)]
            if len(values) == rows and all(isinstance(v, list) and len(v) == cols for v in values):
                return scalar(values, bare_hex)
    if kind == "matrix" and isinstance(value.get("bits_hex_row_major"), list):
        return scalar({"type": "array", "values": value["bits_hex_row_major"],
                       "rows": value["rows"], "cols": value["cols"]}, True)
    raise ValueError("unsupported typed value")


def outcome(value, text=False):
    if isinstance(value, str):
        value.encode("utf-8")
        if value.startswith("ERR:{"):
            return outcome(ast.literal_eval(value[4:]))
        if value.startswith("err:") and value[4:] in ERRORS:
            return "error:" + ERRORS[value[4:]]
        if value.startswith(("error:", "logical:", "text:")):
            if not text:
                return "error:" + ERRORS[value[6:]] if value.startswith("error:") and value[6:] in ERRORS else value
        if value in ERRORS or value in ERRORS.values():
            return "error:" + ERRORS.get(value, value)
        if text:
            return "text:" + value
        return word(value)
    normalized = scalar(value)
    if isinstance(normalized, bool):
        return "logical:" + str(normalized)
    if isinstance(normalized, dict):
        return "error:" + normalized["error"]
    if isinstance(normalized, str):
        if isinstance(value, dict) and value.get("type", value.get("kind")) in ("text", "string"):
            return "text:" + normalized
        return word(normalized)
    raise ValueError("absent or unsupported answer")


def fields(node):
    """Read capture metadata, leaving the provenance of historical files as recorded."""
    provenance = node.get("capture_provenance") or {}
    environment = provenance.get("environment") or node.get("excel_meta") or {}
    capture = {**node, **environment}
    settings = node.get("calculation_settings") or provenance.get("calculation_settings") or {}
    invocation = dict(node.get("invocation") or {})
    for key, tag in [("CompatibilityVersion", "compatibility_version"),
                     ("DecimalSeparator", "decimal_separator"),
                     ("ThousandsSeparator", "thousands_separator")]:
        if settings.get(key) is not None:
            invocation[tag] = str(settings[key])
    if isinstance(settings.get("Date1904"), bool):
        invocation["date_system"] = "1904" if settings["Date1904"] else "1900"
    build = capture.get("excel_file_version") or capture.get("excel_build") or capture.get("build")
    cpu = capture.get("cpu") or capture.get("cpu_id")
    if not cpu and str(capture.get("machine", "")).upper() == "GOVERT-OMEN" and not node.get("excel_cpu"):
        cpu = AMD
    timestamp = capture.get("timestamp", capture.get("captured_utc", capture.get("ts", provenance.get("captured_utc"))))
    return {key: value for key, value in dict(
        excel_build=str(build) if build else None, cpu=cpu, timestamp=timestamp,
        invocation=invocation or None, platform=capture.get("platform"),
        bitness=capture.get("bitness") or capture.get("excel_bitness"),
    ).items() if value is not None}


def normal_build(build):
    # Strip the product version prefix while retaining explicit build revisions.
    return str(build).removeprefix("16.0.")


def case_key(function, args, index, capture):
    return (function, dump(args), tuple(index or ()), normal_build(capture["excel_build"]),
            capture["cpu"].casefold())


def emit_rows(emit, function, args, answer, capture, locator, index=None, text=False, bare_hex=False):
    if isinstance(answer, dict) and answer.get("type", answer.get("kind")) in ("array", "matrix"):
        if index is not None:
            r, c = index
            answer = scalar(answer)[r - 1][c - 1]
            emit(function, args, answer, capture, locator, index, text, bare_hex)
        else:
            values = answer.get("values")
            if isinstance(values, list) and values and all(isinstance(row, list) for row in values):
                for r, row in enumerate(values, 1):
                    for c, value in enumerate(row, 1):
                        emit(function, args, value, capture, locator, [r, c], text, bare_hex)
            else:
                emit(function, args, answer, capture, locator, index, text, bare_hex)
    else:
        emit(function, args, answer, capture, locator, index, text, bare_hex)


def paired_inputs(path):
    """The frozen-design joins used by the lanes' answer writers."""
    stem = path.stem
    stems = [stem.replace("-answers", "-predictions"),
             stem.replace("_answers", "_predictions"),
             stem.replace("_answers", ""),
             stem.replace("answers", "preds")]
    return next((path.with_name(s + ext) for s in stems if s != stem
                 for ext in (".jsonl", ".json") if path.with_name(s + ext).is_file()), None)


def row_args(node):
    for key in ("asked", "args_hex", "args", "args_bits", "q_args"):
        if isinstance(node.get(key), list):
            return node[key]
    if isinstance(node.get("input"), str):
        return [node["input"]]
    return None


def scan(path, doc, emit, omitted, default):
    """Read self-identifying rows, or join frozen designs by the stored ID/index."""
    def pick(node, *keys):
        return next((node[k] for k in keys if k in node and node[k] is not None), None)

    companion = paired_inputs(path)
    design = None
    if companion:
        design = read(companion)
        if isinstance(design, dict):
            design = pick(design, "rows", "cases", "witnesses")
    by_id = {str(row["id"]): row for row in design or []
             if isinstance(row, dict) and "id" in row}

    def walk(node, fn=None, capture=default, loc="$", designs=None, witness=False):
        if isinstance(node, list):
            for i, item in enumerate(node):
                other = designs[i] if designs is not None and i < len(designs) else None
                walk(item, fn, capture, f"{loc}[{i}]", other, witness)
            return
        if not isinstance(node, dict):
            return
        if raw_reply(node):
            return
        fn = pick(node, "function", "fn") or fn
        capture = {**capture, **fields(node)}
        if isinstance(node.get("readings"), list) and isinstance(node.get("witnesses"), list):
            if not witness:
                return
            sources = {s["id"]: s for s in node["readings"] if isinstance(s, dict) and "id" in s}
            for i, row in enumerate(node["witnesses"]):
                source = sources.get(row.get("reading"), {})
                env = {**capture, **fields(source)}
                env["original_source"] = source.get("source")
                emit_rows(emit, fn, row.get("args"), row.get("expected_bits"), env,
                          f"{loc}.witnesses[{i}]", row.get("result_index"))
            return
        args = row_args(node)
        answer = pick(node, "excel_bits", "excel", "answer", "ans", "observed")
        if witness and answer is None:
            answer = node.get("expected_bits")
        if answer is not None and not (isinstance(answer, dict) and
                                        not ("type" in answer or "kind" in answer or "error" in answer)):
            if args is None and isinstance(design, list):
                idx = pick(node, "i", "idx")
                other = by_id.get(str(node.get("id")))
                if other is None and isinstance(idx, int) and 0 <= idx < len(design):
                    other = design[idx]
                if isinstance(other, dict) and (fn is None or pick(other, "fn", "function") in (fn, None)):
                    args = row_args(other)
                    fn = fn or pick(other, "fn", "function")
                    if args is not None:
                        capture = {**capture, "input_source": companion.name}
            if isinstance(args, list) and fn is not None:
                emit_rows(emit, fn, args, answer, capture, loc,
                          node.get("result_index"), bare_hex="args_hex" in node or
                          str(companion or path).split("/")[-2].startswith(("cb", "nx")) or path.name.startswith("subnormal-"))
                return
            if fn and not isinstance(answer, list):
                omitted["answer without exact operands"] += 1
        for key, value in node.items():
            if key in ("readings", "inputs", "capture_provenance", "calculation_settings", "predictions"):
                continue
            keyfn = key if FUNCTION.fullmatch(key) and key not in {"CDF", "PDF", "UTF", "DNA"} else fn
            walk(value, keyfn, capture, f"{loc}.{key}", witness=witness)

    default = dict(default)
    if path.parent.parent.name == "fx3":
        default_fn = path.name.split("-pinned-")[0].upper() if "-pinned-" in path.name else None
        if path.name.startswith("numbervalue-sep"):
            default_fn = "NUMBERVALUE"
    else:
        default_fn = None
    walk(doc, default_fn, default, witness="bank-rows" in path.parts)


def raw_reply(rep):
    return (isinstance(rep, dict) and rep.get("ok") is True
            and isinstance(rep.get("rows"), list) and isinstance(rep.get("inputs"), list)
            and ("excel_build" in rep or "excel_file_version" in rep))


def count_reply_rows(doc):
    if raw_reply(doc):
        return len(doc["rows"])
    if isinstance(doc, dict):
        return sum(count_reply_rows(v) for v in doc.values())
    if isinstance(doc, list):
        return sum(count_reply_rows(v) for v in doc)
    return 0


def raw_rows(doc, function, emit, omitted, default, loc="$", selection=None):
    if isinstance(function, tuple):
        index, function = function
        selection = index
    """Service responses carry exact typed operand readbacks when echo_inputs was used."""
    if raw_reply(doc):
        env = {**default, **fields(doc)}
        if "excel_cpu" in default:
            env.update(cpu=default["cpu"], excel_cpu=default["excel_cpu"])
        rows, inputs = doc["rows"], doc["inputs"]
        if len(rows) != len(inputs) or not function:
            omitted["service reply without function or input pairing"] += len(rows)
            return
        for i, (args, result) in enumerate(zip(inputs, rows)):
            if not isinstance(args, list) or isinstance(result, dict) and result.get("type") == "sheet_case":
                omitted["service reply without exact worksheet operands"] += 1
                continue
            emit_rows(emit, function, args, result, env, f"{loc}.rows[{i}]", selection)
        return
    if isinstance(doc, list):
        for i, value in enumerate(doc):
            if isinstance(value, (dict, list)):
                raw_rows(value, function, emit, omitted, default, f"{loc}[{i}]", selection)
    if isinstance(doc, dict):
        meta = {**default, **fields(doc)}
        function = doc.get("fn") or doc.get("function") or function
        for key, value in doc.items():
            if isinstance(value, (dict, list)):
                keyfn = key if len(key) >= 3 and FUNCTION.fullmatch(key) else function
                raw_rows(value, keyfn, emit, omitted, meta, f"{loc}.{key}", selection)


def reply_function(lane, path):
    if lane == "sx1":
        name = path.stem
        if name.startswith("date-") and name.endswith(("recheck", "holdout", "boundaries")):
            return "DATE"
        if name in ("run2-irr-origin-zero-reply", "run2-irr-power-neighbors",
                    "run2-irr-power-zero-reply", "run2-irr-shape-reply", "run2-irr-matrix-and-scale"):
            return "IRR"
        return {
            "sort-duplicates-answers": "SORT",
            "run2-complex-small-hyperbolic": None,
            "run2-irr-npv-zero-compare": "NPV",
            "run3-yield-seed-reply": "YIELD",
            "run3-bessel-j0-discriminate-replies": "BESSELJ",
            "run3-bessel-recurrence": "BESSELY",
            "run3-text-decade": "CONCAT",
            "run3-irr-origin-layout-replies": "IRR",
            "run4-ets-phase-replies": "FORECAST.ETS.SEASONALITY",
        }.get(name)
    if lane != "ax1":
        return None
    name = path.name.removesuffix(".json.gz")
    if match := re.fullmatch(r"run2-b[123]-tail-(GAMMALN(?:\.PRECISE)?)-\d+", name):
        return match[1]
    if re.fullmatch(r"seed-proof-\d+", name):
        return "GAMMA"
    if re.fullmatch(r"run2-stirling-shapes-exp-\d+", name):
        return "EXP"
    # These tags are passed alongside the function to request() in ax1/w/neg_*.py
    # and the corresponding run2_* probe scripts. Prefixes with several functions
    # require an exact tag or an explicit function in the saved wrapper.
    exact = {
        "frozen-negative-asc-answers": "GAMMA", "frozen-negative-halves-answers": "GAMMA",
        "frozen-negative-increments-answers": "GAMMA", "run2-reflect-negative": "GAMMA",
        "run2-reflect-public-gamma": "GAMMA", "run2-reflect-public-gamma1": "GAMMA",
        "run2-reflect-public-sin": "SIN", "run2-new2-reflect-negative": "GAMMA",
        "run2-new2-reflect-public-gamma": "GAMMA", "run2-new2-reflect-public-sin": "SIN",
        "run2-posleaf-result": "GAMMA", "run2-posleaf-negative-result": "GAMMA",
        "run2-posleaf-correction": "EXP", "run2-posleaf-stored-correction": "EXP",
        "run2-posleaf-ln": "LN", "run2-posleaf-neg-exp": "EXP",
        "run2-posleaf-frac-exp": "EXP", "run2-posleaf-sqrt": "SQRT",
        "run2-posleaf-final-nonhalf-ln": "LN", "run2-posleaf-final-nonhalf-neg-exp": "EXP",
        "run2-posleaf-final-nonhalf-frac-exp": "EXP", "run2-posleaf-final-nonhalf-sqrt": "SQRT",
        "run2-posleaf-last-ln": "LN", "run2-posleaf-last-neg": "EXP",
        "run2-posleaf-last-frac-exp": "EXP", "run2-posleaf-last-sqrt": "SQRT",
        "run2-posleaf-star-arith-exp": "EXP", "run2-posleaf-star-arith-ln": "LN",
        "run2-posleaf-star-arith-neg": "EXP", "run2-posleaf-star-arith-sqrt": "SQRT",
        "run2-posleaf-star-proof-frac-exp": "EXP", "run2-posleaf-star-proof-ln": "LN",
        "run2-posleaf-star-proof-neg-exp": "EXP", "run2-posleaf-star-proof-sqrt": "SQRT",
        "run2-fresh-b2-outer": "GAMMALN", "run2-fresh-b1-final-store": "GAMMALN",
        "run2-fresh-b1-final-store-precise": "GAMMALN.PRECISE",
        "run2-star-arith-actual": "GAMMA", "run2-star-proof-actual": "GAMMA",
        "run2-star-last-public": "GAMMA",
        "run2-tiny-series": "GAMMA", "run2-tiny-edges": "GAMMA", "run2-half-edges": "GAMMA",
        "run2-reflection-underflow-seams": "GAMMA", "run2-reflection-overflow-seams": "GAMMA",
    }
    return exact.get(name)


def special(lane, path, doc, emit, omitted, env):
    name = path.name
    def joined(fn, args, answers, prefix, meta=env, text=False):
        if len(args) != len(answers):
            omitted["batch length differs"] += len(answers)
            return
        for i, (a, result) in enumerate(zip(args, answers)):
            emit_rows(emit, fn, a, result, meta, f"{prefix}[{i}]", text=text, bare_hex=True)

    if lane == "cb9" and name == "frozen_cb9_scored.json":
        # nx8 exported the same captures with the full file version and calculation
        # settings. Use the richer lineage for exact, identified duplicates.
        attestations = {}
        for source in sorted((path.parent.parent / "nx8/bank-rows").glob("*.json")):
            bank = read(source)
            readings = {r["id"]: r for r in bank["readings"]}
            for row in bank["witnesses"]:
                if row["id"].startswith(("cb9-frozen600-", "cb9-binade4-")):
                    key = (bank["function"], dump(row["args"]), row["expected_bits"])
                    attestations[key] = {**fields(readings[row["reading"]]),
                                         "capture_record": f"nx8/bank-rows/{source.name} {row['id']}"}
        journal = read(path.with_name("excel_calls.jsonl"))
        calls = [r for r in journal if r.get("op") == "ask" and r["fn"] != "SQRT"]
        for kind, frozen, at in (("600", "frozen_cb9_predictions.jsonl", 0),
                                 ("binade4", "frozen_cb9_binade4_discriminators.jsonl", 5)):
            source = path.with_name(frozen)
            if hashlib.sha256(source.read_bytes()).hexdigest() != doc[f"sha256_{kind}"]:
                raise ValueError("cb9 frozen design hash differs")
            heldout = read(source)
            scored = doc[f"scored_{kind}"]
            named = sorted({r["fn"] for r in heldout})
            metadata = {}
            for fn, call in zip(named, calls[at:at+len(named)], strict=True):
                if call["fn"] != fn or call["n"] != sum(r["fn"] == fn for r in heldout):
                    raise ValueError("cb9 worksheet journal does not match the paired batch")
                metadata[fn] = {**env, "timestamp": call["ts"], "input_source": frozen}
            for i, (pred, row) in enumerate(zip(heldout, scored, strict=True)):
                if any(row[k] != pred[k] for k in ("id", "fn", "args")):
                    omitted["cb9 design does not match scored identity"] += 1
                    continue
                fn = row["fn"]
                key = (fn, dump([scalar(arg) for arg in row["args"]]), outcome(row["excel"], True))
                meta = {**attestations.get(key, {}), **metadata[fn]}
                if key in attestations:
                    meta["excel_build"] = attestations[key]["excel_build"]
                emit(fn, row["args"], row["excel"], meta, f"scored_{kind}[{i}]", text=True)
        return True
    if lane == "cb9" and name == "excel_calls.jsonl":
        # The review records the observed successful SQRT(4) control and exact build.
        review = path.with_name("review.md").read_text()
        if "SQRT(4.0)" in review and "1 / 1" in review and doc and doc[0]["fn"] == "SQRT":
            emit("SQRT", [4], 2, {**env, "timestamp": doc[0]["ts"], "excel_build": "16.0.20527.20196",
                                  "input_source": "asked_inputs.jsonl", "answer_source": "review.md"}, "$[0]")
        return True
    if lane == "eb6" and name == "heldout.inputs.tsv.gz":
        results = path.with_name("heldout.results.tsv.gz")
        meta = {**env, "input_source": name, "answer_source": results.name}
        with gzip.open(path, "rt") as a, gzip.open(results, "rt") as b:
            for i, (inputs, result) in enumerate(zip(csv.reader(a, delimiter="\t"),
                                                     csv.reader(b, delimiter="\t"), strict=True), 1):
                case, fn, expected, *args = inputs
                if result[:3] != [case, fn, expected]:
                    raise ValueError(f"eb6 replay identity differs at row {i}")
                # The replay runner encodes the ETS histories and timelines as
                # semicolon-separated numeric columns prefixed with '['.
                operands = [[[word(v)] for v in arg[1:].split(";")] if arg.startswith("[")
                            else word(arg) for arg in args]
                emit(fn, operands, expected, meta, f"{i}:{case}")
        return True
    if lane == "eb6" and name == "live-anchors.json.gz":
        order = ("EXP", "GAMMA", "ATAN", "ACOTH", "NORM.INV", "NORMINV",
                 "LOGNORM.INV", "LOGINV", "FORECAST.ETS.CONFINT", "FORECAST.ETS")
        for i, (fn, receipt) in enumerate(zip(order, doc, strict=True)):
            # Retain the live timestamp on the original exact readback.
            raw_rows(receipt, fn, emit, omitted, env, f"$[{i}]")
        return True
    if lane == "fix3f" and name.startswith("ets-"):
        if name == "ets-first-interval-shape.json":
            batches = [(rows, "FORECAST.ETS", rep) for rows, rep in
                       zip(doc["requests"], doc["replies"], strict=True)]
        elif name == "ets-prehistory-affine-shape.json":
            rows = doc["rows"]
            a, b = doc["replies"]
            batches = [(rows, "FORECAST.ETS", a), ([r + [0] for r in rows], "FORECAST.ETS", b)]
        else:
            batches = [(doc["rows"], fn, rep) for fn, rep in
                       zip(("FORECAST.ETS", "FORECAST.ETS.CONFINT"), doc["replies"], strict=True)]
        for i, (operands, fn, rep) in enumerate(batches):
            if rep["ok"]:
                joined(fn, operands, rep["rows"], f"replies[{i}]", {**env, **fields(rep)})
        return True
    if lane == "fix3e" and name == "x87-discriminant-controls.json":
        for i, fn in enumerate(("ATAN", "ACOTH")):
            raw_rows(doc["replies"][i], fn, emit, omitted, env, f"replies[{i}]")
        for rep in doc["replies"][2:]:
            omitted["service reply without verified worksheet function"] += len(rep["rows"])
        return True
    if lane == "fix3e" and name in ("exp-discriminant-controls.json", "gamma-discriminant-controls.json"):
        fn = "EXP" if name.startswith("exp") else "GAMMA.DIST"
        raw_rows(doc["reply"], fn, emit, omitted, env, "reply")
        return True
    if lane == "nc1" and name == "oddfyield_holdout_pred.csv":
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != "92a951f8b00758946ff4ab72bb9d8fed96dd50b7edf2665248c0f600013aa154":
            raise ValueError("frozen ODDFYIELD predictions differ from the reviewed file")
        # nc1/report.md records an exact 250/250 comparison against this hash.
        operands = path.with_name("oddfyield_holdout_inputs.csv")
        with operands.open() as f:
            inputs = list(csv.reader(f))
        if len(inputs) != 250 or len(doc) != 250:
            raise ValueError("ODDFYIELD holdout length differs")
        for a, b in zip(inputs, doc, strict=True):
            if a[0] != b[0] or not b[1].startswith("N:"):
                omitted["ODDFYIELD holdout answer without exact row identity"] += 1
                continue
            emit("ODDFYIELD", list(map(float, a[1:])), b[1][2:],
                 {**env, "input_source": operands.name, "answer_source": "report.md"}, b[0])
        return True
    if lane == "fx2" and name == "rate-answers.txt":
        meta = {**env, "excel_build": doc[0].strip()}
        for i, row in enumerate(doc[1:], 2):
            a, b = row.strip().rsplit(") ", 1)
            emit("RATE", list(ast.literal_eval(a + ")")), b, meta, str(i))
        return True
    if lane == "w109" and name.startswith("answers-irr-npv-objective"):
        meta = {**env, **fields(doc)}
        if not doc["capture_provenance"]["alignment"]["argument_value2_readback_verified"]:
            raise ValueError("NPV input readback was not verified")
        for i, row in enumerate(doc["probes"]):
            inputs, probe = row["argument_value2_readback"], row["probe"]
            if any(inputs[k] != probe[k] for k in ("rate_bits", "tail_bits")):
                omitted["request differs from NPV readback"] += 1
                continue
            emit("NPV", [inputs["rate_bits"], [inputs["tail_bits"]]], row["raw_npv"],
                 meta, f"probes[{i}].raw_npv")
        return True
    if lane == "w109" and name.startswith("answers-tinytie-separators"):
        capture = doc["provenance"]
        meta = {**env, **fields(capture)}
        for i, row in enumerate(doc["results"]):
            if row["input_bits"] != row["input_roundtrip"]:
                omitted["request differs from roundtrip"] += 2
                continue
            for fn, key in (("GAUSS", "gauss_bits"), ("NORMSDIST", "normsdist_bits")):
                emit(fn, [row["input_bits"]], row[key], meta, f"results[{i}].{key}")
        omitted["modern NORM.S.DIST without recorded cumulative argument"] += len(doc["results"])
        return True
    if name == "excel_calls.jsonl" and lane.startswith("cb"):
        # These are totals of calls, including repeats; no per-row answer in the journal.
        omitted["logged calls (overlaps answer files)"] += sum(
            row.get("calls", row.get("n", 0)) for row in doc)
        return True
    if name == "asked_inputs.jsonl" and lane.startswith("cb"):
        omitted["input-log rows (overlaps answer files)"] += len(doc)
        return True
    if lane == "cb1" and name == "frozen_piece_c_results.json":
        pred = path.with_name("frozen_piece_c_predictions.jsonl")
        if hashlib.sha256(pred.read_bytes()).hexdigest() != doc["frozen_sha256"]:
            raise ValueError("frozen prediction hash differs")
        records = read(pred)
        if len(records) != doc["asked_per_function"]:
            raise ValueError("frozen design length differs")
        misses = {r["p_hex"]: r for r in doc["misses"]}
        for fn, countkey in (("NORM.S.INV", "norm_s_inv_matched"), ("NORMSINV", "normsinv_matched")):
            if sum(r[fn] != r["pred"] for r in doc["misses"]) != len(records) - doc[countkey]:
                raise ValueError("the reported misses do not account for every differing result")
            meta = {**env, **fields(doc), "input_source": pred.name}
            for i, row in enumerate(records):
                p = row["p_hex"]
                answer = misses[p][fn] if p in misses else row["pred_hex"]
                emit(fn, [word(p)], answer, meta, f"frozen[{i}]")
        return True
    if lane == "cb1" and path.suffix == ".npz":
        # pin_steps.py and pin_t2_and_atlas.py save the ConsecutiveRun inputs as p,
        # and the typed NORM.S.INV answers as x, both stored in binary64 arrays.
        ts = {}
        journal = read(path.parent.parent / "excel_calls.jsonl")
        for entry in journal:
            if entry.get("kind") == "consecutive_run" and "start" in entry:
                ts[(entry["start"].lower().removeprefix("0x"), entry["calls"])] = entry["ts"]
        meta = dict(env)
        tag = (f"{doc['inputs'][0]:016x}", len(doc["inputs"]))
        if tag in ts:
            meta["timestamp"] = ts[tag]
        for i, (a, b) in enumerate(zip(doc["inputs"], doc["answers"], strict=True)):
            emit("NORM.S.INV", [f"0x{a:016x}"], f"0x{b:016x}", meta, f"x[{i}]")
        return True
    if lane == "cb3" and name == "lnb_grid_runs.json":
        for i, row in enumerate(doc):
            joined("BETA.DIST", [[x, row["a_hex"], row["b_hex"], True] for x in row["xs_hex"]],
                   row["bits"], f"lnb[{i}]")
        return True
    if lane == "cb2" and name == "phase1_boundaries.json":
        answers = doc["beta_ans"]
        used = set()
        for tag, position, fixed, points, start, count in doc["windows_meta"]:
            if len(points) != count or start + count > len(answers):
                raise ValueError("boundary series length differs")
            args = [fixed[:position] + [point] + fixed[position + 1:] for point in points]
            joined("BETA.DIST", args, answers[start:start + count], tag)
            used.update(range(start, start + count))
        # The last seven calls are the E1 dyadic controls in probe_boundaries.py.
        pairs = [(3, 5), (5, 3), (2, 6), (6, 2), (7, 9), (11, 5), (9, 7)]
        joined("BETA.DIST", [[d2 / (d1 + d2), d2 / 2, d1 / 2, True] for d1, d2 in pairs],
               answers[-7:], "E1 beta controls")
        fd = [[2**30 - 1, 2, 2]] + [[1, d1, d2] for d1, d2 in pairs]
        fd.extend([[f"0x{0x3ff8000000000000 + i:016x}", 3, 5] for i in range(33)])
        joined("FDIST", fd, doc["fdist_ans"], "FDIST")
        omitted["answer without exact operands"] += len(answers) - len(used) - 7
        return True
    if lane == "cb2" and name == "phase2_probes.json":
        answers = doc["answers"]
        layouts = {
            "b0_100_basym": (118.5 / 220.0, 120, None),
            "lam_003_a150_b150": (None, 150, 150),
            "a1_x01": (None, 1, 3.7), "b1_x09": (None, 3.7, 1),
            "half_half_x09": (None, .5, .5), "minle1_x03_b20": (None, .5, 20),
            "minle1_b15_x02": (.2, .5, None), "minle1_x01_b4": (None, .5, 4),
            "c10_run": (2 ** -80, 10, None), "c35_run": (2 ** -80, 3.5, None),
            "bfrac_run": (None, 45, 45),
        }
        paired = doc["meta"]["t2t_001_pin"]
        joined("T.DIST.2T", [[t, 4096] for t, _, _ in paired["t_meta"]], answers[paired["t_idx"]], "t2t_001_pin")
        joined("BETA.DIST", [[x, 2048, .5, True] for _, x, _ in paired["t_meta"]], answers[paired["b_idx"]], "beta_001_pin")
        for tag, shape in layouts.items():
            group = doc["meta"][tag]
            result = answers[group["batch_idx"]]
            points = group.get("input_bits")
            if points is None:
                start = int(group.get("b_start", group.get("x_start")), 16)
                points = [f"0x{start+i:016x}" for i in range(len(result))]
            joined("BETA.DIST", [[h if value is None else value for value in shape] + [True]
                                 for h in points], result, tag)
        seen_indices = {paired["t_idx"], paired["b_idx"], *(doc["meta"][tag]["batch_idx"] for tag in layouts)}
        for i, result in enumerate(answers):
            if i not in seen_indices:
                omitted["answer without exact operands"] += len(result)
        return True
    if lane == "cb2" and name == "probe_t_and_lnb.json":
        cases = doc["test_cases"]
        joined("T.DIST.2T", cases, doc["t2t"], "t2t")
        joined("T.DIST", [[-t, df, True] for t, df in cases], doc["td"], "td")
        joined("BETA.DIST", [[x, a, b, True] for a, b, x in doc["tiny_meta"]], doc["tiny"], "tiny")
        joined("FDIST", [r[0][1:4] for r in doc["fdist"]], [r[1] for r in doc["fdist"]], "fdist")
        omitted["answer without exact operands"] += len(doc["bl"]) + len(doc["bs"])
        return True
    if lane == "cb2" and name == "frozen_tinv_x87_sep_actuals.jsonl":
        for row in doc:
            for fn, key in (("TINV", "excel_tinv_bits"), ("T.INV.2T", "excel_tinv2t_bits")):
                emit(fn, [word(row["p_bits"]), word(row["df_bits"])], row[key], env, str(row["idx"]))
        return True
    if lane == "cb3" and name in ("consec_p_runs.json", "stop_grid_runs.json"):
        for tag, series in doc.items():
            start = int(series["start_p_hex"], 16)
            args = [[f"0x{start+i:016x}", series["a_hex"], series["b_hex"]] for i in range(series["count"])]
            joined("BETA.INV", args, series["bits"], tag)
        return True
    if lane == "cb4" and name == "frozen_ets_cb4_answers.jsonl":
        pred = path.with_name("frozen_ets_cb4.jsonl")
        design = {r["id"]: r for r in read(pred)}
        for i, answer in enumerate(doc):
            row = design[answer["id"]]
            yy = [[word(v)] for v in row["y_hex"]]
            tt = [[k + 1] for k in range(len(yy))]
            x = word(row["arg0_hex"])
            args = [x, yy, tt, row["p"]] if row["fn"] == "FORECAST.ETS" else [yy, tt, x, row["p"]]
            emit(row["fn"], args, answer["excel_bits"], {**env, "input_source": pred.name}, str(i))
        return True
    if lane == "cb4" and name == "yield_band_sweep1.json":
        # The fixed operands are the BONDS table in probe_yield_bands1.py.
        bonds = [
            (44013, 44562, .05, 100, 2, 0), (44197, 45658, .0325, 97, 1, 4),
            (44242, 45658, .0875, 105, 4, 0), (44058, 44562, .05, 100, 2, 0),
            (44094, 45658, .06, 103, 2, 2), (44094, 45658, .06, 103, 2, 3),
            (43890, 45658, .04125, 101.5, 2, 1), (44927, 45658, 0, 100, 1, 0),
        ]
        for tag, points in doc["sweeps"].items():
            s, m, r, red, f, b = bonds[int(tag[1])]
            for i, (price, answer) in enumerate(points):
                emit("YIELD", [s, m, r, word(price), red, f, b], answer, env, f"{tag}[{i}]")
            for k, fn in (("n", "COUPNUM"), ("a", "COUPDAYBS"), ("e", "COUPDAYS")):
                emit(fn, [s, m, f, b], doc["sched"][tag][k], env, f"sched.{tag}.{k}")
        return True
    if lane == "cb4" and name == "yield_y1.json":
        # probe_yield_y1.py records the variable price or redemption as a word.
        bonds = {
            "B0": (44013, 44562, .05, 100, 2, 0), "B1": (44197, 45658, .0325, 97, 1, 4),
            "B2": (44242, 45658, .0875, 105, 4, 0), "B3": (44058, 44562, .05, 100, 2, 0),
            "B7": (44927, 45658, 0, 100, 1, 0),
        }
        for tag, points in doc["sweeps"].items():
            s, m, r, red, f, b = bonds[tag[:2]]
            for i, (price, answer) in enumerate(points):
                emit("YIELD", [s, m, r, word(price), red, f, b], answer, env, f"{tag}[{i}]")
        for i, row in enumerate(doc["y1a_red_sweep"]):
            s, m, r, _, f, b = bonds[row["bond"]]
            red, y = row["red"], word(row["yield_bits"])
            emit("PRICE", [s, m, r, .05, red, f, b], row["pr_at_0p05"], env, f"red[{i}].price")
            emit("YIELD", [s, m, r, word(row["pr_at_0p05"]), red, f, b], row["yield_bits"], env, f"red[{i}].yield")
            emit("PRICE", [s, m, r, y, red, f, b], row["price_at_yield"], env, f"red[{i}].price_at_yield")
        return True
    if lane == "cb4" and name == "multi_grid_12x12.json":
        for key, result in doc.items():
            emit("MULTINOMIAL", list(map(int, key.split(","))), result, env, key)
        return True
    if (lane, name) in (("cb4", "ets_basis_probe.json"), ("nx3", "frozen_ets_excel.json")):
        if lane == "nx3":
            design = {r["tag"]: r for r in read(path.with_name("frozen_ets_pred.json"))}
            env = {**env, "input_source": "frozen_ets_pred.json"}
        for row in doc:
            tag = row["tag"]
            p = row["p"]
            y = row["y_hex"] if lane == "cb4" else design[tag]["y_hex"]
            n = len(y)
            if lane == "nx3" and (n != row["n"] or p != design[tag]["p"]):
                raise ValueError("ETS design identity differs")
            yy = [[word(h)] for h in y]
            tt = [[i + 1] for i in range(n)]
            targets = (1, 2, n, n + 1, n + 2, n + 1048576) if lane == "cb4" else (n, n + 1, n + 2, n + 100)
            joined("FORECAST.ETS", [[x, yy, tt, p] for x in targets], row.get("fits_hex", row.get("ets")), tag + ".ets", env)
            joined("FORECAST.ETS.STAT", [[yy, tt, k, p] for k in (1, 2, 3, 6, 7)],
                   row.get("stats_hex", row.get("stat")), tag + ".stat", env)
            if lane == "nx3":
                joined("FORECAST.ETS.CONFINT", [[n + h, yy, tt, .95, p] for h in (1, 2, 10, 100, 10.37)],
                       row["ci"], tag + ".ci", env)
        return True
    if lane == "cb5" and name in ("bfrac_probe1.json", "boundary_probe2.json", "clean_arms_probe.json", "microscope_probe3.json"):
        beta = doc if isinstance(doc, list) else doc["bd"]
        for i, row in enumerate(beta):
            emit("BETA.DIST", [word(row[k]) for k in ("x", "a", "b")] + [row.get("cum", True)],
                 row.get("ans", row.get("val")), env, str(i))
        if isinstance(doc, dict):
            for i, row in enumerate(doc["gd"]):
                emit("GAMMA.DIST", [word(row["z"]), word(row["b"]), 1, row.get("cum", True)], row["ans"], env, f"gd[{i}]")
        return True
    if lane == "nx1" and name == "yearless-date-results.json":
        for fn in ("VALUE", "DATEVALUE", "NUMBERVALUE"):
            meta = {**env, **fields(doc), "invocation": {"capture_date": "2026-11-20"}}
            for i, row in enumerate(doc["groups"][fn]["rows"]):
                emit(fn, [row["input"]], row["observed"], meta, f"{fn}[{i}]")
        return True
    if lane == "nx1" and name == "yearless-date-round2-results.json":
        for i, row in enumerate(doc["nv_extra"]):
            emit("NUMBERVALUE", row["args"], row["observed"], {**env, **fields(doc)}, str(i))
        return True
    if lane == "nx1" and name == "poisson-subnormal-results.json":
        design = {r["id"]: r for r in read(path.with_name("poisson-subnormal-predictions.json"))["cases"]}
        for row in doc["results"]:
            case = design[row["id"]]
            if row["readback"] is None:
                omitted["subnormal case without input readback"] += 1
                continue
            emit("POISSON.DIST", row["readback"], row["observed"], {**env, **fields(doc)}, row["id"])
        return True
    if lane == "nx7" and name == "frozen_wh_cube_scored.json":
        for row in doc:
            emit("GAMMA.INV", [row["p"], row["a"], row["be"]], row["excel"], env, str(row["id"]))
        return True
    if lane == "nc1" and name in ("oddfyield_diverse.json", "oddfyield_edge_probe.json"):
        for i, row in enumerate(doc):
            _, *spec = row["spec"]
            args = spec[:5] + [row.get("p_hex", row["p"])] + spec[5:]
            emit("ODDFYIELD", args, row.get("y_ex_row", row.get("y_row")), env, str(i), bare_hex=True)
        return True
    if lane == "nc1" and name == "nt_ties.json":
        omitted["rounding direction retained without Excel text"] += sum(
            len(v) for k, v in doc.items() if k.endswith("_bits"))
        return True
    if lane == "fx2":
        meta = {**env, **fields(doc)} if isinstance(doc, dict) else env
        if name in ("rate-heldout-answers.json", "rate-overflow-answers.json"):
            joined("RATE", [r.split() for r in doc["inputs"]], doc["excel"], "$", meta)
            return True
        if name == "concat-ties.json":
            for fn in ("CONCAT", "CONCATENATE"):
                joined(fn, [[value] for value in doc["values"]], doc[fn], fn, meta, text=True)
            return True
        if name == "complex-midpoint-fresh.json":
            joined("COMPLEX", [[r[0], 0] for r in doc["pred"]], doc["excel"], "$", meta, text=True)
            return True
        if name == "im-fresh.json":
            for fn, results in doc["excel"].items():
                args = [[word(h), 0] if fn == "COMPLEX" else [word(h)] for h in doc["inputs"]]
                joined(fn, args, results, fn, meta, text=True)
            return True
        if name == "yield-gross-reask.json":
            joined("YIELD", doc["rows"], doc["excel"], "$", meta)
            return True
        if name == "multinomial-single.json":
            for fn in ("MULTINOMIAL", "FACT", "GAMMALN", "GAMMALN.PRECISE", "GAMMA"):
                offset = int(fn.startswith("GAMMA"))
                joined(fn, [[n + offset] for n in doc["n"]], doc[fn], fn, meta)
            return True
        if name == "ipmt-ppmt-heldout.json":
            for fn in ("IPMT", "PPMT"):
                joined(fn, [r.split() for r in doc["inputs"]], doc[fn.lower() + "_excel"], fn, meta)
            return True
    if lane == "sx1":
        # Replies in these files are written in ask_many request order. Prefer the
        # stored request functions; the named legacy cases use their producer's order.
        if isinstance(doc, dict) and isinstance(doc.get("replies"), list):
            for key in ("requests", "arguments"):
                requests = doc.get(key)
                if (isinstance(requests, list) and len(requests) == len(doc["replies"]) and
                    all(isinstance(req, list) and len(req) == 2 and
                        isinstance(req[0], str) and FUNCTION.fullmatch(req[0]) for req in requests)):
                    for i, (req, rep) in enumerate(zip(requests, doc["replies"], strict=True)):
                        fn, operands = req
                        meta = {**env, **fields(rep)}
                        if all(isinstance(a, list) for a in rep["inputs"]):
                            raw_rows(rep, fn, emit, omitted, env, f"replies[{i}]")
                        else:
                            joined(fn, operands, rep["rows"], f"replies[{i}]", meta)
                    return True
        reply_orders = {
            "run2-complex-denominator.json": ("SIN", "COS", "IMTAN", "IMCOT"),
            "run2-yield-coupon-root.json": ("YIELD", "PRICE"),
            "run3-round-precision-replies.json": ("ROUND", "ROUNDUP", "ROUNDDOWN"),
            "run3-bessel-y0.json": ("BESSELJ", "BESSELY"),
            "run3-bessel-y1.json": ("LN", "BESSELJ", "BESSELY"),
            "run3-complex-transition.json": ("IMTAN", "IMCOT"),
        }
        if name in reply_orders:
            for i, (fn, rep) in enumerate(zip(reply_orders[name], doc["replies"], strict=True)):
                raw_rows(rep, fn, emit, omitted, env, f"replies[{i}]")
            return True
        batches_order = {
            "run3-bessel-order-one-replies.json": ("LN", "BESSELJ", "BESSELY"),
            "run3-bessel-shared-square.json": ("LN", "BESSELY"),
            "run3-bessel-y0-holdout-replies.json": ("LN", "BESSELY"),
            "run3-bessel-y0-uniform-replies.json": ("LN", "BESSELY"),
        }
        if name in batches_order:
            for b, batch in enumerate(doc["replies"]):
                for i, (fn, rep) in enumerate(zip(batches_order[name], batch, strict=True)):
                    raw_rows(rep, fn, emit, omitted, env, f"replies[{b}][{i}]")
            return True
        if name == "run3-complex-limit.jsonl":
            for b, (_, batch) in enumerate(doc):
                for i, (fn, rep) in enumerate(zip(("IMTAN", "IMCOT"), batch, strict=True)):
                    raw_rows(rep, fn, emit, omitted, env, f"batches[{b}][{i}]")
            return True
        if name == "run3-yield-seed-design.json":
            raw_rows(doc["price0"], "PRICE", emit, omitted, env, "price0")
            for i, (fn, rep) in enumerate(zip(("COUPNUM", "COUPDAYS", "COUPDAYBS", "COUPDAYSNC"),
                                             doc["calendar"], strict=True)):
                raw_rows(rep, fn, emit, omitted, env, f"calendar[{i}]")
            return True
        if name == "run3-binom-two-shapes.json":
            groups = {
                "replies": ("BINOM.DIST", "BINOM.DIST", "BINOM.DIST", "BETA.DIST", "BETADIST", "POWER"),
                "beta_replies": ("BETADIST", "BETA.DIST", "BETA.DIST", "BETA.DIST"),
            }
            for key, functions in groups.items():
                for i, (fn, rep) in enumerate(zip(functions, doc[key], strict=True)):
                    raw_rows(rep, fn, emit, omitted, env, f"{key}[{i}]")
            return True
        if name == "run3-ets-acf-raw.jsonl":
            design = path.with_name("run3-ets-acf-design.json")
            if not design.is_file():
                return False
            cases = read(design)
            for i, (start, rep) in enumerate(doc):
                picked = cases[start:start + len(rep["rows"])]
                args = [[[[v] for v in case[1]], [[j+1] for j in range(len(case[1]))]] for case in picked]
                joined("FORECAST.ETS.SEASONALITY", args, rep["rows"], f"batches[{i}]",
                       {**env, **fields(rep), "input_source": design.name})
            return True
        keyed_replies = {
            "run2-complex-hyperbolic.json": {"exp_reply": "EXP"},
            "run3-hypgeom-orbit.json": {"reply": "HYPGEOM.DIST", "cdf_reply": "HYPGEOM.DIST"},
            "run4-beta-mirrors.json": {"lo": "BETA.DIST", "hi": "BETA.DIST"},
            "run4-beta-recurrence.json": {"bulk": "BETA.DIST", "density": "BETA.DIST",
                                         "seed": "BETA.DIST", "legacy": "BETADIST"},
            "run4-binomial-tail.json": {"cdf": "BINOM.DIST", "beta": "BETA.DIST", "exp": "EXP"},
            "run4-bond-term.json": {"yield_reply": "YIELD", "odd_reply": "ODDFYIELD"},
        }
        if name in keyed_replies:
            for key, fn in keyed_replies[name].items():
                raw_rows(doc[key], fn, emit, omitted, env, key)
            return True
        if name == "run3-bessel-forward-study.json":
            for key, fn in (("J", "BESSELJ"), ("Y", "BESSELY")):
                raw_rows(doc["replies"][key], fn, emit, omitted, env, key)
            return True
        if name == "run4-bessel-high.json":
            for key, fn in (("J", "BESSELJ"), ("SIN", "SIN"), ("COS", "COS")):
                raw_rows(doc["raw"][key], fn, emit, omitted, env, key)
            return True
        if name == "run2-regression-order-holdout-replies.json" or name.startswith("run2-regression-variance-"):
            if raw_reply(doc) or name == "run2-regression-order-holdout-replies.json":
                holdout = name.endswith("holdout-replies.json")
                design = path.with_name("run2-regression-order-holdout-design.json" if holdout
                                        else "run2-regression-variance-design.json")
                if not design.is_file():
                    return False
                cases = read(design)
                selections = {"df": (4, 2), "residual": (5, 2), "sse": (5, 2), "slope2_se": (2, 1),
                              "slope1_se": (2, 2), "intercept_se": (2, 3), "intercept": (2, 3)}
                receipts = doc if holdout else {path.stem.removeprefix("run2-regression-variance-"): doc}
                for tag, receipt in receipts.items():
                    selection = selections[tag]
                    if len(receipt["rows"]) != len(cases):
                        omitted["LINEST design length differs"] += len(receipt["rows"])
                        continue
                    meta = {**env, **fields(receipt), "input_source": design.name}
                    for i, (case, result) in enumerate(zip(cases, receipt["rows"], strict=True)):
                        args = [[[v] for v in case["y"]], case["x"], True, True]
                        echoed = receipt["inputs"][i]
                        if echoed is not None and [scalar(arg) for arg in echoed] != [scalar(arg) for arg in args]:
                            omitted["LINEST request differs from readback"] += 1
                            continue
                        emit("LINEST", args, result, meta, f"{tag}[{i}]", selection)
                return True
        if name in ("run3-bond-local.json", "run3-bond-zero-and-large.json"):
            for fn, price in (("YIELD", "PRICE"), ("ODDFYIELD", "ODDFPRICE")):
                raw_rows(doc[fn]["reply"], fn, emit, omitted, env, fn + ".reply")
                raw_rows(doc[fn]["price_reply"], price, emit, omitted, env, fn + ".price_reply")
            return True
        if name == "bond-price-residuals.json":
            for fn, key, receipts in (("YIELD", "yield_arguments", doc["yield_replies"]),
                                      ("PRICE", "price_arguments", [doc["price_reply"]]),
                                      ("ODDFPRICE", "oddprice_arguments", [doc["oddprice_reply"]])):
                answers = [v for receipt in receipts for v in receipt["rows"]]
                joined(fn, doc[key], answers, key, {**env, **fields(receipts[0])})
            return True
        if name == "ets-gross-probe.json":
            # The retained list holds original histories. The captured forecast
            # targets and options need their original requests.
            return False
        if name == "run2-ets-outlier-raw.jsonl":
            design = path.with_name("run2-ets-outlier-design.json")
            if not design.is_file():
                return False
            cases = read(design)
            for i, row in enumerate(doc):
                rep = row["reply"]
                picked = cases[row["start"]:row["start"] + len(rep["rows"])]
                args = [[[[v] for v in case["y"]], [[j+1] for j in range(case["n"])]] for case in picked]
                joined("FORECAST.ETS.SEASONALITY", args, rep["rows"], f"batches[{i}]",
                       {**env, **fields(rep), "input_source": design.name})
            return True
        if name in ("run2-ets-local-raw.jsonl", "run2-ets-invariance.json"):
            design = path.with_name("run2-ets-local-design.json")
            if not design.is_file():
                return False
            cases = read(design)
            base, delta = cases["base"], cases["delta"]
            variants = {
                "identity": lambda y: y, "reversed": lambda y: y[::-1],
                "negated": lambda y: [-v for v in y], "translated": lambda y: [v+2 for v in y],
                "linear": lambda y: [v+i*.25 for i, v in enumerate(y)],
            }
            if isinstance(doc, dict):
                batches = [(doc["labels"], doc["reply"], 0)]
            else:
                batches = [([("identity", j, scale, None) for j, scale in
                             zip(row["indices"], row["scales"], strict=True)], row["reply"], 1)
                           for row in doc]
            for i, (labels, rep, start) in enumerate(batches):
                timeline = [[j] for j in range(start, start+len(base))]
                args = []
                for variant, j, scale, _ in labels:
                    y = variants[variant]([b + scale * d for b, d in zip(base, delta[j], strict=True)])
                    args.append([[[v] for v in y], timeline])
                joined("FORECAST.ETS.SEASONALITY", args, rep["rows"], f"batches[{i}]",
                       {**env, **fields(rep), "input_source": design.name})
            return True
        if name == "run2-ets-boundary-raw.jsonl":
            design = path.with_name("run2-ets-boundary-design.json")
            if not design.is_file():
                return False
            cases = read(design)
            for i, row in enumerate(doc):
                args = []
                for k, scale in row["picks"]:
                    case = cases[k]
                    y = [[base + scale * delta] for base, delta in zip(case["base"], case["delta"], strict=True)]
                    args.append([y, [[j+1] for j in range(len(y))]])
                rep = row["answer"]
                joined("FORECAST.ETS.SEASONALITY", args, rep["rows"], f"batches[{i}]",
                       {**env, **fields(rep), "input_source": design.name})
            return True
    if lane == "ax1" and name == "run2-final-shared-leaf-backends.json":
        for i, row in enumerate(doc["native"]["misses"]):
            emit("SIN", [word(row[0])], row[1], env, f"native.misses[{i}]")
        return True
    return False


def atomic_write(path, data):
    if path.is_file() and path.read_bytes() == data:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name("." + path.name + ".tmp")
    temp.write_bytes(data)
    temp.replace(path)


def lane_files(root, lane, legacy):
    base = root / lane
    if not legacy:
        base /= "bank-rows"
    for directory, dirs, names in os.walk(base):
        dirs[:] = sorted(d for d in dirs if not re.match(
            r"\.|target|.*corpus|.*baseline|after_cb|workbooks|xtask-|trusted-origin", d))
        for name in sorted(names):
            path = Path(directory) / name
            if path.is_symlink() or re.search(r"stream|session|token|secret|credential|manifest|inventory", name, re.I):
                continue
            if (lane, name) in (("eb6", "heldout.inputs.tsv.gz"), ("eb6", "live-anchors.json.gz"),
                                ("nc1", "oddfyield_holdout_pred.csv"), ("fx2", "rate-answers.txt")):
                yield path
            elif lane == "cb1" and directory.endswith("/steps_data") and name.endswith(".npz"):
                yield path
            elif directory.endswith("/nt-probes") and name.endswith(".txt"):
                yield path
            elif re.search(r"\.jsonl?$", name) or (lane == "ax1" and "/raw/" in str(path) and name.endswith(".json.gz")):
                yield path


def finished_carbon(root, lane):
    folder = root / lane
    if not (folder / "review.md").is_file():
        return False
    for proc in Path("/proc").glob("[0-9]*"):
        try:
            if (proc / "comm").read_text().strip() != "agy":
                continue
            paths = [proc / "cwd", *list((proc / "fd").iterdir())]
            if any(p.is_symlink() and (str(p.readlink()) + "/").startswith(str(folder) + "/") for p in paths):
                return False
        except FileNotFoundError:
            continue
        except PermissionError:
            return False
    return True


def archive_studies(options):
    root, evidence = options.runs, options.evidence
    study_dir = evidence / STUDIES
    by_lane = defaultdict(dict)
    seen = {}
    totals = defaultdict(Counter)
    audit = {}

    def add_existing(lane, record):
        key = case_key(record["function"], record["args"], record.get("result_index"), record)
        if key in seen:
            raise ValueError(f"duplicate stored case in {lane}")
        seen[key] = (lane, record)
        by_lane[lane][key] = record

    original_counts = {}
    old_manifest = evidence / MANIFEST
    previous_entries = {}
    if old_manifest.is_file():
        for line in old_manifest.read_text().splitlines()[1:]:
            rel = line.split("\t", 1)[0]
            previous_entries[Path(rel).stem] = line
    for archive in sorted(study_dir.glob("*.json.gz")):
        doc = read(archive)
        if doc["format"] != FORMAT:
            raise ValueError(f"{archive}: wrong studies format")
        for record in doc["rows"]:
            add_existing(doc["lane"], record)
        original_counts[doc["lane"]] = len(doc["rows"])

    lanes = options.lanes or list(dict.fromkeys(
        LEGACY_LANES + sorted(path.parent.name for path in root.glob("*/bank-rows") if path.is_dir()) +
        ["w109", *KODERBOT]))
    for lane in lanes:
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", lane):
            raise ValueError(f"invalid lane: {lane}")
        if lane in ("cb9", "cb10") and not finished_carbon(root, lane):
            totals[lane]["next harvest"] += 1
            continue
        source_digests = set()
        source_root = root
        if lane in KODERBOT and not (root / lane).is_dir():
            source_root = root / "wb1/koderbot"
        if lane == "w109":
            archive = evidence / "work/w109"
            paths = [*archive.rglob("answers-irr-npv-objective*.json.gz"),
                     *archive.rglob("answers-tinytie-separators*.json.gz")]
        else:
            paths = lane_files(source_root, lane, lane in LEGACY_LANES or lane in KODERBOT)
        for path in paths:
            with path.open("rb") as f:
                digest = hashlib.file_digest(f, "sha256").digest()
            if digest in source_digests:
                continue
            source_digests.add(digest)
            source = f"w109/{path.relative_to(evidence).as_posix()}" if lane == "w109" else path.relative_to(source_root).as_posix()
            counts = Counter()

            def emit(function, args, answer, capture, loc, index=None, text=False, bare_hex=False):
                try:
                    if not isinstance(function, str) or not FUNCTION.fullmatch(function.upper()):
                        raise ValueError("missing worksheet function")
                    function = function.upper()
                    if not isinstance(args, list):
                        raise ValueError("missing exact worksheet operands")
                    args = [scalar(a, bare_hex) for a in args]
                    expected = outcome(answer, text)
                    if not capture.get("excel_build") or not capture.get("cpu"):
                        raise ValueError("missing Excel build or CPU provenance")
                    key = case_key(function, args, index, capture)
                except (ValueError, OverflowError, struct.error) as error:
                    counts[str(error)] += 1
                    return
                if key in seen:
                    _, old = seen[key]
                    if old["expected_bits"] != expected:
                        counts["conflicting answer for an existing call"] += 1
                        audit.setdefault("conflicts", []).append({
                            "source": source, "locator": loc, "function": function,
                            "args": args, "expected_bits": expected, "original": old,
                        })
                    else:
                        counts["duplicate"] += 1
                    return
                record = {"function": function, "args": args, "expected_bits": expected,
                          "source": source, "locator": loc, **capture}
                if index is not None:
                    record["result_index"] = index
                seen[key] = (lane, record)
                by_lane[lane][key] = record
                counts["added"] += 1

            try:
                if path.parent.name == "nt-probes" and path.suffix == ".txt":
                    with path.open() as f:
                        counts["rounding direction retained without Excel text"] += sum(bool(line.strip()) for line in f)
                elif lane == "ax1" and path.name.startswith(("gl_", "retained-fable-gl_", "m_")) and path.suffix == ".gz":
                    bulk = read(path)
                    counts["bulk capture file awaiting streaming import"] += 1
                    counts["bulk captures awaiting streaming import"] += count_reply_rows(bulk)
                    del bulk
                else:
                    if path.suffix == ".npz":
                        import numpy as np
                        with np.load(path, allow_pickle=False) as arrays:
                            doc = {"inputs": arrays["p"].view(np.uint64), "answers": arrays["x"].view(np.uint64)}
                    elif path.suffix == ".csv":
                        with path.open() as f:
                            doc = list(csv.reader(f))
                    elif path.suffix == ".txt":
                        doc = path.read_text().splitlines()
                    elif path.name == "heldout.inputs.tsv.gz":
                        doc = None
                    else:
                        doc = read(path)
                    default = {"excel_build": "20527", "cpu": AMD, "platform": "Windows", "bitness": "64"}
                    if lane == "w109":
                        default.pop("excel_build")
                    elif lane in KODERBOT:
                        default["evidence_prefix"] = f"dnacalc-corpus/runs/dna-koderbot/{KODERBOT[lane]}"
                        if lane == "eb6":
                            default.update(cpu="GenuineIntel Haswell", excel_cpu=AMD)
                    elif lane not in LEGACY_LANES or "bank-rows" in path.parts:
                        default = {}
                    if not special(lane, path, doc, emit, counts, default):
                        scan(path, doc, emit, counts, default)
                        raw_rows(doc, reply_function(lane, path), emit, counts, default)
            except (OSError, ValueError, TypeError, KeyError, IndexError) as error:
                counts[f"file parse failure ({type(error).__name__})"] += 1
            if counts:
                audit[source] = dict(counts)
                totals[lane].update(counts)
        print(lane, len(by_lane[lane]), dict(totals[lane]), flush=True)

    manifest = ["path\traw_bytes\traw_sha256\tgz_bytes\tgz_sha256"]
    for lane, entries in sorted(by_lane.items()):
        if not entries:
            continue
        if len(entries) == original_counts.get(lane) and lane in previous_entries:
            manifest.append(previous_entries[lane])
            continue
        rows = [record for _, record in sorted(entries.items())]
        doc = {"format": FORMAT, "lane": lane, "rows": rows}
        raw = (dump(doc) + "\n").encode()
        compressed = gzip.compress(raw, compresslevel=6, mtime=0)
        rel = STUDIES / f"{lane}.json"
        atomic_write(evidence / f"{rel}.gz", compressed)
        manifest.append("\t".join(map(str, (rel.as_posix(), len(raw), hashlib.sha256(raw).hexdigest(),
                                          len(compressed), hashlib.sha256(compressed).hexdigest()))))
    atomic_write(evidence / MANIFEST, ("\n".join(manifest) + "\n").encode())
    if options.report:
        atomic_write(options.report, (json.dumps({"lanes": totals, "sources": audit}, indent=2) + "\n").encode())
    print(f"{len(seen)} studies rows, {len(manifest) - 1} archives")


def discrepancy_key(row):
    # Different invocation contexts and contradictory Excel answers both carry evidence.
    return (*case_key(row["function"], row["args"], row.get("result_index"), row),
            dump(row.get("invocation") or {}), comparison_word(row["expected_bits"]))


def comparison_word(word):
    return word.lower() if word.lower().startswith("logical:") else word


def recorded_outcome(value, expected):
    if isinstance(value, str) and value.startswith(("fault:", "unsupported:", "text:")):
        return value
    return outcome(value, text=expected.startswith("text:") and
                   isinstance(value, str) and not value.startswith(("error:", "logical:")))


def archived_rows(evidence, directory, manifest):
    with (evidence / manifest).open() as f:
        for entry in csv.DictReader(f, delimiter="\t"):
            path = Path(entry["path"])
            if path.parent != directory or path.suffix != ".json":
                raise ValueError(f"{manifest}: invalid path {path}")
            doc = read(evidence / f"{path}.gz")
            if doc["format"] != FORMAT or doc["lane"] != path.stem:
                raise ValueError(f"{path}: wrong format or lane")
            yield from doc["rows"]


def locate(doc, locator):
    # The study archive stores original JSON paths, using $ for the root.
    if not re.fullmatch(r"\$?(?:\.?[\w-]+|\[\d+\])+", locator):
        return None
    for field, index in re.findall(r"([\w-]+)|\[(\d+)\]", locator):
        if index and isinstance(doc, list) and int(index) < len(doc):
            doc = doc[int(index)]
        elif field and isinstance(doc, dict):
            doc = doc.get(field)
        else:
            return None
    return doc


def historical_rows(root, evidence):
    """Join earlier implementation outputs by the capture's recorded row identity."""
    scored = {
        "cb6/frozen_holdout_scored.json",
        "cb7/frozen_cb7_scored.json", "cb8/frozen_cb8_scored.json",
        "cb9/frozen_cb9_scored.json", "nx2/frozen_pre_impl_answers.json",
        "nx6/work/frozen_predictions_nx6_scored.json", "nx7/work/frozen_nx7_proof2_scored.json",
        "nx7/work/frozen_wh_cube_scored.json", "nx1/evidence/poisson-subnormal-results.json",
    }
    legacy = {
        "cb3/frozen_betainv_cb3_answers.jsonl": ("frozen_betainv_cb3.jsonl", "i", "pred_master"),
        "cb3/frozen_bfrac_cb3_answers.jsonl": ("frozen_bfrac_cb3.jsonl", "i", "pred_master"),
        "cb3/frozen_lnbeta_cb3_answers.jsonl": ("frozen_lnbeta_cb3.jsonl", "i", "pred_master"),
        "cb4/frozen_ets_cb4_answers.jsonl": ("frozen_ets_cb4.jsonl", "id", "om_bits"),
        "cb5/frozen_cb5_answers.jsonl": ("frozen_cb5_predictions.jsonl", "idx", "pred_master"),
        "nx4/frozen_nx4_answers.jsonl": ("frozen_nx4_predictions.jsonl", "idx", "preds"),
    }
    carbon_ready = {lane: finished_carbon(root, lane) for lane in ("cb9", "cb10")}

    @lru_cache(maxsize=32)
    def local(source):
        lane = source.split("/")[0]
        if lane in carbon_ready and not carbon_ready[lane]:
            return None
        path = root / source
        return read(path) if path.is_file() and not path.is_symlink() else None

    @lru_cache(maxsize=3)
    def earlier_design(source):
        file, key, _ = legacy[source]
        return {str(row[key]): row for row in
                local(str(Path(source).with_name(file))) or []}

    replay = root / "wb1/koderbot/eb6/heldout.results.tsv.gz"
    intel = {}
    if replay.is_file():
        with gzip.open(replay, "rt") as f:
            for number, (case, fn, expected, actual) in enumerate(csv.reader(f, delimiter="\t"), 1):
                old = recorded_outcome(actual, expected)
                if comparison_word(old) != comparison_word(recorded_outcome(expected, expected)):
                    intel[f"{number}:{case}"] = (fn, word(expected) if WORD.fullmatch(expected)
                                                 else outcome(expected), old)

    sin = local("ax1/run2-final-shared-leaf-backends.json")
    sin = {(word(a), word(e)): word(b) for a, e, b in sin["native"]["misses"]} if sin else {}
    anchors = root / "wb1/koderbot/fix3e/x87-discriminant-controls.json"
    x87 = {}
    if anchors.is_file():
        doc = read(anchors)
        for key in ("atan", "acoth"):
            for fn, argument, native, _ in doc[key]:
                x87[fn, word(argument)] = word(native)
    ets_design = local("nx3/work/frozen_ets_pred.json") or []
    ets_old = {row["tag"]: row["old"] for row in ets_design}
    ax3_actual = "ax3/evidence/fresh-arms-answers.jsonl"
    for row in archived_rows(evidence, STUDIES, MANIFEST):
        source, locator, expected = row["source"], row["locator"], row["expected_bits"]
        values = {}
        if source == "eb6/heldout.inputs.tsv.gz" and locator in intel:
            fn, answer, actual = intel[locator]
            if (fn, answer) != (row["function"], expected):
                raise ValueError(f"{source} {locator}: replay identity differs")
            values["heldout.results.tsv.gz"] = actual
        elif row["function"] == "SIN" and len(row["args"]) == 1:
            actual = sin.get((row["args"][0], expected))
            if actual:
                values["run2-final-shared-leaf-backends.json"] = actual
        elif source == "fix3e/x87-discriminant-controls.json" and len(row["args"]) == 1:
            values["fix3e native x87"] = x87.get((row["function"], row["args"][0]))
        elif source == "nx3/work/frozen_ets_excel.json" and ets_old:
            match = re.fullmatch(r"(.*)\.(ets|stat|ci)\[(\d+)\]", locator)
            if match:
                tag, section, index = match.groups()
                old = ets_old[tag]
                outputs = {"ets": old["fcs"], "stat": [*old["par"], old["mae"], old["rmse"]],
                           "ci": [*old["cis"], old["ci_frac_ci"]]}
                values["frozen_ets_pred.json old"] = outputs[section][int(index)]
        elif source == ax3_actual:
            answer = locate(local(source), locator)
            design = local(str(Path(source).with_name("fresh-arms-predictions.jsonl")))
            if isinstance(answer, dict) and design:
                earlier = design[answer["i"]]
                if earlier["fn"] == row["function"]:
                    values["fresh-arms-predictions.jsonl actual"] = earlier["actual"]
        elif source in legacy:
            raw = local(source)
            if raw is not None:
                answer = raw[int(locator.removeprefix("$[").removesuffix("]"))]
                _, key, field = legacy[source]
                design = earlier_design(source).get(str(answer[key]))
                if design:
                    value = design.get(field)
                    values[field] = value.get("base") if isinstance(value, dict) else value
        elif source in scored or source.startswith("ax2/") and source.endswith("-answers.jsonl"):
            raw = local(source)
            node = locate(raw, locator)
            if isinstance(node, dict):
                for key in ("calc_func", "pred_master", "pred_old", "pred_cb7", "application", "actual"):
                    if key in node:
                        values[key] = node[key]
                if isinstance(node.get("preds"), dict):
                    values["preds.master"] = node["preds"].get("master")
        previous = {}
        for label, value in values.items():
            try:
                actual = recorded_outcome(value, expected)
            except (ValueError, TypeError):
                continue
            if comparison_word(actual) != comparison_word(expected):
                previous[label] = actual
        if previous:
            yield row, previous


# These pre-revision exports include ordinary controls. Their observations are still
# examined against the current evaluator, like an archive, before admitting any row.
LEGACY_EXPORTS = {
    "cb11": {"CHISQ.DIST", "GAMMA.DIST", "GAMMA.INV", "GAMMADIST", "GAMMAINV", "SQRT"},
    "nx8": {"CONCAT", "CONCATENATE", "FIXED", "TEXT", "VALUETOTEXT"},
}


def lane_discrepancies(root, lanes):
    for lane in lanes:
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", lane):
            raise ValueError(f"invalid lane: {lane}")
        if lane in ("cb9", "cb10") and not finished_carbon(root, lane):
            continue
        for path in lane_files(root, lane, False):
            if path.suffix not in (".json", ".jsonl"):
                continue
            for bank in [read(path)] if path.suffix == ".json" else read(path):
                if bank.get("format") != "dnacalc-witness-set/1":
                    raise ValueError(f"{path}: expected WitnessSet format")
                function = bank["function"]
                if not FUNCTION.fullmatch(function):
                    raise ValueError(f"{path}: invalid function {function}")
                sources = {entry["id"]: entry for entry in bank["readings"]}
                for witness in bank["witnesses"]:
                    source = sources[witness["reading"]]
                    capture = fields(source)
                    if not all(capture.get(key) for key in ("excel_build", "cpu", "timestamp")):
                        raise ValueError(f"{path}: missing Excel build, CPU or timestamp")
                    expected = outcome(witness["expected_bits"])
                    row = {"function": function, "args": [scalar(a) for a in witness["args"]],
                           "expected_bits": expected, "original_source": source["source"],
                           "source": path.relative_to(root).as_posix(), "locator": witness["id"], **capture}
                    if "result_index" in witness:
                        row["result_index"] = witness["result_index"]
                    actual = witness.get("calc_func")
                    if actual is not None:
                        actual = recorded_outcome(actual, expected)
                        if comparison_word(actual) != comparison_word(expected):
                            yield row, {"recorded": actual}
                    elif path.stem in LEGACY_EXPORTS.get(lane, ()):
                        yield row, None
                    else:
                        yield row, {"reported_by_lane": True}


def run_judge(options, output, inputs=None):
    command = ["cargo", "xtask", "witness", "discrepancies", "--report", str(output)]
    if inputs:
        command.extend(("--inputs", str(inputs)))
    subprocess.run(command, cwd=options.dnacalc, check=True)


def harvest_discrepancies(options):
    evidence, root = options.evidence, options.runs
    rows = {}
    counts = defaultdict(Counter)

    def retain(row, basis):
        row = {key: value for key, value in row.items() if value is not None}
        key = discrepancy_key(row)
        lane = row["source"].split("/")[0]
        if key not in rows:
            row["discrepancy"] = basis
            rows[key] = row
            counts[lane][row["function"]] += 1

    manifest = evidence / DISCREPANCY_MANIFEST
    previous_entries = {}
    if manifest.is_file():
        for line in manifest.read_text().splitlines()[1:]:
            rel = line.split("\t", 1)[0]
            previous_entries[Path(rel).stem] = line
        for row in archived_rows(evidence, DISCREPANCIES, DISCREPANCY_MANIFEST):
            rows[discrepancy_key(row)] = row
    elif next((evidence / DISCREPANCIES).glob("*.json.gz"), None):
        raise ValueError("missing discrepancy manifest")

    with tempfile.TemporaryDirectory(prefix="bank-discrepancies-") as temporary:
        work = Path(temporary)
        reports = list(options.current_report)
        if not options.intake_only and not reports:
            output = work / "archive.jsonl"
            run_judge(options, output)
            reports.append(output)
        lanes = options.lanes or sorted(path.parent.name for path in root.glob("*/bank-rows"))
        legacy = defaultdict(list)
        for row, basis in lane_discrepancies(root, lanes):
            if basis is None:
                legacy[row["source"].split("/")[0]].append(row)
            else:
                retain(row, basis)
        if not options.intake_only:
            if not options.current_report:
                for lane, candidates in legacy.items():
                    source = work / f"{lane}.json"
                    output = work / f"{lane}.jsonl"
                    source.write_text(dump({"format": FORMAT, "lane": lane, "rows": candidates}))
                    run_judge(options, output, source)
                    reports.append(output)
            for row, basis in historical_rows(root, evidence):
                retain(row, {"historical": basis})
        for path in reports:
            with path.open() as f:
                for line in f:
                    item = json.loads(line)
                    if comparison_word(item["row"]["expected_bits"]) == comparison_word(item["actual"]):
                        raise ValueError(f"{path}: comparison report includes a match")
                    retain(item["row"], {"judged": item["actual"]})

    by_lane = defaultdict(list)
    for key, row in sorted(rows.items()):
        by_lane[row["source"].split("/")[0]].append(row)
    entries = ["path\traw_bytes\traw_sha256\tgz_bytes\tgz_sha256"]
    for lane, observations in sorted(by_lane.items()):
        if not counts.get(lane) and lane in previous_entries:
            entries.append(previous_entries[lane])
            continue
        raw = (dump({"format": FORMAT, "lane": lane, "rows": observations}) + "\n").encode()
        blob = gzip.compress(raw, compresslevel=6, mtime=0)
        rel = DISCREPANCIES / f"{lane}.json"
        atomic_write(evidence / f"{rel}.gz", blob)
        entries.append("\t".join(map(str, (rel, len(raw), hashlib.sha256(raw).hexdigest(),
                                         len(blob), hashlib.sha256(blob).hexdigest()))))
    atomic_write(manifest, ("\n".join(entries) + "\n").encode())
    added = sum(sum(tally.values()) for tally in counts.values())
    if options.report:
        audit = {"added": added, "total": len(rows), "by_lane": counts}
        atomic_write(options.report, (dump(audit) + "\n").encode())
    print(f"{added} added; {len(rows)} discrepancy rows retained in {len(by_lane)} archives")


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("lanes", nargs="*", help="finished lanes to read (default: all bank-rows folders)")
    args.add_argument("--runs", type=Path, default=Path.home() / "codex-runs")
    args.add_argument("--evidence", type=Path, default=Path.home() / "projects/DnaCalc/CalcFunc-Evidence")
    args.add_argument("--dnacalc", type=Path, default=Path.home() / "projects/DnaCalc/DnaCalc")
    args.add_argument("--report", type=Path, help="write the per-lane import counts as JSON")
    args.add_argument("--current-report", type=Path, action="append", default=[],
                      help="supply saved witness discrepancies JSONL reports in place of current comparisons")
    args.add_argument("--intake-only", action="store_true",
                      help="import declared lane discrepancies and any supplied reports")
    args.add_argument("--archive-studies", action="store_true", help="run the original studies archive importer")
    options = args.parse_args()
    if options.archive_studies:
        archive_studies(options)
    else:
        harvest_discrepancies(options)


if __name__ == "__main__":
    main()
