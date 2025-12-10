import random
from faker import Faker
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta

fake = Faker()

class MockDatabase:
    def __init__(self):
        self.plants = []
        self.vendors = []
        self.materials = []
        self.purchase_orders = []
        self.invoices = []
        self.sales_orders = []
        self.employees = []
        self._generate_data()

    def _generate_data(self):
        # 1. Plants
        plant_locations = ['Berlin', 'New York', 'Singapore', 'Tokyo', 'London', 'Texas', 'Shanghai']
        for loc in plant_locations:
            self.plants.append({
                'id': str(random.randint(1000, 9999)),
                'name': f"Plant {loc}",
                'location': loc,
                'code': loc[:3].upper()
            })

        # 2. Vendors
        for _ in range(20):
            self.vendors.append({
                'id': str(random.randint(50000, 99999)),
                'name': fake.company(),
                'country': fake.country(),
                'rating': random.choice(['A', 'B', 'C'])
            })

        # 3. Materials
        material_types = ['Steel', 'Aluminum', 'Plastic', 'Electronics', 'Chemicals']
        for _ in range(50):
            self.materials.append({
                'id': str(random.randint(100000, 999999)),
                'name': f"{random.choice(material_types)} {fake.word().capitalize()}",
                'type': random.choice(['Raw', 'Finished']),
                'price': round(random.uniform(10.0, 500.0), 2)
            })

        # 4. Purchase Orders (MM)
        for _ in range(200):
            vendor = random.choice(self.vendors)
            plant = random.choice(self.plants)
            date = fake.date_between(start_date='-30d', end_date='+30d')
            status = random.choices(['Open', 'Late', 'Received', 'Blocked'], weights=[0.4, 0.2, 0.3, 0.1])[0]
            
            self.purchase_orders.append({
                'id': str(random.randint(4500000, 4599999)),
                'vendor_id': vendor['id'],
                'vendor_name': vendor['name'],
                'plant_id': plant['id'],
                'plant_location': plant['location'],
                'date': date.isoformat(),
                'status': status,
                'total_value': round(random.uniform(1000, 50000), 2),
                'delivery_days_actual': random.randint(1, 15) if status == 'Received' else None,
                'delivery_days_promised': random.randint(5, 10)
            })

        # 5. Invoices (FI)
        for po in self.purchase_orders:
            if random.random() > 0.3: # 70% of POs have invoices
                status = 'Blocked' if po['status'] == 'Blocked' else random.choice(['Paid', 'Pending'])
                self.invoices.append({
                    'id': str(random.randint(51000000, 51999999)),
                    'po_id': po['id'],
                    'amount': po['total_value'],
                    'status': status,
                    'due_date': fake.date_between(start_date='-10d', end_date='+30d').isoformat()
                })

        # 6. Sales Orders (SD)
        for _ in range(150):
            plant = random.choice(self.plants)
            self.sales_orders.append({
                'id': str(random.randint(900000, 999999)),
                'customer': fake.company(),
                'plant_id': plant['id'],
                'status': random.choice(['Open', 'Shipped', 'Delayed']),
                'delivery_date': fake.date_between(start_date='-5d', end_date='+20d').isoformat()
            })

        # 7. Employees (HR)
        for _ in range(50):
            self.employees.append({
                'id': str(random.randint(1000, 9999)),
                'name': fake.name(),
                'department': random.choice(['IT', 'Sales', 'Finance', 'HR']),
                'location': random.choice(plant_locations)
            })

    # --- API Methods (Simulating SAP BAPIs) ---

    def analyze_vendor_risk(self, vendor_name: str) -> Dict[str, Any]:
        """
        Simulates SAP RPT-1 behavior: Analyzes historical performance to predict risk.
        In-Context Learning simulation: Looks at last N orders to determine a pattern.
        """
        # 1. Fetch Context (Historical Data)
        vendor_orders = [p for p in self.purchase_orders 
                        if p['vendor_name'].lower() == vendor_name.lower() 
                        and p['status'] == 'Received']
        
        if not vendor_orders:
            return {"risk_score": 0.0, "reason": "No historical data found for context."}
            
        # 2. RPT-1 Logic Simulation (Pattern Recognition)
        # We simulate the model finding a pattern: "Late delivery when Value > 10k" or "Late in Winter"
        late_count = sum(1 for p in vendor_orders if p['delivery_days_actual'] > p['delivery_days_promised'])
        total = len(vendor_orders)
        
        avg_delay = 0
        if late_count > 0:
            delays = [p['delivery_days_actual'] - p['delivery_days_promised'] for p in vendor_orders 
                     if p['delivery_days_actual'] > p['delivery_days_promised']]
            avg_delay = sum(delays) / len(delays)

        risk_score = min(1.0, (late_count / total) * 1.5) # Amplify for sensitivity
        
        return {
            "vendor": vendor_name,
            "risk_score": round(risk_score, 2),
            "total_orders_analyzed": total,
            "late_orders": late_count,
            "avg_delay_days": round(avg_delay, 1),
            "prediction": "High Risk of Delay" if risk_score > 0.5 else "Low Risk",
            "model_model": "sap-rpt-1-large (Simulated)"
        }

    def find_pos(self, vendor_name: str = None, status: str = None, plant_loc: str = None) -> List[Dict]:
        results = self.purchase_orders
        if vendor_name:
            results = [p for p in results if vendor_name.lower() in p['vendor_name'].lower()]
        if status:
            results = [p for p in results if status.lower() == p['status'].lower()]
        if plant_loc:
            results = [p for p in results if plant_loc.lower() in p['plant_location'].lower()]
        return results

    def find_invoices(self, status: str = None, po_id: str = None) -> List[Dict]:
        results = self.invoices
        if status:
            results = [i for i in results if status.lower() == i['status'].lower()]
        if po_id:
            results = [i for i in results if po_id == i['po_id']]
        return results

    def find_sales_orders(self, customer: str = None, status: str = None) -> List[Dict]:
        results = self.sales_orders
        if customer:
            results = [s for s in results if customer.lower() in s['customer'].lower()]
        if status:
            results = [s for s in results if status.lower() == s['status'].lower()]
        return results

    def get_plant_id(self, location: str) -> Optional[str]:
        for p in self.plants:
            if location.lower() in p['location'].lower():
                return p['id']
        return None

# Singleton Instance
mock_db = MockDatabase()
