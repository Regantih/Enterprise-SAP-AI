"""
Comprehensive Test Suite for Athena Core
Tests all major components: workflows, routing, SAP connector, sessions.
"""
import pytest
import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSessionManager:
    """Tests for the session manager."""
    
    def test_create_session(self):
        """Test session creation."""
        from athena_system.utils.session_manager import session_manager
        
        session = session_manager.get_or_create_session(None)
        assert session is not None
        assert session.session_id is not None
        assert len(session.session_id) == 8
    
    def test_session_isolation(self):
        """Test that sessions are isolated."""
        from athena_system.utils.session_manager import SessionManager
        
        sm = SessionManager()
        s1 = sm.get_or_create_session(None)
        s2 = sm.get_or_create_session(None)
        
        s1.add_message("User", "Hello from session 1")
        s2.add_message("User", "Hello from session 2")
        
        assert len(s1.history) == 1
        assert len(s2.history) == 1
        assert s1.history[0]["content"] != s2.history[0]["content"]
    
    def test_context_enrichment(self):
        """Test that context enrichment retrieves previous message."""
        from athena_system.utils.session_manager import Session
        
        session = Session("test123")
        session.add_message("User", "Find leads for FinTech")
        session.add_message("Athena", "Found 3 leads")
        session.add_message("User", "Draft email to them")
        
        last_user_msg = session.get_last_user_message()
        assert last_user_msg == "Find leads for FinTech"
    
    def test_cookie_parsing(self):
        """Test cookie parsing."""
        from athena_system.utils.session_manager import get_session_from_cookie
        
        cookie = "athena_session=abc12345; other_cookie=value"
        session_id = get_session_from_cookie(cookie)
        assert session_id == "abc12345"
        
        # Empty cookie
        assert get_session_from_cookie("") is None
        assert get_session_from_cookie(None) is None


class TestLLMRouter:
    """Tests for the hybrid LLM router."""
    
    def test_keyword_routing(self):
        """Test keyword-based routing."""
        from athena_system.agents.llm_router import route_with_keywords
        
        assert route_with_keywords("Find leads for FinTech") == "Sales"
        assert route_with_keywords("Create risk profile") == "Delivery"
        assert route_with_keywords("Draft NDA contract") == "Legal"
        assert route_with_keywords("Research agentic AI") == "Research"
        assert route_with_keywords("Analyze revenue trends") == "Finance"
    
    def test_route_request_fallback(self):
        """Test that route_request falls back to keywords when Ollama unavailable."""
        from athena_system.agents.llm_router import route_request
        
        result = route_request("Find sales leads for enterprise")
        assert result["category"] == "Sales"
        assert result["method"] == "keyword"
        assert result["ollama_available"] == False  # Ollama not running in tests


class TestSAPConnector:
    """Tests for the SAP OData connector."""
    
    def test_mock_fallback(self):
        """Test that mock data is returned when SAP unavailable."""
        from athena_system.integrations.sap_connector import SAPConnector
        
        sap = SAPConnector()
        status = sap.get_system_status()
        
        assert status["fallback_mode"] == True
        assert status["api_key_configured"] == False
    
    def test_get_business_partners(self):
        """Test business partners endpoint."""
        from athena_system.integrations.sap_connector import sap
        
        result = sap.get_business_partners(top=3)
        
        assert result["source"] == "mock"
        assert len(result["data"]) == 3
        assert "BusinessPartner" in result["data"][0]
        assert "BusinessPartnerFullName" in result["data"][0]
    
    def test_get_sales_orders(self):
        """Test sales orders endpoint."""
        from athena_system.integrations.sap_connector import sap
        
        result = sap.get_sales_orders(top=2)
        
        assert result["source"] == "mock"
        assert len(result["data"]) == 2
        assert "SalesOrder" in result["data"][0]
        assert "NetAmount" in result["data"][0]
    
    def test_revenue_summary(self):
        """Test revenue summary calculation."""
        from athena_system.integrations.sap_connector import sap
        
        result = sap.get_revenue_summary()
        
        assert "total_revenue" in result
        assert "order_count" in result
        assert result["total_revenue"] > 0


class TestWorkflows:
    """Tests for the workflow modules."""
    
    def test_knowledge_arbitrage_import(self):
        """Test knowledge arbitrage workflow can be imported."""
        from athena_system.workflows.knowledge_arbitrage import run_knowledge_arbitrage
        assert callable(run_knowledge_arbitrage)
    
    def test_lead_gen_import(self):
        """Test lead gen workflow can be imported."""
        from athena_system.workflows.lead_gen_outreach import run_lead_gen_workflow
        assert callable(run_lead_gen_workflow)
    
    def test_delivery_framework_import(self):
        """Test delivery framework workflow can be imported."""
        from athena_system.workflows.delivery_framework import run_delivery_workflow
        assert callable(run_delivery_workflow)
    
    def test_business_review_import(self):
        """Test business review workflow can be imported."""
        from athena_system.workflows.business_review import run_business_review
        assert callable(run_business_review)


class TestOrchestrator:
    """Tests for the orchestrator agent."""
    
    def test_orchestrator_import(self):
        """Test orchestrator can be imported."""
        from athena_system.agents.orchestrator import OrchestratorAgent
        orchestrator = OrchestratorAgent()
        assert orchestrator is not None
    
    def test_route_request(self):
        """Test basic routing."""
        from athena_system.agents.orchestrator import OrchestratorAgent
        
        orchestrator = OrchestratorAgent()
        result = orchestrator.route_request("Legal contract review")
        
        assert "status" in result
        # May succeed or fail depending on keywords, but should not error


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
