import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

# Import custom modules
from models.sepsis_model import SepsisPredictor
from utils.data_processing import validate_patient_data, normalize_vitals
from utils.risk_calculator import calculate_risk_score, get_risk_category
from components.patient_input import render_patient_input_form
from components.dashboard import render_patient_dashboard
from components.alerts import render_alert_system

# Page configuration
st.set_page_config(
    page_title="ICU Sepsis Risk Monitor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Medical disclaimer
st.markdown("""
⚠️ **MEDICAL DISCLAIMER**: This application is for educational and research purposes only. 
It should not be used as a substitute for professional medical judgment or diagnosis. 
Always consult qualified healthcare professionals for patient care decisions.
""")

# Initialize session state
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = pd.DataFrame()
if 'current_patient_id' not in st.session_state:
    st.session_state.current_patient_id = None
if 'sepsis_model' not in st.session_state:
    st.session_state.sepsis_model = SepsisPredictor()

def main():
    st.title("🏥 ICU Sepsis Risk Prediction System")
    st.markdown("Real-time patient monitoring and sepsis risk assessment")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        ["Patient Input", "Risk Dashboard", "Historical Analysis", "System Status"]
    )

    # System Pulse Summary in Sidebar
    if not st.session_state.patient_data.empty:
        st.sidebar.markdown("---")
        st.sidebar.subheader("System Pulse")
        high_risk_count = len(st.session_state.patient_data[
            st.session_state.patient_data['risk_score'] >= 75
        ]['patient_id'].unique())
        st.sidebar.metric("Critical Patients", high_risk_count)
        st.sidebar.info(f"Total Patients: {len(st.session_state.patient_data['patient_id'].unique())}")
    
    if page == "Patient Input":
        render_patient_input_page()
    elif page == "Risk Dashboard":
        render_dashboard_page()
    elif page == "Historical Analysis":
        render_historical_page()
    elif page == "System Status":
        render_system_status_page()

def render_patient_input_page():
    st.header("📝 Patient Data Input")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Patient identification
        st.subheader("Patient Information")
        patient_id = st.text_input("Patient ID", placeholder="Enter unique patient identifier")
        
    if patient_id:
            st.session_state.current_patient_id = patient_id
            
            # Render patient input form
            patient_data = render_patient_input_form()
            
            if patient_data and st.button("Submit Patient Data", type="primary"):
                # Validate data
                validation_result = validate_patient_data(patient_data)
                
                if validation_result['valid']:
                    # Add timestamp and patient ID
                    patient_data['timestamp'] = datetime.now()
                    patient_data['patient_id'] = patient_id
                    
                    # Calculate risk score
                    risk_score = st.session_state.sepsis_model.predict_risk(patient_data)
                    patient_data['risk_score'] = risk_score
                    patient_data['risk_category'] = get_risk_category(risk_score)
                    
                    # Store data
                    if st.session_state.patient_data.empty:
                        st.session_state.patient_data = pd.DataFrame([patient_data])
                    else:
                        st.session_state.patient_data = pd.concat([
                            st.session_state.patient_data, 
                            pd.DataFrame([patient_data])
                        ], ignore_index=True)
                    
                    st.success(f"✅ Data submitted successfully! Risk Score: {risk_score:.1f}%")
                    
                    # Show immediate risk assessment
                    render_immediate_risk_assessment(patient_data)
                    
                else:
                    st.error("❌ Data validation failed:")
                    for error in validation_result['errors']:
                        st.error(f"• {error}")
    
    with col2:
        st.subheader("Quick Reference")
        st.markdown("""
        **Normal Vital Sign Ranges:**
        - Temperature: 36.1-37.2°C
        - Heart Rate: 60-100 bpm
        - Respiratory Rate: 12-20 breaths/min
        - Systolic BP: 90-140 mmHg
        - Diastolic BP: 60-90 mmHg
        - WBC Count: 4.5-11.0 × 10³/μL
        - Lactate: 0.5-2.2 mmol/L
        """)

def render_immediate_risk_assessment(patient_data):
    st.subheader("🎯 Immediate Risk Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    risk_score = patient_data['risk_score']
    risk_category = patient_data['risk_category']
    
    with col1:
        # Risk score gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = risk_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Sepsis Risk Score"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 25], 'color': "lightgreen"},
                    {'range': [25, 50], 'color': "yellow"},
                    {'range': [50, 75], 'color': "orange"},
                    {'range': [75, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("Risk Category", risk_category)
        st.metric("Patient ID", patient_data['patient_id'])
        st.metric("Assessment Time", patient_data['timestamp'].strftime("%H:%M:%S"))
    
    with col3:
        # Alert system
        render_alert_system(patient_data)

def render_dashboard_page():
    st.header("📊 Patient Risk Dashboard")
    
    if st.session_state.patient_data.empty:
        st.warning("No patient data available. Please input patient data first.")
        return
    
    # Patient selector
    patients = st.session_state.patient_data['patient_id'].unique()
    selected_patient = st.selectbox("Select Patient", patients)
    
    if selected_patient:
        patient_records = st.session_state.patient_data[
            st.session_state.patient_data['patient_id'] == selected_patient
        ].sort_values('timestamp')
        
        render_patient_dashboard(patient_records)

def render_historical_page():
    st.header("📈 Historical Risk Analysis")
    
    if st.session_state.patient_data.empty:
        st.warning("No historical data available.")
        return
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        # Filters
        st.subheader("Filters")
        patients = st.multiselect(
            "Select Patients",
            st.session_state.patient_data['patient_id'].unique(),
            default=st.session_state.patient_data['patient_id'].unique()
        )
        
        time_range = st.slider(
            "Time Range (hours)",
            min_value=1,
            max_value=24,
            value=12
        )
    
    with col1:
        if patients:
            # Filter data
            filtered_data = st.session_state.patient_data[
                st.session_state.patient_data['patient_id'].isin(patients)
            ]
            
            # Time series plot
            fig = px.line(
                filtered_data,
                x='timestamp',
                y='risk_score',
                color='patient_id',
                title='Risk Score Trends Over Time'
            )
            fig.add_hline(y=75, line_dash="dash", line_color="red", 
            annotation_text="High Risk Threshold")
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk distribution
            fig2 = px.histogram(
                filtered_data,
                x='risk_category',
                title='Risk Category Distribution'
            )
            st.plotly_chart(fig2, use_container_width=True)

def render_system_status_page():
    st.header("⚙️ System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Model Information")
        st.info(f"Model Type: {st.session_state.sepsis_model.model_type}")
        st.info(f"Model Status: {'Active' if st.session_state.sepsis_model.is_loaded else 'Not Loaded'}")
        st.info(f"Total Patients Monitored: {len(st.session_state.patient_data['patient_id'].unique()) if not st.session_state.patient_data.empty else 0}")
        st.info(f"Total Records: {len(st.session_state.patient_data) if not st.session_state.patient_data.empty else 0}")
    
    with col2:
        st.subheader("Data Quality")
        if not st.session_state.patient_data.empty:
            # Calculate data quality metrics
            complete_records = st.session_state.patient_data.dropna().shape[0]
            total_records = st.session_state.patient_data.shape[0]
            completeness = (complete_records / total_records) * 100 if total_records > 0 else 0
            
            st.metric("Data Completeness", f"{completeness:.1f}%")
            st.metric("Recent Records (Last Hour)", 
                len(st.session_state.patient_data[
                        st.session_state.patient_data['timestamp'] > 
                        datetime.now() - timedelta(hours=1)
                    ]))
        else:
            st.warning("No data available for quality analysis")
    
    # Data export
    st.subheader("Data Export")
    if not st.session_state.patient_data.empty:
        csv_data = st.session_state.patient_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Patient Data (CSV)",
            data=csv_data,
            file_name=f"sepsis_monitoring_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
