from langchain.tools import Tool
import time
import random

# Mock Database with SAP SuccessFactors-like Schema
EMPLOYEES = {
    "EMP-101": {
        "userId": "EMP-101",
        "firstName": "Alice",
        "lastName": "Smith",
        "jobTitle": "Senior Developer",
        "department": "Engineering",
        "location": "Berlin",
        "timeAccountBalance": 15
    },
    "EMP-102": {
        "userId": "EMP-102",
        "firstName": "Bob",
        "lastName": "Jones",
        "jobTitle": "Product Manager",
        "department": "Product",
        "location": "San Francisco",
        "timeAccountBalance": 8
    },
    "EMP-103": {
        "userId": "EMP-103",
        "firstName": "Charlie",
        "lastName": "Brown",
        "jobTitle": "Sales Executive",
        "department": "Sales",
        "location": "London",
        "timeAccountBalance": 20
    }
}

LEAVE_REQUESTS = {}

def get_employee_info(employee_id: str) -> str:
    """Retrieves basic information about a User (Employee)."""
    print(f"   [HR Tool] 👤 Fetching info for {employee_id}...")
    time.sleep(0.5)
    emp = EMPLOYEES.get(employee_id)
    if emp:
        return f"User **{emp['userId']}**: {emp['firstName']} {emp['lastName']} ({emp['jobTitle']}) - {emp['department']}, {emp['location']}."
    return f"User {employee_id} not found."

def check_leave_balance(employee_id: str) -> str:
    """Checks the Time Account Balance for a User."""
    print(f"   [HR Tool] 🏖️ Checking leave balance for {employee_id}...")
    time.sleep(0.5)
    emp = EMPLOYEES.get(employee_id)
    if emp:
        return f"User {emp['firstName']} {emp['lastName']} has **{emp['timeAccountBalance']} days** of annual leave remaining."
    return f"User {employee_id} not found."

def create_leave_request(input_str: str) -> str:
    """Creates an EmployeeTime (Leave Request). Input: 'userId, quantityInDays, comment'"""
    print(f"   [HR Tool] 📝 Creating Leave Request: {input_str}...")
    time.sleep(1.0)
    
    try:
        parts = input_str.split(",", 2)
        if len(parts) < 3:
             return "Error: Invalid input. Use 'userId, quantityInDays, comment'."
        
        emp_id = parts[0].strip()
        days = int(parts[1].strip())
        reason = parts[2].strip()
    except Exception as e:
        return f"Error parsing input: {e}"

    emp = EMPLOYEES.get(emp_id)
    if not emp:
        return f"Error: User {emp_id} not found."
        
    if emp['timeAccountBalance'] < days:
        return f"Error: Insufficient balance. Requested: {days}, Available: {emp['timeAccountBalance']}."
        
    req_id = f"LR-{random.randint(1000, 9999)}"
    LEAVE_REQUESTS[req_id] = {
        "userId": emp_id,
        "quantityInDays": days,
        "comment": reason,
        "approvalStatus": "Submitted"
    }
    
    # Deduct mock balance
    emp['timeAccountBalance'] -= days
    
    return f"✅ Leave Request **{req_id}** submitted for {emp['firstName']} {emp['lastName']}. {days} days for '{reason}'. New Balance: {emp['timeAccountBalance']} days."

def get_hr_tools():
    return [
        Tool(
            name="GetEmployeeInfo",
            func=get_employee_info,
            description="Get basic information about an employee. Input: Employee ID (e.g., 'EMP-101')."
        ),
        Tool(
            name="CheckLeaveBalance",
            func=check_leave_balance,
            description="Check leave balance for an employee. Input: Employee ID (e.g., 'EMP-101')."
        ),
        Tool(
            name="CreateLeaveRequest",
            func=create_leave_request,
            description="Submit a leave request. Input: 'EmployeeID, Days, Reason' (comma separated)."
        )
    ]
