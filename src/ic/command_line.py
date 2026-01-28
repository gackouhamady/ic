"""CLI Entry Points."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from ic.lda import describe_document, load_model, save_model, train_lda_from_folder  ## noqa : E501
from ic.linecount import count_lines_in_file
from ic.logging_config import configure_logging
from ic.ng20 import export_ng20_category
from ic.visualization import (
    plot_document_topics,
    plot_file_line_lengths,
    plot_lda_top_words,
    plot_ng20_doc_lengths,
    plot_tsne_doc_topics,
)

logger = logging.getLogger(__name__)


def ng20_export_app() -> None:  # noqa : E302
    """Export NG20 category documents to text files."""
    configure_logging("INFO")

    parser = argparse.ArgumentParser(
        description="Export NG20 category to text files.",
    )  # noqa : E501
    parser.add_argument(
        "--category",
        required=True,
        help="Category name (e.g. comp.graphics)",
    )  # noqa : E501
    parser.add_argument("--n", type=int, required=True, help="Number of docs")
    parser.add_argument("--out", required=True, help="Output folder")
    args = parser.parse_args()

    target_dir = export_ng20_category(args.category, args.n, Path(args.out))
    logger.info("Exported NG20 docs to %s", target_dir)
    print(f"Exported to {target_dir}")

    plot_ng20_doc_lengths(target_dir, target_dir / "doc_lengths.png")


def lda_train_app() -> None:  # noqa : E302
    """Train LDA model from folder and save it as pickle."""
    configure_logging("INFO")

    parser = argparse.ArgumentParser(description="Train LDA model from folder.")  # noqa : E501
    parser.add_argument(
        "--texts",
        required=True,
        help="Input folder with .txt files",
    )  # noqa : E501
    parser.add_argument(
        "--model-out",
        required=True,
        help="Output pickle path",
    )  # noqa : E501
    parser.add_argument(
        "--topics",
        type=int,
        default=10,
        help="Number of topics",
    )  # noqa : E501
    args = parser.parse_args()

    texts_dir = Path(args.texts)
    model_path = Path(args.model_out)

    bundle = train_lda_from_folder(texts_dir, n_topics=args.topics)
    save_model(bundle, model_path)
    logger.info("Model saved to %s", model_path)
    print(f"Model saved to {model_path}")

    out_dir = model_path.parent
    plot_lda_top_words(bundle, out_dir / "lda_topics.png", top_words=10)
    plot_tsne_doc_topics(bundle, texts_dir, out_dir / "lda_tsne.png")


def lda_describe_app() -> None:  # noqa : E302
    """Describe a document using a trained LDA model."""
    configure_logging("INFO")

    parser = argparse.ArgumentParser(
        description="Describe document using trained LDA.",
    )  # noqa : E501
    parser.add_argument(
        "--model",
        required=True,
        help="Path to model pickle",
    )  # noqa : E501
    parser.add_argument(
        "--doc",
        required=True,
        help="Path to document .txt",
    )  # noqa : E501
    args = parser.parse_args()

    model_path = Path(args.model)
    doc_path = Path(args.doc)

    bundle = load_model(model_path)
    doc_text = doc_path.read_text(encoding="utf-8", errors="replace")

    desc = describe_document(bundle, doc_text)
    print(f"--- Document: {doc_path} ---")
    for topic_id, words in desc:
        print(f"Topic {topic_id}: {', '.join(words)}")

    plot_document_topics(bundle, doc_text, doc_path.with_suffix(".topics.png"))


def count_lines_app() -> None:  # noqa : E302
    """Count number of lines in a file and print it."""
    configure_logging("INFO")

    parser = argparse.ArgumentParser(
        description="Count number of lines in a file.",
    )  # noqa : E501
    parser.add_argument(
        "--file",
        required=True,
        help="Path to input file",
    )  # noqa : E501
    args = parser.parse_args()

    file_path = Path(args.file)
    n_lines = count_lines_in_file(file_path)
    print(n_lines)

    plot_file_line_lengths(file_path, file_path.with_suffix(".lines.png"))
