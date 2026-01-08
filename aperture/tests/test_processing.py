"""
Aperture Test Suite - Processing Pipeline
==========================================

Tests for SAR processor, sensor fusion, and inference engine.
"""
import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aperture.processing import SARProcessor, SensorFusion, PredictiveInference
from aperture.processing.sensor_fusion import create_sample_fused_dataset


class TestSARProcessor:
    """Tests for SAR Processor."""
    
    def setup_method(self):
        self.processor = SARProcessor(use_gpu=False)  # CPU for testing
    
    def test_initialization(self):
        """Test processor initializes correctly."""
        assert self.processor is not None
    
    def test_process_scene(self):
        """Test basic scene processing."""
        raw_data = np.random.random((256, 256)).astype(np.float32) * 100
        
        processed, result = self.processor.process_scene(
            raw_data=raw_data,
            scene_id="test-scene-001",
            band="L"
        )
        
        assert processed.shape == raw_data.shape
        assert result.scene_id == "test-scene-001"
        assert result.processing_time_ms > 0
        assert result.metadata["band"] == "L"
    
    def test_speckle_filter(self):
        """Test that speckle filter reduces noise."""
        # Create noisy data
        raw_data = np.random.exponential(1, (128, 128)).astype(np.float32)
        
        filtered, _ = self.processor.process_scene(
            raw_data=raw_data,
            scene_id="speckle-test",
            apply_speckle_filter=True
        )
        
        # Filtered data should have lower variance
        assert np.std(filtered) < np.std(10 * np.log10(raw_data + 1e-10))
    
    def test_soil_moisture_extraction(self):
        """Test soil moisture index extraction."""
        sar_db = np.random.normal(-15, 5, (64, 64))
        
        moisture = self.processor.extract_soil_moisture(sar_db, band="L")
        
        assert moisture.shape == sar_db.shape
        assert np.all(moisture >= 0)
        assert np.all(moisture <= 1)
    
    def test_change_detection(self):
        """Test change detection between scenes."""
        before = np.random.normal(-15, 3, (64, 64))
        after = before.copy()
        # Add change in a region
        after[20:40, 20:40] += 8
        
        change = self.processor.detect_change(before, after, threshold=3.0)
        
        # Should detect positive change in modified region
        assert np.any(change[20:40, 20:40] > 0)
    
    def test_benchmark(self):
        """Test benchmark execution."""
        result = self.processor.benchmark(size=128)
        
        assert "cpu_time_ms" in result
        assert result["cpu_time_ms"] > 0
        assert "image_size" in result


class TestSensorFusion:
    """Tests for Sensor Fusion."""
    
    def setup_method(self):
        self.fusion = SensorFusion(target_resolution_m=10.0)
    
    def test_fuse_single_source(self):
        """Test fusion with single data source."""
        sar = np.random.random((128, 128))
        
        result = self.fusion.fuse(sar_data=sar)
        
        assert result.fused_data.shape == (1, 128, 128)
        assert "SAR_backscatter" in result.channel_names
    
    def test_fuse_multiple_sources(self):
        """Test fusion with multiple data sources."""
        sar = np.random.random((128, 128))
        thermal = np.random.random((128, 128))
        hyperspectral = np.random.random((4, 128, 128))
        
        result = self.fusion.fuse(
            sar_data=sar,
            hyperspectral_data=hyperspectral,
            thermal_data=thermal
        )
        
        # SAR + 4 spectral + thermal = 6 channels
        assert result.fused_data.shape[0] == 6
        assert len(result.channel_names) == 6
    
    def test_fuse_with_lidar(self):
        """Test fusion with LIDAR adds slope channel."""
        lidar = np.random.random((64, 64)) * 100
        
        result = self.fusion.fuse(lidar_data=lidar)
        
        # Elevation + slope = 2 channels
        assert "elevation" in result.channel_names
        assert "slope" in result.channel_names
    
    def test_resampling(self):
        """Test that different sized inputs are resampled."""
        sar = np.random.random((64, 64))
        thermal = np.random.random((128, 128))
        
        result = self.fusion.fuse(sar_data=sar, thermal_data=thermal)
        
        # Should resample to largest dimension
        assert result.fused_data.shape[1:] == (128, 128)
    
    def test_feature_extraction(self):
        """Test feature extraction from fused dataset."""
        fused = create_sample_fused_dataset()
        
        features = self.fusion.extract_features(fused)
        
        assert "ndvi" in features or len(features) > 0
    
    def test_create_sample_fused_dataset(self):
        """Test sample dataset creation."""
        sample = create_sample_fused_dataset()
        
        assert sample.fused_data is not None
        assert len(sample.channel_names) > 0


class TestPredictiveInference:
    """Tests for Predictive Inference Engine."""
    
    def setup_method(self):
        self.inference = PredictiveInference(use_gpu=False)
    
    def test_predict_yield(self):
        """Test yield prediction."""
        fused = np.random.random((10, 64, 64))
        
        result = self.inference.predict_yield(fused, crop_type="wheat")
        
        assert result.prediction["crop_type"] == "wheat"
        assert "yield_tons_per_hectare" in result.prediction
        assert 0 < result.confidence <= 1
        assert result.inference_time_ms > 0
    
    def test_detect_anomalies(self):
        """Test anomaly detection."""
        data = np.random.normal(0, 1, (128, 128))
        # Add anomaly
        data[50:60, 50:60] = 10
        
        result = self.inference.detect_anomalies(data)
        
        assert result.prediction["anomaly_count"] > 0
        assert "severity" in result.prediction
    
    def test_assess_risk(self):
        """Test risk assessment."""
        data = np.random.random((64, 64))
        
        result = self.inference.assess_risk(data, asset_type="pipeline")
        
        assert result.prediction["asset_type"] == "pipeline"
        assert "risk_score" in result.prediction
        assert "risk_level" in result.prediction
        assert "recommended_action" in result.prediction
    
    def test_benchmark(self):
        """Test inference benchmark."""
        result = self.inference.benchmark(iterations=10)
        
        assert result["iterations"] == 10
        assert result["mean_time_ms"] > 0
        assert "throughput_per_sec" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
