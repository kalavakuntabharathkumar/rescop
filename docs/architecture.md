# Architecture and extension plan

1. API validates requests with Pydantic.
2. DocumentStore keeps documents in process memory for a frictionless demo.
3. TF-IDF + cosine similarity ranks text snippets.
4. Research workflow records retrieval, synthesis, and quality-check stages.
5. Risk module computes descriptive statistics on user-provided return observations.

## Production extensions
Replace in-memory storage with PostgreSQL and Qdrant; add durable ingestion workers, Redis caching, an LLM provider adapter, citation-grounded synthesis, evaluation datasets, auth/RBAC, audit trails, observability, and safety controls for prompt injection and unsupported financial claims.
