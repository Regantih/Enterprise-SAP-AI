"""
Supply Chain Sentinel Agent
============================

AI agent that provides real-time port congestion scoring and predicts shipping delays 72 hours ahead.
"""
import numpy as np
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class CongestionScore:
    """Port congestion analysis result."""
    port_id: str
    port_name: str
    congestion_level: float  # 0.0 (empty) to 1.0 (fully congested)
    vessel_count: int
    average_wait_hours: float
    prediction_horizon_hours: int
    predicted_delays: List[Dict[str, Any]]
    timestamp: datetime


class SupplyChainSentinel:
    """
    Supply Chain Sentinel Agent
    
    Provides real-time port congestion scoring and predicts shipping delays.
    
    Input:
        - SAR imagery of ports (vessel detection)
        - Vessel tracking data (AIS)
    
    Output:
        - Congestion score
        - 72-hour delay prediction
    """
    
    def __init__(self, prediction_horizon_hours: int = 72):
        self.prediction_horizon_hours = prediction_horizon_hours
        self.model_version = "1.0.0"
        
    def analyze(
        self,
        sar_data: np.ndarray,
        port_id: str,
        port_name: str,
        port_capacity: int = 50,
        ais_data: Optional[List[Dict]] = None
    ) -> CongestionScore:
        """
        Analyze port congestion from satellite data.
        
        Args:
            sar_data: SAR image of port area
            port_id: Unique port identifier
            port_name: Human-readable port name
            port_capacity: Maximum vessel capacity
            ais_data: Optional AIS vessel tracking data
            
        Returns:
            CongestionScore with predictions
        """
        # Detect vessels in SAR imagery
        vessel_count = self._detect_vessels(sar_data)
        
        # Calculate congestion level
        congestion = min(1.0, vessel_count / max(port_capacity, 1))
        
        # Estimate wait times
        average_wait = self._estimate_wait_time(congestion, vessel_count)
        
        # Predict delays for the next 72 hours
        predicted_delays = self._predict_delays(
            congestion, vessel_count, self.prediction_horizon_hours
        )
        
        return CongestionScore(
            port_id=port_id,
            port_name=port_name,
            congestion_level=congestion,
            vessel_count=vessel_count,
            average_wait_hours=average_wait,
            prediction_horizon_hours=self.prediction_horizon_hours,
            predicted_delays=predicted_delays,
            timestamp=datetime.now()
        )
    
    def _detect_vessels(self, sar_data: np.ndarray) -> int:
        """
        Detect vessels in SAR imagery using bright target detection.
        
        SAR images show vessels as bright spots due to metal reflectance.
        """
        if sar_data.size == 0:
            return 0
        
        # Simple threshold-based detection (would use deep learning in production)
        threshold = np.mean(sar_data) + 2 * np.std(sar_data)
        bright_pixels = np.sum(sar_data > threshold)
        
        # Estimate vessel count (assume ~100 pixels per vessel in typical resolution)
        estimated_vessels = int(bright_pixels / 100)
        
        return max(0, min(estimated_vessels, 200))  # Cap at reasonable maximum
    
    def _estimate_wait_time(self, congestion: float, vessel_count: int) -> float:
        """Estimate average wait time based on congestion level."""
        # Base processing time per vessel (hours)
        base_time = 24
        
        # Congestion multiplier (exponential increase at high congestion)
        if congestion < 0.5:
            multiplier = 1.0 + congestion
        elif congestion < 0.8:
            multiplier = 1.5 + (congestion - 0.5) * 2
        else:
            multiplier = 2.1 + (congestion - 0.8) * 5  # Severe delays
        
        wait_time = (base_time * multiplier * congestion)
        return round(wait_time, 1)
    
    def _predict_delays(
        self,
        current_congestion: float,
        vessel_count: int,
        horizon_hours: int
    ) -> List[Dict[str, Any]]:
        """Predict congestion and delays over the forecast horizon."""
        predictions = []
        
        # Generate predictions at 12-hour intervals
        intervals = horizon_hours // 12
        
        for i in range(intervals):
            hours_ahead = (i + 1) * 12
            
            # Simple decay model (congestion gradually reduces if no new arrivals)
            decay_factor = 0.95 ** (hours_ahead / 24)
            # Random variation for new arrivals
            variation = np.random.normal(0, 0.05)
            
            predicted_congestion = np.clip(
                current_congestion * decay_factor + variation,
                0, 1
            )
            
            predicted_wait = self._estimate_wait_time(
                predicted_congestion,
                int(vessel_count * decay_factor)
            )
            
            # Delay risk assessment
            if predicted_congestion > 0.8:
                risk = "critical"
            elif predicted_congestion > 0.6:
                risk = "high"
            elif predicted_congestion > 0.4:
                risk = "moderate"
            else:
                risk = "low"
            
            predictions.append({
                "hours_ahead": hours_ahead,
                "predicted_congestion": round(float(predicted_congestion), 3),
                "predicted_wait_hours": predicted_wait,
                "delay_risk": risk,
                "timestamp": (datetime.now() + timedelta(hours=hours_ahead)).isoformat()
            })
        
        return predictions
    
    def predict_sample(self) -> Dict[str, Any]:
        """Generate a sample prediction for demo/testing."""
        # Create synthetic SAR data with some bright spots (vessels)
        sar_sample = np.random.normal(-18, 4, (1024, 1024))
        # Add vessel signatures
        for _ in range(35):
            x, y = np.random.randint(0, 1000, 2)
            sar_sample[x:x+10, y:y+10] += 25  # Bright vessel signature
        
        result = self.analyze(
            sar_data=sar_sample,
            port_id="port-sgp-001",
            port_name="Singapore Strait",
            port_capacity=80
        )
        
        return {
            "agent": "SupplyChainSentinel",
            "status": "success",
            "analysis": {
                "port_id": result.port_id,
                "port_name": result.port_name,
                "congestion_level": round(result.congestion_level, 2),
                "vessel_count": result.vessel_count,
                "average_wait_hours": result.average_wait_hours,
                "prediction_horizon_hours": result.prediction_horizon_hours,
                "predicted_delays": result.predicted_delays[:3],  # First 3 intervals
                "timestamp": result.timestamp.isoformat()
            }
        }
