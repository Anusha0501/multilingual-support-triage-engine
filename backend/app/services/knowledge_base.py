from dataclasses import dataclass

@dataclass(slots=True)
class KnowledgeChunk:
    document_id: str
    text: str
    score: float

class KnowledgeBaseService:
    """RAG boundary for PDF ingestion, chunking, embeddings, and retrieval.

    Production adapters can replace this in-memory implementation with ChromaDB,
    pgvector, Pinecone, or Elasticsearch hybrid retrieval without changing the
    ticket triage service contract.
    """

    def chunk_text(self, text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
        chunks: list[str] = []
        start = 0
        while start < len(text):
            chunks.append(text[start:start + chunk_size])
            start += max(chunk_size - overlap, 1)
        return chunks

    def retrieve(self, query: str, limit: int = 4) -> list[KnowledgeChunk]:
        return [KnowledgeChunk(document_id="sop-default", text="Acknowledge the issue, confirm ownership, and provide the next update window.", score=0.71)][:limit]
