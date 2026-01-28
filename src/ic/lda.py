"""LDA Modeling Module."""

from __future__ import annotations

import pickle
from dataclasses import dataclass
from pathlib import Path

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


@dataclass
class LDAModelBundle:
    """Holds the trained vectorizer, LDA model, and feature names."""

    vectorizer: CountVectorizer
    lda: LatentDirichletAllocation
    feature_names: list[str]


def train_lda_from_folder(folder: Path, n_topics: int = 10) -> LDAModelBundle:  # noqa : E501
    """Trains an LDA model on all .txt files found recursively in folder.

    Args:
        folder (Path): Root folder to search for .txt files.
        n_topics (int): Number of topics to extract.

    Returns:
        LDAModelBundle: The trained model bundle.

    Raises:
        FileNotFoundError: If no .txt files are found in the folder.
        ValueError: If n_topics is not a positive integer.
    """
    if n_topics <= 0:
        raise ValueError("n_topics must be > 0")

    files = sorted([p for p in folder.rglob("*.txt") if p.is_file()])
    if not files:
        raise FileNotFoundError(f"No .txt files found in {folder}")

    texts = [f.read_text(encoding="utf-8", errors="replace") for f in files]

    n_docs = len(texts)
    max_df = 0.95
    max_doc_count = int(max_df * n_docs)

    min_df = 2 if max_doc_count >= 2 else 1

    vec = CountVectorizer(max_df=max_df, min_df=min_df, stop_words="english")
    x_matrix = vec.fit_transform(texts)

    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(x_matrix)

    return LDAModelBundle(
        vectorizer=vec,
        lda=lda,
        feature_names=list(vec.get_feature_names_out()),
    )


def save_model(bundle: LDAModelBundle, path: Path) -> None:  # noqa : E501
    """Saves the model bundle to a pickle file.

    Args:
        bundle (LDAModelBundle): Model bundle to save.
        path (Path): Output pickle path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as file_obj:
        pickle.dump(bundle, file_obj)


def load_model(path: Path) -> LDAModelBundle:
    """Loads a model bundle from a pickle file.

    Args:
        path (Path): Input pickle path.

    Returns:
        LDAModelBundle: Loaded model bundle.
    """
    with path.open("rb") as file_obj:
        return pickle.load(file_obj)


def describe_document(
    bundle: LDAModelBundle,
    text: str,
    top_topics: int = 3,
    n_words: int = 5,
) -> list[tuple[int, list[str]]]:  # noqa : E501
    """Infers topics for a document and returns top keywords.

    Args:
        bundle (LDAModelBundle): The trained model.
        text (str): The document text.
        top_topics (int): Number of top topics to return.
        n_words (int): Number of words to list per topic.

    Returns:
        list[tuple[int, list[str]]]: List of (topic_index, [word1, word2...]).

    Raises:
        ValueError: If top_topics or n_words is not positive.
    """
    if top_topics <= 0:
        raise ValueError("top_topics must be > 0")
    if n_words <= 0:
        raise ValueError("n_words must be > 0")

    x_matrix = bundle.vectorizer.transform([text])
    topic_dist = bundle.lda.transform(x_matrix)[0]

    # Get indices of top topics sorted by weight
    top_topic_indices = topic_dist.argsort()[::-1][:top_topics]

    result: list[tuple[int, list[str]]] = []
    for topic_idx in top_topic_indices:
        topic = bundle.lda.components_[topic_idx]
        top_word_indices = topic.argsort()[::-1][:n_words]
        words = [bundle.feature_names[i] for i in top_word_indices]
        result.append((int(topic_idx), words))

    return result
