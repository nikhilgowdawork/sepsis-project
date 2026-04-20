# ICU Sepsis Risk Prediction System

A comprehensive real-time sepsis risk prediction system designed for Intensive Care Unit (ICU) environments. This application uses machine learning models combined with clinical criteria to assess sepsis risk in patients based on vital signs and laboratory values.

## Features

🏥 **Patient Data Input**
- Comprehensive forms for vital signs, lab values, and demographics
- Input validation with clinical range checking
- Preset clinical scenarios for testing and demonstration

📊 **Real-time Risk Assessment**
- Neural network model providing sepsis risk scores (0-100%)
- Clinical rule-based scoring as fallback
- Multi-layered risk assessment combining ML predictions with SIRS criteria

📈 **Interactive Dashboard**
- Real-time vital signs monitoring
- Trend analysis and pattern detection
- Risk score history with visual indicators
- Patient summary cards

🚨 **Alert System**
- Priority-based alert system (Critical, High, Medium, Low)
- Clinical recommendations based on risk assessment
- Intervention urgency with recommended timeframes
- Quick action buttons for common medical interventions

⏰ **Clinical Decision Support**
- Evidence-based recommendations for patient care
- SIRS criteria and Sepsis-3 guideline compliance
- qSOFA scoring and organ dysfunction assessment

## Technology Stack

- **Frontend**: Streamlit for rapid web application development
- **Machine Learning**: TensorFlow/Keras neural network
- **Data Processing**: Pandas and NumPy for data manipulation
- **Visualization**: Plotly for interactive charts and medical data visualization
- **Preprocessing**: StandardScaler for feature normalization

## Installation

### Prerequisites
- Python 3.11+
- pip or uv package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd icu-sepsis-prediction
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or if using uv:
   ```bash
   uv sync
   ```

3. **Configure Streamlit**
   Create `.streamlit/config.toml`:
   ```toml
   [server]
   headless = true
   address = "0.0.0.0"
   port = 5000
   
   [theme]
   base = "light"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py --server.port 5000
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## Usage Guide

### 1. Patient Input
- Navigate to the "Patient Input" page in the sidebar
- Enter patient ID and vital signs/lab values
- Use preset scenarios for quick testing:
  - **Normal Patient**: Baseline healthy parameters
  - **Early Sepsis**: Initial signs of infection
  - **Severe Sepsis**: Advanced sepsis with organ dysfunction
  - **Septic Shock**: Critical condition requiring immediate intervention

### 2. Risk Dashboard
- View real-time risk assessment with gauge visualization
- Monitor vital signs trends over time
- Review clinical recommendations and intervention urgency
- Track risk score history with annotations

### 3. Historical Analysis
- Compare multiple patients over time
- Analyze risk score trends and patterns
- Filter data by time ranges and patient groups
- Export data for further analysis

### 4. System Status
- Monitor model performance and data quality
- View system health and statistics
- Export patient data in CSV format

## Clinical Guidelines

The system implements evidence-based medical protocols:

### SIRS Criteria (Systemic Inflammatory Response Syndrome)
- Temperature: >38°C or <36°C
- Heart Rate: >90 bpm
- Respiratory Rate: >20 breaths/min
- WBC Count: >12,000 or <4,000 cells/μL

### qSOFA Score (Quick Sequential Organ Failure Assessment)
- Systolic blood pressure ≤100 mmHg
- Respiratory rate ≥22 breaths/min
- Altered mental status

### Risk Categories
- **Low Risk** (0-24%): Routine monitoring
- **Moderate Risk** (25-49%): Increased surveillance
- **High Risk** (50-74%): Close monitoring required
- **Critical Risk** (75-100%): Immediate intervention required

## Machine Learning Model

### Architecture
- Sequential neural network with dropout layers
- Input features: 9 clinical parameters
- Output: Sigmoid activation for sepsis probability
- Regularization: Dropout layers to prevent overfitting

### Features Used
1. Temperature (°C)
2. Heart Rate (bpm)
3. Respiratory Rate (breaths/min)
4. Systolic Blood Pressure (mmHg)
5. Diastolic Blood Pressure (mmHg)
6. White Blood Cell Count (×10³/μL)
7. Lactate Level (mmol/L)
8. Age (years)
9. Gender (M/F)

### Model Training
The model is initialized with simulated training data representing realistic ICU patient populations. In production, this would be replaced with actual clinical data from your institution.

## File Structure

```
├── app.py                 # Main Streamlit application
├── components/           
│   ├── alerts.py         # Alert system and notifications
│   ├── dashboard.py      # Patient dashboard components
│   └── patient_input.py  # Data input forms
├── models/
│   └── sepsis_model.py   # ML model implementation
├── utils/
│   ├── data_processing.py # Data validation and processing
│   └── risk_calculator.py # Risk assessment algorithms
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Deployment Options

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your GitHub account to Streamlit Cloud
3. Deploy directly from the repository

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]
```

### Replit Deployment
The application is ready for deployment on Replit with the included configuration.

## Medical Disclaimer

⚠️ **IMPORTANT MEDICAL DISCLAIMER**: This application is for educational and research purposes only. It should not be used as a substitute for professional medical judgment or diagnosis. Always consult qualified healthcare professionals for patient care decisions.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or feature requests, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for healthcare professionals working to save lives in ICU environments.**