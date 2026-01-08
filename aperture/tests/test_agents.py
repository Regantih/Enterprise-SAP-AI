"""
Aperture Test Suite - AI Agents
================================

Unit tests for Yield Forecaster, Supply Chain Sentinel, and Asset Integrity agents.
"""
import pytest
import numpy as np
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aperture.agents import YieldForecaster, SupplyChainSentinel, AssetIntegrity


class TestYieldForecaster:
    """Tests for Yield Forecaster Agent."""
    
    def setup_method(self):
        self.agent = YieldForecaster(prediction_window_days=30)
    
    def test_initialization(self):
        """Test agent initializes correctly."""
        assert self.agent.prediction_window_days == 30
        assert self.agent.model_version == "1.0.0"
    
    def test_analyze_with_valid_data(self):
        """Test analysis with valid SAR and hyperspectral data."""
        sar = np.random.normal(-15, 3, (256, 256))
        hyperspectral = np.random.uniform(0, 1, (4, 256, 256))
        
        result = self.agent.analyze(
            sar_data=sar,
            hyperspectral_data=hyperspectral,
            region_id="test-region-001",
            crop_type="wheat"
        )
        
        assert result.region_id == "test-region-001"
        assert result.crop_type == "wheat"
        assert 0 < result.predicted_yield_tons_ha < 20
        assert 0 <= result.confidence <= 1
        assert result.factors is not None
    
    def test_analyze_different_crops(self):
        """Test predictions for different crop types."""
        sar = np.random.normal(-15, 3, (128, 128))
        hyperspectral = np.random.uniform(0, 1, (4, 128, 128))
        
        for crop in ["wheat", "rice", "corn", "soybean"]:
            result = self.agent.analyze(
                sar_data=sar,
                hyperspectral_data=hyperspectral,
                region_id="test",
                crop_type=crop
            )
            assert result.predicted_yield_tons_ha > 0
    
    def test_predict_sample(self):
        """Test sample prediction generates valid output."""
        result = self.agent.predict_sample()
        
        assert result["agent"] == "YieldForecaster"
        assert result["status"] == "success"
        assert "prediction" in result
        assert "predicted_yield_tons_ha" in result["prediction"]
    
    def test_empty_data_handling(self):
        """Test handling of empty data arrays."""
        result = self.agent.analyze(
            sar_data=np.array([]),
            hyperspectral_data=np.array([]),
            region_id="empty-test",
            crop_type="wheat"
        )
        # Should return default/fallback values
        assert result.predicted_yield_tons_ha >= 0


class TestSupplyChainSentinel:
    """Tests for Supply Chain Sentinel Agent."""
    
    def setup_method(self):
        self.agent = SupplyChainSentinel(prediction_horizon_hours=72)
    
    def test_initialization(self):
        """Test agent initializes correctly."""
        assert self.agent.prediction_horizon_hours == 72
        assert self.agent.model_version == "1.0.0"
    
    def test_analyze_port_congestion(self):
        """Test port congestion analysis."""
        # Create SAR with vessel signatures
        sar = np.random.normal(-18, 4, (512, 512))
        for _ in range(30):
            x, y = np.random.randint(10, 500, 2)
            sar[x:x+10, y:y+10] += 25
        
        result = self.agent.analyze(
            sar_data=sar,
            port_id="port-test-001",
            port_name="Test Port",
            port_capacity=50
        )
        
        assert result.port_id == "port-test-001"
        assert result.port_name == "Test Port"
        assert 0 <= result.congestion_level <= 1
        assert result.vessel_count >= 0
        assert len(result.predicted_delays) > 0
    
    def test_predict_sample(self):
        """Test sample prediction."""
        result = self.agent.predict_sample()
        
        assert result["agent"] == "SupplyChainSentinel"
        assert result["status"] == "success"
        assert "analysis" in result
    
    def test_delay_predictions(self):
        """Test that delay predictions cover the forecast horizon."""
        sar = np.random.normal(-18, 4, (256, 256))
        result = self.agent.analyze(
            sar_data=sar,
            port_id="test",
            port_name="Test"
        )
        
        # Should have predictions at 12-hour intervals
        assert len(result.predicted_delays) == 72 // 12


class TestAssetIntegrity:
    """Tests for Asset Integrity Agent."""
    
    def setup_method(self):
        self.agent = AssetIntegrity(risk_threshold=0.7)
    
    def test_initialization(self):
        """Test agent initializes correctly."""
        assert self.agent.risk_threshold == 0.7
        assert self.agent.model_version == "1.0.0"
    
    def test_analyze_healthy_asset(self):
        """Test analysis of healthy asset (no anomalies)."""
        # Uniform thermal and lidar - no anomalies
        thermal = np.ones((128, 128)) * 25
        lidar = np.ones((128, 128)) * 100
        
        result = self.agent.analyze(
            thermal_data=thermal,
            lidar_data=lidar,
            asset_id="asset-001",
            asset_name="Test Pipeline"
        )
        
        assert result.risk_score < 0.5
        assert len(result.anomalies) == 0
    
    def test_analyze_with_leak(self):
        """Test analysis with thermal anomaly (simulated leak)."""
        thermal = np.random.normal(25, 2, (128, 128))
        # Add cold spot (leak signature)
        thermal[50:70, 50:70] -= 15
        
        lidar = np.random.normal(100, 0.5, (128, 128))
        
        result = self.agent.analyze(
            thermal_data=thermal,
            lidar_data=lidar,
            asset_id="leak-test",
            asset_name="Leak Test Pipeline"
        )
        
        assert result.risk_score > 0.3
        assert len(result.anomalies) > 0
        assert any(a["type"] == "thermal_cold_spot" for a in result.anomalies)
    
    def test_recommendations_generated(self):
        """Test that recommendations are generated for high-risk assets."""
        thermal = np.random.normal(25, 5, (128, 128))
        thermal[40:80, 40:80] -= 12  # Large anomaly
        lidar = np.random.normal(100, 1, (128, 128))
        
        result = self.agent.analyze(
            thermal_data=thermal,
            lidar_data=lidar,
            asset_id="risk-test",
            asset_name="High Risk Pipeline"
        )
        
        assert len(result.recommended_actions) > 0
    
    def test_predict_sample(self):
        """Test sample prediction."""
        result = self.agent.predict_sample()
        
        assert result["agent"] == "AssetIntegrity"
        assert result["status"] == "success"
        assert "analysis" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
