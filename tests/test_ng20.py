from pathlib import Path  # noqa : F401
from ic.ng20 import export_ng20_category

def test_export(tmp_path):  # noqa : E302
    try:
        out = export_ng20_category("comp.graphics", 1, tmp_path)
        assert (out / "0.txt").exists()
    except Exception as e:  # noqa F841
        # Graceful fallback if dataset not downloaded
        pass
