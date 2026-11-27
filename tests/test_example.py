"""The SPEC-142 worked example is a regression test for the framework."""
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "spec-142"
KIT = ROOT / "aqef-kit"
sys.path.insert(0, str(KIT / "bots"))
from gatekeeper import decide  # noqa: E402

CONFIG = yaml.safe_load((KIT / ".aqef" / "config.yaml").read_text(encoding="utf-8"))
METRICS = json.loads((EXAMPLE / "specs" / "SPEC-142" / "metrics.json").read_text(encoding="utf-8"))


def test_example_tests_pass():
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
                          cwd=EXAMPLE, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "20 passed" in proc.stdout


def test_example_waits_for_h3_only_because_t1_always_does():
    res = decide(CONFIG, METRICS)
    assert (res["decision"], res["gates"]) == ("ESCALATE", ["H3"])
    assert res["reasons"] == ["tier t1 requires human gate H3"]
    assert res["advisories"] == ["NFR accessibility: not applicable: "
                                 "No user interface in this change (spec NFR, approved at H1)"]


def test_example_red_run_failed_every_test_the_green_run_passed():
    runs = EXAMPLE / "specs" / "SPEC-142" / "runs"
    assert "20 failed" in (runs / "1-red.txt").read_text(encoding="utf-8")
    assert "20 passed" in (runs / "2-green.txt").read_text(encoding="utf-8")
