# DBIP Architecture

## Overview
DBIP is a 19-stage intelligence transformation pipeline.

## Pipeline Stages

### Phase 1: Ingestion & Collection
1. Source Discovery
2. Multi-Protocol Collection
3. Quality Gate
4. Raw Data Lake

### Phase 2: Normalization & Validation
5. Normalization
6. MDIPS Validation
7. Ontology Mapping

### Phase 3: Extraction & Fusion
8. Entity Extraction
9. Signal Fusion
10. Relationship Construction

### Phase 4: Identity & Evidence
11. Identity Resolution
12. Evidence Assessment
13. Confidence Scoring

### Phase 5: Intelligence Assets
14. Intelligence Asset Builder
15. Dataset Builder
16. Intelligence Packaging

## Technology Stack
- FastAPI (API)
- PostgreSQL (Relational)
- Neo4j (Knowledge Graph)
- OpenSearch (Search)
- Qdrant (Vector)
- Kafka (Events)