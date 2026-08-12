# ❤️ CardioSurvFormer

## An Explainable Hybrid CatBoost–TabTransformer Framework for Early Heart Failure Survival Prediction

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red.svg)](https://streamlit.io/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0-orange.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/NitinDesai01/CardioSurvFormer)](https://github.com/NitinDesai01/CardioSurvFormer)
[![GitHub repo size](https://img.shields.io/github/repo-size/NitinDesai01/CardioSurvFormer)](https://github.com/NitinDesai01/CardioSurvFormer)

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [🏗️ System Architecture](#-system-architecture)
- [✨ Features](#-features)
- [🛠️ Technology Stack](#-technology-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [📊 Model Performance](#-model-performance)
- [🔍 Explainability](#-explainability)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [⚠️ Disclaimer](#-disclaimer)
- [👨‍💻 Authors](#-authors)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

**CardioSurvFormer** is a **production-grade M.Tech research project** that combines cutting-edge machine learning techniques to predict heart failure survival using clinical records. The system provides explainable predictions through SHAP values and attention mechanisms, making it suitable for clinical decision support.

### Key Highlights:

- **🧠 Hybrid AI**: Combines CatBoost's gradient boosting with TabTransformer's attention mechanism
- **🔍 Explainable AI**: SHAP values + attention visualization for transparent predictions
- **📈 Survival Analysis**: Proper handling of censored data with Kaplan-Meier curves
- **🎨 3D Visualizations**: Interactive Plotly 3D dashboards for data exploration
- **🚀 Full-Stack**: FastAPI backend + Streamlit frontend with modern UI
- **❤️ Heart Disease Diagnosis**: Comprehensive cardiovascular risk assessment

---

---

## ✨ Features

### 📊 Dashboard
- Real-time patient monitoring
- Risk distribution visualization
- Recent activity feed
- Interactive 3D visualizations

### 🔮 Survival Prediction
- AI-powered risk assessment
- Clinical parameter input
- Risk score with gauge visualization
- Survival probability estimation

### ❤️ Heart Disease Diagnosis
- Comprehensive cardiovascular evaluation
- Condition identification (CAD, Hypertension, Arrhythmia, etc.)
- Risk factors analysis
- Clinical reference values
- Personalized recommendations

### 📈 Analysis & Explainability
- Kaplan-Meier survival curves
- Feature importance (SHAP values)
- Model interpretability

### 👤 Patient Management
- Search and filter patients
- Add new patients
- Patient records with contact details
- Risk level tracking

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Backend Framework** | FastAPI | 0.104+ |
| **Frontend Dashboard** | Streamlit | 1.29+ |
| **Machine Learning** | PyTorch, CatBoost | 2.0+, 1.2+ |
| **Explainability** | SHAP | 0.42+ |
| **Visualization** | Plotly, Matplotlib | 5.15+, 3.7+ |
| **Database** | PostgreSQL, Redis | 15+, 7+ |
| **Deployment** | Docker, Docker Compose | 24+ |
| **Language** | Python | 3.10+ |

---


---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ |
| Git | Latest |
| Docker (Optional) | 24+ |
| PostgreSQL (Optional) | 15+ |
| Redis (Optional) | 7+ |

### Installation

#### Method 1: Local Development (Recommended)

**Step 1: Clone the Repository**
```bash
git clone https://github.com/NitinDesai01/CardioSurvFormer.git
cd CardioSurvFormer

Step 2: Set Up Backend

bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Step 3: Set Up Frontend

bash
# Open a new terminal
cd frontend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Step 4: Download Dataset

bash
# Download the Heart Failure dataset
Invoke-WebRequest -Uri "https://archive.ics.uci.edu/ml/machine-learning-databases/00519/heart_failure_clinical_records_dataset.csv" -OutFile "data/raw/heart_failure_clinical_records_dataset.csv"
Method 2: Docker (Production)
bash
# Clone the repository
git clone https://github.com/NitinDesai01/CardioSurvFormer.git
cd CardioSurvFormer

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f
Running the Application
Start Backend Server
bash
# In backend directory with venv activated
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Start Frontend Dashboard (New Terminal)
bash
# In frontend directory with venv activated
cd frontend
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
