#!/usr/bin/env python
"""Render candidate score summaries.

This script reads every ``candidate_topics/*/score.yaml`` file and writes:

* ``data/scores.csv``: one row per candidate folder slug.
* ``reports/candidate_matrix.md``: sortable inspection tables.

Scoring and ordering behavior:

* Candidate names are preserved as folder slugs.
* Numeric ranking fields are sorted descending, with missing/TODO/non-numeric
  values left blank and placed last.
* Ties are broken by candidate slug for stable output.
* ``best_use`` is categorical, so its report section groups by the category
  value; candidates inside each group are sorted by the same overall fallback
  order used elsewhere.
* Both flat score files and future nested schemas are accepted. When a field is
  nested, the first matching key found by a depth-first scan is used.
"""

from __future__ import annotations

import csv
import datetime as dt
import re
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
CANDIDATE_DIR = ROOT / "candidate_topics"
CSV_PATH = ROOT / "data" / "scores.csv"
REPORT_PATH = ROOT / "reports" / "candidate_matrix.md"

FIELDS = [
    "candidate",
    "overall_score",
    "theorem_project_suitability",
    "openevolve_suitability",
    "intellectual_interest",
    "open_status",
    "open_status_confidence",
    "saturation_risk",
    "best_use",
    "confidence",
    "notes",
    "score_path",
]

NUMERIC_FIELDS = {
    "overall_score",
    "theorem_project_suitability",
    "openevolve_suitability",
    "intellectual_interest",
}

TEXT_FIELDS = {
    "open_status",
    "open_status_confidence",
    "saturation_risk",
    "best_use",
    "confidence",
    "notes",
}

TODO_VALUES = {"", "todo", "TODO", "tbd", "TBD", "na", "n/a", "none", "null", "~"}


def parse_score_yaml(path: Path) -> dict[str, Any]:
    """Parse a score YAML file.

    PyYAML is intentionally optional. If it is available, use it. Otherwise use
    a conservative parser for simple mapping-based YAML. The fallback supports
    the current flat schema and common nested mapping shapes, and degrades to
    strings for values it does not understand.
    """

    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(text)
        return loaded if isinstance(loaded, dict) else {}
    except Exception:
        return parse_simple_yaml_mapping(text)


def parse_simple_yaml_mapping(text: str) -> dict[str, Any]:
    """Parse a small, mapping-oriented YAML subset.

    This is not a full YAML implementation. It is sufficient for the repository
    score files and future nested score blocks that use indentation and
    ``key: value`` pairs.
    """

    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if ":" not in line:
            continue

        key, raw_value = line.split(":", 1)
        key = key.strip()
        if not key:
            continue

        while stack and indent <= stack[-1][0]:
            stack.pop()

        parent = stack[-1][1]
        raw_value = raw_value.strip()
        if raw_value == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = parse_scalar(raw_value)

    return root


def parse_scalar(value: str) -> Any:
    """Parse a scalar from the fallback YAML reader."""

    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()

    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]

    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False

    if re.fullmatch(r"[-+]?\d+", value):
        try:
            return int(value)
        except ValueError:
            pass

    if re.fullmatch(r"[-+]?(?:\d+\.\d*|\d*\.\d+)", value):
        try:
            return float(value)
        except ValueError:
            pass

    return value


def find_field(data: Any, field: str) -> Any:
    """Find a field in flat or nested mappings."""

    if not isinstance(data, dict):
        return None

    if field in data:
        return data[field]

    for value in data.values():
        found = find_field(value, field)
        if found is not None:
            return found
    return None


def normalize_number(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    if text in TODO_VALUES or text.lower() in TODO_VALUES:
        return None

    try:
        return float(text)
    except ValueError:
        return None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if text in {"null", "None", "~"}:
        return ""
    return " ".join(text.split())


def display_number(value: float | None) -> str:
    if value is None:
        return ""
    if value.is_integer():
        return str(int(value))
    return f"{value:g}"


def load_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for score_path in sorted(CANDIDATE_DIR.glob("*/score.yaml")):
        candidate = score_path.parent.name
        raw = parse_score_yaml(score_path)
        row: dict[str, Any] = {
            "candidate": candidate,
            "score_path": score_path.relative_to(ROOT).as_posix(),
        }

        for field in NUMERIC_FIELDS:
            row[field] = normalize_number(find_field(raw, field))

        for field in TEXT_FIELDS:
            row[field] = normalize_text(find_field(raw, field))

        rows.append(row)
    return rows


def sort_key(field: str):
    def key(row: dict[str, Any]) -> tuple[int, float, str]:
        value = row.get(field)
        if isinstance(value, (int, float)):
            return (0, -float(value), row["candidate"])
        return (1, 0.0, row["candidate"])

    return key


def fallback_sort_key(row: dict[str, Any]) -> tuple[int, float, int, float, int, float, int, float, str]:
    """Stable default ordering for non-numeric sections."""

    values = [
        row.get("overall_score"),
        row.get("theorem_project_suitability"),
        row.get("openevolve_suitability"),
        row.get("intellectual_interest"),
    ]
    parts: list[Any] = []
    for value in values:
        if isinstance(value, (int, float)):
            parts.extend([0, -float(value)])
        else:
            parts.extend([1, 0.0])
    parts.append(row["candidate"])
    return tuple(parts)  # type: ignore[return-value]


def csv_value(row: dict[str, Any], field: str) -> str:
    if field in NUMERIC_FIELDS:
        return display_number(row.get(field))
    return str(row.get(field, ""))


def write_csv(rows: Iterable[dict[str, Any]]) -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row, field) for field in FIELDS})


def md_cell(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\n", " ").replace("|", "\\|")
    return text


def markdown_table(rows: list[dict[str, Any]], include_best_use: bool = True) -> str:
    columns = [
        "candidate",
        "overall_score",
        "theorem_project_suitability",
        "openevolve_suitability",
        "intellectual_interest",
        "open_status",
        "open_status_confidence",
        "saturation_risk",
        "confidence",
    ]
    if include_best_use:
        columns.insert(5, "best_use")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = []
        for column in columns:
            if column in NUMERIC_FIELDS:
                values.append(display_number(row.get(column)))
            else:
                values.append(md_cell(row.get(column, "")))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def notes_table(rows: list[dict[str, Any]]) -> str:
    columns = ["candidate", "notes"]
    lines = [
        "| candidate | notes |",
        "| --- | --- |",
    ]
    for row in rows:
        if row.get("notes"):
            lines.append(f"| {md_cell(row['candidate'])} | {md_cell(row['notes'])} |")
    return "\n".join(lines)


def write_report(rows: list[dict[str, Any]]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    sections: list[str] = [
        "# Candidate Score Matrix",
        "",
        f"Generated by `python scripts/scoring/render_scores.py` on {generated}.",
        "",
        "## Scoring And Ordering Behavior",
        "",
        "- Candidate names are folder slugs from `candidate_topics/*`.",
        "- Numeric score columns are sorted high-to-low; TODO, missing, and non-numeric values are blank and sort last.",
        "- Ties are broken alphabetically by candidate slug for stable diffs.",
        "- `best_use` is categorical, so that section groups by category and sorts candidates within each group by overall score, theorem suitability, OpenEvolve suitability, then intellectual interest.",
        "- The renderer reads flat score files and also searches nested mappings for known fields.",
        "",
        "## Ranked By Overall Score",
        "",
        markdown_table(sorted(rows, key=sort_key("overall_score"))),
        "",
        "## Ranked By Theorem Project Suitability",
        "",
        markdown_table(sorted(rows, key=sort_key("theorem_project_suitability"))),
        "",
        "## Ranked By OpenEvolve Suitability",
        "",
        markdown_table(sorted(rows, key=sort_key("openevolve_suitability"))),
        "",
        "## Ranked By Intellectual Interest",
        "",
        markdown_table(sorted(rows, key=sort_key("intellectual_interest"))),
        "",
        "## Ranked By Best Use",
        "",
    ]

    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row.get("best_use") or "(blank)", []).append(row)

    for best_use in sorted(grouped):
        group_rows = sorted(grouped[best_use], key=fallback_sort_key)
        sections.extend(
            [
                f"### {best_use}",
                "",
                markdown_table(group_rows, include_best_use=False),
                "",
            ]
        )

    sections.extend(
        [
            "## Notes",
            "",
            notes_table(sorted(rows, key=fallback_sort_key)),
            "",
        ]
    )

    REPORT_PATH.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    rows = load_rows()
    ordered_rows = sorted(rows, key=fallback_sort_key)
    write_csv(ordered_rows)
    write_report(rows)
    print(f"Wrote {CSV_PATH.relative_to(ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
