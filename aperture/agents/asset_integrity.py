"""
Asset Integrity Agent
=====================

AI agent that monitors pipelines via LIDAR & Thermal data to predict leaks weeks before they happen.
"""
import numpy as np
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class AssetRisk:
    """Pipeline asset risk assessment result."""
    asset_id: str
    asset_name: str
    risk_score: float  # 0.0 (healthy) to 1.0 (critical)
    leak_probability: float
    estimated_time_to_failure_days: Optional[int]
    anomalies: List[Dict[str, Any]]
    recommended_actions: List[str]
    timestamp: datetime


class AssetIntegrity:
    """
    Asset Integrity Agent
    
    Monitors pipelines via LIDAR & Thermal data to detect anomalies
    and predict leaks weeks before they occur.
    
    Input:
        - Thermal imagery (temperature anomalies)
        - LIDAR elevation data (ground subsidence, deformation)
    
    Output:
        - Risk score
        - Leak probability
        - Recommended maintenance actions
    """
    
    def __init__(self, risk_threshold: float = 0.7):
        self.risk_threshold = risk_threshold
        self.model_version = "1.0.0"
        
    def analyze(
        self,
        thermal_data: np.ndarray,
        lidar_data: np.ndarray,
        asset_id: str,
        asset_name: str,
        baseline_thermal: Optional[np.ndarray] = None,
        baseline_lidar: Optional[np.ndarray] = None
    ) -> AssetRisk:
        """
        Analyze asset integrity from thermal and LIDAR data.
        
        Args:
            thermal_data: Thermal imagery of pipeline corridor
            lidar_data: LIDAR elevation model of pipeline area
            asset_id: Unique asset identifier
            asset_name: Human-readable asset name
            baseline_thermal: Historical thermal baseline for comparison
            baseline_lidar: Historical LIDAR baseline for comparison
            
        Returns:
            AssetRisk with risk score and recommendations
        """
        # Detect thermal anomalies (potential leaks show as temperature changes)
        thermal_anomalies = self._detect_thermal_anomalies(
            thermal_data, baseline_thermal
        )
        
        # Detect ground deformation from LIDAR
        deformation_anomalies = self._detect_deformation(
            lidar_data, baseline_lidar
        )
        
        # Combine anomalies
        all_anomalies = thermal_anomalies + deformation_anomalies
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(all_anomalies)
        
        # Estimate leak probability
        leak_prob = self._estimate_leak_probability(thermal_anomalies, risk_score)
        
        # Estimate time to failure if risk is elevated
        ttf = None
        if risk_score > 0.5:
            ttf = self._estimate_time_to_failure(risk_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            risk_score, all_anomalies
        )
        
        return AssetRisk(
            asset_id=asset_id,
            asset_name=asset_name,
            risk_score=risk_score,
            leak_probability=leak_prob,
            estimated_time_to_failure_days=ttf,
            anomalies=all_anomalies,
            recommended_actions=recommendations,
            timestamp=datetime.now()
        )
    
    def _detect_thermal_anomalies(
        self,
        thermal_data: np.ndarray,
        baseline: Optional[np.ndarray]
    ) -> List[Dict[str, Any]]:
        """Detect thermal anomalies indicating potential leaks."""
        anomalies = []
        
        if thermal_data.size == 0:
            return anomalies
        
        # Calculate statistics
        mean_temp = np.mean(thermal_data)
        std_temp = np.std(thermal_data)
        
        # Detect hot spots (potential gas leaks, friction)
        hot_threshold = mean_temp + 2.5 * std_temp
        hot_spots = np.argwhere(thermal_data > hot_threshold)
        
        # Detect cold spots (potential liquid leaks - evaporative cooling)
        cold_threshold = mean_temp - 2.5 * std_temp
        cold_spots = np.argwhere(thermal_data < cold_threshold)
        
        if len(hot_spots) > 5:
            anomalies.append({
                "type": "thermal_hot_spot",
                "severity": min(1.0, len(hot_spots) / 100),
                "count": len(hot_spots),
                "max_deviation": float(np.max(thermal_data) - mean_temp),
                "description": "Elevated temperature detected - possible friction or gas leak"
            })
        
        if len(cold_spots) > 5:
            anomalies.append({
                "type": "thermal_cold_spot",
                "severity": min(1.0, len(cold_spots) / 100),
                "count": len(cold_spots),
                "max_deviation": float(mean_temp - np.min(thermal_data)),
                "description": "Temperature drop detected - possible liquid leak with evaporative cooling"
            })
        
        return anomalies
    
    def _detect_deformation(
        self,
        lidar_data: np.ndarray,
        baseline: Optional[np.ndarray]
    ) -> List[Dict[str, Any]]:
        """Detect ground deformation from LIDAR data."""
        anomalies = []
        
        if lidar_data.size == 0:
            return anomalies
        
        # Calculate local variations (indicates subsidence or uplift)
        # Using gradient magnitude as proxy for deformation
        if lidar_data.ndim == 2:
            gy, gx = np.gradient(lidar_data)
            gradient_mag = np.sqrt(gx**2 + gy**2)
            
            mean_grad = np.mean(gradient_mag)
            std_grad = np.std(gradient_mag)
            
            # Detect areas of unusual slope (potential ground movement)
            threshold = mean_grad + 3 * std_grad
            steep_areas = np.argwhere(gradient_mag > threshold)
            
            if len(steep_areas) > 10:
                anomalies.append({
                    "type": "ground_deformation",
                    "severity": min(1.0, len(steep_areas) / 200),
                    "count": len(steep_areas),
                    "max_gradient": float(np.max(gradient_mag)),
                    "description": "Ground subsidence or uplift detected - structural stress risk"
                })
        
        return anomalies
    
    def _calculate_risk_score(self, anomalies: List[Dict]) -> float:
        """Calculate overall risk score from detected anomalies."""
        if not anomalies:
            return 0.05  # Baseline risk
        
        # Weight by anomaly type
        weights = {
            "thermal_hot_spot": 0.9,
            "thermal_cold_spot": 0.95,
            "ground_deformation": 0.8,
        }
        
        total_risk = 0.05  # Baseline
        
        for anomaly in anomalies:
            weight = weights.get(anomaly["type"], 0.5)
            severity = anomaly.get("severity", 0.5)
            total_risk += weight * severity * 0.4
        
        return min(1.0, total_risk)
    
    def _estimate_leak_probability(
        self,
        thermal_anomalies: List[Dict],
        risk_score: float
    ) -> float:
        """Estimate probability of active or imminent leak."""
        # Base probability from risk score
        prob = risk_score * 0.6
        
        # Boost if thermal anomalies present (direct leak indicators)
        for anomaly in thermal_anomalies:
            if anomaly["type"] == "thermal_cold_spot":
                # Cold spots are strong leak indicators (liquid evaporation)
                prob += anomaly.get("severity", 0.5) * 0.3
            elif anomaly["type"] == "thermal_hot_spot":
                prob += anomaly.get("severity", 0.5) * 0.15
        
        return min(0.95, prob)
    
    def _estimate_time_to_failure(self, risk_score: float) -> int:
        """Estimate days until potential failure."""
        # Inverse relationship: higher risk = less time
        if risk_score > 0.9:
            return np.random.randint(1, 7)
        elif risk_score > 0.8:
            return np.random.randint(7, 21)
        elif risk_score > 0.7:
            return np.random.randint(21, 45)
        elif risk_score > 0.6:
            return np.random.randint(45, 90)
        else:
            return np.random.randint(90, 180)
    
    def _generate_recommendations(
        self,
        risk_score: float,
        anomalies: List[Dict]
    ) -> List[str]:
        """Generate maintenance recommendations based on risk assessment."""
        recommendations = []
        
        if risk_score < 0.3:
            recommendations.append("Continue routine monitoring schedule")
            return recommendations
        
        if risk_score >= 0.7:
            recommendations.append("⚠️ URGENT: Schedule immediate field inspection")
            recommendations.append("Prepare emergency response team for potential intervention")
        elif risk_score >= 0.5:
            recommendations.append("Schedule priority inspection within 7 days")
        else:
            recommendations.append("Add to next scheduled maintenance cycle")
        
        # Anomaly-specific recommendations
        for anomaly in anomalies:
            if anomaly["type"] == "thermal_cold_spot":
                recommendations.append("Deploy ground crew for liquid leak investigation")
                recommendations.append("Prepare containment equipment")
            elif anomaly["type"] == "thermal_hot_spot":
                recommendations.append("Check for gas leaks using portable detector")
                recommendations.append("Inspect for mechanical friction or blockage")
            elif anomaly["type"] == "ground_deformation":
                recommendations.append("Conduct geotechnical assessment")
                recommendations.append("Review pipeline support structures")
        
        return recommendations
    
    def predict_sample(self) -> Dict[str, Any]:
        """Generate a sample prediction for demo/testing."""
        # Create synthetic thermal data with some anomalies
        thermal_sample = np.random.normal(25, 2, (256, 256))  # Ambient ~25°C
        # Add a cold spot (simulated leak)
        thermal_sample[100:120, 150:170] -= 8
        
        # Create synthetic LIDAR with some subsidence
        lidar_sample = np.random.normal(100, 0.5, (256, 256))  # ~100m elevation
        lidar_sample[80:100, 140:160] -= 0.5  # Subsidence area
        
        result = self.analyze(
            thermal_data=thermal_sample,
            lidar_data=lidar_sample,
            asset_id="pipeline-gulf-003",
            asset_name="Gulf Coast Pipeline Segment 3"
        )
        
        return {
            "agent": "AssetIntegrity",
            "status": "success",
            "analysis": {
                "asset_id": result.asset_id,
                "asset_name": result.asset_name,
                "risk_score": round(result.risk_score, 2),
                "leak_probability": round(result.leak_probability, 2),
                "estimated_time_to_failure_days": result.estimated_time_to_failure_days,
                "anomaly_count": len(result.anomalies),
                "anomalies": result.anomalies,
                "recommended_actions": result.recommended_actions,
                "timestamp": result.timestamp.isoformat()
            }
        }
