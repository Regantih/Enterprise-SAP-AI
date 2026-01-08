"""
Yield Forecaster Agent
======================

AI agent that fuses hyperspectral and SAR data to predict crop yield 30 days in advance.
"""
import numpy as np
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class YieldPrediction:
    """Crop yield prediction result."""
    region_id: str
    crop_type: str
    predicted_yield_tons_ha: float
    confidence: float  # 0.0 to 1.0
    prediction_date: datetime
    target_date: datetime  # 30 days ahead
    factors: Dict[str, float]  # Contributing factors


class YieldForecaster:
    """
    Yield Forecaster Agent
    
    Fuses hyperspectral & SAR data to predict crop yield 30 days in advance.
    
    Input:
        - L-band SAR: Soil moisture penetration depth
        - Hyperspectral: Vegetation indices (NDVI, EVI, LAI)
    
    Output:
        - Yield prediction with confidence interval
    """
    
    def __init__(self, prediction_window_days: int = 30):
        self.prediction_window_days = prediction_window_days
        self.model_version = "1.0.0"
        
    def analyze(
        self,
        sar_data: np.ndarray,
        hyperspectral_data: np.ndarray,
        region_id: str,
        crop_type: str = "wheat"
    ) -> YieldPrediction:
        """
        Analyze satellite data to predict crop yield.
        
        Args:
            sar_data: L-band SAR image (soil moisture)
            hyperspectral_data: Multispectral/hyperspectral image
            region_id: Identifier for the agricultural region
            crop_type: Type of crop (wheat, rice, corn, etc.)
            
        Returns:
            YieldPrediction with forecast and confidence
        """
        # Extract features from SAR (soil moisture indicator)
        soil_moisture = self._extract_soil_moisture(sar_data)
        
        # Extract vegetation indices from hyperspectral
        vegetation_indices = self._compute_vegetation_indices(hyperspectral_data)
        
        # Fuse features and predict
        yield_estimate, confidence, factors = self._predict_yield(
            soil_moisture, vegetation_indices, crop_type
        )
        
        return YieldPrediction(
            region_id=region_id,
            crop_type=crop_type,
            predicted_yield_tons_ha=yield_estimate,
            confidence=confidence,
            prediction_date=datetime.now(),
            target_date=datetime.now() + timedelta(days=self.prediction_window_days),
            factors=factors
        )
    
    def _extract_soil_moisture(self, sar_data: np.ndarray) -> float:
        """Extract soil moisture indicator from L-band SAR backscatter."""
        if sar_data.size == 0:
            return 0.5  # Default neutral value
        
        # Normalized backscatter coefficient (simplified model)
        # SAR data is typically in dB scale, range roughly -30 to 0
        backscatter_mean = np.nanmean(sar_data)
        if np.isnan(backscatter_mean):
            return 0.5  # Default for invalid data
        # Map to soil moisture (0-1 range)
        soil_moisture = np.clip((backscatter_mean + 25) / 35, 0, 1)
        return float(soil_moisture)
    
    def _compute_vegetation_indices(self, hyperspectral_data: np.ndarray) -> Dict[str, float]:
        """Compute vegetation indices from hyperspectral data."""
        if hyperspectral_data.size == 0 or hyperspectral_data.shape[0] < 4:
            return {"ndvi": 0.5, "evi": 0.5, "lai": 2.0}
        
        # Assume bands: [Blue, Green, Red, NIR, ...]
        red = hyperspectral_data[2]
        nir = hyperspectral_data[3]
        
        # NDVI: Normalized Difference Vegetation Index
        ndvi = np.mean((nir - red) / (nir + red + 1e-8))
        ndvi = np.clip(ndvi, -1, 1)
        
        # EVI: Enhanced Vegetation Index (simplified)
        blue = hyperspectral_data[0]
        evi = np.mean(2.5 * (nir - red) / (nir + 6*red - 7.5*blue + 1))
        evi = np.clip(evi, -1, 1)
        
        # LAI: Leaf Area Index (empirical relationship with NDVI)
        lai = 3.618 * float(ndvi) - 0.118
        lai = max(0, lai)
        
        return {
            "ndvi": float(ndvi),
            "evi": float(evi),
            "lai": float(lai)
        }
    
    def _predict_yield(
        self,
        soil_moisture: float,
        vegetation_indices: Dict[str, float],
        crop_type: str
    ) -> tuple:
        """
        Predict yield using fused features.
        
        Returns (yield_tons_ha, confidence, factors)
        """
        # Crop-specific baseline yields (tons/hectare)
        baseline_yields = {
            "wheat": 3.5,
            "rice": 4.5,
            "corn": 10.0,
            "soybean": 2.8,
            "cotton": 1.5,
        }
        
        baseline = baseline_yields.get(crop_type, 3.0)
        
        # Factor contributions
        ndvi_factor = 0.5 + vegetation_indices["ndvi"] * 0.5
        moisture_factor = 0.7 + soil_moisture * 0.6
        lai_factor = min(1.3, 0.6 + vegetation_indices["lai"] / 5)
        
        # Predict yield
        yield_estimate = baseline * ndvi_factor * moisture_factor * lai_factor
        
        # Confidence based on data quality indicators
        confidence = 0.85 - abs(vegetation_indices["ndvi"] - 0.6) * 0.3
        confidence = np.clip(confidence, 0.5, 0.95)
        
        factors = {
            "baseline_yield": baseline,
            "ndvi_contribution": ndvi_factor,
            "soil_moisture_contribution": moisture_factor,
            "lai_contribution": lai_factor,
        }
        
        return float(yield_estimate), float(confidence), factors
    
    def predict_sample(self) -> Dict[str, Any]:
        """Generate a sample prediction for demo/testing."""
        # Create synthetic data
        sar_sample = np.random.normal(-15, 3, (512, 512))
        hyperspectral_sample = np.random.uniform(0, 1, (10, 512, 512))
        # Simulate healthy vegetation
        hyperspectral_sample[3] = hyperspectral_sample[2] * 2.5  # NIR > Red
        
        prediction = self.analyze(
            sar_data=sar_sample,
            hyperspectral_data=hyperspectral_sample,
            region_id="sample-region-001",
            crop_type="wheat"
        )
        
        return {
            "agent": "YieldForecaster",
            "status": "success",
            "prediction": {
                "region_id": prediction.region_id,
                "crop_type": prediction.crop_type,
                "predicted_yield_tons_ha": round(prediction.predicted_yield_tons_ha, 2),
                "confidence": round(prediction.confidence, 2),
                "target_date": prediction.target_date.isoformat(),
                "factors": {k: round(v, 3) for k, v in prediction.factors.items()}
            }
        }
