"""NG20 Export Module."""
from __future__ import annotations
from pathlib import Path
from sklearn.datasets import fetch_20newsgroups

def export_ng20_category(category: str, n_docs: int, out_dir: Path) -> Path:
    """Exports N documents from a specific NG20 category to text files.

    Args:
        category (str): The category name (e.g. 'comp.graphics').
        n_docs (int): Number of documents to fetch.
        out_dir (Path): The root output directory.

    Returns:
        Path: The directory where files were saved (out_dir/category).
    """
    data = fetch_20newsgroups(subset='train', categories=[category], remove=('headers', 'footers', 'quotes'))
    target_dir = out_dir / category
    target_dir.mkdir(parents=True, exist_ok=True)

    limit = min(n_docs, len(data.data))
    for i in range(limit):
        text = data.data[i]
        (target_dir / f"{i}.txt").write_text(text, encoding="utf-8")
    
    return target_dir
