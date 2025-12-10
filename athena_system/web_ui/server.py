import http.server
import socketserver
import os
import json
import sys
import io
import contextlib

# Change to project root to ensure imports work
WEB_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(WEB_DIR))
sys.path.append(PROJECT_ROOT)

from athena_system.workflows.knowledge_arbitrage import run_knowledge_arbitrage
from athena_system.workflows.lead_gen_outreach import run_lead_gen_workflow
from athena_system.workflows.delivery_framework import run_delivery_workflow
from athena_system.workflows.business_review import run_business_review

PORT = 8000

def run_workflow_capture_output(workflow_func, *args):
    """Runs a workflow and captures its stdout."""
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        try:
            workflow_func(*args)
        except Exception as e:
            print(f"Error running workflow: {e}")
    return f.getvalue()

class ConversationManager:
    def __init__(self):
        self.history = []

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

    def get_context(self):
        # Return last 5 messages as context string
        return "\n".join([f"{m['role']}: {m['content']}" for m in self.history[-5:]])

# Global instance for this single-user demo
conversation_manager = ConversationManager()

class AgentHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # SAP Data API Endpoints
        if self.path == '/api/sap/status':
            from athena_system.integrations.sap_connector import sap
            self._send_json(sap.get_system_status())
            return
        
        elif self.path == '/api/sap/partners':
            from athena_system.integrations.sap_connector import sap
            self._send_json(sap.get_business_partners(top=10))
            return
        
        elif self.path == '/api/sap/orders':
            from athena_system.integrations.sap_connector import sap
            self._send_json(sap.get_sales_orders(top=10))
            return
        
        elif self.path == '/api/sap/revenue':
            from athena_system.integrations.sap_connector import sap
            self._send_json(sap.get_revenue_summary())
            return
        
        elif self.path == '/api/dashboard':
            # Dashboard data endpoint
            from athena_system.integrations.sap_connector import sap
            from athena_system.agents.llm_router import check_ollama_available
            self._send_json({
                "sap": sap.get_system_status(),
                "llm": {"ollama_available": check_ollama_available()},
                "agents": {"total": 400, "active": 400},
                "routing_history": list(getattr(self, '_routing_history', []))[-10:]
            })
            return
        
        elif self.path == '/':
            self.path = '/index.html'
        elif self.path == '/dashboard':
            self.path = '/dashboard.html'
        
        return super().do_GET()
    
    def _send_json(self, data):
        """Helper to send JSON response."""
        response_bytes = json.dumps(data).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            prompt = data.get('prompt', '').lower()
            
            # Multi-User Session Support
            from athena_system.utils.session_manager import (
                session_manager, get_session_from_cookie, create_session_cookie
            )
            
            # Get or create session
            cookie_header = self.headers.get('Cookie', '')
            session_id = get_session_from_cookie(cookie_header)
            session = session_manager.get_or_create_session(session_id)
            
            # Add User Message to Session History
            session.add_message("User", prompt)
            
            # Context Enrichment Logic (using session)
            pronouns = ["it", "them", "that", "this", "him", "her"]
            if any(p in prompt.split() for p in pronouns):
                last_user_msg = session.get_last_user_message()
                if last_user_msg:
                    print(f"🔄 Session {session.session_id}: Enriching with context: '{last_user_msg}'")
                    prompt = f"{prompt} {last_user_msg}"
            
            response_text = ""
            trace_data = {"status": "executed", "workflow": "unknown"}

            # Simple Keyword Routing
            if "research" in prompt or "blog" in prompt or "topic" in prompt:
                topic = prompt.replace("research", "").replace("blog", "").strip() or "Agentic AI"
                response_text = run_workflow_capture_output(run_knowledge_arbitrage, topic)
                trace_data["workflow"] = "knowledge_arbitrage"
            
            elif "lead" in prompt or "sales" in prompt:
                criteria = prompt.replace("find leads", "").strip() or "FinTech"
                response_text = run_workflow_capture_output(run_lead_gen_workflow, criteria)
                trace_data["workflow"] = "lead_gen_outreach"
            
            elif "risk" in prompt or "project" in prompt or "profile" in prompt:
                # Import locally to avoid circular dependency and NameError
                from athena_system.workflows.delivery_framework import run_delivery_workflow
                project_name = prompt.replace("create risk profile for", "").replace("project", "").strip() or "New AI Initiative"
                response_text = run_workflow_capture_output(run_delivery_framework, project_name)
                trace_data["workflow"] = "delivery_framework"
            
            elif "review" in prompt or "business" in prompt:
                response_text = run_workflow_capture_output(run_business_review)
                trace_data["workflow"] = "business_review"
                
            else:
                # Hybrid LLM Routing (Ollama + Keyword Fallback)
                from athena_system.agents.llm_router import route_request as llm_route
                from athena_system.agents.orchestrator import OrchestratorAgent
                
                # Log context for debugging
                print(f"🧠 Context: {conversation_manager.get_context()}")
                
                # Use hybrid router to determine category
                route_info = llm_route(prompt)
                category = route_info['category']
                method = route_info['method']
                
                print(f"🎯 Routed to {category} via {method}")
                
                # Use orchestrator to find best agent in category
                orchestrator = OrchestratorAgent()
                route_result = orchestrator.route_request(prompt)
                
                if route_result['status'] == 'success':
                    routing_method = "🤖 LLM" if method == "llm" else "🔤 Keywords"
                    response_text = f"✅ **Dynamic Routing Successful** ({routing_method})\n\n{route_result['message']}\n\n*Agent Category*: {route_result['category']}"
                    trace_data["workflow"] = "dynamic_routing"
                    trace_data["agent"] = route_result['agent']
                    trace_data["routing_method"] = method
                    trace_data["ollama_available"] = route_info['ollama_available']
                else:
                    response_text = f"I could not find a suitable agent. Detected category: {category}. Please try: Research, Sales, Risk, or Business Review."
                    trace_data["status"] = "routing_failed"

            # Add Agent Response to Session History
            session.add_message("Athena", response_text)
            
            # Add session info to trace
            trace_data["session_id"] = session.session_id

            result = {
                "response": response_text,
                "trace": trace_data
            }
            
            response_bytes = json.dumps(result).encode('utf-8')
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-Length', str(len(response_bytes)))
            self.send_header('Set-Cookie', create_session_cookie(session.session_id))
            self.end_headers()
            
            self.wfile.write(response_bytes)
            return
            
        super().do_POST()

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    os.chdir(WEB_DIR)
    print(f"✅ Athena Web UI running at http://localhost:{PORT}")
    with ReusableTCPServer(("", PORT), AgentHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
