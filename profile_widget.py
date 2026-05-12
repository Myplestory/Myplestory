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

WIDTH = 65

WIDGET_RE = re.compile(
    r"(### )?(?:<samp>)?fortifai latest run(?:</samp>)?[^\n]*\n+```\n.*?\n```",
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
    """consecutive days with at least one completed run, anchored to today."""
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


def band_score(question_entry: dict, key: str, band: str):
    for b in question_entry.get(key, []) or []:
        if b.get("band") == band:
            return b.get("score")
    return None


def canonical_field_count(parse_py: Path) -> int | None:
    if not parse_py.exists():
        return None
    text = parse_py.read_text()
    m = re.search(r"CANONICAL_FIELDS\s*:[^=]*=\s*\{(.*?)\n\}", text, re.DOTALL)
    if not m:
        return None
    n = len(re.findall(r"^    \"[\w-]+\"\s*:\s*\{", m.group(1), re.MULTILINE))
    return n or None


def scope_label(run: dict, canonical_count: int | None) -> str:
    fields = run.get("fields_invoked") or []
    topics = run.get("topics_invoked") or []
    domain = run.get("domain") or ""
    stack = run.get("stack") or []
    parts: list[str] = []
    if fields:
        parts.append("fields: " + ", ".join(fields))
    if topics:
        parts.append("topics: " + ", ".join(topics))
    if domain:
        parts.append(f"domain: {domain}")
    if stack:
        parts.append("stack: " + ", ".join(stack))
    if parts:
        return " · ".join(parts)
    industry = (run.get("industry") or "").lower()
    if canonical_count and industry:
        return f"cross-domain · grab-bag · all {canonical_count} {industry} fields"
    if canonical_count:
        return f"cross-domain · grab-bag · all {canonical_count} fields"
    return "cross-domain · grab-bag"


def bias_label(run: dict) -> str:
    biased = run.get("generation_metadata", {}).get("biased_toward_weaknesses", False)
    return "weakness‑biased" if biased else "uniform"


def fmt_num(n) -> str:
    if n is None:
        return "—"
    if isinstance(n, float) and n.is_integer():
        return f"{int(n)}"
    if isinstance(n, float):
        return f"{n:.1f}"
    return str(n)


def fmt_delta(pre, post) -> str:
    if pre is None or post is None:
        return "—"
    d = post - pre
    if isinstance(d, float) and d.is_integer():
        d = int(d)
    if d > 0:
        return f"+{d}"
    if d < 0:
        return f"{d}"
    return " 0"


def render(session: dict, run: dict, canonical_count: int | None = None, streak: int = 0) -> str:
    name = session.get("name", "")
    band = run.get("band") or session.get("band_preference") or ""
    industry = (run.get("industry") or "").lower()
    score = run.get("aggregated_score")
    career = run.get("career_level") or "—"
    duration = run.get("duration") or "—"
    end = run.get("end") or run.get("start") or ""
    date = end[:10] if end else "—"

    fields = run.get("generation_metadata", {}).get("fields_covered", [])
    questions = run.get("questions", [])
    strengths = run.get("strengths", {}).get("topics", []) or []
    gaps = run.get("weaknesses", {}).get("topics", []) or []

    band_label = band.lower() if band else "—"
    header_left = (
        f"{name} · {band_label} / {industry}".strip(" /·-—")
        if industry
        else f"{name} · {band_label}".strip(" /·-—")
    )

    scope = scope_label(run, canonical_count)
    bias = bias_label(run)

    lines: list[str] = []
    lines.append(f"session    {header_left:<{WIDTH - 22}}updated  {date}")
    aggr = f"{fmt_num(score)} / 5 · {career}".strip(" ·")
    lines.append(f"aggregate  {aggr:<{WIDTH - 22}}run      {duration}")
    lines.append(f"scope      {scope:<{WIDTH - 22}}bias     {bias}")
    lines.append("")

    if fields:
        lines.append("fields tested (field‑rotation pick)")
        lines.append("  " + "  ".join(fields))
        lines.append("")

    if questions:
        for i, qd in enumerate(questions, 1):
            q = next(iter(qd.values())) if isinstance(qd, dict) and qd else {}
            field = (q.get("field") or "").strip()
            topics = q.get("topics") or []
            topic = topics[0] if topics else ""
            pre = band_score(q, "bands_pre", band)
            post = band_score(q, "bands", band)
            lines.append(
                f"q{i}  {field:<18s} {topic:<28s} pre {fmt_num(pre):>2} → {fmt_num(post):>2}   Δ {fmt_delta(pre, post):>2}"
            )
        lines.append("")

    if strengths:
        lines.append("strengths   " + " · ".join(strengths[:4]))
    if gaps:
        lines.append("gaps        " + " · ".join(gaps[:4]))
    if strengths or gaps:
        lines.append("")

    lines.append("calibrated   dreyfus · ieee swecom · sfia v9")
    lines.append("scale        1.0 (novice)  →  5.0 (strategic)")

    body = "\n".join(lines).rstrip()
    if streak > 0:
        title = f"<samp>fortifai latest run</samp> \xa0·\xa0 <samp>streak</samp> `{streak}d`"
    else:
        title = "<samp>fortifai latest run</samp>"
    return f"{title}\n\n```\n{body}\n```"


def splice(readme: str, widget: str) -> str:
    m = WIDGET_RE.search(readme)
    if m:
        prefix = m.group(1) or ""
        return readme[:m.start()] + prefix + widget + readme[m.end():]
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
