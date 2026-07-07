"""
DBIP Configuration Management
Loads YAML configuration with environment overrides
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class ConfigLoader:
    """Load configuration from YAML files + environment overrides"""
    
    def __init__(self, env: Optional[str] = None):
        self.env = env or os.getenv("DBIP_ENV", "development")
        self.config_dir = Path(__file__).parent.parent / "config"
        self._config: Optional[Dict[str, Any]] = None
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get loaded configuration"""
        if self._config is None:
            self._config = self.load()
        return self._config
    
    def load(self) -> Dict[str, Any]:
        """Load configuration for current environment"""
        
        # 1. Load base config
        base_config = {}
        base_file = self.config_dir / "base.yaml"
        if base_file.exists():
            with open(base_file, 'r', encoding='utf-8') as f:
                base_config = yaml.safe_load(f) or {}
            print(f"✅ Loaded base config from: {base_file}")
        
        # 2. Load environment-specific config
        env_config = {}
        env_file = self.config_dir / f"{self.env}.yaml"
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                env_config = yaml.safe_load(f) or {}
            print(f"✅ Loaded {self.env} config from: {env_file}")
        
        # 3. Merge: env_config overrides base_config
        merged = self._deep_merge(base_config, env_config)
        
        # 4. Apply environment variable overrides
        self._apply_env_overrides(merged)
        
        print(f"✅ Configuration loaded for environment: {self.env}")
        return merged
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = base.copy()
        for key, value in override.items():
            if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def _apply_env_overrides(self, config: Dict):
        """Apply environment variable overrides (DBIP_ prefix)"""
        for key, value in os.environ.items():
            if key.startswith("DBIP_"):
                # Convert DBIP__SERVER__HOST to nested dict
                path = key[5:].lower().split("__")
                target = config
                for part in path[:-1]:
                    target = target.setdefault(part, {})
                target[path[-1]] = self._parse_env_value(value)
    
    def _parse_env_value(self, value: str) -> Any:
        """Parse environment variable value to appropriate type"""
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            return value
    
    def get(self, key: str, default=None):
        """Get configuration value using dot notation"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value if value is not None else default  


# Global config instance
config_loader = ConfigLoader()
config = config_loader.config


# Test the configuration
if __name__ == "__main__":
    print("=" * 60)
    print("DBIP Configuration Test")
    print("=" * 60)
    
    print(f"\n📌 Environment: {config_loader.env}")
    print(f"📌 App Name: {config_loader.get('app.name', 'Not found')}")
    print(f"📌 App Version: {config_loader.get('app.version', 'Not found')}")
    
    print(f"\n🗄️  Database:")
    print(f"   PostgreSQL Host: {config_loader.get('database.postgres.host', 'Not set')}")
    print(f"   PostgreSQL Port: {config_loader.get('database.postgres.port', 'Not set')}")
    
    print(f"\n⚙️  Pipeline:")
    print(f"   Fusion Threshold: {config_loader.get('pipeline.fusion_threshold', 'Not set')}")
    print(f"   Default Confidence: {config_loader.get('pipeline.default_confidence', 'Not set')}")
    
    # Get lists with defaults to avoid None issues
    entity_types = config_loader.get('entity_types') or []
    relationship_types = config_loader.get('relationship_types') or []
    domains = config_loader.get('domains') or []

    print(f"\n📋  Entity Types: {len(entity_types)} types")
    print(f"📋  Relationship Types: {len(relationship_types)} types")
    print(f"📋  Domains: {len(domains)} domains")
    
    print("\n✅ Configuration test completed!")