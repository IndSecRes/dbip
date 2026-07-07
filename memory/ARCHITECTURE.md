# DBIP v6.0 Architecture

## High-Level Architecture
External Sources → ISCA → DBIP → ISCA → OSIRIS/CORTEX/FICS/TIIP

## DBIP Internal Pipeline (19 Stages)

### Phase 1: Ingestion & Collection
1. Source Discovery (UDIE + ISCA)
2. Multi-Protocol Collection (ISCA + UDIE)
3. Quality Gate (DBIP Core)
4. Raw Data Lake (DBIP Core)

### Phase 2: Normalization & Validation
5. Normalization (UDIE)
6. MDIPS Validation (MDIPS)
7. Ontology Mapping (MDIPS)

### Phase 3: Extraction & Fusion
8. Entity Extraction (UDIE + FICS)
9. Signal Fusion (DBIP Core)
10. Relationship Construction (MDIPS)

### Phase 4: Identity & Evidence
11. Identity Resolution (FICS)
12. Evidence Assessment (OSIRIS)
13. Confidence Scoring (MDIPS + FICS)

### Phase 5: Intelligence Assets
14. Intelligence Asset Builder (MDIPS + AURORA)
15. Dataset Builder (DBIP Core)
16. Intelligence Packaging (DBIP Core)

## Technology Stack
- FastAPI (API)
- PostgreSQL (Relational)
- Neo4j (Knowledge Graph)
- OpenSearch (Search)
- Qdrant (Vector)
- Kafka (Events)
- Docker (Containers)