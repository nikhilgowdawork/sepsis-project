def calculate_risk_score(data):
    """Deterministic manual clinical risk calculation fallback."""
    temp = data.get('temperature', 37.0)
    lactate = data.get('lactate', 1.5)
    
    score = 0.0
    if temp > 39.5 or lactate > 4.0:
        score = 85.0
    elif temp > 38.5 or lactate > 2.5:
        score = 71.0 # Drive risk above High alert threshold (>70%)
    
    return min(max(float(score), 0.0), 100.0)


def get_risk_category(score):
    if score >= 75:
        return "Critical Risk"
    elif score >= 50:
        return "High Risk"
    elif score >= 25:
        return "Moderate Risk"
    else:
        return "Low Risk"


def get_risk_color(score):
    if score >= 75:
        return "red"
    elif score >= 50:
        return "orange"
    elif score >= 25:
        return "yellow"
    else:
        return "green"


# ✅ FIXED FUNCTION (takes 2 arguments)
def generate_risk_recommendations(patient_data, risk_score):
    recommendations = []

    if risk_score >= 75:
        recommendations.extend([
            "🚨 IMMEDIATE ATTENTION REQUIRED",
            "Gemini Insight: High probability of Septic Shock. Activate Sepsis Protocol.",
            "Start antibiotics immediately",
            "Consider Central Line and Vasopressors"
        ])
    elif risk_score >= 50:
        recommendations.extend([
            "⚠️ Gemini Insight: Clinical deterioration likely. Close monitoring required.",
            "Check vitals every 15-30 mins",
            "Consider lab investigations"
        ])
    elif risk_score >= 25:
        recommendations.extend([
            "📋 Increased surveillance",
            "Monitor condition regularly"
        ])
    else:
        recommendations.append("✅ Stable condition")

    # Optional: use patient data
    temp = patient_data.get('temperature', 37)
    if temp > 38:
        recommendations.append("🌡️ High temperature detected")

    return recommendations


def calculate_intervention_urgency(score, data=None):
    """Calculates urgency based on ML score and Sepsis-3 qSOFA criteria."""
    qsofa_points = 0
    if data:
        if data.get('respiratory_rate', 0) >= 22: qsofa_points += 1
        if data.get('systolic_bp', 120) <= 100: qsofa_points += 1
    
    # Sepsis-3: If 2 or more qSOFA criteria are met, urgency is CRITICAL
    if score >= 75 or qsofa_points >= 2:
        return {
            'level': 'EMERGENCY',
            'timeframe': 'Within 15 minutes',
            'priority': 'High',
            'color': 'red'
        }
    elif score >= 50:
        return {
            'level': 'URGENT',
            'timeframe': 'Within 1 hour',
            'priority': 'High',
            'color': 'orange'
        }
    elif score >= 25:
        return {
            'level': 'MODERATE',
            'timeframe': 'Within 2-4 hours',
            'priority': 'Medium',
            'color': 'yellow'
        }
    else:
        return {
            'level': 'ROUTINE',
            'timeframe': 'Per protocol',
            'priority': 'Low',
            'color': 'green'
        }

def get_sepsis_protocol():
    """Returns a formatted string of the Sepsis-3 Clinical Guidelines."""
    return """
    ### 🏥 Sepsis-3 Management Protocol
    
    **1. Recognition & Identification**
    - Screen for infection + organ dysfunction (SOFA ≥ 2).
    - Use **qSOFA** (SBP ≤ 100, RR ≥ 22, Altered Mentation) for rapid bedside assessment.

    **2. The 1-Hour Bundle**
    - **Lactate**: Measure immediately; remeasure if initial > 2 mmol/L.
    - **Cultures**: Obtain blood cultures before starting antibiotics.
    - **Antibiotics**: Administer broad-spectrum IV antibiotics.
    - **Fluids**: 30 mL/kg crystalloid for hypotension or lactate ≥ 4 mmol/L.
    - **Vasopressors**: If hypotensive during/after fluids, maintain MAP ≥ 65 mmHg.

    **3. Ongoing Monitoring**
    - Frequent re-assessment of fluid status and tissue perfusion.
    """
