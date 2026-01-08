"""
Aperture Integrations
=====================

External data source integrations including Bhoonidhi Portal and synthetic data.
"""

from aperture.integrations.bhoonidhi import BhoonidhiClient
from aperture.integrations.synthetic import SyntheticDataGenerator

__all__ = ["BhoonidhiClient", "SyntheticDataGenerator"]
