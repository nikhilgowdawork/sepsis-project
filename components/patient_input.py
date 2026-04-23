import streamlit as st
from utils.data_processing import normalize_vitals

def render_patient_input_form():
    """
    Render the patient data input form.
    
    Returns:
        dict: Patient data if form is complete, None otherwise
    """
    st.subheader("Vital Signs & Laboratory Values")
    
    # Create columns for organized layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Vital Signs**")
        
        # Temperature
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=30.0,
            max_value=45.0,
            value=37.0,
            step=0.1,
            help="Normal range: 36.1-37.2°C"
        )
        
        # Heart Rate
        heart_rate = st.number_input(
            "Heart Rate (bpm)",
            min_value=20,
            max_value=250,
            value=80,
            step=1,
            help="Normal range: 60-100 bpm"
        )
        
        # Respiratory Rate
        respiratory_rate = st.number_input(
            "Respiratory Rate (breaths/min)",
            min_value=5,
            max_value=60,
            value=16,
            step=1,
            help="Normal range: 12-20 breaths/min"
        )
        
    # Blood Pressure
    st.markdown("**Blood Pressure (mmHg)**")
    col_sys, col_dia = st.columns(2)
    with col_sys:
        systolic_bp = st.number_input(
                "Systolic",
                min_value=50,
                max_value=250,
                value=120,
                step=1
            )
    with col_dia:
        diastolic_bp = st.number_input(
                "Diastolic",
                min_value=30,
                max_value=150,
                value=70,
                step=1
            )
    
    with col2:
        st.markdown("**Laboratory Values**")
        
        # White Blood Cell Count
        wbc_count = st.number_input(
            "WBC Count (× 10³/μL)",
            min_value=0.1,
            max_value=50.0,
            value=8.0,
            step=0.1,
            help="Normal range: 4.5-11.0 × 10³/μL"
        )
        
        # Lactate
        lactate = st.number_input(
            "Lactate (mmol/L)",
            min_value=0.1,
            max_value=20.0,
            value=1.5,
            step=0.1,
            help="Normal range: 0.5-2.2 mmol/L"
        )
        
        st.markdown("**Patient Demographics**")
        
        # Age
        age = st.number_input(
            "Age (years)",
            min_value=0,
            max_value=120,
            value=65,
            step=1
        )
        
        # Gender
        gender = st.selectbox(
            "Gender",
            options=["M", "F"],
            index=0
        )
    
    # Additional clinical information
    st.subheader("Additional Clinical Information")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Clinical notes
        clinical_notes = st.text_area(
            "Clinical Notes (Optional)",
            placeholder="Any relevant clinical observations...",
            height=100
        )
    
    with col4:
        # Risk factors
        st.markdown("**Risk Factors** (Optional)")
        
        immunocompromised = st.checkbox("Immunocompromised")
        recent_surgery = st.checkbox("Recent Surgery (< 30 days)")
        diabetes = st.checkbox("Diabetes")
        chronic_kidney_disease = st.checkbox("Chronic Kidney Disease")
        copd = st.checkbox("COPD")
    
    # Validate blood pressure relationship
    if systolic_bp <= diastolic_bp:
        st.error("⚠️ Systolic blood pressure must be greater than diastolic blood pressure")
        return None
    
    # Compile patient data
    patient_data = {
        'temperature': temperature,
        'heart_rate': heart_rate,
        'respiratory_rate': respiratory_rate,
        'systolic_bp': systolic_bp,
        'diastolic_bp': diastolic_bp,
        'wbc_count': wbc_count,
        'lactate': lactate,
        'age': age,
        'gender': gender,
        'clinical_notes': clinical_notes,
        'risk_factors': {
            'immunocompromised': immunocompromised,
            'recent_surgery': recent_surgery,
            'diabetes': diabetes,
            'chronic_kidney_disease': chronic_kidney_disease,
            'copd': copd
        }
    }
    
    # Normalize the data
    normalized_data = normalize_vitals(patient_data)
    
    return normalized_data

def render_quick_input_form():
    """
    Render a simplified quick input form for urgent cases.
    
    Returns:
        dict: Essential patient data
    """
    st.subheader("⚡ Quick Assessment")
    st.markdown("*Essential vitals for rapid risk assessment*")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        temp = st.number_input("Temp (°C)", value=37.0, step=0.1, key="quick_temp")
        hr = st.number_input("HR (bpm)", value=80, step=1, key="quick_hr")
    
    with col2:
        rr = st.number_input("RR (/min)", value=16, step=1, key="quick_rr")
        systolic = st.number_input("SBP (mmHg)", value=120, step=1, key="quick_sbp")
    
    with col3:
        lactate = st.number_input("Lactate (mmol/L)", value=1.5, step=0.1, key="quick_lactate")
        wbc = st.number_input("WBC (×10³)", value=8.0, step=0.1, key="quick_wbc")
    
    quick_data = {
        'temperature': temp,
        'heart_rate': hr,
        'respiratory_rate': rr,
        'systolic_bp': systolic,
        'diastolic_bp': systolic - 40,  # Estimate diastolic
        'wbc_count': wbc,
        'lactate': lactate,
        'age': 65,  # Default age
        'gender': 'M'  # Default gender
    }
    
    return normalize_vitals(quick_data)

def render_input_validation_feedback(patient_data):
    """
    Display validation feedback for input data.
    
    Args:
        patient_data (dict): Patient data to validate
    """
    from utils.data_processing import validate_patient_data
    
    validation_result = validate_patient_data(patient_data)
    
    if not validation_result['valid']:
        st.error("❌ **Data Validation Issues:**")
        for error in validation_result['errors']:
            st.error(f"• {error}")
    else:
        st.success("✅ **Data validation passed**")
    
    # Display clinical flags
    flags = []
    
    # Temperature flags
    temp = patient_data.get('temperature', 37.0)
    if temp > 38.3:
        flags.append("🌡️ Fever detected")
    elif temp < 36.0:
        flags.append("🧊 Hypothermia detected")
    
    # Heart rate flags
    hr = patient_data.get('heart_rate', 80)
    if hr > 100:
        flags.append("💓 Tachycardia")
    elif hr < 60:
        flags.append("🐌 Bradycardia")
    
    # Blood pressure flags
    systolic = patient_data.get('systolic_bp', 120)
    if systolic < 90:
        flags.append("📉 Hypotension")
    elif systolic > 180:
        flags.append("📈 Hypertension")
    
    # Lab value flags
    wbc = patient_data.get('wbc_count', 8.0)
    if wbc > 12.0:
        flags.append("🔬 Elevated WBC")
    elif wbc < 4.0:
        flags.append("📉 Low WBC")
    
    lactate = patient_data.get('lactate', 1.5)
    if lactate > 2.2:
        flags.append("⚠️ Elevated Lactate")
    
    if flags:
        st.warning("**Clinical Flags:**")
        for flag in flags:
            st.warning(f"• {flag}")

def render_preset_scenarios():
    """
    Render preset clinical scenarios for testing and demonstration.
    
    Returns:
        dict: Selected scenario data or None
    """
    st.subheader("📋 Preset Clinical Scenarios")
    st.markdown("*Select a scenario for demonstration or testing*")
    
    scenarios = {
        "Normal Patient": {
            'temperature': 37.0,
            'heart_rate': 75,
            'respiratory_rate': 16,
            'systolic_bp': 120,
            'diastolic_bp': 70,
            'wbc_count': 7.5,
            'lactate': 1.2,
            'age': 45,
            'gender': 'F'
        },
        "Early Sepsis": {
            'temperature': 38.8,
            'heart_rate': 105,
            'respiratory_rate': 24,
            'systolic_bp': 110,
            'diastolic_bp': 65,
            'wbc_count': 14.2,
            'lactate': 2.8,
            'age': 67,
            'gender': 'M'
        },
        "Severe Sepsis": {
            'temperature': 39.2,
            'heart_rate': 125,
            'respiratory_rate': 28,
            'systolic_bp': 85,
            'diastolic_bp': 50,
            'wbc_count': 18.5,
            'lactate': 4.2,
            'age': 72,
            'gender': 'F'
        },
        "Septic Shock": {
            'temperature': 35.8,
            'heart_rate': 140,
            'respiratory_rate': 32,
            'systolic_bp': 70,
            'diastolic_bp': 40,
            'wbc_count': 3.2,
            'lactate': 6.8,
            'age': 78,
            'gender': 'M'
        }
    }
    
    selected_scenario = st.selectbox(
        "Choose a scenario:",
        ["None"] + list(scenarios.keys())
    )
    
    if selected_scenario != "None":
        scenario_data = scenarios[selected_scenario].copy()
        
        st.info(f"**{selected_scenario}** scenario loaded")
        
        # Display scenario details
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Temperature", f"{scenario_data['temperature']}°C")
            st.metric("Heart Rate", f"{scenario_data['heart_rate']} bpm")
            st.metric("Respiratory Rate", f"{scenario_data['respiratory_rate']}/min")
        
        with col2:
            st.metric("Blood Pressure", f"{scenario_data['systolic_bp']}/{scenario_data['diastolic_bp']}")
            st.metric("WBC Count", f"{scenario_data['wbc_count']} ×10³")
            st.metric("Lactate", f"{scenario_data['lactate']} mmol/L")
        
        with col3:
            st.metric("Age", f"{scenario_data['age']} years")
            st.metric("Gender", scenario_data['gender'])
        
        if st.button("Load This Scenario", type="primary"):
            return scenario_data
    
    return None
