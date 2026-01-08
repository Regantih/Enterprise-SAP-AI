"""
Aperture Platform Configuration
"""
import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ApertureConfig:
    """Central configuration for Aperture platform."""
    
    # Platform settings
    platform_name: str = "Aperture"
    version: str = "0.1.0"
    
    # Processing settings
    use_gpu: bool = True
    target_latency_ms: int = 100  # Target processing latency in milliseconds
    batch_size: int = 32
    
    # Bhoonidhi API (NISAR data access)
    bhoonidhi_api_url: str = "https://bhoonidhi.nrsc.gov.in/api"
    bhoonidhi_user: Optional[str] = field(default_factory=lambda: os.environ.get("BHOONIDHI_USER"))
    bhoonidhi_password: Optional[str] = field(default_factory=lambda: os.environ.get("BHOONIDHI_PASSWORD"))
    
    # Synthetic data settings (for development)
    use_synthetic_data: bool = True  # Default to synthetic until credentials provided
    synthetic_image_size: tuple = (512, 512)
    
    # Edge processing
    edge_node_id: str = "dgx-spark-001"
    max_scenes_per_batch: int = 10
    
    # AI Agent settings
    agent_yield_window_days: int = 30
    agent_supply_chain_horizon_hours: int = 72
    agent_asset_risk_threshold: float = 0.7
    
    # Web UI
    web_port: int = 8001
    
    @property
    def has_bhoonidhi_credentials(self) -> bool:
        """Check if Bhoonidhi API credentials are configured."""
        return bool(self.bhoonidhi_user and self.bhoonidhi_password)
    
    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            "platform_name": self.platform_name,
            "version": self.version,
            "use_gpu": self.use_gpu,
            "target_latency_ms": self.target_latency_ms,
            "use_synthetic_data": self.use_synthetic_data,
            "has_bhoonidhi_credentials": self.has_bhoonidhi_credentials,
            "edge_node_id": self.edge_node_id,
        }


# Global config instance
config = ApertureConfig()
