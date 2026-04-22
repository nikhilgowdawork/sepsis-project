import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

def validate_patient_data(patient_data: Dict) -> Dict:
    """
    Validate patient data for completeness and clinical ranges.
    
    Args:
        patient_data (Dict): Dictionary containing patient vital signs
        
    Returns:
        Dict: Validation result with 'valid' boolean and 'errors' list
    """
    errors = []
    
    # Required fields
    required_fields = [
        'temperature', 'heart_rate', 'respiratory_rate',
        'systolic_bp', 'diastolic_bp', 'wbc_count', 'lactate'
    ]
    
    # Check for missing required fields
    for field in required_fields:
        if field not in patient_data or patient_data[field] is None:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return {'valid': False, 'errors': errors}
    
    # Validate ranges
    validations = [
        ('temperature', 30.0, 45.0, "Temperature must be between 30-45°C"),
        ('heart_rate', 20, 250, "Heart rate must be between 20-250 bpm"),
        ('respiratory_rate', 5, 60, "Respiratory rate must be between 5-60 breaths/min"),
        ('systolic_bp', 50, 250, "Systolic BP must be between 50-250 mmHg"),
        ('diastolic_bp', 30, 150, "Diastolic BP must be between 30-150 mmHg"),
        ('wbc_count', 0.1, 50.0, "WBC count must be between 0.1-50.0 × 10³/μL"),
        ('lactate', 0.1, 20.0, "Lactate must be between 0.1-20.0 mmol/L")
    ]
    
    for field, min_val, max_val, error_msg in validations:
        value = patient_data.get(field)
        if value is not None:
            try:
                value = float(value)
                if not (min_val <= value <= max_val):
                    errors.append(error_msg)
            except (ValueError, TypeError):
                errors.append(f"Invalid value for {field}: must be a number")
    
    # Additional validation rules
    if 'systolic_bp' in patient_data and 'diastolic_bp' in patient_data:
        try:
            systolic = float(patient_data['systolic_bp'])
            diastolic = float(patient_data['diastolic_bp'])
            if systolic <= diastolic:
                errors.append("Systolic BP must be greater than diastolic BP")
        except (ValueError, TypeError):
            pass  # Already caught above
    
    # Age validation if provided
    if 'age' in patient_data and patient_data['age'] is not None:
        try:
            age = float(patient_data['age'])
            if not (0 <= age <= 120):
                errors.append("Age must be between 0-120 years")
        except (ValueError, TypeError):
            errors.append("Invalid age: must be a number")
    
    return {'valid': len(errors) == 0, 'errors': errors}

def normalize_vitals(patient_data: Dict) -> Dict:
    """
    Normalize vital signs to standard units and formats.
    
    Args:
        patient_data (Dict): Raw patient data
        
    Returns:
        Dict: Normalized patient data
    """
    normalized_data = patient_data.copy()
    
    # Ensure numeric types
    numeric_fields = [
        'temperature', 'heart_rate', 'respiratory_rate',
        'systolic_bp', 'diastolic_bp', 'wbc_count', 'lactate', 'age'
    ]
    
    for field in numeric_fields:
        if field in normalized_data and normalized_data[field] is not None:
            try:
                normalized_data[field] = float(normalized_data[field])
            except (ValueError, TypeError):
                normalized_data[field] = None
    
    # Round to appropriate decimal places
    if 'temperature' in normalized_data:
        normalized_data['temperature'] = round(normalized_data['temperature'], 1)
    
    if 'wbc_count' in normalized_data:
        normalized_data['wbc_count'] = round(normalized_data['wbc_count'], 1)
    
    if 'lactate' in normalized_data:
        normalized_data['lactate'] = round(normalized_data['lactate'], 2)
    
    # Ensure integer types for whole number vitals
    integer_fields = ['heart_rate', 'respiratory_rate', 'systolic_bp', 'diastolic_bp']
    for field in integer_fields:
        if field in normalized_data and normalized_data[field] is not None:
            normalized_data[field] = int(round(normalized_data[field]))
    
    return normalized_data

def calculate_vital_signs_scores(patient_data: Dict) -> Dict:
    """
    Calculate individual vital sign abnormality scores.
    
    Args:
        patient_data (Dict): Patient vital signs
        
    Returns:
        Dict: Vital sign scores and overall severity
    """
    scores = {}
    
    # Temperature score
    temp = patient_data.get('temperature', 37.0)
    if 36.1 <= temp <= 37.2:
        scores['temperature_score'] = 0
    elif 35.0 <= temp < 36.1 or 37.3 <= temp <= 38.5:
        scores['temperature_score'] = 1
    elif 34.0 <= temp < 35.0 or 38.6 <= temp <= 39.0:
        scores['temperature_score'] = 2
    else:
        scores['temperature_score'] = 3
    
    # Heart rate score
    hr = patient_data.get('heart_rate', 80)
    if 60 <= hr <= 100:
        scores['heart_rate_score'] = 0
    elif 50 <= hr < 60 or 101 <= hr <= 120:
        scores['heart_rate_score'] = 1
    elif 40 <= hr < 50 or 121 <= hr <= 150:
        scores['heart_rate_score'] = 2
    else:
        scores['heart_rate_score'] = 3
    
    # Respiratory rate score
    rr = patient_data.get('respiratory_rate', 16)
    if 12 <= rr <= 20:
        scores['respiratory_rate_score'] = 0
    elif 10 <= rr < 12 or 21 <= rr <= 25:
        scores['respiratory_rate_score'] = 1
    elif 8 <= rr < 10 or 26 <= rr <= 30:
        scores['respiratory_rate_score'] = 2
    else:
        scores['respiratory_rate_score'] = 3
    
    # Blood pressure score (using systolic)
    systolic = patient_data.get('systolic_bp', 120)
    if 90 <= systolic <= 140:
        scores['bp_score'] = 0
    elif 80 <= systolic < 90 or 141 <= systolic <= 160:
        scores['bp_score'] = 1
    elif 70 <= systolic < 80 or 161 <= systolic <= 180:
        scores['bp_score'] = 2
    else:
        scores['bp_score'] = 3
    
    # WBC count score
    wbc = patient_data.get('wbc_count', 8.0)
    if 4.5 <= wbc <= 11.0:
        scores['wbc_score'] = 0
    elif 3.5 <= wbc < 4.5 or 11.1 <= wbc <= 15.0:
        scores['wbc_score'] = 1
    elif 2.0 <= wbc < 3.5 or 15.1 <= wbc <= 20.0:
        scores['wbc_score'] = 2
    else:
        scores['wbc_score'] = 3
    
    # Lactate score
    lactate = patient_data.get('lactate', 1.5)
    if lactate <= 2.2:
        scores['lactate_score'] = 0
    elif 2.3 <= lactate <= 4.0:
        scores['lactate_score'] = 2
    else:
        scores['lactate_score'] = 3
    
    # Calculate total severity score
    total_score = sum(scores.values())
    scores['total_score'] = total_score
    
    # Determine severity level
    if total_score <= 3:
        scores['severity'] = 'Low'
    elif total_score <= 7:
        scores['severity'] = 'Moderate'
    elif total_score <= 12:
        scores['severity'] = 'High'
    else:
        scores['severity'] = 'Critical'
    
    return scores

def detect_trends(patient_history: pd.DataFrame, window_size: int = 3) -> Dict:
    """
    Detect trends in patient vital signs over time.
    
    Args:
        patient_history (pd.DataFrame): Historical patient data
        window_size (int): Number of recent measurements to analyze
        
    Returns:
        Dict: Trend analysis results
    """
    if len(patient_history) < 2:
        return {'trends': {}, 'alerts': []}
    
    # Sort by timestamp
    history = patient_history.sort_values('timestamp').tail(window_size)
    
    trends = {}
    alerts = []
    
    vital_signs = ['temperature', 'heart_rate', 'respiratory_rate', 
                   'systolic_bp', 'diastolic_bp', 'wbc_count', 'lactate', 'risk_score']
    
    for vital in vital_signs:
        if vital in history.columns and len(history[vital].dropna()) >= 2:
            values = history[vital].dropna().values
            
            # Calculate trend direction
            if len(values) >= 2:
                recent_change = values[-1] - values[0]
                percent_change = (recent_change / values[0]) * 100 if values[0] != 0 else 0
                
                # Determine trend direction
                if abs(percent_change) < 5:
                    direction = 'stable'
                elif recent_change > 0:
                    direction = 'increasing'
                else:
                    direction = 'decreasing'
                
                trends[vital] = {
                    'direction': direction,
                    'change': recent_change,
                    'percent_change': percent_change,
                    'current_value': values[-1],
                    'previous_value': values[0]
                }
                
                # Generate alerts for concerning trends
                if vital == 'risk_score' and direction == 'increasing' and percent_change > 20:
                    alerts.append(f"⚠️ Risk score trending upward ({percent_change:.1f}% increase)")
                elif vital == 'lactate' and direction == 'increasing' and percent_change > 15:
                    alerts.append(f"⚠️ Lactate levels rising ({percent_change:.1f}% increase)")
                elif vital == 'temperature' and values[-1] > 38.5:
                    alerts.append(f"🌡️ High fever detected ({values[-1]:.1f}°C)")
    
    return {'trends': trends, 'alerts': alerts}

def calculate_risk_score(data):
    # temporary logic
    return 0.5

def get_risk_category(score):
    if score > 0.7:
        return "High Risk"
    elif score > 0.4:
        return "Medium Risk"
    else:
        return "Low Risk"

