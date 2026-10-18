#!/usr/bin/env python3
"""Export canonical route prompts without expected semantics for blind canaries."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from safe_files import read_text


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=str(Path(__file__).parents[1]),
        help="repository root containing tests/route-contracts.json",
    )
    parser.add_argument(
        "--output",
        default="-",
        help="output JSON path, or - for stdout",
    )
    return parser.parse_args(argv)


def build_prompt_manifest(root: Path) -> dict[str, object]:
    contract_path = root / "tests" / "route-contracts.json"
    contract = json.loads(read_text(contract_path, root=root))
    scenarios = contract.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("route contracts must contain a non-empty scenarios list")

    prompt_items: list[dict[str, str]] = []
    seen: set[str] = set()
    started = time.monotonic()
    for index, scenario in enumerate(scenarios, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(scenarios) - index)
        scenario_id = scenario.get("id") if isinstance(scenario, dict) else None
        prompt = scenario.get("prompt") if isinstance(scenario, dict) else None
        print(
            f"PROMPT [{index}/{len(scenarios)}] id={scenario_id or 'invalid'} eta={eta:.1f}s",
            file=sys.stderr,
            flush=True,
        )
        if not isinstance(scenario_id, str) or not scenario_id.strip():
            raise ValueError(f"scenario {index} lacks a valid id")
        if scenario_id in seen:
            raise ValueError(f"duplicate scenario id: {scenario_id}")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError(f"{scenario_id} lacks a valid prompt")
        seen.add(scenario_id)
        prompt_items.append({"id": scenario_id, "prompt": prompt})

    return {
        "schema_version": 1,
        "source_contract_schema_version": contract.get("schema_version"),
        "evidence_class": "prompt-only blind canary input",
        "scenarios": prompt_items,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        manifest = build_prompt_manifest(Path(args.root).expanduser().resolve())
        rendered = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        if args.output == "-":
            sys.stdout.write(rendered)
        else:
            output = Path(args.output).expanduser().resolve()
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered, encoding="utf-8")
            print(f"WROTE prompts={len(manifest['scenarios'])} output={output}", file=sys.stderr)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
