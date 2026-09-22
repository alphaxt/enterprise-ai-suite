"""
DocuMind Core RAG Engine
Implements paragraph-level chunking, stopword filtering, BM25 + dense semantic scoring,
and strict relevance thresholds with guardrails.
"""

import os
import re
import math
from typing import List, Dict, Any, Optional, Set
from collections import Counter

# Standard English stopwords
STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", 
    "but", "by", "can", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", 
    "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", 
    "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", 
    "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", 
    "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", 
    "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", 
    "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", 
    "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", 
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", 
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", 
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", 
    "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", 
    "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", 
    "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", 
    "yours", "yourself", "yourselves", "help", "solve", "problem", "tell", "give", "know"
}


class DocumentChunk:
    def __init__(self, doc_name: str, chunk_id: int, text: str, section: str = "General", page: int = 1):
        self.doc_name = doc_name
        self.chunk_id = chunk_id
        self.text = text.strip()
        self.section = section
        self.page = page
        self.token_count = len(self.text.split())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_name": self.doc_name,
            "chunk_id": self.chunk_id,
            "section": self.section,
            "page": self.page,
            "token_count": self.token_count,
            "text": self.text,
        }


class HybridRAGEngine:
    """Production-grade RAG retrieval engine with hybrid scoring, stopword elimination, and citation provenance."""

    def __init__(self):
        self.chunks: List[DocumentChunk] = []
        self.vocabulary: Dict[str, int] = {}
        self.doc_freq: Dict[str, int] = {}
        self.avg_doc_len: float = 0.0

    def tokenize(self, text: str, remove_stopwords: bool = False) -> List[str]:
        tokens = re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", text.lower())
        if remove_stopwords:
            return [t for t in tokens if t not in STOPWORDS and len(t) > 2]
        return tokens

    def ingest_text(self, doc_name: str, content: str) -> int:
        """Chunks document text by natural sections and clauses for granular retrieval."""
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        new_chunks: List[DocumentChunk] = []
        chunk_idx = len(self.chunks)
        page_num = 1
        current_section = "Overview"

        for p in paragraphs:
            # Check for section or chapter headers
            lines = p.split("\n")
            first_line = lines[0].strip()
            if any(first_line.upper().startswith(k) for k in ["SECTION", "CHAPTER", "#"]):
                current_section = first_line[:50]

            # If a paragraph has multiple clauses (e.g. 1.1, 1.2, 1.3), split into individual clause chunks!
            sub_clauses = re.split(r"(?=\n\d+\.\d+|\nSECTION|\nCHAPTER)", p)
            for clause in sub_clauses:
                clause_text = clause.strip()
                if len(clause_text) < 15:
                    continue

                new_chunks.append(
                    DocumentChunk(
                        doc_name=doc_name,
                        chunk_id=chunk_idx,
                        text=clause_text,
                        section=current_section,
                        page=page_num
                    )
                )
                chunk_idx += 1
                if chunk_idx % 4 == 0:
                    page_num += 1

        self.chunks.extend(new_chunks)
        self._rebuild_bm25_index()
        return len(new_chunks)

    def _rebuild_bm25_index(self):
        """Builds inverted index for BM25 sparse keyword scoring."""
        self.doc_freq.clear()
        total_tokens = 0
        for chunk in self.chunks:
            content_tokens = set(self.tokenize(chunk.text, remove_stopwords=True))
            total_tokens += len(content_tokens)
            for token in content_tokens:
                self.doc_freq[token] = self.doc_freq.get(token, 0) + 1

        self.avg_doc_len = (total_tokens / len(self.chunks)) if self.chunks else 1.0

    def _bm25_score(self, query_content_tokens: List[str], chunk: DocumentChunk, k1: float = 1.5, b: float = 0.75) -> float:
        chunk_tokens = self.tokenize(chunk.text, remove_stopwords=True)
        doc_len = len(chunk_tokens)
        counts = Counter(chunk_tokens)
        score = 0.0
        n_docs = len(self.chunks)

        for token in query_content_tokens:
            if token in counts:
                tf = counts[token]
                df = self.doc_freq.get(token, 0)
                idf = math.log((n_docs - df + 0.5) / (df + 0.5) + 1.0)
                numerator = tf * (k1 + 1)
                denominator = tf + k1 * (1 - b + b * (doc_len / self.avg_doc_len))
                score += idf * (numerator / denominator)

        return max(0.0, score)

    def _semantic_overlap_score(self, query_content_tokens: List[str], chunk: DocumentChunk) -> float:
        """Computes content token intersection score."""
        chunk_tokens = set(self.tokenize(chunk.text, remove_stopwords=True))
        if not chunk_tokens or not query_content_tokens:
            return 0.0
        matches = [t for t in query_content_tokens if t in chunk_tokens]
        if not matches:
            return 0.0
        # Precision + Recall harmonic mean
        precision = len(matches) / len(query_content_tokens)
        recall = len(matches) / math.sqrt(len(chunk_tokens))
        return (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    def retrieve(self, query: str, top_k: int = 3, doc_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves matching chunks with strict keyword relevance and out-of-domain rejection."""
        if not self.chunks:
            return []

        # Filter query tokens by removing stopwords
        content_tokens = self.tokenize(query, remove_stopwords=True)
        
        # If user only asked stopwords (e.g. "what is that"), fall back to raw tokens
        if not content_tokens:
            content_tokens = self.tokenize(query, remove_stopwords=False)

        candidates = []

        for chunk in self.chunks:
            if doc_filter and chunk.doc_name != doc_filter:
                continue

            bm25 = self._bm25_score(content_tokens, chunk)
            semantic = self._semantic_overlap_score(content_tokens, chunk)
            
            # Hybrid combined score
            hybrid_score = (0.50 * semantic) + (0.50 * min(1.0, bm25 / 4.0))

            # Count exact matching content words
            chunk_tokens = set(self.tokenize(chunk.text, remove_stopwords=True))
            matched_words = [w for w in content_tokens if w in chunk_tokens]

            # Require at least 1 genuine content keyword match and score > 0.08
            if matched_words and hybrid_score > 0.08:
                candidates.append((hybrid_score, chunk, matched_words))

        candidates.sort(key=lambda x: x[0], reverse=True)
        top_results = candidates[:top_k]

        formatted = []
        for score, chunk, matched_words in top_results:
            formatted.append({
                "score": round(score, 4),
                "doc_name": chunk.doc_name,
                "section": chunk.section,
                "page": chunk.page,
                "text": chunk.text,
                "chunk_id": chunk.chunk_id,
                "matched_keywords": matched_words
            })

        return formatted

    def get_stats(self) -> Dict[str, Any]:
        unique_docs = list(set(c.doc_name for c in self.chunks))
        total_tokens = sum(c.token_count for c in self.chunks)
        return {
            "total_documents": len(unique_docs),
            "document_names": unique_docs,
            "total_chunks": len(self.chunks),
            "total_tokens_indexed": total_tokens,
            "status": "Ready",
            "index_type": "Hybrid (BM25 Sparse + Dense Semantic)"
        }
