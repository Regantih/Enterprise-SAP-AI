from langchain_core.prompts import ChatPromptTemplate

# Mock Data for Travel (Concur)
TRIPS = {
    "TRIP-8001": {"dest": "Berlin", "dates": "Dec 10-15", "status": "Booked", "cost": "$1200"},
    "TRIP-8002": {"dest": "New York", "dates": "Jan 5-8", "status": "Approval Pending", "cost": "$850"}
}

class MockTravelLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"].lower()
        
        if "trip" in prompt or "travel" in prompt or "booking" in prompt:
            return {"output": "**My Trips (Concur)**:\n- Berlin (Dec 10): Booked ($1200)\n- New York (Jan 5): Pending Approval ($850)\n\n*Action*: 'Book a new trip'?"}
            
        if "expense" in prompt:
            return {"output": "**Expense Report**: Dec Expenses ($450) - Submitted."}

        return {"output": "I can help with Travel Bookings and Expenses (Concur)."}

def create_travel_agent():
    return MockTravelLLM()
