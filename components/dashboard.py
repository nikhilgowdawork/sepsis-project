import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime, timedelta
from utils.risk_calculator import get_risk_category, get_risk_color, generate_risk_recommendations, get_sepsis_protocol
from utils.data_processing import detect_trends, calculate_vital_signs_scores
from components.alerts import get_gemini_recommendations

def render_patient_dashboard(patient_records):
    """
    Render the main patient dashboard with current status and trends.
    
    Args:
        patient_records (pd.DataFrame): Patient data records sorted by timestamp
    """
    if patient_records.empty:
        st.warning("No data available for selected patient.")
        return
    
    # Get latest record
    latest_record = patient_records.iloc[-1]
    patient_id = latest_record['patient_id']
    
    st.subheader(f"Patient Dashboard: {patient_id}")
    
    # Current Status Overview
    render_current_status(latest_record)
    
    # Trends Analysis
    if len(patient_records) > 1:
        render_trends_analysis(patient_records)
    
    # Vital Signs Timeline
    render_vital_signs_timeline(patient_records)
    
    # Risk History
    render_risk_history(patient_records)
    
    # Clinical Recommendations
    render_clinical_recommendations(latest_record)
    
    st.divider()
    render_dashboard_actions(latest_record.to_dict())

def render_dashboard_actions(patient_data):
    """Render unique dashboard intervention buttons and handle persistent UI state."""
    st.markdown("### ⚡ Clinical Interventions")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📞 Call MD", key='dash_call_physician', use_container_width=True):
            st.session_state.show_phys_card = not st.session_state.show_phys_card
            
    with col2:
        if st.button("🔄 Re-Lactate", key='dash_repeat_lactate', use_container_width=True):
            predictor = st.session_state.sepsis_model
            updated_risk = predictor.predict_risk(patient_data)
            if not isinstance(updated_risk, str):
                pid = patient_data.get('patient_id')
                df = st.session_state.patient_data
                p_indices = df[df['patient_id'] == pid].index
                if not p_indices.empty:
                    st.session_state.patient_data.at[p_indices[-1], 'risk_score'] = updated_risk
                    st.session_state.patient_data.at[p_indices[-1], 'risk_category'] = get_risk_category(updated_risk)
                    st.toast(f"Risk Updated: {updated_risk:.1f}%", icon="🔄")
                    time.sleep(0.5)
                    st.rerun()
            
    with col3:
        if st.button("✨ AI Recs", key='dash_view_recommendations_v2', use_container_width=True):
            st.session_state.ready_to_show_ai = not st.session_state.get('ready_to_show_ai', False)
            
    with col4:
        if st.button("💊 Protocol", key='dash_sepsis_protocol', use_container_width=True):
            st.session_state.show_protocol = not st.session_state.show_protocol
            
    with col5:
        if st.button("❓ Help", key='dash_help', use_container_width=True):
            st.session_state.show_help = not st.session_state.show_help

    # --- Persistent UI Elements ---
    if st.session_state.show_phys_card:
        with st.container(border=True):
            st.error("🆘 **EMERGENCY CONTACT**")
            st.markdown(f"""
            **On-Call Intensivist**: Dr. Kumar  
            **Unit**: Medical ICU  
            **Direct Link**: [📞 Call Now](tel:+91XXXXXXXXXX)
            """)
            st.text_area("Physician Notes", key="dash_phys_notes_input", placeholder="Log conversation or instructions here...")
            if st.button("Close Contact Card", key="dash_close_phys_card"):
                st.session_state.show_phys_card = False
                st.rerun()

    if st.session_state.get('ready_to_show_ai', False):
        vitals_summary = {k: v for k, v in patient_data.items() if k in 
                          ['temperature', 'heart_rate', 'respiratory_rate', 'systolic_bp', 'lactate', 'wbc_count']}
        with st.spinner("Consulting AI Specialist (Gemini 1.5 Flash)..."):
            recommendations = get_gemini_recommendations(vitals_summary)
            st.info(f"💡 **AI Clinical Insights**:\n\n{recommendations}")
        if st.button("Dismiss AI Recommendations", key="dash_dismiss_ai_recs"):
            st.session_state.ready_to_show_ai = False
            st.rerun()

    if st.session_state.show_protocol:
        with st.expander("📖 Sepsis-3 Guidelines", expanded=True):
            st.markdown(get_sepsis_protocol())
            if st.button("Close Protocol View", key="dash_close_protocol"):
                st.session_state.show_protocol = False
                st.rerun()

    if st.session_state.show_help:
        st.info("💡 **Dashboard Help**: This view provides real-time risk tracking. Buttons in the grid allow for immediate clinical interventions.")
        if st.button("Close Help", key="dash_close_help_text"):
            st.session_state.show_help = False
            st.rerun()

def render_current_status(latest_record):
    """Render current patient status with key metrics."""
    st.markdown("### 📊 Current Status")
    
    # Risk Score Display
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        # Large risk score gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = latest_record['risk_score'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Sepsis Risk Score"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': get_risk_color(latest_record['risk_score'])},
                'steps': [
                    {'range': [0, 25], 'color': "lightgreen"},
                    {'range': [25, 50], 'color': "yellow"},
                    {'range': [50, 75], 'color': "orange"},
                    {'range': [75, 100], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric(
            "Risk Category",
            latest_record['risk_category'],
            delta=None
        )
        st.metric(
            "Assessment Time",
            latest_record['timestamp'].strftime("%H:%M"),
            delta=None
        )
    
    with col3:
        # Key vital signs
        st.metric(
            "Temperature",
            f"{latest_record['temperature']:.1f}°C",
            delta=f"{latest_record['temperature'] - 37.0:+.1f}" if latest_record['temperature'] != 37.0 else None
        )
        st.metric(
            "Heart Rate",
            f"{latest_record['heart_rate']} bpm",
            delta=f"{latest_record['heart_rate'] - 80:+}" if latest_record['heart_rate'] != 80 else None
        )
    
    with col4:
        st.metric(
            "Blood Pressure",
            f"{latest_record['systolic_bp']}/{latest_record['diastolic_bp']}",
            delta=None
        )
        st.metric(
            "Lactate",
            f"{latest_record['lactate']:.1f} mmol/L",
            delta=f"{latest_record['lactate'] - 1.5:+.1f}" if latest_record['lactate'] != 1.5 else None
        )

def render_vital_signs_overview(latest_record):
    """Render detailed vital signs overview."""
    st.markdown("### 🩺 Vital Signs Overview")
    
    # Calculate vital signs scores
    vital_scores = calculate_vital_signs_scores(latest_record.to_dict())
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Vital signs table
        vital_data = {
            'Parameter': ['Temperature', 'Heart Rate', 'Respiratory Rate', 'Systolic BP', 'Diastolic BP'],
            'Value': [
                f"{latest_record['temperature']:.1f}°C",
                f"{latest_record['heart_rate']} bpm",
                f"{latest_record['respiratory_rate']}/min",
                f"{latest_record['systolic_bp']} mmHg",
                f"{latest_record['diastolic_bp']} mmHg"
            ],
            'Normal Range': [
                "36.1-37.2°C",
                "60-100 bpm",
                "12-20/min",
                "90-140 mmHg",
                "60-90 mmHg"
            ],
            'Score': [
                vital_scores.get('temperature_score', 0),
                vital_scores.get('heart_rate_score', 0),
                vital_scores.get('respiratory_rate_score', 0),
                vital_scores.get('bp_score', 0),
                vital_scores.get('bp_score', 0)  # Same score for systolic/diastolic
            ]
        }
        
        vital_df = pd.DataFrame(vital_data)
        st.dataframe(vital_df, use_container_width=True)
    
    with col2:
        # Laboratory values
        lab_data = {
            'Parameter': ['WBC Count', 'Lactate'],
            'Value': [
                f"{latest_record['wbc_count']:.1f} ×10³/μL",
                f"{latest_record['lactate']:.2f} mmol/L"
            ],
            'Normal Range': [
                "4.5-11.0 ×10³/μL",
                "0.5-2.2 mmol/L"
            ],
            'Score': [
                vital_scores.get('wbc_score', 0),
                vital_scores.get('lactate_score', 0)
            ]
        }
        
        lab_df = pd.DataFrame(lab_data)
        st.dataframe(lab_df, use_container_width=True)
        
        # Overall severity
        st.metric(
            "Overall Severity",
            vital_scores.get('severity', 'Unknown'),
            delta=f"Score: {vital_scores.get('total_score', 0)}"
        )

def render_trends_analysis(patient_records):
    """Render trends analysis for the patient."""
    st.markdown("### 📈 Trends Analysis")
    
    trends_data = detect_trends(patient_records)
    trends = trends_data.get('trends', {})
    alerts = trends_data.get('alerts', [])
    
    if alerts:
        st.markdown("**🚨 Trend Alerts:**")
        for alert in alerts:
            st.error(alert)
    
    if trends:
        # Create trend indicators
        col1, col2, col3, col4 = st.columns(4)
        
        trend_cols = [col1, col2, col3, col4]
        vital_signs = ['risk_score', 'temperature', 'heart_rate', 'lactate']
        
        for i, vital in enumerate(vital_signs):
            if vital in trends and i < len(trend_cols):
                trend = trends[vital]
                
                with trend_cols[i]:
                    # Trend direction indicator
                    if trend['direction'] == 'increasing':
                        delta_color = 'inverse' if vital == 'risk_score' else 'normal'
                        arrow = "↗️"
                    elif trend['direction'] == 'decreasing':
                        delta_color = 'normal' if vital == 'risk_score' else 'inverse'
                        arrow = "↘️"
                    else:
                        delta_color = 'off'
                        arrow = "→"
                    
                    st.metric(
                        vital.replace('_', ' ').title(),
                        f"{trend['current_value']:.1f}",
                        delta=f"{arrow} {trend['percent_change']:+.1f}%",
                        delta_color=delta_color
                    )

def render_vital_signs_timeline(patient_records):
    """Render timeline visualization of vital signs."""
    st.markdown("### ⏱️ Vital Signs Timeline")
    
    # Select vital signs to display
    vital_options = ['temperature', 'heart_rate', 'respiratory_rate', 'systolic_bp', 'lactate', 'wbc_count']
    selected_vitals = st.multiselect(
        "Select vital signs to display:",
        vital_options,
        default=['temperature', 'heart_rate', 'lactate']
    )
    
    if selected_vitals:
        # Create subplots for selected vitals
        from plotly.subplots import make_subplots
        
        n_plots = len(selected_vitals)
        fig = make_subplots(
            rows=n_plots, cols=1,
            subplot_titles=[vital.replace('_', ' ').title() for vital in selected_vitals],
            vertical_spacing=0.15
        )
        
        colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
        
        for i, vital in enumerate(selected_vitals):
            if vital in patient_records.columns:
                fig.add_trace(
                    go.Scatter(
                        x=patient_records['timestamp'],
                        y=patient_records[vital],
                        mode='lines+markers',
                        name=vital.replace('_', ' ').title(),
                        line=dict(color=colors[i % len(colors)], width=2),
                        marker=dict(size=6)
                    ),
                    row=i+1, col=1
                )
        
        fig.update_layout(
            height=200 * n_plots,
            showlegend=False,
            title_text="Vital Signs Over Time"
        )
        
        st.plotly_chart(fig, use_container_width=True)

def render_risk_history(patient_records):
    """Render risk score history with annotations."""
    st.markdown("### 🎯 Risk Score History")
    
    fig = go.Figure()
    
    # Risk score line
    fig.add_trace(go.Scatter(
        x=patient_records['timestamp'],
        y=patient_records['risk_score'],
        mode='lines+markers',
        name='Risk Score',
        line=dict(color='red', width=3),
        marker=dict(size=8)
    ))
    
    # Risk level zones
    fig.add_hline(y=75, line_dash="dash", line_color="red", 
                  annotation_text="Critical Risk", annotation_position="right")
    fig.add_hline(y=50, line_dash="dash", line_color="orange", 
                  annotation_text="High Risk", annotation_position="right")
    fig.add_hline(y=25, line_dash="dash", line_color="yellow", 
                  annotation_text="Moderate Risk", annotation_position="right")
    
    # Add risk category annotations
    for _, record in patient_records.iterrows():
        if record['risk_score'] >= 75:
            fig.add_annotation(
                x=record['timestamp'],
                y=record['risk_score'],
                text="🚨",
                showarrow=False,
                font=dict(size=16)
            )
    
    fig.update_layout(
        title="Sepsis Risk Score Over Time",
        xaxis_title="Time",
        yaxis_title="Risk Score (%)",
        yaxis=dict(range=[0, 100]),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_clinical_recommendations(latest_record):
    """Render clinical recommendations based on current assessment."""
    st.markdown("### 💊 Clinical Recommendations")
    
    risk_score = latest_record['risk_score']
    patient_data = latest_record.to_dict()
    
    recommendations = generate_risk_recommendations(patient_data, risk_score)
    
    if recommendations:
        for recommendation in recommendations:
            if "🚨" in recommendation or "IMMEDIATE" in recommendation:
                st.error(recommendation)
            elif "⚠️" in recommendation:
                st.warning(recommendation)
            elif "📋" in recommendation:
                st.info(recommendation)
            else:
                st.success(recommendation)
    
    # Intervention urgency using Sepsis-3 qSOFA standard
    from utils.risk_calculator import calculate_intervention_urgency
    urgency = calculate_intervention_urgency(risk_score, latest_record.to_dict())
    
    st.markdown("#### ⏰ Intervention Urgency")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if urgency['level'] == 'EMERGENCY':
            st.markdown(f"Urgency Level: <span style='color:red; font-weight:bold;'>{urgency['level']}</span>", unsafe_allow_html=True)
        else:
            st.metric("Urgency Level", urgency['level'])
            
    with col2:
        st.metric("Timeframe", urgency['timeframe'])
    with col3:
        st.metric("Priority", urgency['priority'])

def render_patient_summary_card(patient_record):
    """Render a summary card for a patient."""
    risk_score = patient_record['risk_score']
    risk_color = get_risk_color(risk_score)
    
    with st.container():
        st.markdown(f"""
        <div style="
            border-left: 5px solid {risk_color};
            padding: 10px;
            margin: 10px 0;
            background-color: #f9f9f9;
            border-radius: 5px;
        ">
            <h4>Patient ID: {patient_record['patient_id']}</h4>
            <p><strong>Risk Score:</strong> {risk_score:.1f}% ({patient_record['risk_category']})</p>
            <p><strong>Last Assessment:</strong> {patient_record['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Key Vitals:</strong> T: {patient_record['temperature']:.1f}°C, 
            HR: {patient_record['heart_rate']}, BP: {patient_record['systolic_bp']}/{patient_record['diastolic_bp']}</p>
        </div>
        """, unsafe_allow_html=True)
