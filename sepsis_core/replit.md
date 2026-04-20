# ICU Sepsis Risk Prediction System

## Overview

This is a comprehensive real-time sepsis risk prediction system designed for Intensive Care Unit (ICU) environments. The application uses machine learning models combined with clinical criteria to assess sepsis risk in patients based on vital signs and laboratory values. Built with Streamlit for the web interface, the system provides healthcare professionals with risk scoring, trend analysis, alert systems, and clinical recommendations to support early sepsis detection and intervention decisions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for rapid web application development
- **Layout**: Wide layout with expandable sidebar navigation
- **Visualization**: Plotly (Graph Objects and Express) for interactive charts and medical data visualization
- **Component Structure**: Modular design with separate components for patient input, dashboard, and alerts
- **Session Management**: Streamlit session state for maintaining patient data and model instances

### Backend Architecture
- **Core Logic**: Python-based modular architecture with separation of concerns
- **Model Layer**: TensorFlow/Keras neural network for sepsis prediction with fallback clinical scoring
- **Data Processing**: Pandas and NumPy for data manipulation and validation
- **Risk Assessment**: Multi-layered approach combining ML predictions with clinical criteria (SIRS)
- **Utilities**: Dedicated modules for data validation, risk calculation, and clinical scoring

### Machine Learning Model
- **Architecture**: Sequential neural network with dropout layers for regularization
- **Input Features**: 9 clinical parameters (vitals, labs, demographics)
- **Output**: Sigmoid activation for sepsis probability (0-1)
- **Fallback System**: Clinical rule-based scoring when ML model unavailable
- **Preprocessing**: StandardScaler for feature normalization

### Data Validation and Processing
- **Input Validation**: Comprehensive range checking for all clinical parameters
- **Data Normalization**: Standardized preprocessing pipeline for consistent model input
- **Trend Detection**: Time-series analysis for patient condition monitoring
- **Clinical Scoring**: SIRS criteria implementation and vital signs scoring

### Alert and Risk Management
- **Risk Categorization**: Multi-level risk classification (Low/Medium/High/Critical)
- **Alert Generation**: Priority-based alert system with clinical thresholds
- **Intervention Urgency**: Time-sensitive recommendations based on risk scores
- **Clinical Recommendations**: Evidence-based suggestions for patient care

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework for medical dashboard
- **pandas**: Data manipulation and analysis for patient records
- **numpy**: Numerical computations for clinical calculations
- **plotly**: Interactive visualization for medical charts and trends

### Machine Learning Stack
- **tensorflow**: Deep learning framework for sepsis prediction model
- **scikit-learn**: StandardScaler for data preprocessing and model utilities
- **joblib**: Model serialization and loading capabilities

### Data Processing
- **datetime**: Time-based calculations for patient monitoring and trends
- **typing**: Type hints for robust medical data validation

### Potential Future Integrations
- Database connectivity for patient record persistence
- HL7 FHIR standards for healthcare interoperability
- Electronic Health Record (EHR) system integration
- Hospital information systems connectivity
- Real-time monitoring device data streams