"""
Synthetic Data Generator
========================

Generates synthetic satellite data for development and testing
when live API access is not available.
"""
import numpy as np
from typing import Dict, Tuple, Optional, Any
from dataclasses import dataclass


@dataclass
class SyntheticScene:
    """Synthetic satellite scene."""
    scene_id: str
    scene_type: str
    data: np.ndarray
    metadata: Dict[str, Any]


class SyntheticDataGenerator:
    """
    Generates realistic synthetic satellite data.
    
    Supports:
        - SAR imagery (L-band and S-band)
        - Hyperspectral/multispectral imagery
        - Thermal infrared
        - LIDAR elevation models
        
    Scenarios:
        - Agriculture (crop fields with various health)
        - Ports (vessels and congestion)
        - Pipelines (with leak anomalies)
    """
    
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            np.random.seed(seed)
    
    def generate_sar_scene(
        self,
        shape: Tuple[int, int] = (512, 512),
        band: str = "L",
        scenario: str = "generic"
    ) -> SyntheticScene:
        """
        Generate synthetic SAR image.
        
        Args:
            shape: Image dimensions
            band: 'L' (L-band, deeper penetration) or 'S' (S-band, surface)
            scenario: 'generic', 'agriculture', 'port', 'pipeline'
        """
        # Base backscatter (dB scale)
        if band == "L":
            mean_backscatter = -15  # L-band typically -10 to -20 dB
            std_backscatter = 4
        else:
            mean_backscatter = -12  # S-band slightly higher
            std_backscatter = 3
        
        data = np.random.normal(mean_backscatter, std_backscatter, shape)
        
        # Add scenario-specific features
        if scenario == "agriculture":
            data = self._add_crop_fields(data)
        elif scenario == "port":
            data = self._add_vessels(data)
        elif scenario == "pipeline":
            data = self._add_pipeline(data)
        
        # Add speckle noise (multiplicative)
        speckle = np.random.exponential(1, shape)
        data = data + 10 * np.log10(speckle + 0.1)
        
        return SyntheticScene(
            scene_id=f"synthetic_sar_{band}_{scenario}_{np.random.randint(10000)}",
            scene_type=f"SAR_{band}",
            data=data.astype(np.float32),
            metadata={
                "band": band,
                "scenario": scenario,
                "shape": shape,
                "mean_backscatter_db": mean_backscatter
            }
        )
    
    def generate_hyperspectral_scene(
        self,
        shape: Tuple[int, int] = (512, 512),
        num_bands: int = 10,
        scenario: str = "vegetation"
    ) -> SyntheticScene:
        """
        Generate synthetic hyperspectral/multispectral image.
        
        Creates bands approximating: Blue, Green, Red, Red Edge, NIR, SWIR, etc.
        """
        data = np.zeros((num_bands, *shape), dtype=np.float32)
        
        # Generate base reflectance for each band
        wavelengths = np.linspace(450, 2200, num_bands)  # nm
        
        for i, wl in enumerate(wavelengths):
            base_reflectance = np.random.uniform(0.02, 0.15, shape)
            
            if scenario == "vegetation":
                # Vegetation has high NIR reflectance (700-1300nm)
                if 700 < wl < 1300:
                    base_reflectance *= 3.0
                # Low red reflectance (absorbed by chlorophyll)
                elif 600 < wl < 700:
                    base_reflectance *= 0.5
            
            # Add texture
            texture = self._generate_texture(shape, scale=50)
            data[i] = base_reflectance * (0.8 + 0.4 * texture)
        
        # Normalize to 0-1
        data = np.clip(data, 0, 1)
        
        return SyntheticScene(
            scene_id=f"synthetic_hyper_{scenario}_{np.random.randint(10000)}",
            scene_type="hyperspectral",
            data=data,
            metadata={
                "num_bands": num_bands,
                "wavelengths_nm": wavelengths.tolist(),
                "scenario": scenario,
                "shape": (num_bands, *shape)
            }
        )
    
    def generate_thermal_scene(
        self,
        shape: Tuple[int, int] = (256, 256),
        scenario: str = "pipeline"
    ) -> SyntheticScene:
        """
        Generate synthetic thermal infrared image.
        
        Temperature in Celsius.
        """
        # Ambient temperature with variation
        ambient = np.random.uniform(20, 30)
        data = np.random.normal(ambient, 2, shape)
        
        if scenario == "pipeline":
            data = self._add_thermal_anomalies(data)
        elif scenario == "urban":
            # Urban heat islands
            data = self._add_urban_heat(data)
        
        return SyntheticScene(
            scene_id=f"synthetic_thermal_{scenario}_{np.random.randint(10000)}",
            scene_type="thermal",
            data=data.astype(np.float32),
            metadata={
                "scenario": scenario,
                "ambient_temp_c": ambient,
                "shape": shape
            }
        )
    
    def generate_lidar_scene(
        self,
        shape: Tuple[int, int] = (256, 256),
        scenario: str = "terrain"
    ) -> SyntheticScene:
        """
        Generate synthetic LIDAR elevation model.
        
        Elevation in meters.
        """
        # Base terrain
        base_elevation = 100  # meters
        data = np.ones(shape) * base_elevation
        
        # Add terrain variation
        terrain = self._generate_terrain(shape)
        data += terrain * 20
        
        if scenario == "pipeline":
            data = self._add_subsidence(data)
        elif scenario == "urban":
            data = self._add_buildings(data)
        
        return SyntheticScene(
            scene_id=f"synthetic_lidar_{scenario}_{np.random.randint(10000)}",
            scene_type="lidar",
            data=data.astype(np.float32),
            metadata={
                "scenario": scenario,
                "base_elevation_m": base_elevation,
                "shape": shape
            }
        )
    
    def generate_complete_dataset(
        self,
        shape: Tuple[int, int] = (256, 256),
        scenario: str = "pipeline"
    ) -> Dict[str, SyntheticScene]:
        """Generate a complete multi-sensor dataset for a scenario."""
        return {
            "sar_l": self.generate_sar_scene(shape, "L", scenario),
            "sar_s": self.generate_sar_scene(shape, "S", scenario),
            "hyperspectral": self.generate_hyperspectral_scene(shape, 10, scenario),
            "thermal": self.generate_thermal_scene(shape, scenario),
            "lidar": self.generate_lidar_scene(shape, scenario)
        }
    
    # Helper methods for adding scenario-specific features
    
    def _add_crop_fields(self, data: np.ndarray) -> np.ndarray:
        """Add crop field patterns to SAR data."""
        h, w = data.shape
        # Create field boundaries
        for _ in range(5):
            x = np.random.randint(0, w - 100)
            y = np.random.randint(0, h - 100)
            fw = np.random.randint(50, 150)
            fh = np.random.randint(50, 150)
            # Fields have different backscatter based on crop type/moisture
            field_value = np.random.uniform(-20, -10)
            data[y:y+fh, x:x+fw] = field_value
        return data
    
    def _add_vessels(self, data: np.ndarray) -> np.ndarray:
        """Add vessel signatures to SAR data."""
        h, w = data.shape
        num_vessels = np.random.randint(10, 50)
        for _ in range(num_vessels):
            x = np.random.randint(5, w - 15)
            y = np.random.randint(5, h - 15)
            vw = np.random.randint(3, 12)
            vh = np.random.randint(8, 25)
            # Vessels appear as bright targets
            data[y:y+vh, x:x+vw] = np.random.uniform(-2, 5)
        return data
    
    def _add_pipeline(self, data: np.ndarray) -> np.ndarray:
        """Add pipeline corridor to SAR data."""
        h, w = data.shape
        # Horizontal pipeline corridor
        pipeline_y = h // 2
        corridor_width = np.random.randint(3, 8)
        data[pipeline_y-corridor_width:pipeline_y+corridor_width, :] = -18
        return data
    
    def _add_thermal_anomalies(self, data: np.ndarray) -> np.ndarray:
        """Add thermal anomalies (leak signatures)."""
        h, w = data.shape
        # Add a few cold spots (liquid leaks)
        for _ in range(np.random.randint(1, 4)):
            x = np.random.randint(20, w - 30)
            y = np.random.randint(20, h - 30)
            radius = np.random.randint(5, 15)
            yy, xx = np.ogrid[:h, :w]
            mask = (xx - x)**2 + (yy - y)**2 <= radius**2
            data[mask] -= np.random.uniform(5, 12)
        return data
    
    def _add_urban_heat(self, data: np.ndarray) -> np.ndarray:
        """Add urban heat island effects."""
        h, w = data.shape
        # Hot spots (buildings, roads)
        for _ in range(10):
            x = np.random.randint(0, w - 40)
            y = np.random.randint(0, h - 40)
            bw = np.random.randint(10, 50)
            bh = np.random.randint(10, 50)
            data[y:y+bh, x:x+bw] += np.random.uniform(3, 8)
        return data
    
    def _add_subsidence(self, data: np.ndarray) -> np.ndarray:
        """Add ground subsidence to LIDAR data."""
        h, w = data.shape
        # Subsidence area
        x = np.random.randint(w//4, 3*w//4)
        y = np.random.randint(h//4, 3*h//4)
        radius = np.random.randint(15, 30)
        yy, xx = np.ogrid[:h, :w]
        distance = np.sqrt((xx - x)**2 + (yy - y)**2)
        mask = distance <= radius
        subsidence = 0.5 * (1 - distance / radius)
        subsidence[~mask] = 0
        data -= subsidence * np.random.uniform(0.3, 1.0)
        return data
    
    def _add_buildings(self, data: np.ndarray) -> np.ndarray:
        """Add building footprints to LIDAR data."""
        h, w = data.shape
        for _ in range(15):
            x = np.random.randint(0, w - 30)
            y = np.random.randint(0, h - 30)
            bw = np.random.randint(10, 40)
            bh = np.random.randint(10, 40)
            height = np.random.uniform(5, 30)
            data[y:y+bh, x:x+bw] += height
        return data
    
    def _generate_texture(self, shape: Tuple[int, int], scale: int = 50) -> np.ndarray:
        """Generate smooth texture using Perlin-like noise."""
        # Simplified texture using interpolated random values
        small_shape = (shape[0] // scale + 1, shape[1] // scale + 1)
        small = np.random.random(small_shape)
        
        from scipy.ndimage import zoom
        texture = zoom(small, (scale, scale), order=2)[:shape[0], :shape[1]]
        return texture
    
    def _generate_terrain(self, shape: Tuple[int, int]) -> np.ndarray:
        """Generate terrain elevation using multi-scale noise."""
        terrain = np.zeros(shape)
        
        for scale in [100, 50, 25]:
            texture = self._generate_texture(shape, scale)
            terrain += texture * (scale / 100)
        
        return terrain / terrain.max()
