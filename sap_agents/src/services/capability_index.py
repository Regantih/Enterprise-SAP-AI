import json

class CapabilityIndex:
    """
    A dynamic index of all available SAP capabilities (Agents & Tools).
    Allows for 'semantic' lookup of the best tool for a given query.
    """
    def __init__(self):
        self.index = []
        self._build_index()

    def _build_index(self):
        """
        Builds the capability index from registered agents.
        In a real system, this would embed descriptions into a Vector DB.
        """
        # Hardcoded for now, but structure is ready for dynamic loading
        self.index = [
            {
                "id": "sales_order_status",
                "agent": "SalesOrderAssistant",
                "description": "Check the status, shipping details, and amount of a Sales Order.",
                "keywords": ["order", "status", "shipping", "tracking", "so-"]
            },
            {
                "id": "sales_create_order",
                "agent": "SalesOrderAssistant",
                "description": "Create a new Sales Order for a customer.",
                "keywords": ["create", "order", "buy", "purchase", "new order"]
            },
            {
                "id": "finance_invoice_status",
                "agent": "FinanceReconciliationAgent",
                "description": "Check the status and payment details of a Supplier Invoice.",
                "keywords": ["invoice", "payment", "status", "due", "inv-"]
            },
            {
                "id": "finance_gl_balance",
                "agent": "FinanceReconciliationAgent",
                "description": "Check the balance of a General Ledger (GL) account.",
                "keywords": ["gl", "balance", "ledger", "account", "finance"]
            },
            {
                "id": "hr_employee_info",
                "agent": "HREmployeeAssistant",
                "description": "Get contact and job information for an employee.",
                "keywords": ["employee", "info", "contact", "job", "role", "emp-"]
            },
            {
                "id": "hr_leave_balance",
                "agent": "HREmployeeAssistant",
                "description": "Check remaining leave or vacation balance.",
                "keywords": ["leave", "vacation", "balance", "time off", "holiday"]
            },
            {
                "id": "analytics_strategy",
                "agent": "AnalyticsAgent",
                "description": "Provide high-level business metrics, financial health, and strategic advice.",
                "keywords": ["business", "doing", "performance", "metrics", "strategy", "revenue", "profit", "analysis", "wall street"]
            },
            {
                "id": "procurement_ariba",
                "agent": "ProcurementNegotiationAssistant",
                "description": "Manage supplier negotiations and sourcing via SAP Ariba.",
                "keywords": ["ariba", "sourcing", "supplier", "negotiation", "procurement", "rfp"]
            },
            {
                "id": "supply_chain_ibp",
                "agent": "SupplyChainAgent",
                "description": "Supply Chain Management (SCM) for demand planning and inventory.",
                "keywords": ["supply chain", "scm", "demand", "forecast", "inventory", "ibp-"]
            },
            {
                "id": "ppm_projects",
                "agent": "ProjectSystemAgent",
                "description": "Portfolio and Project Management (PPM) for tracking projects and budgets.",
                "keywords": ["ppm", "project", "wbs", "budget", "portfolio", "milestone", "proj-"]
            },
            {
                "id": "pp_manufacturing",
                "agent": "ManufacturingAgent",
                "description": "Manufacturing (PP) for production orders and shop floor control.",
                "keywords": ["manufacturing", "production", "order", "bom", "shop floor", "po-", "work center"]
            },
            {
                "id": "eam_assets",
                "agent": "AssetManagementAgent",
                "description": "Enterprise Asset Management (EAM) for equipment and maintenance.",
                "keywords": ["asset", "equipment", "maintenance", "work order", "repair", "eq-", "wo-"]
            },
            {
                "id": "cs_service",
                "agent": "CustomerServiceAgent",
                "description": "Customer Service (CS) for tickets and warranties.",
                "keywords": ["service", "ticket", "warranty", "return", "rma", "tkt-", "war-"]
            },
            {
                "id": "trm_treasury",
                "agent": "TreasuryAgent",
                "description": "Treasury and Risk Management (TRM) for cash and liquidity.",
                "keywords": ["treasury", "cash", "liquidity", "bank", "position", "forecast", "trm"]
            },
            {
                "id": "ext_integration",
                "agent": "IntegrationAgent",
                "description": "Integration with external systems (ServiceNow, Salesforce, n8n).",
                "keywords": ["servicenow", "salesforce", "n8n", "integration", "ticket", "opportunity", "inc-", "opp-"]
            },
            {
                "id": "xm_experience",
                "agent": "ExperienceAgent",
                "description": "Experience Management (XM) for sentiment and surveys.",
                "keywords": ["sentiment", "satisfaction", "nps", "survey", "qualtrics", "experience", "feedback"]
            },
            {
                "id": "bn_network",
                "agent": "NetworkAgent",
                "description": "Business Network for supplier collaboration (Ariba).",
                "keywords": ["ariba", "network", "rfq", "bid", "supplier", "collaboration", "sourcing"]
            },
            {
                "id": "tv_travel",
                "agent": "TravelAgent",
                "description": "Travel and Expense Management (Concur).",
                "keywords": ["travel", "trip", "flight", "hotel", "expense", "concur", "booking"]
            },
            {
                "id": "pl_planning",
                "agent": "PlanningAgent",
                "description": "Predictive Planning and Analytics (SAC).",
                "keywords": ["plan", "forecast", "simulate", "sac", "predictive", "model", "scenario"]
            },
            {
                "id": "bpm_process",
                "agent": "ProcessAgent",
                "description": "Business Process Management (Signavio).",
                "keywords": ["process", "mining", "signavio", "efficiency", "bottleneck", "optimization", "flow"]
            },
            {
                "id": "sus_sustainability",
                "agent": "SustainabilityAgent",
                "description": "Sustainability and ESG (Green Ledger).",
                "keywords": ["carbon", "footprint", "esg", "green", "emission", "sustainability", "ledger", "co2"]
            },
            {
                "id": "rag_knowledge",
                "agent": "KnowledgeAgent",
                "description": "Knowledge Base for documents (RAG).",
                "keywords": ["policy", "handbook", "manual", "document", "pdf", "guideline", "procedure", "wiki", "remote work", "travel policy", "password", "security policy", "flight policy", "work from home"]
            },
            {
                "id": "strat_market",
                "agent": "MarketIntelligenceAgent",
                "description": "Market Intelligence for Competitor Analysis and Trends.",
                "keywords": ["competitor", "market", "trend", "r&d", "patent", "tariff", "macro", "policy", "strategy", "growth", "external"]
            }
        ]
        print(f"[Capability Index] 📚 Indexed {len(self.index)} capabilities.")

    def find_capability(self, query: str) -> dict:
        """
        Finds the best capability for a given query.
        Simulates a semantic search by scoring keyword overlaps.
        """
        best_match = None
        highest_score = 0
        query_words = set(query.lower().split())

        for cap in self.index:
            score = 0
            # Keyword match
            import re
            for kw in cap['keywords']:
                # Use regex for word boundary to avoid "rma" matching "Germany"
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, query.lower()):
                    if kw.endswith("-"):
                        score += 20 # Strong signal for ID prefixes
                    else:
                        score += 5
            
            # Description overlap
            desc_words = set(cap['description'].lower().split())
            overlap = query_words.intersection(desc_words)
            score += len(overlap)

            if score > highest_score:
                highest_score = score
                best_match = cap

        if best_match and highest_score > 0:
            return best_match
        return None

# Global Instance
capability_index = CapabilityIndex()
