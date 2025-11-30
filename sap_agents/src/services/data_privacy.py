import re

class DataPrivacyService:
    """
    Masks sensitive data based on user role and clearance level.
    """
    def __init__(self):
        self.sensitive_patterns = {
            "email": r"[^@]+@[^@]+\.[^@]+",
            "salary": r"\$\d+(?:,\d{3})*(?:\.\d{2})?",
            "credit_limit": r"Credit Limit \$\d+"
        }

    def secure_data(self, content: str, user_role: str, clearance: str) -> str:
        """
        Redacts sensitive information if the user is not authorized.
        """
        print(f"   [Data Privacy] 🛡️ Securing data for {user_role} ({clearance})...")
        
        secured_content = content
        
        # Rule: Only 'CFO' or 'L2+' can see Financials (Salary, Credit Limit)
        if user_role != "CFO" and clearance not in ["L2", "L3"]:
            secured_content = re.sub(self.sensitive_patterns["salary"], "[REDACTED SALARY]", secured_content)
            secured_content = re.sub(self.sensitive_patterns["credit_limit"], "Credit Limit [REDACTED]", secured_content)
            
        # Rule: Only 'Admin' or 'L3' can see PII (Emails)
        if user_role != "IT Admin" and clearance != "L3":
             secured_content = re.sub(self.sensitive_patterns["email"], "[REDACTED EMAIL]", secured_content)

        return secured_content

# Global Instance
data_privacy = DataPrivacyService()
