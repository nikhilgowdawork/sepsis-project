def calculate_risk_score(data):
    return 0.5


def get_risk_category(score):
    if score > 75:
        return "Critical Risk"
    elif score > 50:
        return "High Risk"
    elif score > 25:
        return "Moderate Risk"
    else:
        return "Low Risk"


def get_risk_color(score):
    if score > 75:
        return "red"
    elif score > 50:
        return "orange"
    elif score > 25:
        return "yellow"
    else:
        return "green"


# ✅ FIXED FUNCTION (takes 2 arguments)
def generate_risk_recommendations(patient_data, risk_score):
    recommendations = []

    if risk_score >= 75:
        recommendations.extend([
            "🚨 IMMEDIATE ATTENTION REQUIRED",
            "Activate sepsis protocol",
            "Start antibiotics immediately",
            "Consider ICU admission"
        ])
    elif risk_score >= 50:
        recommendations.extend([
            "⚠️ Close monitoring required",
            "Check vitals frequently",
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


def calculate_intervention_urgency(score):
    if score >= 75:
        return {
            'level': 'IMMEDIATE',
            'timeframe': 'Within 15 minutes',
            'priority': 'Critical',
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
