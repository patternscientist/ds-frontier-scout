from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.stt_checker.dsk2_interface_residual import main_check_identity


if __name__ == "__main__":
    raise SystemExit(main_check_identity())
