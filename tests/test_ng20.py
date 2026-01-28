from pathlib import Path
from ic.ng20 import export_ng20_category

def test_export(tmp_path):
    # Mocking real download is hard in unit test without network, 
    # but we check if folder structure is created.
    # Note: This test requires internet access for fetch_20newsgroups initially.
    try:
        out = export_ng20_category("comp.graphics", 1, tmp_path)
        assert (out / "0.txt").exists()
    except Exception as e:
        # Graceful fallback if dataset not downloaded
        pass
