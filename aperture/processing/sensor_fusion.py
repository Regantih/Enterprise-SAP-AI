"""
Sensor Fusion
=============

Multi-sensor data fusion for SAR, Hyperspectral, Thermal, and LIDAR data.
"""
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass


@dataclass
class FusedDataset:
    """Result from multi-sensor fusion."""
    fused_data: np.ndarray
    channel_names: List[str]
    spatial_resolution_m: float
    metadata: Dict[str, Any]


class SensorFusion:
    """
    Multi-sensor data fusion engine.
    
    Fuses heterogeneous sensor data:
        - SAR (Synthetic Aperture Radar)
        - Hyperspectral/Multispectral imagery
        - Thermal infrared
        - LIDAR elevation data
    
    Operations:
        - Coregistration and resampling
        - Feature-level fusion
        - Decision-level fusion
    """
    
    def __init__(self, target_resolution_m: float = 10.0):
        self.target_resolution_m = target_resolution_m
    
    def fuse(
        self,
        sar_data: Optional[np.ndarray] = None,
        hyperspectral_data: Optional[np.ndarray] = None,
        thermal_data: Optional[np.ndarray] = None,
        lidar_data: Optional[np.ndarray] = None,
        target_shape: Optional[Tuple[int, int]] = None
    ) -> FusedDataset:
        """
        Fuse multiple sensor data sources.
        
        Args:
            sar_data: SAR backscatter image (2D)
            hyperspectral_data: Multispectral/hyperspectral cube (3D: bands x H x W)
            thermal_data: Thermal infrared image (2D)
            lidar_data: LIDAR elevation model (2D)
            target_shape: Output spatial dimensions
            
        Returns:
            FusedDataset with aligned multi-channel data
        """
        layers = []
        channel_names = []
        
        # Determine target shape
        if target_shape is None:
            target_shape = self._infer_target_shape(
                sar_data, hyperspectral_data, thermal_data, lidar_data
            )
        
        # Process and add each data source
        if sar_data is not None:
            resampled = self._resample(sar_data, target_shape)
            layers.append(resampled)
            channel_names.append("SAR_backscatter")
        
        if hyperspectral_data is not None:
            # Add each spectral band
            for i in range(hyperspectral_data.shape[0]):
                resampled = self._resample(hyperspectral_data[i], target_shape)
                layers.append(resampled)
                channel_names.append(f"spectral_band_{i}")
        
        if thermal_data is not None:
            resampled = self._resample(thermal_data, target_shape)
            layers.append(resampled)
            channel_names.append("thermal")
        
        if lidar_data is not None:
            # Add elevation and derived slope
            elevation = self._resample(lidar_data, target_shape)
            slope = self._compute_slope(elevation)
            layers.append(elevation)
            layers.append(slope)
            channel_names.extend(["elevation", "slope"])
        
        if not layers:
            raise ValueError("At least one data source must be provided")
        
        # Stack all layers
        fused = np.stack(layers, axis=0)
        
        return FusedDataset(
            fused_data=fused,
            channel_names=channel_names,
            spatial_resolution_m=self.target_resolution_m,
            metadata={
                "num_channels": len(channel_names),
                "shape": fused.shape,
                "sources": {
                    "sar": sar_data is not None,
                    "hyperspectral": hyperspectral_data is not None,
                    "thermal": thermal_data is not None,
                    "lidar": lidar_data is not None
                }
            }
        )
    
    def _infer_target_shape(self, *arrays) -> Tuple[int, int]:
        """Infer target shape from input arrays."""
        shapes = []
        for arr in arrays:
            if arr is not None:
                if arr.ndim == 2:
                    shapes.append(arr.shape)
                elif arr.ndim == 3:
                    shapes.append(arr.shape[1:])
        
        if not shapes:
            return (512, 512)  # Default
        
        # Use maximum dimensions
        max_h = max(s[0] for s in shapes)
        max_w = max(s[1] for s in shapes)
        return (max_h, max_w)
    
    def _resample(self, data: np.ndarray, target_shape: Tuple[int, int]) -> np.ndarray:
        """Resample data to target shape using bilinear interpolation."""
        if data.shape == target_shape:
            return data
        
        from scipy.ndimage import zoom
        
        zoom_factors = (
            target_shape[0] / data.shape[0],
            target_shape[1] / data.shape[1]
        )
        
        return zoom(data, zoom_factors, order=1)  # Bilinear
    
    def _compute_slope(self, elevation: np.ndarray) -> np.ndarray:
        """Compute slope from elevation data."""
        gy, gx = np.gradient(elevation)
        slope = np.sqrt(gx**2 + gy**2)
        return slope
    
    def extract_features(self, fused: FusedDataset) -> Dict[str, np.ndarray]:
        """
        Extract derived features from fused dataset.
        
        Returns common indices and features for downstream analysis.
        """
        features = {}
        data = fused.fused_data
        names = fused.channel_names
        
        # Find channel indices
        sar_idx = None
        red_idx = None
        nir_idx = None
        thermal_idx = None
        
        for i, name in enumerate(names):
            if "SAR" in name:
                sar_idx = i
            elif "band_2" in name:  # Typical red band
                red_idx = i
            elif "band_3" in name:  # Typical NIR band
                nir_idx = i
            elif "thermal" in name:
                thermal_idx = i
        
        # Compute NDVI if red and NIR available
        if red_idx is not None and nir_idx is not None:
            red = data[red_idx]
            nir = data[nir_idx]
            ndvi = (nir - red) / (nir + red + 1e-8)
            features["ndvi"] = np.clip(ndvi, -1, 1)
        
        # Compute SAR-based water index
        if sar_idx is not None:
            sar = data[sar_idx]
            # Water appears dark in SAR
            water_index = np.clip(-sar / 30, 0, 1)
            features["water_index"] = water_index
        
        # Compute thermal anomaly map
        if thermal_idx is not None:
            thermal = data[thermal_idx]
            mean_temp = np.mean(thermal)
            std_temp = np.std(thermal)
            anomaly = (thermal - mean_temp) / (std_temp + 1e-8)
            features["thermal_anomaly"] = anomaly
        
        return features


def create_sample_fused_dataset() -> FusedDataset:
    """Create a sample fused dataset for testing."""
    shape = (256, 256)
    
    # Synthetic SAR
    sar = np.random.normal(-15, 3, shape)
    
    # Synthetic 4-band hyperspectral (Blue, Green, Red, NIR)
    hyperspectral = np.random.uniform(0, 1, (4, *shape))
    hyperspectral[3] = hyperspectral[2] * 1.5  # NIR > Red for vegetation
    
    # Synthetic thermal
    thermal = np.random.normal(25, 5, shape)
    
    # Synthetic LIDAR
    lidar = np.random.normal(100, 10, shape)
    
    fusion = SensorFusion(target_resolution_m=10.0)
    return fusion.fuse(
        sar_data=sar,
        hyperspectral_data=hyperspectral,
        thermal_data=thermal,
        lidar_data=lidar
    )
