import random
from typing import List, Dict
from src.core.mock_sap import mock_db

class ScenarioGenerator:
    def __init__(self):
        self.db = mock_db

    def generate_scenarios(self, count: int = 150) -> List[str]:
        scenarios = []
        templates = [
            "Find {status} purchase orders for {vendor}.",
            "Show me {status} invoices.",
            "List sales orders for {customer}.",
            "What is the status of orders in {plant}?",
            "Check for {status} items from {vendor}.",
            "Find invoices linked to PO {po_id}.",
            "Show me orders in {plant} that are {status}.",
            "Are there any {status} sales orders for {customer}?",
            "List all purchase orders for {vendor} in {plant}."
        ]

        for _ in range(count):
            template = random.choice(templates)
            
            # Pick random entities from DB
            vendor = random.choice(self.db.vendors)['name']
            customer = random.choice(self.db.sales_orders)['customer']
            plant = random.choice(self.db.plants)['location']
            po = random.choice(self.db.purchase_orders)
            po_id = po['id']
            
            # Pick random statuses
            po_status = random.choice(['Open', 'Late', 'Blocked'])
            inv_status = random.choice(['Paid', 'Pending', 'Blocked'])
            so_status = random.choice(['Open', 'Shipped', 'Delayed'])
            
            # Fill template
            query = template.format(
                vendor=vendor,
                customer=customer,
                plant=plant,
                po_id=po_id,
                status=random.choice([po_status, inv_status, so_status])
            )
            scenarios.append(query)
            
        return scenarios

if __name__ == "__main__":
    gen = ScenarioGenerator()
    scenarios = gen.generate_scenarios(10)
    for s in scenarios:
        print(s)
