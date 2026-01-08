"""
Bhoonidhi Client
================

Client for accessing NISAR data via the ISRO Bhoonidhi Portal API.
Uses STAC (Spatio-Temporal Asset Catalog) format.
"""
import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import urllib.request
import urllib.parse


@dataclass
class STACItem:
    """STAC catalog item representing a satellite scene."""
    item_id: str
    collection: str
    datetime: datetime
    bbox: List[float]  # [west, south, east, north]
    assets: Dict[str, str]  # asset_name -> url
    properties: Dict[str, Any]


class BhoonidhiClient:
    """
    Client for Bhoonidhi Portal API.
    
    Provides access to NISAR (NASA-ISRO SAR) data products.
    
    Features:
        - JWT-based authentication
        - STAC catalog search
        - Scene download
        - L-band and S-band SAR data access
    
    Registration: bhoonidhi@nrsc.gov.in
    Portal: https://bhoonidhi.nrsc.gov.in/NISAR/
    """
    
    API_BASE = "https://bhoonidhi.nrsc.gov.in/api"
    
    def __init__(
        self,
        user_id: Optional[str] = None,
        password: Optional[str] = None
    ):
        self.user_id = user_id or os.environ.get("BHOONIDHI_USER")
        self.password = password or os.environ.get("BHOONIDHI_PASSWORD")
        self._token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None
    
    @property
    def is_authenticated(self) -> bool:
        """Check if client has valid authentication."""
        if not self._token:
            return False
        if self._token_expiry and datetime.now() > self._token_expiry:
            return False
        return True
    
    def authenticate(self) -> bool:
        """
        Authenticate with Bhoonidhi API using credentials.
        
        Returns True if authentication successful.
        """
        if not self.user_id or not self.password:
            print("⚠️ Bhoonidhi credentials not configured")
            print("   Set BHOONIDHI_USER and BHOONIDHI_PASSWORD environment variables")
            print("   Or register at: bhoonidhi@nrsc.gov.in")
            return False
        
        try:
            # POST to auth endpoint
            auth_url = f"{self.API_BASE}/auth/token"
            data = {
                "username": self.user_id,
                "password": self.password
            }
            
            # This would make actual API call in production
            # For now, return False to indicate credentials needed
            print(f"🔐 Attempting authentication for user: {self.user_id}")
            
            # Simulated response - replace with actual API call
            # response = self._post(auth_url, data)
            # self._token = response.get("access_token")
            # self._token_expiry = datetime.now() + timedelta(hours=1)
            
            return False  # Credentials not verified yet
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def search_catalog(
        self,
        bbox: List[float],
        datetime_range: tuple,
        product_type: str = "L1",
        band: str = "L",
        limit: int = 100
    ) -> List[STACItem]:
        """
        Search NISAR catalog for scenes.
        
        Args:
            bbox: Bounding box [west, south, east, north] in degrees
            datetime_range: Tuple of (start_datetime, end_datetime)
            product_type: NISAR product level (L0, L1, L2, L3, L4)
            band: L-band or S-band
            limit: Maximum results to return
            
        Returns:
            List of STACItem objects matching search criteria
        """
        if not self.is_authenticated:
            print("⚠️ Not authenticated. Call authenticate() first or use synthetic data.")
            return []
        
        # Build STAC search query
        search_params = {
            "bbox": ",".join(map(str, bbox)),
            "datetime": f"{datetime_range[0].isoformat()}/{datetime_range[1].isoformat()}",
            "collections": f"nisar-{band.lower()}-{product_type.lower()}",
            "limit": limit
        }
        
        search_url = f"{self.API_BASE}/stac/search"
        
        try:
            # This would make actual API call
            # response = self._get(search_url, search_params)
            # items = [self._parse_stac_item(item) for item in response.get("features", [])]
            
            # Return empty for now - use synthetic data instead
            return []
            
        except Exception as e:
            print(f"❌ Catalog search failed: {e}")
            return []
    
    def download_scene(
        self,
        scene_id: str,
        output_dir: str,
        asset_key: str = "data"
    ) -> Optional[str]:
        """
        Download a NISAR scene.
        
        Args:
            scene_id: STAC item ID
            output_dir: Directory to save downloaded file
            asset_key: Which asset to download (data, metadata, etc.)
            
        Returns:
            Path to downloaded file, or None if failed
        """
        if not self.is_authenticated:
            print("⚠️ Not authenticated. Cannot download.")
            return None
        
        print(f"📥 Downloading scene: {scene_id}")
        
        # This would make actual download
        # For now, return None
        return None
    
    def get_sample_scenes(self) -> List[Dict[str, Any]]:
        """
        Get list of sample NISAR scenes available for testing.
        
        Sample data is available without authentication.
        """
        # Known sample data locations
        samples = [
            {
                "id": "NISAR_L1_SAMPLE_001",
                "collection": "nisar-l-l1",
                "datetime": "2024-06-15T10:30:00Z",
                "bbox": [77.5, 12.9, 77.7, 13.1],  # Bangalore area
                "description": "Sample L-band L1 product over urban area",
                "url": "https://bhoonidhi.nrsc.gov.in/samples/nisar_l1_sample_001.zip"
            },
            {
                "id": "NISAR_L2_SAMPLE_001",
                "collection": "nisar-l-l2",
                "datetime": "2024-06-15T10:30:00Z",
                "bbox": [77.5, 12.9, 77.7, 13.1],
                "description": "Sample L-band L2 product (geocoded)",
                "url": "https://bhoonidhi.nrsc.gov.in/samples/nisar_l2_sample_001.zip"
            }
        ]
        return samples
    
    def _get(self, url: str, params: Dict) -> Dict:
        """Make authenticated GET request."""
        query = urllib.parse.urlencode(params)
        full_url = f"{url}?{query}"
        
        req = urllib.request.Request(full_url)
        req.add_header("Authorization", f"Bearer {self._token}")
        req.add_header("Accept", "application/json")
        
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    
    def _post(self, url: str, data: Dict) -> Dict:
        """Make POST request."""
        json_data = json.dumps(data).encode()
        
        req = urllib.request.Request(url, data=json_data, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")
        
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    
    def _parse_stac_item(self, item: Dict) -> STACItem:
        """Parse STAC JSON to STACItem dataclass."""
        return STACItem(
            item_id=item["id"],
            collection=item.get("collection", ""),
            datetime=datetime.fromisoformat(item["properties"]["datetime"].replace("Z", "+00:00")),
            bbox=item.get("bbox", []),
            assets={k: v["href"] for k, v in item.get("assets", {}).items()},
            properties=item.get("properties", {})
        )
    
    def status(self) -> Dict[str, Any]:
        """Get client status."""
        return {
            "has_credentials": bool(self.user_id and self.password),
            "is_authenticated": self.is_authenticated,
            "api_base": self.API_BASE,
            "sample_data_available": True
        }
