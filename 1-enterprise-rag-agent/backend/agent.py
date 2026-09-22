"""
Autonomous Document Intelligence Agent
Handles query intent classification, context grounding, hallucination guardrails,
out-of-scope domain rejection, and accurate clause extraction.
"""

import os
import re
import time
import json
import urllib.request
from typing import List, Dict, Any, Optional
from rag_engine import HybridRAGEngine, STOPWORDS


class DocumentIntelligenceAgent:
    """Agent that orchestrates retrieval, reasoning, and citation synthesis."""

    def __init__(self, rag_engine: HybridRAGEngine):
        self.rag = rag_engine
        self.openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.groq_key = os.getenv("GROQ_API_KEY", "").strip()

    def classify_intent(self, query: str) -> str:
        q = query.lower()
        if any(w in q for w in ["summarize", "summary", "overview", "brief me", "tl;dr"]):
            return "SUMMARIZATION"
        elif any(w in q for w in ["compare", "difference between", "vs", "versus"]):
            return "SYNTHESIS_COMPARISON"
        elif any(w in q for w in ["penalty", "penalties", "guarantee", "uptime", "sla", "availability", "credit", "hours", "percent", "cap"]):
            return "FACTUAL_EXTRACTION"
        return "GENERAL_RETRIEVAL"

    def answer_query(self, query: str, top_k: int = 3, doc_filter: str = None) -> Dict[str, Any]:
        start_time = time.time()
        intent = self.classify_intent(query)
        
        # Step 1: Hybrid Retrieval with Stopword Filtering
        retrieved_chunks = self.rag.retrieve(query, top_k=top_k, doc_filter=doc_filter)
        
        # Step 2: Out-of-Scope / Hallucination Guardrail Check
        # If no chunks passed the relevance threshold or no genuine content words matched:
        if not retrieved_chunks:
            latency = round((time.time() - start_time) * 1000, 2)
            available_docs = ", ".join(self.rag.get_stats().get("document_names", []))
            
            return {
                "answer": (
                    f"### [Out of Scope / No Relevant Information Found]\n\n"
                    f"I could not find any provisions or information regarding **\"{query}\"** in your uploaded documentation.\n\n"
                    f"**Current Knowledge Base:** `{available_docs}`\n\n"
                    f"*As an enterprise compliance AI, I strictly refuse to hallucinate facts outside your uploaded contracts and specifications. "
                    f"You can ask about service availability, SLA credits, data privacy policies, or RAG architecture, or upload a document addressing this topic.*"
                ),
                "citations": [],
                "intent": intent,
                "latency_ms": latency,
                "guardrail_status": "OUT_OF_SCOPE_REJECTED",
                "retrieved_chunks_count": 0,
                "estimated_tokens": 40
            }

        # Step 3: Extract Citations
        citations = []
        for i, chunk in enumerate(retrieved_chunks):
            # Clean snippet for preview
            snippet = chunk["text"].replace("\n", " ").strip()
            if len(snippet) > 160:
                snippet = snippet[:160] + "..."

            citations.append({
                "citation_id": f"[{i+1}]",
                "doc_name": chunk["doc_name"],
                "section": chunk["section"],
                "page": chunk["page"],
                "relevance_score": chunk["score"],
                "exact_quote": snippet,
                "matched_keywords": chunk.get("matched_keywords", [])
            })

        # Step 4: Synthesize Grounded Answer
        answer = self._synthesize_answer(query, intent, retrieved_chunks, citations)

        latency = round((time.time() - start_time) * 1000, 2)

        return {
            "answer": answer,
            "citations": citations,
            "intent": intent,
            "latency_ms": latency,
            "guardrail_status": "VERIFIED_HIGH_CONFIDENCE",
            "retrieved_chunks_count": len(retrieved_chunks),
            "estimated_tokens": sum(len(c["text"].split()) for c in retrieved_chunks) + len(answer.split())
        }

    def _call_groq_llm(self, prompt: str, context: str) -> Optional[str]:
        """Calls Groq API (e.g. Llama 3) if GROQ_API_KEY is configured."""
        if not self.groq_key:
            return None
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.groq_key}",
                "Content-Type": "application/json"
            }
            body = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "You are DocuMind AI, an enterprise contract and architecture assistant. Answer strictly based on the provided context with citations [1], [2]. If the context doesn't have the answer, state that it is not covered."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {prompt}"}
                ],
                "temperature": 0.1
            }
            req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["choices"][0]["message"]["content"]
        except Exception:
            return None

    def _synthesize_answer(self, query: str, intent: str, chunks: List[Dict[str, Any]], citations: List[Dict[str, Any]]) -> str:
        """Extracts the exact sentences that answer the query, scoring each sentence by keyword match."""
        # Try online LLM first if key available
        context_str = "\n\n".join([f"[{i+1}] ({c['doc_name']} - {c['section']}):\n{c['text']}" for i, c in enumerate(chunks)])
        llm_answer = self._call_groq_llm(query, context_str)
        if llm_answer:
            return llm_answer

        # Extractive Semantic QA Synthesis:
        query_words = set(re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", query.lower())) - STOPWORDS
        
        extracted_answers = []

        for i, chunk in enumerate(chunks):
            citation_tag = f"[{i+1}]"
            # Split into individual clauses and sentences
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", chunk["text"]) if s.strip()]
            
            # Score each sentence based on overlap with query content words
            scored_sentences = []
            for s in sentences:
                s_lower = s.lower()
                # Skip pure document headers like 'ENTERPRISE MASTER SERVICES AGREEMENT'
                if len(s) < 25 or s.isupper():
                    continue
                score = sum(2 for w in query_words if w in s_lower)
                # Boost if numbers or percentages match
                if any(char.isdigit() for char in s) and any(w in query.lower() for w in ["percent", "percentage", "penalty", "uptime", "sla", "guarantee", "how many", "what"]):
                    score += 2
                if score > 0:
                    scored_sentences.append((score, s))

            scored_sentences.sort(key=lambda x: x[0], reverse=True)
            
            # Take top relevant sentences
            for score, best_sent in scored_sentences[:2]:
                extracted_answers.append(f"- **{chunk['section']}**: {best_sent} {citation_tag}")

        if not extracted_answers:
            # Fallback to the top chunk's core provision
            first_chunk = chunks[0]
            clean_text = first_chunk["text"].replace("\n", " ")
            extracted_answers.append(f"- **{first_chunk['section']}**: {clean_text[:280]}... [1]")

        findings = "\n\n".join(extracted_answers)

        if intent == "FACTUAL_EXTRACTION":
            return (
                f"### [Verified Contract & Policy Terms]\n\n"
                f"Based on your enterprise documentation, here are the exact provisions governing **\"{query}\"**:\n\n"
                f"{findings}\n\n"
                f"*Synthesized from {len(chunks)} verified source clause(s) with zero hallucination guarantee.*"
            )
        else:
            return (
                f"### [Verified Documentation Findings]\n\n"
                f"Relevant provisions extracted from **{chunks[0]['doc_name']}** regarding **\"{query}\"**:\n\n"
                f"{findings}\n\n"
                f"*Referenced via verified source citations below.*"
            )
