#!/usr/bin/env python3
"""Evaluate output/results.json against evaluation/gold.csv.

Run from the project root:
    python evaluation/evaluate_results.py output/results.json
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


def main() -> int:
    result_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("output/results.json")
    gold_path = Path("evaluation/gold.csv")

    with gold_path.open(encoding="utf-8") as f:
        gold = {row["vacancy_id"]: row for row in csv.DictReader(f)}
    with result_path.open(encoding="utf-8") as f:
        results = {str(row["vacancy_id"]): row for row in json.load(f)}

    tp = fp = fn = tn = 0
    count_errors = 0

    for vid, g in gold.items():
        expected = g["expected_has_phone"] == "True"
        row = results.get(vid)
        if row is None:
            count_errors += 1
            continue
        predicted = bool(row.get("has_phone"))
        if expected and predicted:
            tp += 1
        elif not expected and predicted:
            fp += 1
        elif expected and not predicted:
            fn += 1
        else:
            tn += 1

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0

    print(f"Gold:      {len(gold)}")
    print(f"Results:   {len(results)}")
    print(f"TP: {tp}  FP: {fp}  FN: {fn}  TN: {tn}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall:    {recall:.2%}")
    if count_errors:
        print(f"Missing results: {count_errors}")

    return 0 if not count_errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
