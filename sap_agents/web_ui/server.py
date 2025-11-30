import http.server
import socketserver
import os
import json
import sys
import subprocess

# Add parent directory to path to find src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.orchestrator import handle_request

PORT = 8000
WEB_DIR = os.path.dirname(os.path.abspath(__file__))

class AgentHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # API: Get Registry
        if self.path == '/api/agents':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
import http.server
import socketserver
import os
import json
import sys
import subprocess

# Add parent directory to path to find src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.orchestrator import handle_request

PORT = 8000
WEB_DIR = os.path.dirname(os.path.abspath(__file__))

# Custom TCP server to allow address reuse
class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class AgentHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # API: Get Registry
        if self.path == '/api/agents':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            registry_path = os.path.join(os.path.dirname(WEB_DIR), 'src', 'config', 'registry.json')
            with open(registry_path, 'r') as f:
                registry_data = json.load(f)
            self.wfile.write(json.dumps(registry_data).encode())
        
        elif self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Mock Health Data
            health_data = {
                "system": {
                    "success_rate": 98,
                    "avg_rating": 4.8,
                    "active_agents_count": 12
                },
                "business": {
                    "revenue_ytd": "$4.2M",
                    "open_orders": 145,
                    "csat_score": 4.5
                }
            }
            self.wfile.write(json.dumps(health_data).encode())
        
        elif self.path == '/api/formula':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            from src.services.enterprise_formula import enterprise_formula
            
            # Mock Metrics for Demo (In real app, fetch from agents)
            metrics = {
                "performance": 85,  # High Revenue
                "efficiency": 70,   # Moderate Margins
                "innovation": 90,   # High R&D
                "risk": 2           # Low Churn
            }
            
            data = enterprise_formula.calculate_score(metrics)
            self.wfile.write(json.dumps(data).encode())

        else:
            # Serve static files
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))

            user_message = request_data.get('message')
            if not user_message:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No message provided"}).encode())
                return

            try:
                response_message = handle_request(user_message)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"response": response_message}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def translate_path(self, path):
        # Serve files from the current directory (WEB_DIR)
        return os.path.join(WEB_DIR, path.lstrip('/'))

if __name__ == "__main__":
    # Ensure the 'web' directory exists for static files
    if not os.path.exists(WEB_DIR):
        print(f"Error: Web directory not found at {WEB_DIR}")
        sys.exit(1)

    # Start the server
    with ReusableTCPServer(("", PORT), AgentHandler) as httpd:
        print(f"✅ SAP Joule Agent Server running at http://localhost:{PORT}")
        print(f"📂 Serving from {WEB_DIR}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
