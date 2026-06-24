"""Orchestrate gen → answer × reps → blind judge for portable A/B harness."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

try:
    from .protocol import (
        HarnessConfig,
        RepScores,
        ScoreRow,
        score_reps,
        score_row_to_dict,
        slim_row_from_score,
        unswap_verdict,
    )
except ImportError:
    from protocol import (
        HarnessConfig,
        RepScores,
        ScoreRow,
        score_reps,
        score_row_to_dict,
        slim_row_from_score,
        unswap_verdict,
    )


class Driver(Protocol):
    def generate_scenario(self, target: Any) -> str: ...
    def answer_base(self, scenario: str, rep: int) -> str: ...
    def answer_with_skill(self, scenario: str, skill_body: str, rep: int) -> str: ...
    def judge(
        self, scenario: str, answer1: str, answer2: str, focus: str
    ) -> dict[str, Any]: ...


def _runs_dir() -> Path:
    root = Path(__file__).resolve().parents[3]
    d = root / "eval" / "runs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def new_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def write_checkpoint(run_dir: Path, payload: dict[str, Any]) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / "results.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_target(
    driver: Driver,
    target: Any,
    *,
    reps: int,
    target_index: int = 0,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Run full pipeline for one target; returns checkpoint fragment."""
    try:
        from .anthropic_driver import read_skill_body
    except ImportError:
        from anthropic_driver import read_skill_body

    stage: dict[str, Any] = {
        "skill": target.skill,
        "file": target.file,
        "focus": target.focus,
        "reps": reps,
        "dry_run": dry_run,
    }

    scenario = driver.generate_scenario(target)
    stage["scenario"] = scenario

    skill_body = read_skill_body(target.file)
    rep_rows: list[RepScores] = []
    rep_details: list[dict[str, Any]] = []

    for r in range(reps):
        wo = driver.answer_base(scenario, r)
        wi = driver.answer_with_skill(scenario, skill_body, r)
        even = ((target_index + r) % 2) == 0
        a1 = wo if even else wi
        a2 = wi if even else wo
        verdict = driver.judge(scenario, a1, a2, target.focus)
        scores = unswap_verdict(
            float(verdict["score1"]),
            float(verdict["score2"]),
            even=even,
        )
        rep_rows.append(scores)
        rep_details.append(
            {
                "rep": r,
                "even_swap": even,
                "with_score": scores.ws,
                "without_score": scores.wos,
                "reason": verdict.get("reason", ""),
            }
        )

    stage["rep_details"] = rep_details
    row = score_reps(target.skill, rep_rows)
    if row is None:
        stage["error"] = "no valid reps"
        return stage

    stage["result"] = score_row_to_dict(row)
    return stage


def run_harness(
    config: HarnessConfig,
    driver: Driver,
    *,
    dry_run: bool = False,
    run_id: str | None = None,
) -> dict[str, Any]:
    """Run all targets; checkpoint to eval/runs/<run_id>/results.json."""
    rid = run_id or new_run_id()
    run_dir = _runs_dir() / rid
    rows: list[ScoreRow] = []
    targets_out: list[dict[str, Any]] = []

    for i, target in enumerate(config.targets):
        fragment = run_target(
            driver,
            target,
            reps=config.reps,
            target_index=i,
            dry_run=dry_run,
        )
        targets_out.append(fragment)
        result = fragment.get("result")
        if result:
            rows.append(
                ScoreRow(
                    skill=result["skill"],
                    reps=result["reps"],
                    mean_without=result["meanWithout"],
                    mean_with=result["meanWith"],
                    delta=result["delta"],
                    se=result["se"],
                    sigma=result.get("sigma"),
                    threshold=result["threshold"],
                    kind=result["kind"],
                )
            )
        write_checkpoint(
            run_dir,
            {
                "run_id": rid,
                "reps": config.reps,
                "dry_run": dry_run,
                "targets": targets_out,
            },
        )

    sorted_rows = sorted(rows, key=lambda r: r.delta, reverse=True)
    summary = {
        "run_id": rid,
        "n": len(sorted_rows),
        "reps": config.reps,
        "dry_run": dry_run,
        "rows": [score_row_to_dict(r) for r in sorted_rows],
    }
    write_checkpoint(run_dir, {**summary, "targets": targets_out, "complete": True})
    return summary


def summary_table(summary: dict[str, Any]) -> str:
    lines = [
        f"run={summary.get('run_id')}  n={summary.get('n')}  reps={summary.get('reps')}"
        + ("  [dry-run]" if summary.get("dry_run") else ""),
        f"{'skill':<40} {'delta':>6} {'kind':<12} {'mW':>5} {'mWo':>5} {'sigma':>6}",
        "-" * 82,
    ]
    for row in summary.get("rows", []):
        sigma = row.get("sigma")
        sig_s = f"{sigma:.2f}" if sigma is not None else "n/a"
        lines.append(
            f"{row['skill']:<40} {row['delta']:>6.2f} {row['kind']:<12} "
            f"{row['meanWith']:>5.2f} {row['meanWithout']:>5.2f} {sig_s:>6}"
        )
    return "\n".join(lines)


def slim_rows_from_summary(summary: dict[str, Any], run_id: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    method = f"x{summary.get('reps', 3)}"
    for row in summary.get("rows", []):
        score = ScoreRow(
            skill=row["skill"],
            reps=row["reps"],
            mean_without=row["meanWithout"],
            mean_with=row["meanWith"],
            delta=row["delta"],
            se=row["se"],
            sigma=row.get("sigma"),
            threshold=row["threshold"],
            kind=row["kind"],
        )
        out.append(slim_row_from_score(score, run_id=run_id, method=method))
    return out
