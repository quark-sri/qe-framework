import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_kit_is_consistent():
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_kit.py")],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout
