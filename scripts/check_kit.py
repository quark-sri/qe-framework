#!/usr/bin/env python3
"""Consistency checks for the AQEF starter kit.

Checks:
1. Each agent and skill file has front matter with `name` and `description`.
2. Each agent in `.aqef/config.yaml` autonomy has a definition file, and the reverse.
3. Each KB file has an `id`; every `relates_to` id exists.
4. Every relative markdown link in the kit and docs resolves to a file.
5. The JSON schemas are valid Draft 2020-12 schemas.

Exit code 0 when clean, 1 when a check fails.
"""
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
KIT = ROOT / "aqef-kit"
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    return yaml.safe_load(text[4:end]) if end != -1 else None


def check_agents_and_skills(errors):
    agent_names = set()
    for path in sorted((KIT / "agents").glob("*.md")):
        if path.name == "README.md":
            continue
        fm = front_matter(path) or {}
        for key in ("name", "description", "tools"):
            if not fm.get(key):
                errors.append(f"{path.relative_to(ROOT)}: front matter has no '{key}'")
        if fm.get("name") and fm["name"] != path.stem:
            errors.append(f"{path.relative_to(ROOT)}: name '{fm['name']}' does not match file name")
        agent_names.add(path.stem)
    for path in sorted((KIT / "skills").glob("*/SKILL.md")):
        fm = front_matter(path) or {}
        for key in ("name", "description"):
            if not fm.get(key):
                errors.append(f"{path.relative_to(ROOT)}: front matter has no '{key}'")
        if fm.get("name") and fm["name"] != path.parent.name:
            errors.append(f"{path.relative_to(ROOT)}: name '{fm['name']}' does not match folder name")
    return agent_names


def check_config(errors, agent_names):
    config = yaml.safe_load((KIT / ".aqef" / "config.yaml").read_text(encoding="utf-8"))
    configured = set(config["autonomy"]["agents"])
    for name in sorted(configured - agent_names):
        errors.append(f"config autonomy lists '{name}' but agents/{name}.md does not exist")
    for name in sorted(agent_names - configured):
        errors.append(f"agents/{name}.md has no autonomy level in .aqef/config.yaml")
    states = set(config["triage"]["confidence_bars"]) | {"expected_change", "regression_of_fixed_defect"}
    for state in config["triage"].get("never_autonomous", []) + config["triage"].get("t1_requires_human", []):
        if state not in states:
            errors.append(f"config triage: unknown state '{state}'")


def check_kb(errors):
    ids, links = {}, []
    for path in sorted((KIT / "domain").rglob("*.md")):
        if path.name == "README.md":
            continue
        fm = front_matter(path) or {}
        if not fm.get("id"):
            errors.append(f"{path.relative_to(ROOT)}: KB file has no 'id'")
            continue
        ids[fm["id"]] = path
        for target in fm.get("relates_to") or []:
            links.append((path, target))
    for path, target in links:
        if target not in ids:
            errors.append(f"{path.relative_to(ROOT)}: relates_to '{target}' does not exist")


def check_links(errors):
    for path in sorted(list(KIT.rglob("*.md")) + list((ROOT / "docs").rglob("*.md")) + [ROOT / "README.md"]):
        if not path.exists():
            continue
        text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
        for target in LINK.findall(text):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            target = target.split("#")[0]
            if target and not (path.parent / target).exists():
                errors.append(f"{path.relative_to(ROOT)}: broken link '{target}'")


def check_schemas(errors):
    for path in sorted((KIT / "schemas").glob("*.json")):
        try:
            Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))
        except Exception as exc:  # noqa: BLE001 - report any schema problem
            errors.append(f"{path.relative_to(ROOT)}: invalid schema: {exc}")


def main():
    errors = []
    agent_names = check_agents_and_skills(errors)
    check_config(errors, agent_names)
    check_kb(errors)
    check_links(errors)
    check_schemas(errors)
    for error in errors:
        print(f"FAIL {error}")
    print(f"AQEF kit check: {'clean' if not errors else f'{len(errors)} problem(s)'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
