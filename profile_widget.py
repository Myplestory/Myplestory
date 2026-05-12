#!/usr/bin/env python3
"""regenerate the github profile widget from FortifAI's session.json."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SESSION = HERE.parent / "FortifAI" / "data" / "session.json"
DEFAULT_README = HERE / "README.md"

SUBSCRIPT_DIGITS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

WIDTH_LEFT_LABEL = 13
WIDTH_LEFT_VALUE = 37
WIDTH_RIGHT_LABEL = 16
WIDTH_Q = 4
WIDTH_FIELD = 19
WIDTH_TOPIC = 24
WIDTH_BAND_CELL = 4
HEADER_BAND_PAD = 46

ALL_BANDS = ["b1", "b2", "b3", "b4", "b5"]
DISTRIBUTION_BANDS = ["b2", "b3", "b4"]
SUBSCRIPT_BANDS = {"b2", "b4"}

SWECOM_LABELS = {
    "b1": "technician",
    "b3": "practitioner",
    "b5": "principal",
}

WIDGET_RE = re.compile(
    r"<details>\n<summary><samp>fortifai · self-audit loop[^\n]*</summary>"
    r".*?<sub><samp><i>widget regenerated[^<]*</i></samp></sub>\n</details>",
    re.DOTALL,
)
LEGACY_WIDGET_RE = re.compile(
    r"<samp>fortifai latest run</samp>[^\n]*\n```\n.*?\n```\n"
    r"<sub><samp><i>widget regenerated[^<]*</i></samp></sub>",
    re.DOTALL,
)


def load_blob(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def pick_user(blob: dict, user_id: str | None) -> tuple[str, dict]:
    if user_id is None:
        user_id = next(iter(blob))
    return user_id, blob[user_id]


def pick_run(user: dict):
    sessions = user.get("sessions", {})
    if not sessions:
        return None
    name = user.get("current") or next(iter(sessions))
    session = sessions[name]
    graded = [
        r for r in session.get("runs", [])
        if r.get("status") == "complete" and r.get("aggregated_score") is not None
    ]
    if not graded:
        return None
    graded.sort(key=lambda r: r.get("end") or r.get("start") or "")
    return session, graded[-1]


def compute_streak(user: dict, today: date | None = None) -> int:
    today = today or datetime.now(timezone.utc).date()
    dates: set[date] = set()
    for session in user.get("sessions", {}).values():
        for run in session.get("runs", []):
            if run.get("status") != "complete":
                continue
            ts = run.get("end") or run.get("start")
            if not ts:
                continue
            try:
                dates.add(date.fromisoformat(ts[:10]))
            except ValueError:
                continue
    if not dates:
        return 0
    latest = max(dates)
    if (today - latest).days > 1:
        return 0
    streak = 0
    cursor = latest
    while cursor in dates:
        streak += 1
        cursor = date.fromordinal(cursor.toordinal() - 1)
    return streak


def canonical_field_count(parse_py: Path) -> int | None:
    if not parse_py.exists():
        return None
    text = parse_py.read_text()
    m = re.search(r"CANONICAL_FIELDS\s*:[^=]*=\s*\{(.*?)\n\}", text, re.DOTALL)
    if not m:
        return None
    n = len(re.findall(r"^    \"[\w-]+\"\s*:\s*\{", m.group(1), re.MULTILINE))
    return n or None


def band_score(q: dict, key: str, band: str):
    target = (band or "").lower()
    for b in q.get(key, []) or []:
        if (b.get("band") or "").lower() == target:
            return b.get("score")
    return None


def normalize_band(b: str | None) -> str | None:
    if not b:
        return None
    s = b.strip().lower()
    if s and s[0] != "b":
        s = "b" + s
    return s


def ceiling_and_transitional(q: dict) -> tuple[str, str | None]:
    ceiling = normalize_band(q.get("band_ceiling_post")) or "b1"
    transitional = normalize_band(q.get("transitional_post"))
    return ceiling, transitional


def short_topic(topic: str, max_width: int = 22) -> str:
    if not topic:
        return ""
    if len(topic) <= max_width:
        return topic
    parts = topic.split("-")
    while len(parts) > 1:
        parts.pop()
        candidate = "-".join(parts)
        if len(candidate) <= max_width:
            return candidate
    return topic[:max_width]


def fmt_band_cell(score, use_subscript: bool) -> str:
    if score is None:
        return "—"
    if use_subscript:
        return str(int(score)).translate(SUBSCRIPT_DIGITS)
    return str(int(score))


def fmt_num(n) -> str:
    if n is None:
        return "—"
    if isinstance(n, float) and n.is_integer():
        return str(int(n))
    if isinstance(n, float):
        return f"{n:.1f}"
    return str(n)


def pad(s: str, width: int) -> str:
    return s + " " * max(0, width - len(s))


def scope_value(run: dict, canonical_count: int | None) -> str:
    if canonical_count:
        return f"cross-domain · {canonical_count} field grab-bag"
    return "cross-domain · grab-bag"


def rotation_bias_value(run: dict) -> str:
    return "underindexed-weighted"


def calibration_value(band: str) -> str:
    label = SWECOM_LABELS.get(band.lower(), "")
    return f'{band.lower()} "{label}"' if label else band.lower()


def render_header_rows(industry: str, run_date: str, scope: str, duration: str,
                       calib: str, bias: str) -> list[str]:
    rows = []
    rows.append(
        pad("industry", WIDTH_LEFT_LABEL)
        + pad(industry, WIDTH_LEFT_VALUE)
        + pad("updated", WIDTH_RIGHT_LABEL)
        + run_date
    )
    rows.append(
        pad("scope", WIDTH_LEFT_LABEL)
        + pad(scope, WIDTH_LEFT_VALUE)
        + pad("duration", WIDTH_RIGHT_LABEL)
        + duration
    )
    rows.append(
        pad("calibration", WIDTH_LEFT_LABEL)
        + pad(calib, WIDTH_LEFT_VALUE)
        + pad("rotation bias", WIDTH_RIGHT_LABEL)
        + bias
    )
    return rows


def render_distribution_rows(questions: list[dict]) -> list[str]:
    rows: list[str] = []
    rows.append(" " * HEADER_BAND_PAD + "b₂  b3  b₄")
    for i, qd in enumerate(questions, 1):
        q = next(iter(qd.values())) if isinstance(qd, dict) and qd else {}
        field = (q.get("field") or "").strip()
        topics = q.get("topics") or []
        topic = short_topic(topics[0] if topics else "")
        cells = ""
        for b in DISTRIBUTION_BANDS:
            score = band_score(q, "bands", b)
            cell = fmt_band_cell(score, b in SUBSCRIPT_BANDS)
            cells += pad(cell, WIDTH_BAND_CELL)
        cells = cells.rstrip()
        rows.append(
            pad(f"q{i}", WIDTH_Q)
            + pad(field, WIDTH_FIELD)
            + pad(topic, WIDTH_TOPIC)
            + cells
        )
    return rows


def render_strengths_gaps(run: dict) -> list[str]:
    rows = []
    strengths = run.get("strengths", {}).get("topics", []) or []
    gaps = run.get("weaknesses", {}).get("topics", []) or []
    if strengths:
        rows.append(pad("strengths", WIDTH_LEFT_LABEL) + " · ".join(strengths[:4]))
    if gaps:
        rows.append(pad("gaps", WIDTH_LEFT_LABEL) + " · ".join(gaps[:4]))
    return rows


def render_scale_rows() -> list[str]:
    return [
        "score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)",
        "band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)",
    ]


def render_data_block(run: dict, canonical_count: int | None) -> str:
    industry = (run.get("industry") or "").lower()
    band = normalize_band(run.get("band")) or "b3"
    end = run.get("end") or run.get("start") or ""
    run_date = end[:10] if end else "—"
    duration = run.get("duration") or "—"

    scope = scope_value(run, canonical_count)
    calib = calibration_value(band)
    bias = rotation_bias_value(run)

    lines = render_header_rows(industry, run_date, scope, duration, calib, bias)
    lines.append("")
    lines.extend(render_distribution_rows(run.get("questions", [])))
    lines.append("")
    sg = render_strengths_gaps(run)
    if sg:
        lines.extend(sg)
        lines.append("")
    lines.extend(render_scale_rows())
    return "\n".join(lines).rstrip()


def render_literature(q: dict) -> list[str]:
    out: list[str] = []
    for item in q.get("literature", []) or []:
        tag = (item.get("type") or "").lower()
        title = item.get("title") or ""
        section = item.get("section") or ""
        time_str = item.get("reading_time_estimate") or ""
        parts = [f"[{tag}]" if tag else "", title]
        tail = [section] if section else []
        if time_str:
            tail.append(time_str)
        line = " ".join(p for p in parts if p)
        if tail:
            line += " — " + " — ".join(tail)
        out.append("- " + line)
    return out


def render_question_summary(idx: int, q: dict, calibrated_band: str) -> str:
    field = (q.get("field") or "").strip()
    topics = q.get("topics") or []
    topic = topics[0] if topics else ""
    pre = band_score(q, "bands_pre", calibrated_band)
    post = band_score(q, "bands", calibrated_band)
    ceiling, transitional = ceiling_and_transitional(q)
    line = (
        f"q{idx} · {field} · {topic} · pre {fmt_num(pre)} → post {fmt_num(post)} · ceiling {ceiling}"
    )
    if transitional and transitional != ceiling:
        line += f" · transitional {transitional}"
    return line


def render_question_details(idx: int, q: dict, calibrated_band: str) -> str:
    summary = render_question_summary(idx, q, calibrated_band)
    scenario = (q.get("question") or "").strip()
    assessment = (q.get("assessment") or "").strip()
    lit_lines = render_literature(q)
    lit_block = "\n".join(lit_lines) if lit_lines else ""
    return (
        "<details>\n"
        f"<summary><samp>{summary}</samp></summary>\n"
        "\n"
        "<small>\n"
        "\n"
        "\xa0\n"
        "\n"
        f"**Scenario:** {scenario}\n"
        "\n"
        "\xa0\n"
        "\n"
        f"**Assessment:** {assessment}\n"
        "\n"
        "**Literature**\n"
        "\n"
        f"{lit_block}\n"
        "\n"
        "</small>\n"
        "</details>"
    )


def render_inline_framing(band: str, canonical_count: int | None, industry: str) -> str:
    count = canonical_count or 8
    industry_tag = industry or "swe"
    line1 = (
        f"self-audit: scenario-based time-pressured recall, cross-domain breadth, "
        f"{band}-calibrated"
    )
    line2 = (
        "invariant: zero outside assistance. no docs, no ai, no peers. "
        "10m/response, 5m/single refinement"
    )
    line3 = f"bar: consistent ≥3 across all {count} {industry_tag} fields"
    return (
        "<sub><samp><i>"
        f"{line1}<br>\n"
        f"{line2}<br>\n"
        f"{line3}"
        "</i></samp></sub>"
    )


def render(session: dict, run: dict, canonical_count: int | None = None, streak: int = 0) -> str:
    band = normalize_band(run.get("band")) or "b3"
    industry = (run.get("industry") or "").lower() or "swe"

    streak_clause = f" · streak {streak}d" if streak > 0 else ""
    summary = (
        f"<summary><samp>fortifai · self-audit loop{streak_clause}</samp></summary>"
    )

    inline = render_inline_framing(band, canonical_count, industry)
    data_block = render_data_block(run, canonical_count)

    questions = run.get("questions", [])
    q_blocks = []
    for i, qd in enumerate(questions, 1):
        q = next(iter(qd.values())) if isinstance(qd, dict) and qd else {}
        q_blocks.append(render_question_details(i, q, band))

    footer = (
        "<sub><samp><i>widget regenerated from fortifai's data/session.json via "
        "profile_widget.py</i></samp></sub>"
    )

    parts = [
        "<details>",
        summary,
        "",
        inline,
        "",
        "```",
        data_block,
        "```",
        "",
    ]
    for block in q_blocks:
        parts.append(block)
        parts.append("")
    parts.append(footer)
    parts.append("</details>")
    return "\n".join(parts)


def splice(readme: str, widget: str) -> str:
    m = WIDGET_RE.search(readme)
    if m:
        return readme[:m.start()] + widget + readme[m.end():]
    m = LEGACY_WIDGET_RE.search(readme)
    if m:
        return readme[:m.start()] + widget + readme[m.end():]
    return readme.rstrip() + "\n\n" + widget + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--readme", default=str(DEFAULT_README))
    ap.add_argument("--session-file", default=str(DEFAULT_SESSION))
    ap.add_argument("--user", default=None, help="discord user id (defaults to first key)")
    ap.add_argument("--stdout", action="store_true", help="print widget instead of writing")
    args = ap.parse_args()

    session_path = Path(args.session_file)
    if not session_path.exists():
        print(f"session file not found: {session_path}", file=sys.stderr)
        return 1
    blob = load_blob(session_path)
    _, user = pick_user(blob, args.user)
    picked = pick_run(user)
    if not picked:
        print("no graded runs found", file=sys.stderr)
        return 1
    count = canonical_field_count(session_path.parent.parent / "parse.py")
    streak = compute_streak(user)
    widget = render(*picked, canonical_count=count, streak=streak)

    if args.stdout:
        print(widget)
        return 0

    path = Path(args.readme)
    text = path.read_text() if path.exists() else ""
    path.write_text(splice(text, widget))
    print(f"updated widget in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
