"""
Summarize raw JSONL experiment records.

Reads results/raw/*.jsonl and writes CSV summaries under results/summary/.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_records(raw_dir: Path) -> list[dict]:
    # Read every JSONL record from the raw results directory.
    records = []
    for path in sorted(raw_dir.glob("*.jsonl")):
        with path.open() as handle:
            for line_number, line in enumerate(handle, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Bad JSON in {path}:{line_number}") from exc
    return records


def pct(numerator: int, denominator: int) -> str:
    # Return a readable percentage, or NA when the denominator is missing.
    if denominator == 0:
        return "NA"
    return f"{numerator / denominator:.4f}"


def average(values: list[float]) -> str:
    if not values:
        return "NA"
    return f"{sum(values) / len(values):.1f}"


def median(values: list[float]) -> str:
    if not values:
        return "NA"
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return f"{ordered[middle]:.1f}"
    return f"{(ordered[middle - 1] + ordered[middle]) / 2:.1f}"


def group_by(records: list[dict], key: str) -> dict[str, list[dict]]:
    groups = defaultdict(list)
    for record in records:
        groups[str(record[key])].append(record)
    return dict(groups)


def summarize_by_defense(records: list[dict]) -> list[dict]:
    """Compute ASR, benign refusal rate, error count, and average latency."""
    rows = []
    for defense, group in sorted(group_by(records, "defense").items()):
        attacks = [r for r in group if not r["is_benign"]]
        benign = [r for r in group if r["is_benign"]]
        successful_attacks = sum(bool(r["attack_success"]) for r in attacks)
        benign_refused = sum(bool(r["refused"]) for r in benign)
        latencies = [float(r["latency_ms"]) for r in group if not r.get("error")]

        rows.append(
            {
                "defense": defense,
                "total_records": len(group),
                "attack_records": len(attacks),
                "successful_attacks": successful_attacks,
                "asr": pct(successful_attacks, len(attacks)),
                "benign_records": len(benign),
                "benign_refused": benign_refused,
                "benign_refusal_rate": pct(benign_refused, len(benign)),
                "error_count": sum(bool(r.get("error")) for r in group),
                "avg_latency_ms": average(latencies),
            }
        )
    return rows


def summarize_asr_by_category(records: list[dict]) -> list[dict]:
    """Compute attack success rate for each attack category and defense."""
    attacks = [r for r in records if not r["is_benign"]]
    rows = []
    for defense, defense_group in sorted(group_by(attacks, "defense").items()):
        for category, category_group in sorted(group_by(defense_group, "category").items()):
            successful = sum(bool(r["attack_success"]) for r in category_group)
            rows.append(
                {
                    "defense": defense,
                    "category": category,
                    "attack_records": len(category_group),
                    "successful_attacks": successful,
                    "asr": pct(successful, len(category_group)),
                }
            )
    return rows


def summarize_latency(records: list[dict]) -> list[dict]:
    """Summarize latency by defense. Error records are excluded."""
    rows = []
    for defense, group in sorted(group_by(records, "defense").items()):
        latencies = [float(r["latency_ms"]) for r in group if not r.get("error")]
        rows.append(
            {
                "defense": defense,
                "records_without_error": len(latencies),
                "avg_latency_ms": average(latencies),
                "median_latency_ms": median(latencies),
                "min_latency_ms": f"{min(latencies):.1f}" if latencies else "NA",
                "max_latency_ms": f"{max(latencies):.1f}" if latencies else "NA",
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    """Write rows even when the result is empty, using a stable filename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def print_table(title: str, rows: list[dict]) -> None:
    """Small readable console table for quick terminal checks."""
    print(f"\n{title}")
    if not rows:
        print("(no rows)")
        return

    headers = list(rows[0].keys())
    widths = {
        header: max(len(header), *(len(str(row[header])) for row in rows))
        for header in headers
    }
    print(" | ".join(header.ljust(widths[header]) for header in headers))
    print("-+-".join("-" * widths[header] for header in headers))
    for row in rows:
        print(" | ".join(str(row[header]).ljust(widths[header]) for header in headers))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", default=str(ROOT / "results" / "raw"))
    parser.add_argument("--summary-dir", default=str(ROOT / "results" / "summary"))
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    records = load_records(raw_dir)
    if not records:
        raise SystemExit(f"No JSONL records found in {raw_dir}")

    by_defense = summarize_by_defense(records)
    by_category = summarize_asr_by_category(records)
    by_latency = summarize_latency(records)

    summary_dir = Path(args.summary_dir)
    write_csv(summary_dir / "summary_by_defense.csv", by_defense)
    write_csv(summary_dir / "asr_by_category.csv", by_category)
    write_csv(summary_dir / "latency_by_defense.csv", by_latency)

    print(f"Loaded {len(records)} raw records from {raw_dir}")
    print_table("Summary by defense", by_defense)
    print_table("ASR by category", by_category)
    print_table("Latency by defense", by_latency)
    print(f"\nWrote summaries to {summary_dir}")


if __name__ == "__main__":
    main()
