"""
Aperture Web UI Server
======================

HTTP server for the Aperture dashboard with API endpoints for AI agents.
"""
import http.server
import socketserver
import os
import sys
import json
from urllib.parse import urlparse, parse_qs

# Add parent directory to path for imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
sys.path.insert(0, PROJECT_ROOT)

from aperture.agents import YieldForecaster, SupplyChainSentinel, AssetIntegrity
from aperture.processing import SARProcessor
from aperture.integrations import BhoonidhiClient, SyntheticDataGenerator
from aperture.config import config

PORT = 8001


class ApertureHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for Aperture dashboard and API."""
    
    def __init__(self, *args, **kwargs):
        # Initialize agents
        self.yield_agent = YieldForecaster()
        self.supply_agent = SupplyChainSentinel()
        self.asset_agent = AssetIntegrity()
        self.sar_processor = SARProcessor(use_gpu=config.use_gpu)
        self.data_generator = SyntheticDataGenerator()
        self.bhoonidhi = BhoonidhiClient()
        
        super().__init__(*args, directory=SCRIPT_DIR, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        
        # API routes
        if path.startswith('/api/'):
            self._handle_api(path, parsed.query)
        elif path == '/' or path == '/index.html':
            # Serve dashboard
            self.path = '/dashboard.html'
            super().do_GET()
        else:
            super().do_GET()
    
    def _handle_api(self, path, query):
        """Handle API requests."""
        try:
            if path == '/api/status':
                self._send_json({
                    "status": "ok",
                    "platform": config.platform_name,
                    "version": config.version,
                    "gpu_enabled": config.use_gpu,
                    "bhoonidhi_status": self.bhoonidhi.status()
                })
            
            elif path == '/api/agent/yield':
                result = self.yield_agent.predict_sample()
                self._send_json(result)
            
            elif path == '/api/agent/supply':
                result = self.supply_agent.predict_sample()
                self._send_json(result)
            
            elif path == '/api/agent/asset':
                result = self.asset_agent.predict_sample()
                self._send_json(result)
            
            elif path == '/api/benchmark':
                sar_bench = self.sar_processor.benchmark(size=1024)
                self._send_json({
                    "sar_processing": sar_bench,
                    "target_latency_ms": config.target_latency_ms
                })
            
            elif path == '/api/synthetic/generate':
                params = parse_qs(query)
                scenario = params.get('scenario', ['pipeline'])[0]
                dataset = self.data_generator.generate_complete_dataset(
                    shape=(256, 256),
                    scenario=scenario
                )
                # Return metadata only (data too large for JSON)
                self._send_json({
                    "status": "generated",
                    "scenario": scenario,
                    "datasets": {
                        name: {
                            "scene_id": scene.scene_id,
                            "scene_type": scene.scene_type,
                            "shape": list(scene.data.shape),
                            "metadata": scene.metadata
                        }
                        for name, scene in dataset.items()
                    }
                })
            
            else:
                self._send_json({"error": "Unknown API endpoint"}, status=404)
                
        except Exception as e:
            self._send_json({"error": str(e)}, status=500)
    
    def _send_json(self, data, status=200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[Aperture] {args[0]}")


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main():
    """Start the Aperture web server."""
    os.chdir(SCRIPT_DIR)
    
    print(f"""
╭─────────────────────────────────────────────────╮
│                                                 │
│   🛰️  APERTURE                                  │
│   Space-to-Earth Analytics Platform             │
│                                                 │
│   Dashboard: http://localhost:{PORT}              │
│   API:       http://localhost:{PORT}/api/status   │
│                                                 │
│   Agents:                                       │
│     • Yield Forecaster    /api/agent/yield      │
│     • Supply Chain        /api/agent/supply     │
│     • Asset Integrity     /api/agent/asset      │
│                                                 │
│   Press Ctrl+C to stop                          │
│                                                 │
╰─────────────────────────────────────────────────╯
    """)
    
    with ReusableTCPServer(("", PORT), ApertureHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✅ Aperture server stopped")


if __name__ == "__main__":
    main()
