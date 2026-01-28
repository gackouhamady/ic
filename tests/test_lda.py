from pathlib import Path
from ic.lda import train_lda_from_folder, LDAModelBundle

def test_train(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    (d / "1.txt").write_text("apple banana fruit", encoding="utf-8")
    (d / "2.txt").write_text("apple orange juice", encoding="utf-8")
    
    bundle = train_lda_from_folder(d, n_topics=2)
    assert isinstance(bundle, LDAModelBundle)
    assert len(bundle.feature_names) > 0
