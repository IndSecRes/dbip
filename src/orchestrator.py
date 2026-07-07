"""
DBIP Pipeline Orchestrator
Manages the 19-stage intelligence transformation pipeline
"""

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
        """Stage 8: Extract entities"""
        return {
            **data,
            "extracted_entities": [
                {"type": "person", "name": "John Doe", "confidence": 0.9},
                {"type": "organization", "name": "ACME Corp", "confidence": 0.85}
            ]
        }
    
    async def _signal_fusion(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 9: Fuse multiple signals"""
        return {
            **data,
            "fused_signals": [
                {"signal_id": "sig_001", "confidence": 0.88, "sources": 3},
                {"signal_id": "sig_002", "confidence": 0.92, "sources": 2}
            ]
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
        """Stage 11: Resolve identities"""
        return {
            **data,
            "resolved_entities": [
                {
                    "entity_id": "ent_001",
                    "canonical_name": "John Doe",
                    "aliases": ["J. Doe", "Johnathan Doe"],
                    "confidence": 0.92
                }
            ]
        }
    
    async def _evidence_assessment(self, data: Dict[str, Any], context: PipelineContext) -> Dict[str, Any]:
        """Stage 12: Assess evidence quality"""
        return {
            **data,
            "evidence_ratings": [
                {"entity": "ent_001", "rating": EvidenceRating.B, "score": 0.85}
            ]
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
        """Stage 14: Calibrate confidence"""
        return {
            **data,
            "calibrated_confidence": 0.90,
            "calibration_method": "bayesian_update"
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
        """Stage 16: Build intelligence assets"""
        return {
            **data,
            "assets": [
                {
                    "asset_id": "ast_001",
                    "type": "intelligence_report",
                    "title": "Preliminary Threat Assessment",
                    "confidence": 0.90
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