#!/usr/bin/env python3
"""AQEF Test Guard.

Blocks diffs that make tests weaker, so that no agent (or person) gets a green build by
changing the tests instead of the code (principle P8).

Rules, checked per changed test file:
  deleted_test_file   a test file is deleted
  removed_tests       the file has fewer test definitions than before
  removed_assertions  the file has fewer assertions than before
  added_skip          a skip, ignore, disable or focus marker is added
  added_retry         a retry or rerun setting is added

Language-neutral: the patterns cover pytest, unittest, JUnit, TestNG, Kotlin, NUnit, xUnit,
MSTest, Jest, Vitest, Mocha, Playwright, Cypress, Go and Gherkin.

A violation can be waived in the waivers file (`test_guard.waivers` in .aqef/config.yaml):

  - path: tests/test_old_api.py
    rule: deleted_test_file
    reason: API v1 removed in SPEC-201
    approved_by: jane.doe

Waived violations are reported separately; the gatekeeper asks a human to confirm them.
Protect the waivers file with CODEOWNERS so an agent cannot approve its own waiver.

Exit codes: 0 clean (or all waived), 1 violations, 3 bad input.
"""
import argparse
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_INCLUDE = ["test_*.py", "*_test.py", "*.test.*", "*.spec.*", "*Test.java", "*Tests.java",
                   "*Test.kt", "*Test.cs", "*Tests.cs", "*_test.go", "*.feature",
                   "tests/*", "test/*", "*/tests/*", "*/test/*", "*/__tests__/*"]

TEST_DEF = re.compile(
    r"^\s*(async\s+)?def\s+test\w*\s*\("          # pytest, unittest
    r"|@(Test|ParameterizedTest|RepeatedTest|TestFactory)\b"  # JUnit, TestNG, Kotlin
    r"|\[(Test|TestCase|Fact|Theory|TestMethod)\b"  # NUnit, xUnit, MSTest
    r"|(^|[^.\w])(it|test)(\.each\([^)]*\))?\s*\(\s*['\"`]"  # Jest, Vitest, Mocha, Playwright
    r"|^func\s+Test\w*\s*\("                      # Go
    r"|^\s*Scenario( Outline)?:"                  # Gherkin
)
ASSERTION = re.compile(
    r"\bassert\w*"                       # assert, assertEqual, assertThat, assert_called
    r"|\bexpect\s*\("                    # Jest, Vitest, Playwright
    r"|\.should\s*\("                    # Cypress, Chai
    r"|\bAssert\.\w+|\bAssertions\.\w+"   # NUnit, MSTest, JUnit
    r"|\brequire\.\w+\s*\("              # Go testify
    r"|\bt\.(Error|Errorf|Fatal|Fatalf|Fail)\b"  # Go testing
    r"|^\s*Then\b"                       # Gherkin
)
SKIP = re.compile(
    r"@pytest\.mark\.(skip|skipif|xfail)\b|\bpytest\.skip\s*\(|@unittest\.skip"
    r"|@Disabled\b|@Ignore\b|\[Ignore\b|Skip\s*="
    r"|\b(it|test|describe)\.(skip|only|fixme)\s*\(|\bx(it|test|describe)\s*\(|\bf(it|describe)\s*\("
    r"|\bt\.Skip(Now|f)?\s*\("
    r"|^\s*@(skip|ignore|wip|disabled)\b"
)
RETRY = re.compile(
    r"@pytest\.mark\.flaky\b|@flaky\b|--reruns\b|\breruns\s*="
    r"|\bretries\s*[:=]\s*[1-9]|\.retries\s*\(\s*[1-9]|@RetryingTest\b|@Retry\b|\[Retry\b"
)


def is_test_file(path, include):
    name = path.rsplit("/", 1)[-1]
    return any(fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(name, pat) for pat in include)


def parse_diff(diff_text):
    """Map file path -> (removed lines, added lines) from a unified diff."""
    files, old, current, in_hunk = {}, None, None, False
    for line in diff_text.splitlines():
        if line.startswith("diff --git "):
            old, current, in_hunk = None, None, False
        elif not in_hunk and line.startswith("--- "):
            name = line[4:].strip()
            old = name[2:] if name.startswith("a/") else None
        elif not in_hunk and line.startswith("+++ "):
            name = line[4:].strip()
            current = files.setdefault(name[2:] if name.startswith("b/") else old, ([], []))
        elif line.startswith("@@"):
            in_hunk = current is not None
        elif in_hunk and line[:1] in ("+", "-"):
            current[0 if line[0] == "-" else 1].append(line[1:])
    return files


def count(pattern, lines):
    return sum(1 for line in lines if pattern.search(line))


def analyze(diff_text, deleted_paths, include=None):
    """Return the list of violations for a diff. Pure: no git, no files."""
    include = include or DEFAULT_INCLUDE
    violations = []
    for path in sorted(deleted_paths):
        if is_test_file(path, include):
            violations.append({"path": path, "rule": "deleted_test_file", "detail": "test file deleted"})
    for path, (removed, added) in sorted(parse_diff(diff_text).items()):
        if path in deleted_paths or not is_test_file(path, include):
            continue
        for rule, pattern, label in (("removed_tests", TEST_DEF, "test definitions"),
                                     ("removed_assertions", ASSERTION, "assertions")):
            before, after = count(pattern, removed), count(pattern, added)
            if after < before:
                violations.append({"path": path, "rule": rule,
                                   "detail": f"{before - after} fewer {label} ({before} removed, {after} added)"})
        for rule, pattern in (("added_skip", SKIP), ("added_retry", RETRY)):
            net = count(pattern, added) - count(pattern, removed)
            if net > 0:
                violations.append({"path": path, "rule": rule, "detail": f"{net} added"})
    return violations


def apply_waivers(violations, waivers):
    valid = [w for w in waivers or [] if w.get("path") and w.get("rule") and w.get("reason") and w.get("approved_by")]
    open_, waived = [], []
    for v in violations:
        match = next((w for w in valid if w["path"] == v["path"] and w["rule"] == v["rule"]), None)
        (waived if match else open_).append({**v, **({"waiver": match} if match else {})})
    return open_, waived


def git(*args, cwd=None):
    proc = subprocess.run(["git", *args], capture_output=True, text=True, cwd=cwd)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def run(base, head="HEAD", config_path=".aqef/config.yaml", cwd=None):
    import yaml

    config = {}
    if Path(cwd or ".", config_path).exists():
        config = yaml.safe_load(Path(cwd or ".", config_path).read_text(encoding="utf-8")) or {}
    guard = config.get("test_guard", {})
    include = guard.get("include") or DEFAULT_INCLUDE
    waivers_path = Path(cwd or ".", guard.get("waivers", ".aqef/test-guard-waivers.yaml"))
    waivers = (yaml.safe_load(waivers_path.read_text(encoding="utf-8")) or []) if waivers_path.exists() else []
    if not isinstance(waivers, list):
        raise ValueError(f"{waivers_path} must be a YAML list of waivers")

    span = f"{base}...{head}"
    status = git("diff", "--name-status", "--find-renames", span, cwd=cwd)
    deleted = {line.split("\t")[1] for line in status.splitlines() if line.startswith("D\t")}
    diff = git("diff", "--unified=0", "--find-renames", span, cwd=cwd)
    open_, waived = apply_waivers(analyze(diff, deleted, include), waivers)
    return {"base": base, "head": head, "test_guard_violations": len(open_),
            "test_guard_waived": len(waived), "violations": open_, "waived": waived}


def main(argv=None):
    parser = argparse.ArgumentParser(description="AQEF Test Guard")
    parser.add_argument("--base", required=True, help="base ref, for example origin/main")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--config", default=".aqef/config.yaml")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        res = run(args.base, args.head, args.config)
    except Exception as exc:  # noqa: BLE001 - any input problem is exit 3, never a silent pass
        print(f"AQEF test guard: ERROR\n  - {exc}")
        return 3
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"AQEF test guard: {res['test_guard_violations']} violation(s), {res['test_guard_waived']} waived")
        for v in res["violations"]:
            print(f"  - {v['path']}: {v['rule']} ({v['detail']})")
        for v in res["waived"]:
            print(f"  waived: {v['path']}: {v['rule']} by {v['waiver']['approved_by']}: {v['waiver']['reason']}")
    return 1 if res["test_guard_violations"] else 0


if __name__ == "__main__":
    sys.exit(main())
