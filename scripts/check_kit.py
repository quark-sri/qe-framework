#!/usr/bin/env python3
"""Consistency checks for the AQEF starter kit.

Checks:
1. Each agent and skill file has front matter with `name` and `description`.
2. Each agent declares its permission contract: `kind` (report or act), `writes`,
   and `commands` when it has Bash. Report agents have no Edit or Bash and write only reports.
3. Each agent in `.aqef/config.yaml` autonomy has a definition file, and the reverse.
4. The config matches `schemas/config.schema.json`, and every key in that schema says
   who enforces it (`x-aqef-enforced-by`). Each stage runs only commands defined in the config.
5. Each KB file has an `id`; every `relates_to` id exists.
6. Every relative markdown link in the kit and docs resolves to a file.
7. The JSON schemas are valid Draft 2020-12 schemas. Example records in `schemas/examples/`
   validate (`*.valid*.json`) or fail (`*.invalid*.json`) as named. The example metrics validate.
8. Decisions (`docs/decisions/AQEF-nnn-*.md`): required keys, unique ids; each file in `applies_to`
   cites the id; every cited id exists and is live; no retired wording comes back.

Usage: check_kit.py [--root DIR]. Exit code 0 when clean, 1 when a check fails.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
REPORT_ROOTS = ("specs/", "triage/", "reports/", ".aqef/private/")
ENFORCERS = {"gatekeeper", "test-guard", "bot-contract", "agents", "humans", "kit", "mixed"}


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    return yaml.safe_load(text[4:end]) if end != -1 else None


def tools_of(fm):
    return {t.strip() for t in str(fm.get("tools", "")).split(",") if t.strip()}


def check_agents_and_skills(errors, root, kit, config):
    agent_names = set()
    commands = set((config or {}).get("commands") or {})
    for path in sorted((kit / "agents").glob("*.md")):
        if path.name == "README.md":
            continue
        rel = path.relative_to(root)
        fm = front_matter(path) or {}
        for key in ("name", "description", "tools", "kind", "writes"):
            if not fm.get(key):
                errors.append(f"{rel}: front matter has no '{key}'")
        if fm.get("name") and fm["name"] != path.stem:
            errors.append(f"{rel}: name '{fm['name']}' does not match file name")
        agent_names.add(path.stem)

        tools, writes, cmds = tools_of(fm), fm.get("writes") or [], fm.get("commands") or []
        if fm.get("kind") not in (None, "report", "act"):
            errors.append(f"{rel}: kind must be 'report' or 'act'")
        if not isinstance(writes, list):
            errors.append(f"{rel}: writes must be a list of paths")
            writes = []
        if "Bash" in tools and not cmds:
            errors.append(f"{rel}: has Bash but no 'commands' allow-list")
        if "Bash" not in tools and cmds:
            errors.append(f"{rel}: lists 'commands' but has no Bash tool")
        for cmd in cmds:
            if cmd not in commands:
                errors.append(f"{rel}: command '{cmd}' is not defined in .aqef/config.yaml commands")
        if fm.get("kind") == "report":
            for tool in sorted(tools & {"Edit", "Bash"}):
                errors.append(f"{rel}: report agent must not have the {tool} tool")
            for target in writes:
                if not str(target).startswith(REPORT_ROOTS):
                    errors.append(f"{rel}: report agent writes outside report folders: '{target}'")

    for path in sorted((kit / "skills").glob("*/SKILL.md")):
        fm = front_matter(path) or {}
        for key in ("name", "description"):
            if not fm.get(key):
                errors.append(f"{path.relative_to(root)}: front matter has no '{key}'")
        if fm.get("name") and fm["name"] != path.parent.name:
            errors.append(f"{path.relative_to(root)}: name '{fm['name']}' does not match folder name")
    return agent_names


def unannotated(schema, where="config"):
    """Yield schema paths of properties that do not say who enforces them."""
    for name, prop in (schema.get("properties") or {}).items():
        if prop.get("x-aqef-enforced-by") not in ENFORCERS:
            yield f"{where}.{name}"
        yield from unannotated(prop, f"{where}.{name}")
    for name, sub in (schema.get("$defs") or {}).items():
        yield from unannotated(sub, f"$defs.{name}")


def check_config(errors, kit, config, agent_names):
    schema = json.loads((kit / "schemas" / "config.schema.json").read_text(encoding="utf-8"))
    for err in Draft202012Validator(schema).iter_errors(config):
        errors.append(f"config: {'/'.join(map(str, err.absolute_path)) or '(root)'}: {err.message}")
    for path in unannotated(schema):
        errors.append(f"config.schema.json: {path} has no valid x-aqef-enforced-by")
    if not isinstance(config, dict):
        return
    configured = set((config.get("autonomy") or {}).get("agents") or {})
    for name in sorted(configured - agent_names):
        errors.append(f"config autonomy lists '{name}' but agents/{name}.md does not exist")
    for name in sorted(agent_names - configured):
        errors.append(f"agents/{name}.md has no autonomy level in .aqef/config.yaml")
    commands = set(config.get("commands") or {})
    for stage, spec in (config.get("stages") or {}).items():
        for cmd in (spec or {}).get("runs") or []:
            if cmd not in commands:
                errors.append(f"config: stage '{stage}' runs '{cmd}', which is not in commands")
    triage = config.get("triage") or {}
    states = set(triage.get("confidence_bars") or {}) | {"expected_change", "regression_of_fixed_defect"}
    for state in (triage.get("never_autonomous") or []) + (triage.get("t1_requires_human") or []):
        if state not in states:
            errors.append(f"config triage: unknown state '{state}'")


def check_kb(errors, root, kit):
    ids, links = {}, []
    for path in sorted((kit / "domain").rglob("*.md")):
        if path.name == "README.md":
            continue
        fm = front_matter(path) or {}
        if not fm.get("id"):
            errors.append(f"{path.relative_to(root)}: KB file has no 'id'")
            continue
        ids[fm["id"]] = path
        for target in fm.get("relates_to") or []:
            links.append((path, target))
    for path, target in links:
        if target not in ids:
            errors.append(f"{path.relative_to(root)}: relates_to '{target}' does not exist")


def check_links(errors, root, kit):
    paths = list(kit.rglob("*.md")) + list((root / "docs").rglob("*.md"))
    paths += [root / name for name in ("README.md", "CHANGELOG.md", "CONTRIBUTING.md", "ROADMAP.md")]
    for path in sorted(p for p in paths if p.exists()):
        text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
        for target in LINK.findall(text):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            target = target.split("#")[0]
            if target and not (path.parent / target).exists():
                errors.append(f"{path.relative_to(root)}: broken link '{target}'")


def check_schemas(errors, root, kit):
    schemas = {}
    for path in sorted((kit / "schemas").glob("*.schema.json")):
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            schemas[path.name.removesuffix(".schema.json")] = Draft202012Validator(schema)
        except Exception as exc:  # noqa: BLE001 - report any schema problem
            errors.append(f"{path.relative_to(root)}: invalid schema: {exc}")

    examples = sorted((kit / "schemas" / "examples").glob("*.json"))
    examples.append(kit / "bots" / "example-metrics.json")
    for path in examples:
        if not path.exists():
            continue
        rel = path.relative_to(root)
        name = "metrics" if path.name == "example-metrics.json" else path.name.split(".")[0]
        expect_valid = ".invalid" not in path.name
        validator = schemas.get(name)
        if validator is None:
            errors.append(f"{rel}: no schema '{name}.schema.json' for this example")
            continue
        problems = list(validator.iter_errors(json.loads(path.read_text(encoding="utf-8"))))
        if expect_valid and problems:
            errors.append(f"{rel}: should be valid: {problems[0].message}")
        if not expect_valid and not problems:
            errors.append(f"{rel}: should be invalid but passes {name}.schema.json")


DECISION_ID = re.compile(r"\bAQEF-\d{3}\b")
DECISION_KEYS = ("id", "title", "status", "scope", "date", "applies_to")
LIVE = {"proposed", "accepted"}


def repo_text_files(root, kit):
    """Files that may state or cite a decision."""
    files = [root / name for name in ("README.md", "CHANGELOG.md", "CONTRIBUTING.md", "ROADMAP.md", "AGENTS.md", "CLAUDE.md")]
    files += list((root / "docs").rglob("*.md"))
    files += [p for p in kit.rglob("*") if p.suffix in (".md", ".yaml", ".yml", ".py", ".json")]
    return sorted(p for p in files if p.is_file())


def check_decisions(errors, root, kit):
    folder = root / "docs" / "decisions"
    decisions = {}
    for path in sorted(folder.glob("AQEF-*.md")):
        rel = path.relative_to(root)
        fm = front_matter(path) or {}
        for key in DECISION_KEYS:
            if not fm.get(key) and key != "applies_to":
                errors.append(f"{rel}: decision has no '{key}'")
        did = fm.get("id")
        if not did:
            continue
        if not path.name.startswith(f"{did}-"):
            errors.append(f"{rel}: file name does not start with its id '{did}'")
        if did in decisions:
            errors.append(f"{rel}: duplicate decision id '{did}'")
        if fm.get("status") not in LIVE | {"superseded", "retired"}:
            errors.append(f"{rel}: status must be proposed, accepted, superseded or retired")
        if fm.get("scope") not in ("phase", "permanent"):
            errors.append(f"{rel}: scope must be phase or permanent")
        decisions[did] = (path, fm)

    texts = {p: p.read_text(encoding="utf-8") for p in repo_text_files(root, kit)}
    decision_files = {path for path, _ in decisions.values()}
    for did, (path, fm) in decisions.items():
        for target in fm.get("applies_to") or []:
            target_path = root / target
            if not target_path.is_file():
                errors.append(f"{path.relative_to(root)}: applies_to '{target}' does not exist")
            elif fm.get("status") in LIVE and did not in target_path.read_text(encoding="utf-8"):
                errors.append(f"{target}: states decision {did} but does not cite it")
        for phrase in fm.get("retired_wording") or []:
            for file, text in texts.items():
                if file in decision_files or file.name == "CHANGELOG.md":
                    continue
                if phrase in text:
                    errors.append(f"{file.relative_to(root)}: contains retired wording of {did}: '{phrase}'")

    for file, text in texts.items():
        if file.parent == folder:
            continue  # decision files and the index may cite any decision
        for did in sorted(set(DECISION_ID.findall(text))):
            if did not in decisions:
                errors.append(f"{file.relative_to(root)}: cites unknown decision {did}")
            elif decisions[did][1].get("status") not in LIVE:
                errors.append(f"{file.relative_to(root)}: cites {did}, which is {decisions[did][1]['status']}")


def check(root=ROOT):
    kit = root / "aqef-kit"
    errors = []
    config = yaml.safe_load((kit / ".aqef" / "config.yaml").read_text(encoding="utf-8"))
    agent_names = check_agents_and_skills(errors, root, kit, config)
    check_config(errors, kit, config, agent_names)
    check_kb(errors, root, kit)
    check_links(errors, root, kit)
    check_schemas(errors, root, kit)
    check_decisions(errors, root, kit)
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description="AQEF kit consistency check")
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root that holds aqef-kit/")
    args = parser.parse_args(argv)
    errors = check(args.root.resolve())
    for error in errors:
        print(f"FAIL {error}")
    print(f"AQEF kit check: {'clean' if not errors else f'{len(errors)} problem(s)'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
