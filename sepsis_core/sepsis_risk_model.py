import numpy as np
from typing import Dict, List, Tuple, Optional

def calculate_risk_score(patient_data: Dict, model_prediction: Optional[float] = None) -> float:
    """
    Calculate comprehensive sepsis risk score combining model prediction with clinical rules.
    
    Args:
        patient_data (Dict): Patient vital signs and demographics
        model_prediction (float): ML model prediction (0-100)
        
    Returns:
        float: Final risk score (0-100)
    """
    if model_prediction is not None:
        base_score = model_prediction
    else:
        # Fallback calculation if model is unavailable
        base_score = calculate_clinical_risk_score(patient_data)
    
    # Apply clinical adjustments
    adjusted_score = apply_sepsis_criteria(patient_data, base_score)
    
    # Ensure score is within bounds
    return min(max(adjusted_score, 0.0), 100.0)

def calculate_clinical_risk_score(patient_data: Dict) -> float:
    """
    Calculate risk score using clinical criteria when ML model is unavailable.
    Based on SIRS (Systemic Inflammatory Response Syndrome) criteria and other indicators.
    """
    score = 0.0
    
    # SIRS Criteria
    sirs_count = 0
    
    # Temperature criterion
    temp = patient_data.get('temperature', 37.0)
    if temp > 38.0 or temp < 36.0:
        sirs_count += 1
        score += 15
    
    # Heart rate criterion
    hr = patient_data.get('heart_rate', 80)
    if hr > 90:
        sirs_count += 1
        score += 10
    
    # Respiratory rate criterion
    rr = patient_data.get('respiratory_rate', 16)
    if rr > 20:
        sirs_count += 1
        score += 10
    
    # WBC criterion
    wbc = patient_data.get('wbc_count', 8.0)
    if wbc > 12.0 or wbc < 4.0:
        sirs_count += 1
        score += 15
    
    # SIRS bonus (≥2 criteria significantly increases risk)
    if sirs_count >= 2:
        score += 20
    if sirs_count >= 3:
        score += 30
    
    # Organ dysfunction indicators
    
    # Hypotension
    systolic = patient_data.get('systolic_bp', 120)
    if systolic < 90:
        score += 25
    elif systolic < 100:
        score += 15
    
    # Elevated lactate (tissue hypoperfusion)
    lactate = patient_data.get('lactate', 1.5)
    if lactate > 2.0:
        score += 20
    if lactate > 4.0:
        score += 40
    
    # Age factor
    age = patient_data.get('age', 65)
    if age > 65:
        score += 5
    if age > 75:
        score += 10
    
    return score

def apply_sepsis_criteria(patient_data: Dict, base_score: float) -> float:
    """
    Apply Sepsis-3 criteria and other clinical guidelines to adjust risk score.
    """
    adjusted_score = base_score
    
    # Quick SOFA (qSOFA) criteria
    qsofa_score = calculate_qsofa_score(patient_data)
    if qsofa_score >= 2:
        adjusted_score += 15  # Significantly increased risk
    
    # Severe sepsis indicators
    if is_severe_sepsis_suspected(patient_data):
        adjusted_score += 25
    
    # Septic shock indicators
    if is_septic_shock_suspected(patient_data):
        adjusted_score += 40
    
    return adjusted_score

def calculate_qsofa_score(patient_data: Dict) -> int:
    """
    Calculate quick Sequential Organ Failure Assessment (qSOFA) score.
    
    Returns:
        int: qSOFA score (0-3)
    """
    score = 0
    
    # Altered mental status (assumed normal for this implementation)
    # In real implementation, this would be assessed separately
    
    # Systolic blood pressure ≤ 100 mmHg
    systolic = patient_data.get('systolic_bp', 120)
    if systolic <= 100:
        score += 1
    
    # Respiratory rate ≥ 22 breaths/min
    rr = patient_data.get('respiratory_rate', 16)
    if rr >= 22:
        score += 1
    
    return score

def is_severe_sepsis_suspected(patient_data: Dict) -> bool:
    """
    Check for severe sepsis indicators (sepsis with organ dysfunction).
    """
    indicators = []
    
    # Cardiovascular dysfunction
    systolic = patient_data.get('systolic_bp', 120)
    if systolic < 90:
        indicators.append('hypotension')
    
    # Tissue hypoperfusion
    lactate = patient_data.get('lactate', 1.5)
    if lactate > 2.0:
        indicators.append('elevated_lactate')
    
    # Respiratory dysfunction (simplified)
    rr = patient_data.get('respiratory_rate', 16)
    if rr > 30:
        indicators.append('respiratory_dysfunction')
    
    # Hematologic dysfunction
    wbc = patient_data.get('wbc_count', 8.0)
    if wbc < 4.0:
        indicators.append('leukopenia')
    
    return len(indicators) >= 1

def is_septic_shock_suspected(patient_data: Dict) -> bool:
    """
    Check for septic shock indicators (severe sepsis with persistent hypotension).
    """
    # Persistent hypotension despite fluid resuscitation
    systolic = patient_data.get('systolic_bp', 120)
    lactate = patient_data.get('lactate', 1.5)
    
    # Simplified criteria: hypotension + elevated lactate
    return systolic < 90 and lactate > 2.0

def get_risk_category(risk_score: float) -> str:
    """
    Categorize risk score into clinical risk levels.
    
    Args:
        risk_score (float): Risk score (0-100)
        
    Returns:
        str: Risk category
    """
    if risk_score < 25:
        return "Low Risk"
    elif risk_score < 50:
        return "Moderate Risk"
    elif risk_score < 75:
        return "High Risk"
    else:
        return "Critical Risk"

def get_risk_color(risk_score: float) -> str:
    """
    Get color code for risk visualization.
    
    Args:
        risk_score (float): Risk score (0-100)
        
    Returns:
        str: Color name or hex code
    """
    if risk_score < 25:
        return "green"
    elif risk_score < 50:
        return "yellow"
    elif risk_score < 75:
        return "orange"
    else:
        return "red"

def generate_risk_recommendations(patient_data: Dict, risk_score: float) -> List[str]:
    """
    Generate clinical recommendations based on risk assessment.
    
    Args:
        patient_data (Dict): Patient data
        risk_score (float): Calculated risk score
        
    Returns:
        List[str]: List of clinical recommendations
    """
    recommendations = []
    
    if risk_score >= 75:
        recommendations.extend([
            "🚨 IMMEDIATE ATTENTION REQUIRED",
            "Consider sepsis protocol activation",
            "Obtain blood cultures before antibiotics",
            "Consider broad-spectrum antibiotics",
            "Fluid resuscitation if hypotensive",
            "Consider ICU consultation"
        ])
    elif risk_score >= 50:
        recommendations.extend([
            "⚠️ Close monitoring required",
            "Consider blood cultures",
            "Monitor vital signs q15-30 minutes",
            "Consider infectious disease consultation",
            "Reassess in 1-2 hours"
        ])
    elif risk_score >= 25:
        recommendations.extend([
            "📋 Increased surveillance",
            "Monitor vital signs q1-2 hours",
            "Consider basic labs if not recent",
            "Reassess in 2-4 hours"
        ])
    else:
        recommendations.extend([
            "✅ Continue routine monitoring",
            "Standard vital sign monitoring",
            "Reassess per unit protocol"
        ])
    
    # Specific recommendations based on vital signs
    temp = patient_data.get('temperature', 37.0)
    if temp > 38.5:
        recommendations.append("🌡️ Consider antipyretics and cooling measures")
    
    lactate = patient_data.get('lactate', 1.5)
    if lactate > 4.0:
        recommendations.append("🔬 Repeat lactate in 2-6 hours")
    
    systolic = patient_data.get('systolic_bp', 120)
    if systolic < 90:
        recommendations.append("💧 Consider fluid bolus if no contraindications")
    
    return recommendations

def calculate_intervention_urgency(risk_score: float) -> Dict:
    """
    Calculate intervention urgency based on risk score.
    
    Args:
        risk_score (float): Risk score (0-100)
        
    Returns:
        Dict: Urgency information including timeframe and priority
    """
    if risk_score >= 75:
        return {
            'level': 'IMMEDIATE',
            'timeframe': 'Within 15 minutes',
            'priority': 'Critical',
            'color': 'red'
        }
    elif risk_score >= 50:
        return {
            'level': 'URGENT',
            'timeframe': 'Within 1 hour',
            'priority': 'High',
            'color': 'orange'
        }
    elif risk_score >= 25:
        return {
            'level': 'MODERATE',
            'timeframe': 'Within 2-4 hours',
            'priority': 'Medium',
            'color': 'yellow'
        }
    else:
        return {
            'level': 'ROUTINE',
            'timeframe': 'Per unit protocol',
            'priority': 'Low',
            'color': 'green'
        }
