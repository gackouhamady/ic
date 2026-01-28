"""LDA Modeling Module."""
from __future__ import annotations
import pickle
from dataclasses import dataclass
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

@dataclass
class LDAModelBundle:
    """Holds the trained vectorizer, LDA model, and feature names."""
    vectorizer: CountVectorizer
    lda: LatentDirichletAllocation
    feature_names: list[str]

def train_lda_from_folder(folder: Path, n_topics: int = 10) -> LDAModelBundle:
    """Trains an LDA model on all .txt files found recursively in folder.

    Args:
        folder (Path): Root folder to search for .txt files.
        n_topics (int): Number of topics to extract.

    Returns:
        LDAModelBundle: The trained model bundle.
    """
    files = sorted(folder.rglob("*.txt"))
    if not files:
        raise FileNotFoundError(f"No .txt files found in {folder}")

    texts = [f.read_text(encoding="utf-8", errors="replace") for f in files]
    
    vec = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    X = vec.fit_transform(texts)
    
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)
    
    return LDAModelBundle(vec, lda, vec.get_feature_names_out())

def save_model(bundle: LDAModelBundle, path: Path) -> None:
    """Saves the model bundle to a pickle file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(bundle, f)

def load_model(path: Path) -> LDAModelBundle:
    """Loads a model bundle from a pickle file."""
    with open(path, "rb") as f:
        return pickle.load(f)

def describe_document(bundle: LDAModelBundle, text: str, top_topics: int = 3, n_words: int = 5) -> list[tuple[int, list[str]]]:
    """Infers topics for a document and returns top keywords.

    Args:
        bundle (LDAModelBundle): The trained model.
        text (str): The document text.
        top_topics (int): Number of top topics to return.
        n_words (int): Number of words to list per topic.

    Returns:
        list[tuple[int, list[str]]]: List of (topic_index, [word1, word2...]).
    """
    X = bundle.vectorizer.transform([text])
    topic_dist = bundle.lda.transform(X)[0]
    
    # Get indices of top topics sorted by weight
    top_topic_indices = topic_dist.argsort()[::-1][:top_topics]
    
    result = []
    for topic_idx in top_topic_indices:
        topic = bundle.lda.components_[topic_idx]
        top_word_indices = topic.argsort()[::-1][:n_words]
        words = [bundle.feature_names[i] for i in top_word_indices]
        result.append((topic_idx, words))
        
    return result
