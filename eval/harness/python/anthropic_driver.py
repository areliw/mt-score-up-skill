"""Anthropic API driver for portable A/B harness."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

try:
    from .protocol import load_prompt
except ImportError:
    from protocol import load_prompt

MODEL_OPUS = "claude-opus-4-20250514"
MODEL_HAIKU = "claude-3-5-haiku-20241022"

SCENARIO_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"scenario": {"type": "string"}},
    "required": ["scenario"],
    "additionalProperties": False,
}

VERDICT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "score1": {"type": "number"},
        "score2": {"type": "number"},
        "reason": {"type": "string"},
    },
    "required": ["score1", "score2", "reason"],
    "additionalProperties": False,
}


class DryRunDriver:
    """Deterministic stub for --dry-run (no API key)."""

    def generate_scenario(self, target: Any) -> str:
        return (
            f"[dry-run] สถานการณ์ MT ที่ล่อให้ตกหลุม: {target.focus} "
            f"(skill={target.skill})"
        )

    def answer_base(self, scenario: str, rep: int) -> str:
        return f"[dry-run base rep {rep}] ตอบโดยไม่มีสกิล: {scenario[:80]}…"

    def answer_with_skill(self, scenario: str, skill_body: str, rep: int) -> str:
        return (
            f"[dry-run skill rep {rep}] ใช้ judgment จากสกิล "
            f"({len(skill_body)} chars): {scenario[:60]}…"
        )

    def judge(
        self,
        scenario: str,
        answer1: str,
        answer2: str,
        focus: str,
    ) -> dict[str, Any]:
        return {
            "score1": 3.0,
            "score2": 4.0,
            "reason": "[dry-run] blind judge stub",
        }


class AnthropicDriver:
    def __init__(self, *, client: Any | None = None) -> None:
        if client is not None:
            self._client = client
            return
        api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY not set — use --dry-run or export the key"
            )
        try:
            import anthropic
        except ImportError as exc:
            raise RuntimeError(
                "anthropic package not installed — pip install -r requirements-dev.txt"
            ) from exc
        self._client = anthropic.Anthropic(api_key=api_key)

    def _structured(
        self,
        prompt: str,
        schema: dict[str, Any],
        *,
        model: str,
        max_tokens: int = 1024,
    ) -> dict[str, Any]:
        response = self._client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "harness_output",
                    "strict": True,
                    "schema": schema,
                },
            },
        )
        text = response.content[0].text
        return json.loads(text)

    def _text(self, prompt: str, *, model: str, max_tokens: int = 512) -> str:
        response = self._client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()

    def generate_scenario(self, target: Any) -> str:
        root = Path(__file__).resolve().parents[3]
        skill_path = root / target.file
        skill_body = skill_path.read_text(encoding="utf-8") if skill_path.is_file() else ""
        prompt = load_prompt(
            "generate.txt",
            file=target.file,
            focus=target.focus,
        )
        # Include skill excerpt for Python path (no Read tool)
        if skill_body:
            prompt = (
                f"เนื้อหาสกิล (อ่านแล้ว):\n---\n{skill_body[:8000]}\n---\n\n" + prompt
            )
        result = self._structured(prompt, SCENARIO_SCHEMA, model=MODEL_OPUS)
        return str(result["scenario"]).strip()

    def answer_base(self, scenario: str, rep: int) -> str:
        prompt = load_prompt("answer_base.txt", rep=rep, scenario=scenario)
        return self._text(prompt, model=MODEL_HAIKU)

    def answer_with_skill(self, scenario: str, skill_body: str, rep: int) -> str:
        prompt = load_prompt(
            "answer_with_skill.txt",
            rep=rep,
            scenario=scenario,
            skill_body=skill_body,
        )
        return self._text(prompt, model=MODEL_HAIKU)

    def judge(
        self,
        scenario: str,
        answer1: str,
        answer2: str,
        focus: str,
    ) -> dict[str, Any]:
        prompt = load_prompt(
            "judge.txt",
            scenario=scenario,
            answer1=answer1,
            answer2=answer2,
            focus=focus,
        )
        return self._structured(prompt, VERDICT_SCHEMA, model=MODEL_OPUS)


def read_skill_body(skill_file: str) -> str:
    root = Path(__file__).resolve().parents[3]
    path = root / skill_file
    return path.read_text(encoding="utf-8")
