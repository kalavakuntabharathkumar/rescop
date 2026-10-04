from dataclasses import dataclass, asdict
from threading import RLock
from typing import Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class Document:
    id: int
    title: str
    text: str
    source: str

class DocumentStore:
    def __init__(self):
        self._docs: list[Document] = []
        self._next_id = 1
        self._lock = RLock()

    def add(self, title: str, text: str, source: str = "manual") -> dict[str, Any]:
        with self._lock:
            doc = Document(self._next_id, title, text, source)
            self._next_id += 1
            self._docs.append(doc)
            return asdict(doc)

    def all(self) -> list[Document]:
        with self._lock:
            return list(self._docs)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        docs = self.all()
        if not docs:
            return []
        corpus = [d.title + " " + d.text for d in docs]
        vectorizer = TfidfVectorizer(stop_words="english", max_features=50000)
        matrix = vectorizer.fit_transform(corpus + [query])
        scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
        ranked = sorted(zip(docs, scores), key=lambda pair: float(pair[1]), reverse=True)[:top_k]
        return [
            {"id": d.id, "title": d.title, "source": d.source, "score": round(float(score), 4),
             "snippet": d.text[:360] + ("…" if len(d.text) > 360 else "")}
            for d, score in ranked if score > 0
        ]

store = DocumentStore()
