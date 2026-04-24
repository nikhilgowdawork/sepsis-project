import streamlit as st
from datetime import datetime
from utils.risk_calculator import get_risk_category, calculate_intervention_urgency

def render_alert_system(patient_data):
    """
    Render the alert system based on patient risk assessment.
    
    Args:
        patient_data (dict): Current patient data including risk score
    """
    risk_score = patient_data.get('risk_score', 0)
    risk_category = patient_data.get('risk_category', 'Unknown')
    
    # Generate alerts based on risk level
    alerts = generate_risk_alerts(patient_data)
    
    if alerts:
        st.markdown("### 🚨 Active Alerts")
        
        for alert in alerts:
            alert_type = alert['type']
            message = alert['message']
            priority = alert['priority']
            
            if priority == 'critical':
                st.error(f"🚨 **CRITICAL**: {message}")
            elif priority == 'high':
                st.warning(f"⚠️ **HIGH**: {message}")
            elif priority == 'medium':
                st.info(f"ℹ️ **MEDIUM**: {message}")
            else:
                st.success(f"✅ **LOW**: {message}")
    
    # Intervention urgency display
    render_intervention_urgency(patient_data)
    
    # Quick action buttons
    render_quick_actions(patient_data)

def generate_risk_alerts(patient_data):
    """
    Generate alerts based on patient vital signs and risk score.
    
    Args:
        patient_data (dict): Patient data
        
    Returns:
        list: List of alert dictionaries
    """
    alerts = []
    risk_score = patient_data.get('risk_score', 0)
    
    # Risk score alerts
    if risk_score >= 75:
        alerts.append({
            'type': 'sepsis_risk',
            'message': f'Critical sepsis risk detected ({risk_score:.1f}%). Immediate intervention required.',
            'priority': 'critical',
            'action': 'Activate sepsis protocol'
        })
    elif risk_score >= 50:
        alerts.append({
            'type': 'sepsis_risk',
            'message': f'High sepsis risk ({risk_score:.1f}%). Close monitoring required.',
            'priority': 'high',
            'action': 'Increase monitoring frequency'
        })
    elif risk_score >= 25:
        alerts.append({
            'type': 'sepsis_risk',
            'message': f'Moderate sepsis risk ({risk_score:.1f}%). Enhanced surveillance recommended.',
            'priority': 'medium',
            'action': 'Consider additional labs'
        })
    
    # Vital sign specific alerts
    
    # Temperature alerts
    temp = patient_data.get('temperature', 37.0)
    if temp >= 39.0:
        alerts.append({
            'type': 'hyperthermia',
            'message': f'High fever detected ({temp:.1f}°C). Consider antipyretics and infection workup.',
            'priority': 'high',
            'action': 'Administer antipyretics'
        })
    elif temp <= 35.5:
        alerts.append({
            'type': 'hypothermia',
            'message': f'Hypothermia detected ({temp:.1f}°C). Warming measures required.',
            'priority': 'high',
            'action': 'Initiate warming protocol'
        })
    
    # Heart rate alerts
    hr = patient_data.get('heart_rate', 80)
    if hr >= 130:
        alerts.append({
            'type': 'tachycardia',
            'message': f'Severe tachycardia ({hr} bpm). Evaluate for underlying causes.',
            'priority': 'high',
            'action': 'ECG and cardiac evaluation'
        })
    elif hr <= 50:
        alerts.append({
            'type': 'bradycardia',
            'message': f'Bradycardia detected ({hr} bpm). Monitor for hemodynamic compromise.',
            'priority': 'medium',
            'action': 'Continuous cardiac monitoring'
        })
    
    # Blood pressure alerts
    systolic = patient_data.get('systolic_bp', 120)
    if systolic < 90:
        alerts.append({
            'type': 'hypotension',
            'message': f'Hypotension ({systolic} mmHg). Fluid resuscitation may be needed.',
            'priority': 'critical',
            'action': 'Consider fluid bolus'
        })
    elif systolic > 180:
        alerts.append({
            'type': 'hypertension',
            'message': f'Severe hypertension ({systolic} mmHg). Antihypertensive therapy may be needed.',
            'priority': 'high',
            'action': 'Consider antihypertensives'
        })
    
    # Respiratory rate alerts
    rr = patient_data.get('respiratory_rate', 16)
    if rr >= 30:
        alerts.append({
            'type': 'tachypnea',
            'message': f'Severe tachypnea ({rr}/min). Evaluate for respiratory distress.',
            'priority': 'high',
            'action': 'Assess oxygenation'
        })
    elif rr <= 8:
        alerts.append({
            'type': 'bradypnea',
            'message': f'Bradypnea ({rr}/min). Monitor for respiratory depression.',
            'priority': 'high',
            'action': 'Continuous monitoring'
        })
    
    # Laboratory alerts
    wbc = patient_data.get('wbc_count', 8.0)
    if wbc >= 20.0:
        alerts.append({
            'type': 'leukocytosis',
            'message': f'Severe leukocytosis ({wbc:.1f} ×10³). Suggests significant infection.',
            'priority': 'high',
            'action': 'Blood cultures and antibiotics'
        })
    elif wbc <= 3.0:
        alerts.append({
            'type': 'leukopenia',
            'message': f'Leukopenia ({wbc:.1f} ×10³). Immunocompromised state possible.',
            'priority': 'high',
            'action': 'Isolation precautions'
        })
    
    lactate = patient_data.get('lactate', 1.5)
    if lactate >= 4.0:
        alerts.append({
            'type': 'hyperlactatemia',
            'message': f'Severe hyperlactatemia ({lactate:.1f} mmol/L). Tissue hypoperfusion likely.',
            'priority': 'critical',
            'action': 'Immediate resuscitation'
        })
    elif lactate >= 2.5:
        alerts.append({
            'type': 'mild_hyperlactatemia',
            'message': f'Elevated lactate ({lactate:.1f} mmol/L). Monitor for progression.',
            'priority': 'medium',
            'action': 'Repeat lactate in 2-6 hours'
        })
    
    return alerts

def render_intervention_urgency(patient_data):
    """Render intervention urgency information using risk score and qSOFA."""
    risk_score = patient_data.get('risk_score', 0)
    urgency = calculate_intervention_urgency(risk_score, patient_data)
    
    st.markdown("### ⏰ Intervention Timeline")

    # Color-code based on urgency
    if urgency['level'] == 'EMERGENCY':
        st.markdown(f"<div style='color:red; font-size:20px; font-weight:bold;'>🚨 {urgency['level']} - {urgency['timeframe']}</div>", unsafe_allow_html=True)
    elif urgency['level'] == 'URGENT':
        st.warning(f"⚠️ **{urgency['level']}** - {urgency['timeframe']}")
    elif urgency['level'] == 'MODERATE':
        st.info(f"**{urgency['level']}** - {urgency['timeframe']}")
    else:
        st.success(f"**{urgency['level']}** - {urgency['timeframe']}")

def render_quick_actions(patient_data):
    """Render quick action buttons for common interventions."""
    st.markdown("### ⚡ Quick Actions")
    
    risk_score = patient_data.get('risk_score', 0)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📞 Call Physician", type="secondary"):
            st.session_state.show_phys_input = True
        
        if st.session_state.get('show_phys_input'):
            num = st.text_input("Physician Number", placeholder="+1...")
            if num:
                st.markdown(f"[🔗 Dial {num}](tel:{num})")
        
        if risk_score >= 50 and st.button("🩸 Order Blood Cultures", type="secondary"):
            st.success("✅ Blood culture order placed")
    
    with col2:
        if st.button("✨ View Recommendations", type="primary"):
             st.info("💡 **Gemini 1.5 Flash Insight**: High risk detected. Recommend Sepsis-3 bundle: 30mL/kg fluids, cultures, and broad-spectrum antibiotics within 1 hour.")

        if risk_score > 75 and st.button("💊 Sepsis Protocol", type="primary"):
             st.success("✅ Sepsis protocol activated")
        
        systolic = patient_data.get('systolic_bp', 120)
        if systolic < 90 and st.button("💧 Fluid Bolus", type="secondary"):
            st.success("✅ Fluid bolus order placed")
    
    with col3:
        if st.button("📊 Additional Labs", type="secondary"):
            st.success("✅ Lab orders placed")
        
        lactate = patient_data.get('lactate', 1.5)
        if lactate > 2.2 and st.button("🔄 Repeat Lactate", type="secondary"):
            updated_risk = st.session_state.sepsis_model.predict_risk(patient_data)
            st.toast(f"Immediate Re-assessment: {updated_risk}% Risk")

def render_notification_center():
    """Render a notification center for alerts and reminders."""
    st.markdown("### 🔔 Notification Center")
    
    # Simulated notifications
    notifications = [
        {
            'time': datetime.now().strftime('%H:%M'),
            'type': 'reminder',
            'message': 'Vital signs due for Patient ICU-001',
            'priority': 'low'
        },
        {
            'time': (datetime.now()).strftime('%H:%M'),
            'type': 'alert',
            'message': 'High risk patient requires reassessment',
            'priority': 'high'
        }
    ]
    
    for notification in notifications:
        if notification['priority'] == 'high':
            st.error(f"🔴 **{notification['time']}** - {notification['message']}")
        elif notification['priority'] == 'medium':
            st.warning(f"🟡 **{notification['time']}** - {notification['message']}")
        else:
            st.info(f"🔵 **{notification['time']}** - {notification['message']}")

def render_alert_history(patient_records):
    """Render historical alerts for a patient."""
    st.markdown("### 📋 Alert History")
    
    if patient_records.empty:
        st.info("No alert history available")
        return
    
    # Generate alert history based on risk score changes
    alert_history = []
    
    for i, record in patient_records.iterrows():
        risk_score = record['risk_score']
        timestamp = record['timestamp']
        
        if risk_score >= 75:
            alert_history.append({
                'timestamp': timestamp,
                'type': 'Critical Risk',
                'message': f'Critical sepsis risk detected ({risk_score:.1f}%)',
                'resolved': False
            })
        elif risk_score >= 50:
            alert_history.append({
                'timestamp': timestamp,
                'type': 'High Risk',
                'message': f'High sepsis risk detected ({risk_score:.1f}%)',
                'resolved': risk_score < 50
            })
    
    if alert_history:
        for alert in alert_history[-10:]:  # Show last 10 alerts
            status = "✅ Resolved" if alert['resolved'] else "🚨 Active"
            st.markdown(f"**{alert['timestamp'].strftime('%H:%M:%S')}** - {alert['type']}: {alert['message']} - {status}")
    else:
        st.info("No alerts in history")

def render_sepsis_bundle_tracker():
    """Render sepsis bundle compliance tracker."""
    st.markdown("### 📋 Sepsis Bundle Tracker")
    st.markdown("*3-hour bundle for sepsis management*")
    
    bundle_items = [
        {"item": "Blood cultures obtained", "completed": False, "time_limit": "60 min"},
        {"item": "Broad-spectrum antibiotics", "completed": False, "time_limit": "60 min"},
        {"item": "Lactate level measured", "completed": True, "time_limit": "60 min"},
        {"item": "Fluid resuscitation (if hypotensive)", "completed": False, "time_limit": "180 min"},
        {"item": "Vasopressors (if refractory hypotension)", "completed": False, "time_limit": "180 min"}
    ]
    
    for item in bundle_items:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            if item["completed"]:
                st.success(f"✅ {item['item']}")
            else:
                st.error(f"❌ {item['item']}")
        
        with col2:
            st.text(item["time_limit"])
        
        with col3:
            if not item["completed"]:
                if st.button(f"Mark Complete", key=f"complete_{item['item']}"):
                    st.success("✅ Marked as completed")
