import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from check_kit import check  # noqa: E402


def test_kit_is_consistent():
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_kit.py")],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout


@pytest.fixture
def kit_copy(tmp_path):
    copy = tmp_path / "repo"
    shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(
        ".git", ".ai", ".pytest_cache", "__pycache__", ".venv", "venv", "*.zip"))
    return copy


def edit(path, old, new):
    text = path.read_text(encoding="utf-8")
    assert old in text, f"fixture text not found in {path.name}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def test_copy_is_clean(kit_copy):
    assert check(kit_copy) == []


@pytest.mark.parametrize("file, old, new, expected", [
    ("agents/test-review-panel.md", "tools: Read, Grep, Glob, Write", "tools: Read, Grep, Glob, Write, Bash",
     "report agent must not have the Bash tool"),
    ("agents/report-analyst.md", 'writes: ["reports/**"]', 'writes: ["src/**"]',
     "report agent writes outside report folders"),
    ("agents/automation-engineer.md", "commands: [unit, integration, api, ui, by_tags]", "commands: [deploy]",
     "command 'deploy' is not defined"),
    ("agents/test-fixer.md", "commands: [by_tags]\n", "",
     "has Bash but no 'commands' allow-list"),
    ("agents/spec-critic.md", "kind: report\n", "",
     "front matter has no 'kind'"),
    (".aqef/config.yaml", "on_escalate: follow_up", "on_escalate: sometimes",
     "config: tiers/t2/on_escalate"),
    (".aqef/config.yaml", "  ui_share_max: 0.10", "  ui_shar_max: 0.10",
     "config: suite_rules"),
    ("schemas/config.schema.json", '"on_escalate": {"enum": ["block", "follow_up", "comment"], "x-aqef-enforced-by": "gatekeeper"}',
     '"on_escalate": {"enum": ["block", "follow_up", "comment"]}', "on_escalate has no valid x-aqef-enforced-by"),
    ("schemas/examples/test-result.invalid-level-nfr.json", '"level": "nfr"', '"level": "api"',
     "should be invalid"),
    ("bots/example-metrics.json", '"criteria_coverage": 1.0', '"criteria_coverage": "high"',
     "example-metrics.json: should be valid"),
    ("domain/rules/REF-001-refund-window.md", "relates_to: [", "relates_to: [no.such.id, ",
     "relates_to 'no.such.id' does not exist"),
])
def test_check_catches_problem(kit_copy, file, old, new, expected):
    edit(kit_copy / "aqef-kit" / file, old, new)
    errors = check(kit_copy)
    assert any(expected in e for e in errors), errors


# --- Decisions --------------------------------------------------------------------

D1 = "docs/decisions/AQEF-001-session-first.md"


@pytest.mark.parametrize("file, old, new, expected", [
    ("aqef-kit/skills/aqef-triage/SKILL.md", "no API key is needed (AQEF-001)", "no API key is needed",
     "aqef-kit/skills/aqef-triage/SKILL.md: states decision AQEF-001 but does not cite it"),
    ("aqef-kit/gates/human-gates.md", "(AQEF-002)", "(AQEF-099)",
     "cites unknown decision AQEF-099"),
    (D1, "status: accepted", "status: superseded",
     "cites AQEF-001, which is superseded"),
    ("docs/AQEF.md", "## Core principles", "Triage runs after every post-deploy run.\n\n## Core principles",
     "contains retired wording of AQEF-001: 'after every post-deploy run'"),
    (D1, "  - README.md\n", "  - README.md\n  - no/such/file.md\n",
     "applies_to 'no/such/file.md' does not exist"),
    (D1, "scope: phase", "scope: forever",
     "scope must be phase or permanent"),
    (D1, "id: AQEF-001", "id: AQEF-002",
     "duplicate decision id 'AQEF-002'"),
])
def test_check_catches_decision_problem(kit_copy, file, old, new, expected):
    edit(kit_copy / file, old, new)
    errors = check(kit_copy)
    assert any(expected in e for e in errors), errors


def test_retired_wording_is_allowed_in_the_changelog(kit_copy):
    path = kit_copy / "CHANGELOG.md"
    path.write_text(path.read_text(encoding="utf-8") + "\n- Removed: triage after every post-deploy run.\n", encoding="utf-8")
    assert check(kit_copy) == []
