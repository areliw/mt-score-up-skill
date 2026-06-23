#!/usr/bin/env python3
"""Portable A/B harness CLI — Anthropic API path (Cursor / Codex / local).

Usage:
  python scripts/ab_harness.py --skill choose-stat-test --reps 1 --dry-run
  python scripts/ab_harness.py --config eval/harness/backfill-screen-only.json --reps 3
  python scripts/ab_harness.py --skill foo-judgment --reps 5 --append-slim
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "eval" / "harness" / "python"))

from append_slim import append_rows  # noqa: E402
from anthropic_driver import AnthropicDriver, DryRunDriver  # noqa: E402
from protocol import HarnessConfig, parse_config, resolve_target_by_skill  # noqa: E402
from runner import run_harness, slim_rows_from_summary, summary_table  # noqa: E402


def load_config_file(path: Path) -> HarnessConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and data.get("workflow", {}).get("args"):
        return parse_config(data["workflow"]["args"])
    if isinstance(data, dict) and data.get("targets"):
        return parse_config(data)
    return parse_config(data)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Portable ×N A/B blind-judge harness")
    p.add_argument(
        "--config",
        type=Path,
        help="JSON config (targets + reps) or backfill-screen-only.json wrapper",
    )
    p.add_argument(
        "--skill",
        help="Single skill slug (implies skills/<slug>.md)",
    )
    p.add_argument(
        "--reps",
        type=int,
        default=3,
        help="Reps per arm (default 3 = screen; 5 = act-grade)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Stub LLM calls — no API key required",
    )
    p.add_argument(
        "--append-slim",
        action="store_true",
        help="Append full-tier rows to eval/_ab_slim.json",
    )
    p.add_argument(
        "--run-id",
        help="Override checkpoint run id (default UTC timestamp)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.config:
        config = load_config_file(args.config)
        if args.reps != 3:
            config = HarnessConfig(targets=config.targets, reps=args.reps)
    elif args.skill:
        target = resolve_target_by_skill(args.skill)
        config = HarnessConfig(targets=[target], reps=args.reps)
    else:
        print("error: pass --config or --skill", file=sys.stderr)
        return 2

    if not config.targets:
        print("error: no targets", file=sys.stderr)
        return 2

    driver = DryRunDriver() if args.dry_run else AnthropicDriver()
    summary = run_harness(
        config,
        driver,
        dry_run=args.dry_run,
        run_id=args.run_id,
    )
    print(summary_table(summary))

    if args.append_slim:
        rows = slim_rows_from_summary(summary, summary["run_id"])
        n = append_rows(rows, dry_run=args.dry_run)
        action = "would append" if args.dry_run else "appended"
        print(f"\n{ab_action_msg(action, n)}")

    return 0


def ab_action_msg(action: str, n: int) -> str:
    return f"{action} {n} row(s) to eval/_ab_slim.json (tier=full, method=x*)"


if __name__ == "__main__":
    raise SystemExit(main())
