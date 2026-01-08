"""
Aperture Test Suite - Integration Tests
=======================================

End-to-end integration tests for the complete Aperture pipeline.
"""
import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aperture.config import ApertureConfig, config
from aperture.agents import YieldForecaster, SupplyChainSentinel, AssetIntegrity
from aperture.processing import SARProcessor, SensorFusion, PredictiveInference
from aperture.integrations import BhoonidhiClient, SyntheticDataGenerator


class TestEndToEndPipeline:
    """End-to-end pipeline tests."""
    
    def setup_method(self):
        self.generator = SyntheticDataGenerator(seed=42)
        self.sar_processor = SARProcessor(use_gpu=False)
        self.fusion = SensorFusion()
    
    def test_agriculture_pipeline(self):
        """Test complete agriculture/yield prediction pipeline."""
        # 1. Generate synthetic SAR and hyperspectral
        sar_scene = self.generator.generate_sar_scene(
            shape=(256, 256),
            band="L",
            scenario="agriculture"
        )
        hyper_scene = self.generator.generate_hyperspectral_scene(
            shape=(256, 256),
            scenario="vegetation"
        )
        
        # 2. Process SAR
        processed_sar, sar_result = self.sar_processor.process_scene(
            raw_data=sar_scene.data,
            scene_id=sar_scene.scene_id
        )
        
        # 3. Fuse sensors
        fused = self.fusion.fuse(
            sar_data=processed_sar,
            hyperspectral_data=hyper_scene.data
        )
        
        # 4. Run yield forecaster
        yield_agent = YieldForecaster()
        prediction = yield_agent.analyze(
            sar_data=processed_sar,
            hyperspectral_data=hyper_scene.data,
            region_id="integration-test",
            crop_type="wheat"
        )
        
        # Verify complete pipeline worked
        assert sar_result.processing_time_ms > 0
        assert fused.fused_data is not None
        assert prediction.predicted_yield_tons_ha > 0
    
    def test_port_monitoring_pipeline(self):
        """Test complete port/supply chain pipeline."""
        # 1. Generate synthetic port SAR
        sar_scene = self.generator.generate_sar_scene(
            shape=(512, 512),
            band="S",
            scenario="port"
        )
        
        # 2. Process SAR
        processed_sar, _ = self.sar_processor.process_scene(
            raw_data=sar_scene.data,
            scene_id=sar_scene.scene_id
        )
        
        # 3. Run supply chain agent
        supply_agent = SupplyChainSentinel()
        analysis = supply_agent.analyze(
            sar_data=processed_sar,
            port_id="integration-port",
            port_name="Integration Test Port"
        )
        
        assert analysis.vessel_count >= 0
        assert len(analysis.predicted_delays) > 0
    
    def test_pipeline_monitoring_pipeline(self):
        """Test complete pipeline/asset integrity pipeline."""
        # 1. Generate complete dataset for pipeline scenario
        dataset = self.generator.generate_complete_dataset(
            shape=(256, 256),
            scenario="pipeline"
        )
        
        # 2. Fuse thermal and LIDAR
        fused = self.fusion.fuse(
            thermal_data=dataset["thermal"].data,
            lidar_data=dataset["lidar"].data
        )
        
        # 3. Run asset integrity agent
        asset_agent = AssetIntegrity()
        risk = asset_agent.analyze(
            thermal_data=dataset["thermal"].data,
            lidar_data=dataset["lidar"].data,
            asset_id="integration-pipeline",
            asset_name="Integration Test Pipeline"
        )
        
        assert risk.risk_score >= 0
        assert len(risk.recommended_actions) > 0


class TestConfiguration:
    """Tests for platform configuration."""
    
    def test_default_config(self):
        """Test default configuration values."""
        assert config.platform_name == "Aperture"
        assert config.version == "0.1.0"
        assert config.target_latency_ms > 0
    
    def test_config_to_dict(self):
        """Test config serialization."""
        d = config.to_dict()
        
        assert "platform_name" in d
        assert "version" in d
        assert "use_gpu" in d
    
    def test_custom_config(self):
        """Test custom configuration."""
        custom = ApertureConfig(
            target_latency_ms=50,
            use_synthetic_data=True
        )
        
        assert custom.target_latency_ms == 50
        assert custom.use_synthetic_data is True


class TestBhoonidhiIntegration:
    """Tests for Bhoonidhi client."""
    
    def setup_method(self):
        self.client = BhoonidhiClient()
    
    def test_client_status(self):
        """Test client status without credentials."""
        status = self.client.status()
        
        assert "has_credentials" in status
        assert "sample_data_available" in status
        assert status["sample_data_available"] is True
    
    def test_get_sample_scenes(self):
        """Test getting sample scene metadata."""
        samples = self.client.get_sample_scenes()
        
        assert len(samples) > 0
        assert "id" in samples[0]
        assert "bbox" in samples[0]


class TestSyntheticDataGenerator:
    """Tests for synthetic data generator."""
    
    def setup_method(self):
        self.generator = SyntheticDataGenerator(seed=123)
    
    def test_generate_sar_all_scenarios(self):
        """Test SAR generation for all scenarios."""
        for scenario in ["generic", "agriculture", "port", "pipeline"]:
            scene = self.generator.generate_sar_scene(scenario=scenario)
            assert scene.data is not None
            assert scene.scene_type.startswith("SAR")
    
    def test_generate_hyperspectral(self):
        """Test hyperspectral generation."""
        scene = self.generator.generate_hyperspectral_scene(num_bands=10)
        
        assert scene.data.shape[0] == 10
        assert "wavelengths_nm" in scene.metadata
    
    def test_generate_complete_dataset(self):
        """Test complete dataset generation."""
        dataset = self.generator.generate_complete_dataset()
        
        assert "sar_l" in dataset
        assert "sar_s" in dataset
        assert "hyperspectral" in dataset
        assert "thermal" in dataset
        assert "lidar" in dataset
    
    def test_reproducibility_with_seed(self):
        """Test that seed produces reproducible results."""
        gen1 = SyntheticDataGenerator(seed=999)
        gen2 = SyntheticDataGenerator(seed=999)
        
        scene1 = gen1.generate_sar_scene(shape=(64, 64))
        scene2 = gen2.generate_sar_scene(shape=(64, 64))
        
        np.testing.assert_array_equal(scene1.data, scene2.data)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
