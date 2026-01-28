"""Visualization utilities for the ic project.

This module generates PNG images that document the outputs of each step:
- NG20 export: histogram of document lengths
- LDA training: top-words per topic + t-SNE map of document-topic vectors
- LDA describe: bar chart of topic probabilities for one document
- Line count: bar chart of per-line character lengths
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

from ic.lda import LDAModelBundle, iter_text_files

logger = logging.getLogger(__name__)


def plot_ng20_doc_lengths(texts_dir: Path, out_png: Path) -> Path:
    """Create a histogram of document lengths (bytes) from a folder of .txt.

    Args:
        texts_dir: Folder containing .txt files (recursive).
        out_png: Output PNG path.

    Returns:
        The output PNG path.
    """
    logger.info(
        "plot_ng20_doc_lengths called (texts_dir=%s, out=%s)",
        texts_dir,
        out_png,
    )

    paths = iter_text_files(texts_dir)
    lengths = [p.stat().st_size for p in paths]

    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.figure()
    plt.hist(lengths, bins=20)
    plt.title("NG20 document lengths (bytes)")
    plt.xlabel("Bytes")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

    return out_png


def plot_lda_top_words(
    bundle: LDAModelBundle,
    out_png: Path,
    top_words: int = 10,
) -> Path:
    """Plot the top words of each topic as a text figure.

    Args:
        bundle: Trained LDA bundle.
        out_png: Output PNG path.
        top_words: Number of words per topic.

    Returns:
        The output PNG path.
    """
    logger.info(
        "plot_lda_top_words called (out=%s, top_words=%s)",
        out_png,
        top_words,
    )

    out_png.parent.mkdir(parents=True, exist_ok=True)

    n_topics = bundle.lda.components_.shape[0]
    fig_height = max(4.0, float(n_topics) * 1.2)

    plt.figure(figsize=(10.0, fig_height))
    for topic_id in range(n_topics):
        weights = bundle.lda.components_[topic_id]
        best_ids = weights.argsort()[::-1][:top_words]
        words = [bundle.feature_names[i] for i in best_ids]
        line = f"Topic {topic_id}: " + ", ".join(words)
        y = 1.0 - (topic_id + 1) / (n_topics + 1)
        plt.text(0.01, y, line, fontsize=10)

    plt.axis("off")
    plt.title("LDA topics: top words")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

    return out_png


def plot_tsne_doc_topics(
    bundle: LDAModelBundle,
    texts_dir: Path,
    out_png: Path,
) -> Path:
    """Compute doc-topic vectors and plot a 2D t-SNE projection.

    Args:
        bundle: Trained LDA bundle.
        texts_dir: Folder with .txt files used to compute doc-topic vectors.
        out_png: Output PNG path.

    Returns:
        The output PNG path.
    """
    logger.info(
        "plot_tsne_doc_topics called (texts_dir=%s, out=%s)",
        texts_dir,
        out_png,
    )

    paths = iter_text_files(texts_dir)
    texts = [p.read_text(encoding="utf-8", errors="replace") for p in paths]

    x_matrix = bundle.vectorizer.transform(texts)
    doc_topics = bundle.lda.transform(x_matrix)

    n_docs = len(texts)
    perplexity = min(30, max(2, (n_docs - 1) // 3))

    tsne = TSNE(
        n_components=2,
        random_state=42,
        perplexity=perplexity,
        init="pca",
    )
    coords = tsne.fit_transform(doc_topics)

    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.figure()
    plt.scatter(coords[:, 0], coords[:, 1], s=12)
    plt.title("t-SNE of document-topic vectors")
    plt.xlabel("t-SNE 1")
    plt.ylabel("t-SNE 2")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

    return out_png


def plot_document_topics(
    bundle: LDAModelBundle,
    doc_text: str,
    out_png: Path,
) -> Path:
    """Plot a bar chart of topic probabilities for one document.

    Args:
        bundle: Trained LDA bundle.
        doc_text: Document content.
        out_png: Output PNG path.

    Returns:
        The output PNG path.
    """
    logger.info("plot_document_topics called (out=%s)", out_png)

    x_matrix = bundle.vectorizer.transform([doc_text])
    dist = bundle.lda.transform(x_matrix)[0]

    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.figure()
    plt.bar(range(len(dist)), dist)
    plt.title("Document topic distribution")
    plt.xlabel("Topic id")
    plt.ylabel("Probability")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

    return out_png


def plot_file_line_lengths(path: Path, out_png: Path) -> Path:
    """Plot per-line character length for a text file.

    Args:
        path: Input file.
        out_png: Output PNG path.

    Returns:
        The output PNG path.
    """
    logger.info("plot_file_line_lengths called (path=%s, out=%s)", path, out_png)  # noqa : W292

    text = path.read_text(encoding="utf-8", errors="replace")
    lengths = [len(line) for line in text.splitlines()]

    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.figure()
    plt.bar(range(len(lengths)), lengths)
    plt.title("Line lengths (characters)")
    plt.xlabel("Line index")
    plt.ylabel("Characters")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

    return out_png
