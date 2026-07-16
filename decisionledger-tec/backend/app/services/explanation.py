class ExplanationService:
    @staticmethod
    def generate_explanation(top_features: dict, prob: float) -> str:
        if prob < 0.5:
            return "This transaction appears normal with no significant risk factors."
            
        feature_descriptions = {
            "impossible_travel": "an impossible travel pattern was detected",
            "vpn_detected": "the connection originated from a VPN",
            "ip_reputation": "the IP address has a poor reputation",
            "velocity_score": "the transaction velocity is unusually high",
            "failed_logins": "there were multiple failed login attempts recently",
            "powershell_execution": "suspicious PowerShell execution was detected on the endpoint",
            "browser_changed": "the user logged in from a newly changed browser",
            "known_device": "the device used is unknown or new",
            "session_risk": "the session risk score is elevated",
            "device_trust_score": "the device trust score is critically low",
            "endpoint_alert": "a security alert was triggered on the endpoint",
            "amount": "the transaction amount is unusually large for this account",
        }
        
        reasons = []
        for feature, impact in top_features.items():
            if impact > 0.05 and feature in feature_descriptions:
                reasons.append(feature_descriptions[feature])
        
        if not reasons:
            return "This transaction appears normal with no significant risk factors."
            
        explanation = "This transaction is considered high risk because "
        if len(reasons) == 1:
            explanation += reasons[0] + "."
        elif len(reasons) == 2:
            explanation += f"{reasons[0]} and {reasons[1]}."
        else:
            explanation += ", ".join(reasons[:-1]) + f", and {reasons[-1]}."
            
        return explanation
