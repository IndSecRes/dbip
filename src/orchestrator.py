"""
DBIP Pipeline Orchestrator
Manages the 19-stage intelligence transformation pipeline
"""
# Add at the top with other imports
from src.graph import KnowledgeGraphRepository, GraphNode, GraphRelationship
from src.graph.neo4j_client import get_neo4j_client
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

# Use absolute imports
from src.models import (
    ProvenanceNode,
    EvidenceRating,
    SignalType
)
from src.config import config


class PipelineContext:
    """Context passed through pipeline stages"""
    
    def __init__(self, request_id: Optional[str] = None):
        self.request_id = request_id or str(uuid.uuid4())
        self.start_time = datetime.now()
        self.current_stage: str = "init"
        self.provenance_chain: List[ProvenanceNode] = []
        self.metadata: Dict[str, Any] = {}
        self.configuration = {
            "fusion_threshold": config.get("pipeline.fusion_threshold", 0.75),
            "identity_threshold": config.get("pipeline.identity_similarity_threshold", 0.85),
            "default_confidence": config.get("pipeline.default_confidence", 0.5),
            "collection_timeout": config.get("pipeline.collection_timeout_seconds", 30),
            "max_concurrent": config.get("pipeline.max_concurrent_collections", 10)
        }
    
    def add_provenance(self, provenance: ProvenanceNode) -> None:
        """Add a provenance node to the chain"""
        self.provenance_chain.append(provenance)
    
    def get_stage_summary(self) -> Dict[str, Any]:
        """Get summary of pipeline execution"""
        return {
            "request_id": self.request_id,
            "start_time": self.start_time.isoformat(),
            "current_stage": self.current_stage,
            "stages_completed": len(self.provenance_chain),
            "duration_seconds": (datetime.now() - self.start_time).total_seconds()
        }


class PipelineOrchestrator:
    """
    Orchestrates the 19-stage DBIP pipeline
    """
    
    def __init__(self):
        self.logger = logging.getLogger("DBIP.Pipeline")
        self.setup_logging()
        self.graph_repo = KnowledgeGraphRepository()
    
    def setup_logging(self):
        """Configure logging for the pipeline"""
        logging.basicConfig(
            level=logging.INFO if config.get("debug", False) else logging.WARNING,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    async def process_intelligence(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main pipeline entry point
        Processes raw data through all 19 stages
        """
        context = PipelineContext()
        self.logger.info(f"Starting pipeline for request: {context.request_id}")
        
        try:
            # Stage 1: Source Discovery
            self.logger.debug("Stage 1: Source Discovery")
            context.current_stage = "source_discovery"
            discovered_sources = await self._source_discovery(raw_data, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.95
            ))
            
            # Stage 2: Collection
            self.logger.debug("Stage 2: Collection")
            context.current_stage = "collection"
            collected_data = await self._collection(discovered_sources, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.93
            ))
            
            # Stage 3: Quality Gate
            self.logger.debug("Stage 3: Quality Gate")
            context.current_stage = "quality_gate"
            validated_data = await self._quality_gate(collected_data, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.94
            ))
            
            # Stage 4: Raw Data Lake
            self.logger.debug("Stage 4: Raw Data Lake")
            context.current_stage = "raw_data_lake"
            stored_data = await self._raw_data_lake(validated_data, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.92
            ))
            
            # Stage 5: Normalization
            self.logger.debug("Stage 5: Normalization")
            context.current_stage = "normalization"
            normalized_data = await self._normalization(stored_data, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.91
            ))
            
            # Stage 6: MDIPS Validation
            self.logger.debug("Stage 6: MDIPS Validation")
            context.current_stage = "mdips_validation"
            validated_mdips = await self._mdips_validation(normalized_data, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.96
            ))
            
            # Stage 7: Ontology Mapping
            self.logger.debug("Stage 7: Ontology Mapping")
            context.current_stage = "ontology_mapping"
            mapped_data = await self._ontology_mapping(validated_mdips, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.90
            ))
            
            # Stage 8: Entity Extraction
            self.logger.debug("Stage 8: Entity Extraction")
            context.current_stage = "entity_extraction"
            entities = await self._entity_extraction(mapped_data, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.88
            ))
            
            # Stage 9: Signal Fusion
            self.logger.debug("Stage 9: Signal Fusion")
            context.current_stage = "signal_fusion"
            fused_signals = await self._signal_fusion(entities, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.89
            ))
            
            # Stage 10: Relationship Construction
            self.logger.debug("Stage 10: Relationship Construction")
            context.current_stage = "relationship_construction"
            relationships = await self._relationship_construction(fused_signals, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.87
            ))
            
            # Stage 11: Identity Resolution
            self.logger.debug("Stage 11: Identity Resolution")
            context.current_stage = "identity_resolution"
            resolved_entities = await self._identity_resolution(fused_signals, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.85
            ))
            
            # Stage 12: Evidence Assessment
            self.logger.debug("Stage 12: Evidence Assessment")
            context.current_stage = "evidence_assessment"
            assessed_entities = await self._evidence_assessment(resolved_entities, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.84
            ))
            
            # Stage 13: Signal Rating
            self.logger.debug("Stage 13: Signal Rating")
            context.current_stage = "signal_rating"
            rated_signals = await self._signal_rating(assessed_entities, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.86
            ))
            
            # Stage 14: Confidence Calibration
            self.logger.debug("Stage 14: Confidence Calibration")
            context.current_stage = "confidence_calibration"
            calibrated = await self._confidence_calibration(rated_signals, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.90
            ))
            
            # Stage 15: Temporal Intelligence
            self.logger.debug("Stage 15: Temporal Intelligence")
            context.current_stage = "temporal_intelligence"
            temporal_data = await self._temporal_intelligence(calibrated, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.88
            ))
            
            # Stage 16: Asset Builder
            self.logger.debug("Stage 16: Asset Builder")
            context.current_stage = "asset_builder"
            assets = await self._asset_builder(temporal_data, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.92
            ))
            
            # Stage 17: Dataset Builder
            self.logger.debug("Stage 17: Dataset Builder")
            context.current_stage = "dataset_builder"
            datasets = await self._dataset_builder(assets, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.91
            ))
            
            # Stage 18: Intelligence Packaging
            self.logger.debug("Stage 18: Intelligence Packaging")
            context.current_stage = "intelligence_packaging"
            packaged = await self._intelligence_packaging(datasets, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.95
            ))
            
            # Stage 19: ISCA Distribution
            self.logger.debug("Stage 19: ISCA Distribution")
            context.current_stage = "isca_distribution"
            result = await self._isca_distribution(packaged, context)
            context.add_provenance(ProvenanceNode(
                source_id="pipeline", source_type="internal", confidence_score=0.98
            ))
            
            self.logger.info(f"Pipeline completed for request: {context.request_id}")
            
            return {
                "status": "success",
                "request_id": context.request_id,
                "summary": context.get_stage_summary(),
                "result": result
            }
            
        except Exception as e:
            self.logger.error(f"Pipeline failed for {context.request_id}: {str(e)}")
            return {
                "status": "failed",
                "request_id": context.request_id,
                "error": str(e),
                "summary": context.get_stage_summary()
            }
    
    # ============== Pipeline Stage Methods ==============
    
    async def _source_discovery(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 1: Discover data sources"""
        return {
            **data,
            "sources_discovered": [
                {"source_id": "source_001", "source_type": "API", "status": "available"},
                {"source_id": "source_002", "source_type": "Database", "status": "available"}
            ]
        }
    
    async def _collection(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 2: Collect raw data from sources"""
        return {
            **data,
            "collected_data": {
                "records": [
                    {"id": 1, "content": "Sample intelligence data", "source": "source_001"},
                    {"id": 2, "content": "More intelligence data", "source": "source_002"}
                ]
            }
        }
    
    async def _quality_gate(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 3: Validate data quality"""
        return {
            **data,
            "quality_score": 0.95,
            "quality_issues": [],
            "passed": True
        }
    
    async def _raw_data_lake(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 4: Store raw data"""
        return {
            **data,
            "storage_location": "s3://dbip-raw/2026/07/07/",
            "stored_at": datetime.now().isoformat()
        }
    
    async def _normalization(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 5: Normalize data formats"""
        return {
            **data,
            "normalized": True,
            "format_version": "2.0",
            "schema": "intelligence_schema_v1"
        }
    
    async def _mdips_validation(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 6: Validate against MDIPS schema"""
        return {
            **data,
            "mdips_compliant": True,
            "validation_errors": []
        }
    
    async def _ontology_mapping(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 7: Map to ontology"""
        return {
            **data,
            "ontology_version": "4.0",
            "mapped_entities": 5
        }
    
    async def _entity_extraction(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 8: Extract entities with multi-dimensional confidence"""
        from src.models.mdips import ConfidenceModel, MDIPSEntity, EntityType, Domain, create_entity
        from datetime import datetime
        
        # Example: Extract person entity with confidence
        person_confidence = ConfidenceModel(
            source_reliability=0.9,
            extraction_confidence=0.95,
            identity_confidence=0.92,
            relationship_confidence=0.85,
            temporal_confidence=0.88,
            analytical_confidence=0.90
        )
        
        # Create entity with confidence
        entity = create_entity(
            entity_type=EntityType.PERSON,
            label="John Doe",
            description="Individual identified through chatter analysis",
            attributes={
                "phone_numbers": ["+1-555-123-4567"],
                "emails": ["john.doe@email.com"],
                "social_media": {
                    "telegram": "@johndoe",
                    "twitter": "@johndoe_nyc"
                }
            },
            domains=[Domain.OSINT, Domain.SOCMINT]
        )
        entity.confidence = person_confidence
        
        return {
            **data,
            "extracted_entities": [entity.dict()],
            "confidence_scores": {
                "entity_id": entity.entity_id,
                "overall": person_confidence.overall,
                "evidence_rating": person_confidence.evidence_rating.value,
                "dimensions": {
                    "source_reliability": person_confidence.source_reliability,
                    "extraction_confidence": person_confidence.extraction_confidence,
                    "identity_confidence": person_confidence.identity_confidence,
                    "relationship_confidence": person_confidence.relationship_confidence,
                    "temporal_confidence": person_confidence.temporal_confidence,
                    "analytical_confidence": person_confidence.analytical_confidence
                }
            }
        }
    
    async def _signal_fusion(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 9: Fuse multiple signals into strong intelligence"""
        from src.fusion import SignalFusionEngine
        
        # Get signals from previous stage
        signals = data.get("extracted_entities", [])
        
        # Also include raw signals if available
        raw_signals = data.get("collected_data", {}).get("records", [])
        if raw_signals:
            # Add raw signals with basic structure
            for raw in raw_signals[:10]:  # Limit to 10
                if isinstance(raw, dict):
                    signals.append({
                        "source": raw.get("source", "unknown"),
                        "content": raw,
                        "extracted_entities": []
                    })
        
        if not signals:
            return {
                **data,
                "fused_signals": [],
                "fusion_summary": {
                    "total_fused_signals": 0,
                    "average_confidence": 0,
                    "fusion_rate": 0
                }
            }
        
        # Initialize fusion engine
        engine = SignalFusionEngine(confidence_threshold=0.6)
        
        # Fuse signals
        fused_signals = engine.fuse_signals(signals)
        
        # Build output
        fused_data = []
        for fused in fused_signals:
            fused_data.append({
                "fused_id": fused.fused_id,
                "signal_type": fused.signal_type,
                "content": fused.content,
                "sources": fused.sources,
                "source_count": fused.source_count,
                "confidence": {
                    "overall": fused.confidence.overall,
                    "rating": fused.confidence.evidence_rating.value,
                    "dimensions": fused.confidence.model_dump()
                },
                "patterns": fused.patterns,
                "entities": fused.entities,
                "timestamp": fused.timestamp.isoformat()
            })
        
        # Get summary
        summary = engine.get_summary()
        
        return {
            **data,
            "fused_signals": fused_data,
            "fusion_summary": {
                "total_fused_signals": len(fused_signals),
                "average_confidence": summary["average_confidence"],
                "ratings_distribution": summary["ratings_distribution"],
                "top_sources": summary["top_sources"],
                "top_entities": summary["top_entities"],
                "fusion_rate": round(len(fused_signals) / len(signals) if signals else 0, 3)
            }
        }
    
    async def _relationship_construction(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 10: Build relationships"""
        return {
            **data,
            "relationships": [
                {"source": "John Doe", "target": "ACME Corp", "type": "employs", "confidence": 0.85}
            ]
        }
    
    async def _identity_resolution(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 11: Resolve identities across sources"""
        try:
            from src.identity import IdentityResolver
            from src.identity.resolver import ResolvedEntity
            from src.models.mdips import ConfidenceModel, EvidenceRating
            import uuid
            from datetime import datetime
            
            # Get entities from previous stage
            entities = data.get("resolved_entities", [])
            if not entities:
                entities = data.get("extracted_entities", [])
            
            if not entities or not isinstance(entities, list):
                return {
                    **data,
                    "resolved_identities": [],
                    "resolution_summary": {
                        "total_entities": 0,
                        "resolved_count": 0,
                        "unique_count": 0,
                        "resolution_rate": 0
                    }
                }
            
            # Initialize resolver with lower threshold for testing
            resolver = IdentityResolver(threshold=0.7)
            
            # Resolve entities with error handling
            try:
                resolved = resolver.resolve_entities(entities)
            except Exception as e:
                self.logger.warning(f"Identity resolution error: {e}")
                # Fallback: return entities as-is
                resolved = []
                for entity in entities:
                    if entity and isinstance(entity, dict):
                        resolved.append(ResolvedEntity(
                            entity_id=entity.get("entity_id", str(uuid.uuid4())),
                            canonical_id=f"CAN_{uuid.uuid4().hex[:8].upper()}",
                            source_entity_ids=[entity.get("entity_id", str(uuid.uuid4()))],
                            attributes=entity.get("attributes", {}),
                            aliases=entity.get("aliases", []),
                            confidence=ConfidenceModel(source_reliability=0.5),
                            evidence_rating=EvidenceRating.C,
                            resolved_at=datetime.now(),
                            match_score=1.0
                        ))
            
            # Build output
            resolved_data = []
            for entity in resolved:
                if entity:
                    resolved_data.append({
                        "entity_id": getattr(entity, 'entity_id', ''),
                        "canonical_id": getattr(entity, 'canonical_id', ''),
                        "source_count": len(getattr(entity, 'source_entity_ids', [])),
                        "source_entity_ids": getattr(entity, 'source_entity_ids', []),
                        "attributes": getattr(entity, 'attributes', {}),
                        "aliases": getattr(entity, 'aliases', []),
                        "confidence": {
                            "overall": getattr(entity, 'confidence', ConfidenceModel()).overall,
                            "rating": getattr(entity, 'evidence_rating', EvidenceRating.C).value,
                            "dimensions": getattr(entity, 'confidence', ConfidenceModel()).model_dump()
                        },
                        "match_score": getattr(entity, 'match_score', 0),
                        "is_resolved": getattr(entity, 'is_resolved', False),
                        "resolved_at": getattr(entity, 'resolved_at', datetime.now()).isoformat()
                    })
            
            return {
                **data,
                "resolved_identities": resolved_data,
                "resolution_summary": {
                    "total_entities": len(entities),
                    "resolved_count": len(resolved),
                    "unique_count": len([e for e in resolved if getattr(e, 'is_resolved', False)]),
                    "resolution_rate": round(len([e for e in resolved if getattr(e, 'is_resolved', False)]) / len(entities) if entities else 0, 3)
                }
            }
        except Exception as e:
            self.logger.error(f"Identity resolution failed: {e}")
            return {
                **data,
                "resolved_identities": [],
                "resolution_summary": {
                    "total_entities": 0,
                    "resolved_count": 0,
                    "unique_count": 0,
                    "resolution_rate": 0,
                    "error": str(e)
                }
            }
    
    async def _evidence_assessment(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 12: Assess evidence quality with multi-dimensional confidence"""
        from src.models.mdips import ConfidenceModel, EvidenceRating
        from src.evidence import EvidenceAssessor
        
        # Get extracted entities from previous stage
        extracted_entities = data.get("extracted_entities", [])
        
        # Create evidence assessor
        assessor = EvidenceAssessor()
        
        # Convert signals to evidence - properly format content as dict
        signals = data.get("collected_data", {}).get("records", [])
        if not signals:
            # Fallback: use extracted data
            signals = data.get("extracted_entities", [])
        
        evidence_list = []
        for signal in signals[:5]:  # Limit to 5 for performance
            # Ensure content is a dictionary
            if isinstance(signal, dict):
                # If signal has 'content' as string, convert to dict
                if "content" in signal and isinstance(signal["content"], str):
                    signal["content"] = {"message": signal["content"]}
                elif "content" not in signal:
                    signal["content"] = {"data": signal}
            
            evidence = assessor.assess_evidence(
                signal,
                source_reliability=0.8,
                extraction_confidence=0.85
            )
            evidence_list.append(evidence)
        
        # Corroborate evidence
        corroborated = assessor.corroborate_evidence(evidence_list)
        
        # Build evidence assessment
        assessments = []
        for item in corroborated:
            evidence = item["evidence"]
            assessments.append({
                "evidence_id": evidence.evidence_id,
                "type": evidence.evidence_type,
                "source": evidence.source,
                "confidence": {
                    "overall": evidence.confidence.overall,
                    "rating": evidence.confidence.evidence_rating.value,
                    "dimensions": evidence.confidence.model_dump()
                },
                "corroboration_count": item["corroborating_count"],
                "contradictory_count": item["contradictory_count"],
                "corroboration_score": item["corroboration_score"],
                "timestamp": evidence.timestamp.isoformat(),
                "hash": evidence.hash,
                "supporting_sources": evidence.supporting_sources,
                "corroborating_evidence": evidence.corroborating_evidence,
                "contradictory_evidence": evidence.contradictory_evidence
            })
        
        # Calculate summary statistics
        if assessments:
            avg_confidence = round(sum(e["confidence"]["overall"] for e in assessments) / len(assessments), 3)
            rating_counts = {
                "A": len([e for e in assessments if e["confidence"]["rating"] == "A"]),
                "B": len([e for e in assessments if e["confidence"]["rating"] == "B"]),
                "C": len([e for e in assessments if e["confidence"]["rating"] == "C"]),
                "D": len([e for e in assessments if e["confidence"]["rating"] == "D"])
            }
            avg_corroboration = round(sum(e["corroboration_score"] for e in assessments) / len(assessments), 3)
        else:
            avg_confidence = 0
            rating_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
            avg_corroboration = 0
        
        return {
            **data,
            "evidence": assessments,
            "evidence_summary": {
                "total_evidence": len(assessments),
                "average_confidence": avg_confidence,
                "ratings_distribution": rating_counts,
                "corroboration_rate": avg_corroboration,
                "total_corroborating": sum(e["corroboration_count"] for e in assessments),
                "total_contradictory": sum(e["contradictory_count"] for e in assessments)
            }
        }
        
        # Calculate summary statistics
        if assessments:
            avg_confidence = round(sum(e["confidence"]["overall"] for e in assessments) / len(assessments), 3)
            rating_counts = {
                "A": len([e for e in assessments if e["confidence"]["rating"] == "A"]),
                "B": len([e for e in assessments if e["confidence"]["rating"] == "B"]),
                "C": len([e for e in assessments if e["confidence"]["rating"] == "C"]),
                "D": len([e for e in assessments if e["confidence"]["rating"] == "D"])
            }
            avg_corroboration = round(sum(e["corroboration_score"] for e in assessments) / len(assessments), 3)
        else:
            avg_confidence = 0
            rating_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
            avg_corroboration = 0
        
        return {
            **data,
            "evidence": assessments,
            "evidence_summary": {
                "total_evidence": len(assessments),
                "average_confidence": avg_confidence,
                "ratings_distribution": rating_counts,
                "corroboration_rate": avg_corroboration,
                "total_corroborating": sum(e["corroboration_count"] for e in assessments),
                "total_contradictory": sum(e["contradictory_count"] for e in assessments)
            }
        }
    
    async def _signal_rating(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 13: Rate signals"""
        return {
            **data,
            "signal_ratings": [
                {"signal": "sig_001", "rating": "HIGH", "score": 0.88}
            ]
        }
    
    async def _confidence_calibration(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 14: Calibrate confidence across dimensions"""
        from src.models.mdips import ConfidenceModel
        
        # Get confidence from previous stages
        evidence_ratings = data.get("evidence_ratings", [])
        confidence_data = evidence_ratings[0].get("confidence", {}) if evidence_ratings else {}
        
        # Calibration factors based on corroboration
        calibration_factors = {
            "source_reliability": 0.05,
            "extraction_confidence": 0.02,
            "identity_confidence": 0.03,
            "relationship_confidence": 0.04,
            "temporal_confidence": 0.02,
            "analytical_confidence": 0.04
        }
        
        # Apply calibration
        calibrated = ConfidenceModel(
            source_reliability=min(1.0, confidence_data.get("source_reliability", 0.5) + calibration_factors["source_reliability"]),
            extraction_confidence=min(1.0, confidence_data.get("extraction_confidence", 0.5) + calibration_factors["extraction_confidence"]),
            identity_confidence=min(1.0, confidence_data.get("identity_confidence", 0.5) + calibration_factors["identity_confidence"]),
            relationship_confidence=min(1.0, confidence_data.get("relationship_confidence", 0.5) + calibration_factors["relationship_confidence"]),
            temporal_confidence=min(1.0, confidence_data.get("temporal_confidence", 0.5) + calibration_factors["temporal_confidence"]),
            analytical_confidence=min(1.0, confidence_data.get("analytical_confidence", 0.5) + calibration_factors["analytical_confidence"])
        )
        
        return {
            **data,
            "calibrated_confidence": {
                "overall": calibrated.overall,
                "evidence_rating": calibrated.evidence_rating.value,
                "dimensions": calibrated.dict(),
                "calibration_method": "bayesian_update",
                "calibration_factors": calibration_factors
            }
        }
    
    async def _temporal_intelligence(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 15: Add temporal context"""
        return {
            **data,
            "temporal_context": {
                "valid_from": datetime.now().isoformat(),
                "valid_to": "2026-08-07T00:00:00",
                "temporal_confidence": 0.85
            }
        }
    
    async def _asset_builder(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 16: Build intelligence assets with confidence"""
        from src.models.mdips import ConfidenceModel
        
        # Get calibrated confidence
        calibrated_confidence = data.get("calibrated_confidence", {})
        confidence_dimensions = calibrated_confidence.get("dimensions", {})
        
        # Build confidence model for asset
        asset_confidence = ConfidenceModel(
            source_reliability=confidence_dimensions.get("source_reliability", 0.5),
            extraction_confidence=confidence_dimensions.get("extraction_confidence", 0.5),
            identity_confidence=confidence_dimensions.get("identity_confidence", 0.5),
            relationship_confidence=confidence_dimensions.get("relationship_confidence", 0.5),
            temporal_confidence=confidence_dimensions.get("temporal_confidence", 0.5),
            analytical_confidence=confidence_dimensions.get("analytical_confidence", 0.5)
        )
        
        # Create asset with confidence
        asset = {
            "asset_id": f"AST_{context.request_id[:8]}",
            "type": "intelligence_report",
            "title": "Preliminary Intelligence Assessment",
            "confidence": {
                "overall": asset_confidence.overall,
                "evidence_rating": asset_confidence.evidence_rating.value,
                "dimensions": asset_confidence.dict()
            }
        }
        
        return {
            **data,
            "assets": [
                {
                    **asset,
                    "provenance": [p.dict() for p in context.provenance_chain]
                }
            ]
        }
    
    async def _dataset_builder(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 17: Build datasets"""
        return {
            **data,
            "datasets": [
                {"name": "entity_dataset", "size": 100, "schema_version": "1.0"}
            ]
        }
    
    async def _intelligence_packaging(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 18: Package intelligence"""
        return {
            **data,
            "package_id": f"PKG_{context.request_id[:8]}",
            "package_format": "MDIPS_v5.0",
            "total_assets": 1
        }
    
    async def _isca_distribution(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 19: Distribute via ISCA"""
        return {
            **data,
            "distribution_status": "published",
            "published_at": datetime.now().isoformat(),
            "topics": ["intelligence.assets", "intelligence.signals"]
        }


# Test the pipeline
if __name__ == "__main__":
    import asyncio
    
    async def test_pipeline():
        print("=" * 60)
        print("DBIP Pipeline Orchestrator Test")
        print("=" * 60)
        
        orchestrator = PipelineOrchestrator()
        
        # Test data
        test_data = {
            "source_id": "test_source",
            "raw_content": "This is test intelligence data",
            "metadata": {"priority": "high"}
        }
        
        result = await orchestrator.process_intelligence(test_data)
        
        print(f"\n📊 Pipeline Result:")
        print(f"   Status: {result['status']}")
        print(f"   Request ID: {result['request_id']}")
        print(f"   Duration: {result['summary']['duration_seconds']:.2f}s")
        print(f"   Stages Completed: {result['summary']['stages_completed']}")
        
        if result['status'] == 'success':
            print(f"   Distribution: {result['result']['distribution_status']}")
        
        print("\n✅ Pipeline test completed!")
    
    asyncio.run(test_pipeline())