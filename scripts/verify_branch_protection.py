#!/usr/bin/env python3
"""Verify (or apply) GitHub branch protection required CI checks on main.

Required job names (must match workflow job `name:` fields):
  validate, check, maturity-gate, pytest

Exit 0 when all four are required on main; exit 1 with maintainer instructions otherwise.
Optional: pass --apply to attempt the gh api PUT (needs repo admin).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

REPO = "areliw/mt-score-up-skill"
BRANCH = "main"
REQUIRED = ("validate", "check", "maturity-gate", "pytest")

PROTECTION_PUT = {
    "required_status_checks": {
        "strict": True,
        "checks": [{"context": c} for c in REQUIRED],
    },
    "enforce_admins": False,
    "required_pull_request_reviews": {"required_approving_review_count": 0},
    "restrictions": None,
}


def _gh(endpoint: str, *, method: str | None = None, input_json: dict | None = None) -> subprocess.CompletedProcess[str]:
    cmd = ["gh", "api"]
    if method:
        cmd.extend(["-X", method])
    cmd.append(endpoint)
    if input_json is not None:
        cmd.extend(["--input", "-"])
    return subprocess.run(
        cmd,
        input=json.dumps(input_json) if input_json is not None else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def _contexts_from_protection(data: dict) -> list[str]:
    checks_block = data.get("required_status_checks") or {}
    raw = checks_block.get("checks") or checks_block.get("contexts") or []
    out: list[str] = []
    for item in raw:
        if isinstance(item, dict):
            ctx = item.get("context") or item.get("app_id")
            if ctx:
                out.append(str(ctx))
        elif item:
            out.append(str(item))
    return out


def fetch_protection() -> tuple[int, dict | None, str]:
    proc = _gh(f"repos/{REPO}/branches/{BRANCH}/protection")
    if proc.returncode != 0:
        return proc.returncode, None, (proc.stderr or proc.stdout or "").strip()
    try:
        return 0, json.loads(proc.stdout), ""
    except json.JSONDecodeError as exc:
        return 1, None, f"invalid JSON from gh api: {exc}"


def verify() -> int:
    code, data, err = fetch_protection()
    if code != 0 or data is None:
        print("Could not read branch protection for main.")
        if err:
            print(err)
        print("\nMaintainer: enable required checks per docs/BRANCH-PROTECTION.md")
        print("  python scripts/verify_branch_protection.py --apply   # if you are repo admin")
        return 1

    contexts = _contexts_from_protection(data)
    missing = [c for c in REQUIRED if c not in contexts]
    if missing:
        print("Branch protection is incomplete on main.")
        print(f"  missing required checks: {', '.join(missing)}")
        print(f"  current contexts: {', '.join(contexts) or '(none)'}")
        print("\nFix: docs/BRANCH-PROTECTION.md or run with --apply (admin token)")
        return 1

    print(f"Branch protection OK on {BRANCH}: {', '.join(REQUIRED)}")
    return 0


def apply() -> int:
    proc = _gh(
        f"repos/{REPO}/branches/{BRANCH}/protection",
        method="PUT",
        input_json=PROTECTION_PUT,
    )
    if proc.returncode == 0:
        print("Branch protection updated successfully.")
        return verify()
    print("Could not apply branch protection (needs repo admin + valid gh auth).")
    print(proc.stderr or proc.stdout or f"gh exit {proc.returncode}")
    print("\nManual step: run the PUT block in docs/BRANCH-PROTECTION.md in GitHub UI or gh.")
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Attempt gh api PUT to set required checks (repo admin only)",
    )
    args = parser.parse_args(argv)
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("GitHub CLI (gh) is required. Install from https://cli.github.com/")
        return 1
    return apply() if args.apply else verify()


if __name__ == "__main__":
    raise SystemExit(main())
