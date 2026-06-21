# System Design Notes

## Architecture diagram

```mermaid
flowchart TB
  subgraph Client
    Browser[Next.js SaaS]
  end
  subgraph API
    FastAPI[FastAPI Routers]
    Service[Service Layer]
    Repo[Repository Layer]
  end
  subgraph AI
    Lang[Language Classifier]
    Intent[Intent Classifier]
    SLA[SLA Predictor]
    Draft[Reply Draft Chain]
    RAG[RAG Retriever]
  end
  Browser --> FastAPI --> Service
  Service --> Repo --> Postgres[(PostgreSQL)]
  Service --> Redis[(Redis)]
  Service --> Lang
  Service --> Intent
  Service --> SLA
  Service --> RAG --> Chroma[(ChromaDB)]
  Service --> Draft --> LangSmith[(LangSmith)]
```

## Commit roadmap

- `feat(architecture): add system design and project foundation`
- `feat(api): add ticket triage endpoint`
- `feat(rag): add knowledge-base retrieval boundary`
- `feat(ui): add SaaS dashboard shell`
- `ci: add backend and frontend validation workflow`
