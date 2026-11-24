import json
import subprocess
import sys
from pathlib import Path

import pytest

KIT = Path(__file__).resolve().parent.parent / "aqef-kit"
sys.path.insert(0, str(KIT / "bots"))
from testguard import analyze, apply_waivers, is_test_file, parse_diff  # noqa: E402


def diff(path, removed=(), added=()):
    body = "".join(f"-{line}\n" for line in removed) + "".join(f"+{line}\n" for line in added)
    return f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n@@ -1,{len(removed)} +1,{len(added)} @@\n{body}"


def rules(violations):
    return sorted(v["rule"] for v in violations)


# --- Which files are tests ------------------------------------------------------

@pytest.mark.parametrize("path, expected", [
    ("tests/test_refund.py", True),
    ("src/refund/refund_test.go", True),
    ("web/refund.spec.ts", True),
    ("web/__tests__/refund.tsx", True),
    ("src/test/java/RefundServiceTest.java", True),
    ("features/payments/refund.feature", True),
    ("src/refund/service.py", False),
    ("src/main/java/RefundService.java", False),
])
def test_is_test_file(path, expected):
    from testguard import DEFAULT_INCLUDE
    assert is_test_file(path, DEFAULT_INCLUDE) is expected


# --- Rules --------------------------------------------------------------------

def test_deleted_test_file():
    assert rules(analyze("", {"tests/test_refund.py"})) == ["deleted_test_file"]


def test_deleted_production_file_is_ignored():
    assert analyze("", {"src/refund.py"}) == []


def test_changes_to_production_code_are_ignored():
    d = diff("src/refund.py", removed=["    assert amount > 0"], added=[])
    assert analyze(d, set()) == []


@pytest.mark.parametrize("path, removed", [
    ("tests/test_refund.py", ["def test_rejects_late_refund():"]),
    ("web/refund.spec.ts", ["test('rejects late refund', async () => {"]),
    ("src/test/java/RefundTest.java", ["    @Test"]),
    ("refund_test.go", ["func TestRejectsLateRefund(t *testing.T) {"]),
    ("features/refund.feature", ["  Scenario: Refund is rejected after the window"]),
])
def test_removed_test_definition(path, removed):
    assert "removed_tests" in rules(analyze(diff(path, removed=removed), set()))


@pytest.mark.parametrize("removed, added", [
    (["    assert refund.status == 'REJECTED'"], []),
    (["  expect(res.status).toBe(422);"], ["  // expect removed"]),
    (["    assertThat(refund.amount()).isEqualTo(10);"], []),
    (["    Then the refund is rejected"], []),
])
def test_removed_assertion(removed, added):
    assert rules(analyze(diff("tests/test_refund.py", removed, added), set())) == ["removed_assertions"]


def test_rewritten_assertion_is_not_a_violation():
    d = diff("tests/test_refund.py", removed=["    assert total == 10"], added=["    assert total == Decimal('10.00')"])
    assert analyze(d, set()) == []


def test_moved_test_is_not_a_violation():
    lines = ["def test_rejects_late_refund():", "    assert refund.rejected"]
    assert analyze(diff("tests/test_refund.py", removed=lines, added=lines), set()) == []


@pytest.mark.parametrize("added", [
    "@pytest.mark.skip(reason='later')",
    "    pytest.skip('flaky')",
    "  @Disabled",
    "test.skip('rejects late refund', async () => {",
    "it.only('focus', () => {",
    "xit('rejects late refund', () => {",
    "    t.Skip(\"later\")",
    "  @skip",
])
def test_added_skip(added):
    assert "added_skip" in rules(analyze(diff("tests/test_refund.py", added=[added]), set()))


@pytest.mark.parametrize("added", [
    "@pytest.mark.flaky(reruns=3)",
    "  retries: 2,",
    "test.describe.configure({ retries: 3 });",
    "  @RetryingTest(3)",
])
def test_added_retry(added):
    assert "added_retry" in rules(analyze(diff("tests/test_refund.py", added=[added]), set()))


def test_removing_a_skip_is_fine():
    assert analyze(diff("tests/test_refund.py", removed=["@pytest.mark.skip"]), set()) == []


def test_removed_sql_comment_line_is_not_read_as_a_header():
    d = diff("tests/test_refund.py", removed=["-- seed data", "    assert x"], added=["    assert x"])
    assert parse_diff(d)["tests/test_refund.py"] == (["-- seed data", "    assert x"], ["    assert x"])
    assert analyze(d, set()) == []


# --- Waivers --------------------------------------------------------------------

def test_waiver_needs_reason_and_approver():
    violations = [{"path": "tests/test_old.py", "rule": "deleted_test_file", "detail": ""}]
    open_, waived = apply_waivers(violations, [{"path": "tests/test_old.py", "rule": "deleted_test_file"}])
    assert len(open_) == 1 and waived == []
    open_, waived = apply_waivers(violations, [{"path": "tests/test_old.py", "rule": "deleted_test_file",
                                                "reason": "API v1 removed", "approved_by": "qe-lead"}])
    assert open_ == [] and len(waived) == 1


@pytest.mark.parametrize("approver", [None, ""])
def test_proposed_waiver_with_empty_approver_still_fails(approver):
    violations = [{"path": "tests/test_old.py", "rule": "deleted_test_file", "detail": ""}]
    open_, waived = apply_waivers(violations, [{"path": "tests/test_old.py", "rule": "deleted_test_file",
                                                "reason": "API v1 removed", "approved_by": approver}])
    assert len(open_) == 1 and waived == []


# --- End to end on a real git repo ------------------------------------------------

def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                   env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
                        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
                        "HOME": str(repo), "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"})


def guard(repo, *args):
    return subprocess.run([sys.executable, str(KIT / "bots" / "testguard.py"), "--base", "main", "--json", *args],
                          capture_output=True, text=True, cwd=repo)


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, "init", "-q", "-b", "main")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_refund.py").write_text(
        "def test_late_refund_rejected():\n    assert refund(days=31) == 'REJECTED'\n\n"
        "def test_refund_accepted():\n    assert refund(days=1) == 'ACCEPTED'\n", encoding="utf-8")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-q", "-m", "base")
    git(tmp_path, "checkout", "-q", "-b", "feature")
    return tmp_path


def test_cli_clean_branch(repo):
    (repo / "src.py").write_text("x = 1\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "code only")
    proc = guard(repo)
    assert proc.returncode == 0, proc.stdout
    assert json.loads(proc.stdout)["test_guard_violations"] == 0


def test_cli_catches_a_weakened_test(repo):
    (repo / "tests" / "test_refund.py").write_text(
        "import pytest\n\n@pytest.mark.skip\ndef test_late_refund_rejected():\n    pass\n\n"
        "def test_refund_accepted():\n    assert refund(days=1) == 'ACCEPTED'\n", encoding="utf-8")
    git(repo, "commit", "-q", "-am", "weaken")
    proc = guard(repo)
    assert proc.returncode == 1
    assert rules(json.loads(proc.stdout)["violations"]) == ["added_skip", "removed_assertions"]


def test_cli_waived_deletion_passes_but_is_reported(repo):
    git(repo, "rm", "-q", "tests/test_refund.py")
    (repo / ".aqef").mkdir()
    (repo / ".aqef" / "test-guard-waivers.yaml").write_text(
        "- path: tests/test_refund.py\n  rule: deleted_test_file\n  reason: refunds retired in SPEC-300\n"
        "  approved_by: qe-lead\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "retire refunds")
    proc = guard(repo)
    out = json.loads(proc.stdout)
    assert proc.returncode == 0
    assert (out["test_guard_violations"], out["test_guard_waived"]) == (0, 1)


def test_cli_bad_base_ref_is_an_input_error(repo):
    proc = subprocess.run([sys.executable, str(KIT / "bots" / "testguard.py"), "--base", "no-such-ref"],
                          capture_output=True, text=True, cwd=repo)
    assert proc.returncode == 3
