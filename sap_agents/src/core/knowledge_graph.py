"""
Knowledge Graph for SAP Business Entities.
Enables multi-hop reasoning: "Find risk for the vendor of Invoice #999"
"""
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque

@dataclass
class GraphNode:
    """Entity type in the business domain."""
    name: str  # e.g., "PurchaseOrder"
    attributes: List[str]  # e.g., ["id", "status", "vendor_id"]
    
@dataclass
class GraphEdge:
    """Relationship between entities, mapped to an API tool."""
    source: str           # e.g., "Vendor"
    target: str           # e.g., "PurchaseOrder"
    relation: str         # e.g., "supplies"
    tool_name: str        # e.g., "find_purchase_orders"
    param_map: Dict[str, str]  # Maps source attribute to tool param

class BusinessGraph:
    """
    Semantic Knowledge Graph for SAP Business Logic.
    Supports BFS pathfinding to discover tool chains.
    """
    
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []
        self.adjacency: Dict[str, List[GraphEdge]] = {}
        self._build_graph()

    def _build_graph(self):
        """Populate the graph with SAP entities and relationships."""
        
        # --- NODES (Entity Types) ---
        self._add_node("Vendor", ["id", "name", "rating"])
        self._add_node("Customer", ["id", "name", "industry"])
        self._add_node("PurchaseOrder", ["id", "vendor_id", "vendor_name", "plant_id", "status"])
        self._add_node("SalesOrder", ["id", "customer", "plant_id", "status"])
        self._add_node("Invoice", ["id", "po_id", "status", "amount"])
        self._add_node("Plant", ["id", "location", "code"])
        self._add_node("RiskAssessment", ["vendor", "risk_score", "prediction"])

        # --- EDGES (Relationships + API Mappings) ---
        
        # ========== MM MODULE (Procurement) ==========
        
        # Vendor -> PurchaseOrders: "Find all POs for this vendor"
        self._add_edge(
            source="Vendor", target="PurchaseOrder",
            relation="supplies",
            tool_name="find_purchase_orders",
            param_map={"name": "vendor_name"}
        )
        
        # PurchaseOrder -> Vendor (reverse): "Get the vendor for this PO"
        self._add_edge(
            source="PurchaseOrder", target="Vendor",
            relation="supplied_by",
            tool_name="get_vendor_from_po",  # Virtual tool - extracts from PO data
            param_map={"id": "po_id"}
        )
        
        # PurchaseOrder -> Invoice: "Find invoices for this PO"
        self._add_edge(
            source="PurchaseOrder", target="Invoice",
            relation="billed_via",
            tool_name="find_invoices",
            param_map={"id": "po_id"}
        )
        
        # Invoice -> PurchaseOrder (reverse): "Get the PO for this invoice"
        self._add_edge(
            source="Invoice", target="PurchaseOrder",
            relation="bills",
            tool_name="get_po_from_invoice",  # Virtual tool
            param_map={"po_id": "po_id"}
        )
        
        # Plant -> PurchaseOrders: "Find all POs in this plant"
        self._add_edge(
            source="Plant", target="PurchaseOrder",
            relation="receives",
            tool_name="find_purchase_orders",
            param_map={"location": "plant_loc"}
        )
        
        # Vendor -> RiskAssessment (Predictive): "Assess delivery risk"
        self._add_edge(
            source="Vendor", target="RiskAssessment",
            relation="has_delivery_risk",
            tool_name="analyze_vendor_risk",
            param_map={"name": "vendor_name"}
        )
        
        # ========== SD MODULE (Sales) ==========
        
        # Customer -> SalesOrders: "Find all orders for this customer"
        self._add_edge(
            source="Customer", target="SalesOrder",
            relation="ordered_by",
            tool_name="find_sales_orders",
            param_map={"name": "customer"}
        )
        
        # SalesOrder -> Customer (reverse): "Get customer for this order"
        self._add_edge(
            source="SalesOrder", target="Customer",
            relation="placed_by",
            tool_name="get_customer_from_so",  # Virtual tool
            param_map={"id": "so_id"}
        )
        
        # Plant -> SalesOrders: "Find orders in this plant"
        self._add_edge(
            source="Plant", target="SalesOrder",
            relation="ships_from",
            tool_name="find_sales_orders",
            param_map={"location": "plant_loc"}
        )
        
        # ========== CROSS-MODULE PATHS ==========
        
        # Invoice -> Vendor (via PO): Enables "Risk for vendor of Invoice #X"
        # This is handled by multi-hop: Invoice -> PO -> Vendor -> Risk

    def _add_node(self, name: str, attributes: List[str]):
        self.nodes[name] = GraphNode(name, attributes)
        self.adjacency[name] = []

    def _add_edge(self, source: str, target: str, relation: str, 
                  tool_name: str, param_map: Dict[str, str]):
        edge = GraphEdge(source, target, relation, tool_name, param_map)
        self.edges.append(edge)
        self.adjacency[source].append(edge)

    def get_neighbors(self, node_type: str) -> List[GraphEdge]:
        """Get all outgoing edges from a node type."""
        return self.adjacency.get(node_type, [])

    def find_path(self, start_type: str, end_type: str) -> List[GraphEdge]:
        """
        BFS to find the shortest path of edges from start to end entity type.
        Returns the list of edges (tool calls) to traverse.
        
        Example: find_path("Invoice", "RiskAssessment")
        Returns: [Invoice->PO, PO->Vendor, Vendor->Risk]
        """
        if start_type not in self.nodes or end_type not in self.nodes:
            return []
            
        if start_type == end_type:
            return []
            
        # BFS
        queue = deque([(start_type, [])])
        visited = {start_type}
        
        while queue:
            current, path = queue.popleft()
            
            for edge in self.adjacency.get(current, []):
                if edge.target == end_type:
                    return path + [edge]
                    
                if edge.target not in visited:
                    visited.add(edge.target)
                    queue.append((edge.target, path + [edge]))
                    
        return []  # No path found

    def explain_path(self, path: List[GraphEdge]) -> str:
        """Human-readable explanation of a traversal path."""
        if not path:
            return "Direct lookup (no traversal needed)."
            
        steps = []
        for i, edge in enumerate(path):
            steps.append(f"{i+1}. {edge.source} --({edge.relation})--> {edge.target} [Tool: {edge.tool_name}]")
        
        return "\n".join(steps)

# Singleton instance
knowledge_graph = BusinessGraph()
