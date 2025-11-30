class EnterpriseFormula:
    """
    Calculates the Enterprise Health Score (EHS) based on the formula:
    EHS = ((P * 0.4) + (E * 0.3) + (I * 0.2)) / (1 + R * 0.1)
    """
    def __init__(self):
        # Weights
        self.w_p = 0.4
        self.w_e = 0.3
        self.w_i = 0.2
        self.w_r = 0.1

    def calculate_score(self, metrics: dict) -> dict:
        """
        Metrics input format:
        {
            "performance": 0-100,
            "efficiency": 0-100,
            "innovation": 0-100,
            "risk": 0-10 (Risk is a drag factor)
        }
        """
        p = metrics.get("performance", 0)
        e = metrics.get("efficiency", 0)
        i = metrics.get("innovation", 0)
        r = metrics.get("risk", 0)

        # Numerator: Success Factors
        numerator = (p * self.w_p) + (e * self.w_e) + (i * self.w_i)
        
        # Denominator: Failure/Risk Drag
        denominator = 1 + (r * self.w_r)
        
        ehs = numerator / denominator
        
        # Breakdown for visualization
        breakdown = {
            "score": round(ehs, 1),
            "components": {
                "performance": {"value": p, "weight": self.w_p, "contribution": round(p * self.w_p, 1)},
                "efficiency": {"value": e, "weight": self.w_e, "contribution": round(e * self.w_e, 1)},
                "innovation": {"value": i, "weight": self.w_i, "contribution": round(i * self.w_i, 1)},
                "risk": {"value": r, "weight": self.w_r, "drag": round(r * self.w_r, 2)}
            },
            "formula": f"(({p}*0.4) + ({e}*0.3) + ({i}*0.2)) / (1 + {r}*0.1)"
        }
        
        return breakdown

# Singleton
enterprise_formula = EnterpriseFormula()
