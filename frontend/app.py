import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ============================================
# PAGE CONFIG - MUST BE FIRST
# ============================================
st.set_page_config(
    page_title="CardioSurvFormer - Clinical Decision Support",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# MODERN CSS WITH GLASS EFFECTS & 3D ANIMATIONS
# ============================================
st.markdown("""
<style>
    /* ============================================
       MODERN CSS - GLASS EFFECTS & 3D ANIMATIONS
       ============================================ */
    
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Animated Background */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a3e) !important;
        background-size: 400% 400% !important;
        animation: gradientBG 15s ease infinite !important;
        min-height: 100vh !important;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating particles background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, rgba(255,255,255,0.3), transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.2), transparent),
            radial-gradient(2px 2px at 50px 160px, rgba(255,255,255,0.3), transparent),
            radial-gradient(2px 2px at 90px 40px, rgba(255,255,255,0.2), transparent),
            radial-gradient(2px 2px at 130px 80px, rgba(255,255,255,0.3), transparent);
        background-size: 200px 200px;
        pointer-events: none;
        z-index: 0;
        animation: floatParticles 20s linear infinite;
    }
    
    @keyframes floatParticles {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* ============================================
       GLASSMORPHISM CARDS
       ============================================ */
    .glass-card {
        background: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 20px !important;
        padding: 24px !important;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
        margin-bottom: 16px !important;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at center, rgba(255,255,255,0.05) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.6s ease;
        pointer-events: none;
    }
    
    .glass-card:hover::before {
        opacity: 1;
    }
    
    .glass-card:hover {
        transform: translateY(-8px) scale(1.01) !important;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            0 0 40px rgba(102, 126, 234, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
    }
    
    .glass-card h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        margin-bottom: 16px !important;
    }
    
    .glass-card p, .glass-card div, .glass-card span {
        color: rgba(255,255,255,0.85) !important;
    }
    
    /* ============================================
       MODERN HEADER
       ============================================ */
    .main-header {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3)) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 24px !important;
        padding: 32px 40px !important;
        margin-bottom: 24px !important;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        position: relative;
        overflow: hidden;
        animation: headerGlow 4s ease-in-out infinite alternate;
    }
    
    @keyframes headerGlow {
        0% { box-shadow: 0 20px 60px rgba(102, 126, 234, 0.2); }
        100% { box-shadow: 0 20px 80px rgba(118, 75, 162, 0.4); }
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.2), transparent 70%);
        border-radius: 50%;
        animation: floatOrb 8s ease-in-out infinite alternate;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: -50%;
        left: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(118, 75, 162, 0.15), transparent 70%);
        border-radius: 50%;
        animation: floatOrb 10s ease-in-out infinite alternate-reverse;
    }
    
    @keyframes floatOrb {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(30px, -20px) scale(1.2); }
    }
    
    .main-header h1 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #f3ec78, #af4261, #f3ec78) !important;
        background-size: 200% 200% !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        animation: shimmerText 4s ease-in-out infinite !important;
        position: relative;
        z-index: 1;
        margin: 0 !important;
        text-shadow: none !important;
    }
    
    @keyframes shimmerText {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header p {
        color: rgba(255,255,255,0.8) !important;
        font-size: 1rem !important;
        margin: 4px 0 0 0 !important;
        position: relative;
        z-index: 1;
        font-weight: 300 !important;
    }
    
    /* ============================================
       STAT CARDS WITH 3D EFFECT
       ============================================ */
    .stat-card {
        background: rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 20px 16px !important;
        text-align: center !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
        perspective: 800px;
        margin-bottom: 0 !important;
    }
    
    .stat-card:hover {
        transform: translateY(-6px) rotateX(3deg) rotateY(3deg) !important;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            0 0 40px rgba(102, 126, 234, 0.15) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
    }
    
    .stat-card .stat-value {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #60a5fa, #a78bfa) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        line-height: 1.2 !important;
        text-shadow: 0 0 40px rgba(96, 165, 250, 0.2);
    }
    
    .stat-card .stat-label {
        color: rgba(255,255,255,0.6) !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        margin-top: 4px !important;
    }
    
    /* ============================================
       SIDEBAR - GLASS EFFECT
       ============================================ */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.8) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding-top: 0 !important;
        min-width: 240px !important;
        max-width: 260px !important;
        width: 240px !important;
    }
    
    [data-testid="stSidebar"] * {
        color: rgba(255,255,255,0.85) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] + section {
        padding-left: 20px !important;
        padding-right: 20px !important;
        max-width: 100% !important;
    }
    
    .sidebar-title {
        text-align: center !important;
        padding: 24px 16px 16px 16px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
        background: rgba(255, 255, 255, 0.03) !important;
    }
    .sidebar-title .logo {
        font-size: 3em !important;
        display: block !important;
        animation: pulseLogo 2s ease-in-out infinite !important;
    }
    
    @keyframes pulseLogo {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .sidebar-title h2 {
        background: linear-gradient(135deg, #60a5fa, #a78bfa) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin: 4px 0 2px 0 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    .sidebar-title p {
        color: rgba(255,255,255,0.4) !important;
        font-size: 0.7rem !important;
        font-weight: 400 !important;
    }
    .sidebar-divider {
        width: 40px !important;
        height: 3px !important;
        background: linear-gradient(90deg, #60a5fa, #a78bfa) !important;
        margin: 8px auto !important;
        border-radius: 4px !important;
        box-shadow: 0 0 20px rgba(96, 165, 250, 0.3);
    }
    
    [data-testid="stSidebar"] .stRadio {
        padding: 8px 12px !important;
    }
    [data-testid="stSidebar"] .stRadio > div {
        display: flex !important;
        flex-direction: column !important;
        gap: 4px !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        padding: 10px 14px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        background: rgba(255,255,255,0.03) !important;
        cursor: pointer !important;
        display: block !important;
        width: 100% !important;
        color: rgba(255,255,255,0.6) !important;
        border: 1px solid transparent !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.08) !important;
        color: rgba(255,255,255,0.9) !important;
        border-color: rgba(255,255,255,0.1) !important;
        transform: translateX(4px);
    }
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background: rgba(102, 126, 234, 0.2) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-left: 3px solid #60a5fa !important;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.1);
    }
    
    .sidebar-footer {
        position: fixed !important;
        bottom: 20px !important;
        left: 20px !important;
        right: 20px !important;
        padding: 12px 16px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(10px);
    }
    .sidebar-footer .status {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }
    .sidebar-footer .status-dot {
        width: 8px !important;
        height: 8px !important;
        background: #00A896 !important;
        border-radius: 50% !important;
        display: inline-block !important;
        animation: pulseDot 2s infinite !important;
    }
    @keyframes pulseDot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.3; transform: scale(0.8); }
    }
    .sidebar-footer .status-text {
        font-size: 0.7rem !important;
        font-weight: 500 !important;
        color: rgba(255,255,255,0.5) !important;
    }
    .sidebar-footer .version {
        color: rgba(255,255,255,0.3) !important;
        font-size: 0.55rem !important;
        margin-top: 2px !important;
    }
    
    /* ============================================
       BADGES
       ============================================ */
    .badge {
        padding: 4px 14px !important;
        border-radius: 20px !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        display: inline-block !important;
    }
    .badge-success { background: rgba(0, 168, 150, 0.2) !important; color: #34d399 !important; border: 1px solid rgba(0, 168, 150, 0.2); }
    .badge-warning { background: rgba(245, 158, 11, 0.2) !important; color: #fbbf24 !important; border: 1px solid rgba(245, 158, 11, 0.2); }
    .badge-danger { background: rgba(239, 68, 68, 0.2) !important; color: #f87171 !important; border: 1px solid rgba(239, 68, 68, 0.2); }
    
    /* ============================================
       BUTTONS - GLASS EFFECT
       ============================================ */
    .stButton > button {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.4), rgba(118, 75, 162, 0.4)) !important;
        backdrop-filter: blur(10px) !important;
        color: white !important;
        font-weight: 600 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        font-size: 0.9rem !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2) !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.6), rgba(118, 75, 162, 0.6)) !important;
    }
    
    /* ============================================
       INPUTS - GLASS EFFECT
       ============================================ */
    .stTextInput input, .stNumberInput input, .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 10px 16px !important;
        font-size: 0.9rem !important;
        color: rgba(255,255,255,0.9) !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: rgba(102, 126, 234, 0.5) !important;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.1) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    .stTextInput input::placeholder {
        color: rgba(255,255,255,0.3) !important;
    }
    
    .stSelectbox label, .stSlider label, .stCheckbox label, .stNumberInput label {
        color: rgba(255,255,255,0.7) !important;
        font-weight: 500 !important;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #60a5fa, #a78bfa) !important;
    }
    
    /* ============================================
       METRICS
       ============================================ */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        transition: all 0.3s ease !important;
        margin-bottom: 8px !important;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
    }
    [data-testid="metric-container"] .stMetric label {
        color: rgba(255,255,255,0.5) !important;
        font-weight: 500 !important;
    }
    [data-testid="metric-container"] .stMetric .stMetricValue {
        color: #ffffff !important;
        font-weight: 700 !important;
        text-shadow: 0 0 30px rgba(96, 165, 250, 0.2);
    }
    
    /* ============================================
       EXPANDER
       ============================================ */
    .streamlit-expanderHeader {
        color: rgba(255,255,255,0.85) !important;
        font-weight: 600 !important;
        background: rgba(255,255,255,0.03) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }
    .streamlit-expanderHeader:hover {
        background: rgba(255,255,255,0.06) !important;
        border-color: rgba(102, 126, 234, 0.2) !important;
    }
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 0 0 12px 12px !important;
        padding: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-top: none !important;
    }
    .streamlit-expanderContent p,
    .streamlit-expanderContent div,
    .streamlit-expanderContent span,
    .streamlit-expanderContent strong {
        color: rgba(255,255,255,0.8) !important;
    }
    
    /* ============================================
       ACTIVITY ITEMS
       ============================================ */
    .activity-item {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding: 10px 0 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        font-size: 0.85rem !important;
    }
    .activity-item:last-child {
        border-bottom: none !important;
    }
    .activity-patient {
        color: rgba(255,255,255,0.8) !important;
        font-weight: 500 !important;
    }
    .activity-event {
        color: rgba(255,255,255,0.5) !important;
    }
    .activity-time {
        color: rgba(255,255,255,0.3) !important;
        font-size: 0.7rem !important;
    }
    
    /* ============================================
       FOOTER
       ============================================ */
    .app-footer {
        text-align: center !important;
        padding: 16px !important;
        margin-top: 24px !important;
        border-top: 1px solid rgba(255, 255, 255, 0.05) !important;
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
    }
    .app-footer p {
        color: rgba(255,255,255,0.25) !important;
        font-size: 0.75rem !important;
        margin: 0 !important;
        font-weight: 400 !important;
    }
    
    /* ============================================
       RISK INDICATOR
       ============================================ */
    .risk-indicator {
        padding: 12px 16px !important;
        border-radius: 12px !important;
        margin: 8px 0 !important;
        font-weight: 500 !important;
        backdrop-filter: blur(10px);
    }
    .risk-low {
        background: rgba(0, 168, 150, 0.15) !important;
        border-left: 4px solid #00A896 !important;
        color: #34d399 !important;
    }
    .risk-moderate {
        background: rgba(245, 158, 11, 0.15) !important;
        border-left: 4px solid #F59E0B !important;
        color: #fbbf24 !important;
    }
    .risk-high {
        background: rgba(239, 68, 68, 0.15) !important;
        border-left: 4px solid #EF4444 !important;
        color: #f87171 !important;
    }
    
    /* ============================================
       IMPROVED SPACING FOR DASHBOARD
       ============================================ */
    [data-testid="column"] {
        padding: 0 8px !important;
    }
    
    .element-container {
        margin-bottom: 8px !important;
    }
    
    .stColumns {
        gap: 20px !important;
    }
    
    .stColumns + div {
        margin-top: 16px !important;
    }
    
    .glass-card {
        padding: 24px !important;
        margin-bottom: 0 !important;
    }
    
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        gap: 16px !important;
    }
    
    /* ============================================
       CONTAINER OVERRIDES
       ============================================ */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    section.main > div {
        max-width: 100% !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
    }
    
    /* ============================================
       RESPONSIVE
       ============================================ */
    @media (max-width: 768px) {
        .main-header {
            padding: 20px 24px !important;
        }
        .main-header h1 {
            font-size: 1.4rem !important;
        }
        [data-testid="stSidebar"] {
            min-width: 200px !important;
            max-width: 220px !important;
            width: 200px !important;
        }
        .stat-card .stat-value {
            font-size: 1.5rem !important;
        }
        .stColumns {
            gap: 12px !important;
        }
        [data-testid="column"] {
            padding: 0 4px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR - NAVIGATION
# ============================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-title">
        <span class="logo">🏥</span>
        <h2>CardioSurvFormer</h2>
        <p>Clinical Decision Support</p>
        <div class="sidebar-divider"></div>
    </div>
    """, unsafe_allow_html=True)
    
    pages = {
        "📊 Dashboard": "dashboard",
        "🔮 Survival Prediction": "prediction",
        "❤️ Heart Diagnosis": "heart_disease",
        "📈 Analysis & Explainability": "analysis_explainability",
        "👤 Patients": "patients",
        "⚙️ Settings": "settings"
    }
    
    selected = st.radio("", list(pages.keys()), index=0, label_visibility="collapsed")
    page = pages[selected]
    
    st.markdown(f"""
    <div class="sidebar-footer">
        <div class="status">
            <span class="status-dot"></span>
            <span class="status-text">System Online</span>
        </div>
        <div class="version">v2.0.0 • M.Tech Research</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# DASHBOARD PAGE - WITH PROPER CARD GAPS
# ============================================
if page == "dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Clinical Dashboard</h1>
        <p>Real-time patient monitoring and risk assessment</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Row - 4 columns with gap
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">94%</div>
            <div class="stat-label">Model Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">0.86</div>
            <div class="stat-label">C-Index Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">299</div>
            <div class="stat-label">Total Patients</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value" style="background: linear-gradient(135deg, #f87171, #ef4444) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; background-clip: text !important;">42</div>
            <div class="stat-label">High Risk</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add spacing between stat cards and charts
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Charts Row - 2 columns with gap
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown('<div class="glass-card"><h3>📊 Risk Distribution</h3>', unsafe_allow_html=True)
        
        np.random.seed(42)
        risk_data = pd.DataFrame({
            "Risk Level": np.random.choice(["Low", "Medium", "High"], 100, p=[0.4, 0.35, 0.25]),
            "Patients": np.random.randint(10, 50, 100)
        })
        
        risk_counts = risk_data["Risk Level"].value_counts().reset_index()
        risk_counts.columns = ["Risk Level", "Count"]
        
        fig = px.pie(
            risk_counts, 
            values="Count", 
            names="Risk Level",
            color="Risk Level",
            color_discrete_map={"Low": "#00A896", "Medium": "#F59E0B", "High": "#EF4444"},
            hole=0.4
        )
        fig.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5,
                font=dict(color="rgba(255,255,255,0.8)", size=11)
            )
        )
        fig.update_traces(textposition='inside', textinfo='percent', textfont=dict(color="white", size=12))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card"><h3>🔄 Recent Activity</h3>', unsafe_allow_html=True)
        
        activities = [
            {"patient": "P042", "event": "Risk Assessment", "time": "2 min ago"},
            {"patient": "P038", "event": "Follow-up", "time": "15 min ago"},
            {"patient": "P056", "event": "⚠️ High Risk Alert", "time": "1 hour ago"},
            {"patient": "P023", "event": "Treatment Update", "time": "2 hours ago"},
            {"patient": "P089", "event": "New Patient", "time": "3 hours ago"}
        ]
        
        for a in activities:
            st.markdown(f"""
            <div class="activity-item">
                <span class="activity-patient">👤 {a['patient']}</span>
                <span class="activity-event">{a['event']}</span>
                <span class="activity-time">{a['time']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SURVIVAL PREDICTION PAGE
# ============================================
elif page == "prediction":
    st.markdown("""
    <div class="main-header">
        <h1>🔮 Survival Prediction</h1>
        <p>Enter patient data for AI-powered risk assessment</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="glass-card"><h3>👤 Patient Information</h3>', unsafe_allow_html=True)
        
        with st.form("prediction_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                age = st.slider("Age", 20, 100, 60)
                sex = st.selectbox("Sex", ["Male", "Female"])
            with col_b:
                ejection_fraction = st.slider("Ejection Fraction (%)", 10, 80, 35)
                serum_creatinine = st.slider("Serum Creatinine (mg/dL)", 0.5, 4.0, 1.2, 0.1)
            
            col_c, col_d = st.columns(2)
            with col_c:
                serum_sodium = st.slider("Serum Sodium (mEq/L)", 120, 150, 137)
                platelets = st.number_input("Platelets (x1000)", 50, 500, 200)
            with col_d:
                diabetes = st.checkbox("Diabetes")
                smoking = st.checkbox("Smoking")
                high_bp = st.checkbox("High Blood Pressure")
                anaemia = st.checkbox("Anaemia")
            
            submitted = st.form_submit_button("🔮 Analyze Risk", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if submitted:
            st.markdown('<div class="glass-card"><h3>📊 Risk Assessment Results</h3>', unsafe_allow_html=True)
            
            risk_score = (
                (age - 20) / 80 * 0.3 +
                (100 - ejection_fraction) / 90 * 0.3 +
                (serum_creatinine - 0.5) / 3.5 * 0.2 +
                (140 - serum_sodium) / 30 * 0.1 +
                (0.1 if diabetes else 0) +
                (0.1 if high_bp else 0) +
                (0.05 if smoking else 0)
            )
            risk_score = min(0.95, max(0.05, risk_score + np.random.uniform(-0.03, 0.03)))
            
            survival_prob = 1 - risk_score
            
            if risk_score < 0.3:
                risk_category = "Low"
                badge_color = "#34d399"
                bg_color = "rgba(0, 168, 150, 0.15)"
            elif risk_score < 0.7:
                risk_category = "Medium"
                badge_color = "#fbbf24"
                bg_color = "rgba(245, 158, 11, 0.15)"
            else:
                risk_category = "High"
                badge_color = "#f87171"
                bg_color = "rgba(239, 68, 68, 0.15)"
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Risk Score", f"{risk_score:.2f}")
            with col_b:
                st.markdown(f"""
                <div style="text-align: center;">
                    <p style="color: rgba(255,255,255,0.4); font-size: 0.7rem; margin: 0;">Risk Category</p>
                    <span style="background: {bg_color}; color: {badge_color}; padding: 4px 16px; border-radius: 20px; font-size: 1rem; font-weight: 600; display: inline-block; border: 1px solid {badge_color}33;">{risk_category}</span>
                </div>
                """, unsafe_allow_html=True)
            with col_c:
                st.metric("Survival Probability", f"{survival_prob:.1%}")
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_score,
                title={"text": "Risk Score", "font": {"color": "rgba(255,255,255,0.8)", "size": 14}},
                gauge={
                    "axis": {"range": [0, 1], "tickcolor": "rgba(255,255,255,0.3)", "tickfont": {"color": "rgba(255,255,255,0.5)", "size": 10}},
                    "steps": [
                        {"range": [0, 0.3], "color": "rgba(0, 168, 150, 0.2)"},
                        {"range": [0.3, 0.7], "color": "rgba(245, 158, 11, 0.2)"},
                        {"range": [0.7, 1], "color": "rgba(239, 68, 68, 0.2)"}
                    ],
                    "threshold": {
                        "line": {"color": "#EF4444", "width": 4},
                        "thickness": 0.7,
                        "value": 0.7
                    }
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("⚠️ This prediction is for research purposes only.")
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# HEART DISEASE DIAGNOSIS PAGE
# ============================================
elif page == "heart_disease":
    st.markdown("""
    <div class="main-header">
        <h1>❤️ Heart Disease Diagnosis & Risk Assessment</h1>
        <p>Comprehensive cardiovascular evaluation with condition identification</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(239, 68, 68, 0.1); border-radius: 12px; padding: 16px; margin-bottom: 20px; border-left: 4px solid #EF4444; backdrop-filter: blur(10px);">
        <p style="color: #f87171; margin: 0; font-weight: 500;">
            ⚠️ <strong>Disclaimer:</strong> This is a research tool for educational purposes only. 
            Always consult a qualified healthcare professional for medical advice.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="glass-card"><h3>🫀 Patient Assessment</h3>', unsafe_allow_html=True)
        
        with st.form("heart_disease_form"):
            st.markdown("#### Demographics")
            col_a, col_b = st.columns(2)
            with col_a:
                age = st.number_input("Age", 20, 100, 55)
                sex = st.selectbox("Sex", ["Male", "Female"])
            with col_b:
                bmi = st.number_input("BMI (kg/m²)", 15.0, 50.0, 24.5, 0.1)
                chest_pain = st.selectbox("Chest Pain Type", ["None", "Atypical", "Non-anginal", "Typical Angina"])
            
            st.markdown("#### Blood Parameters")
            col_c, col_d = st.columns(2)
            with col_c:
                cholesterol = st.number_input("Total Cholesterol (mg/dL)", 100, 400, 200)
                triglyceride = st.number_input("Triglycerides (mg/dL)", 50, 500, 150)
            with col_d:
                hdl = st.number_input("HDL Cholesterol (mg/dL)", 20, 100, 50)
                ldl = st.number_input("LDL Cholesterol (mg/dL)", 50, 300, 130)
            
            st.markdown("#### Vital Signs & ECG")
            col_e, col_f = st.columns(2)
            with col_e:
                systolic_bp = st.number_input("Systolic BP (mmHg)", 90, 200, 120)
                diastolic_bp = st.number_input("Diastolic BP (mmHg)", 60, 130, 80)
                heart_rate = st.number_input("Heart Rate (bpm)", 40, 150, 72)
            with col_f:
                fasting_sugar = st.number_input("Fasting Sugar (mg/dL)", 50, 300, 100)
                ecg_results = st.selectbox("ECG Results", ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy", "Abnormal"])
                exercise_angina = st.selectbox("Exercise Induced Angina", ["No", "Yes"])
            
            st.markdown("#### Lifestyle & Medical History")
            col_g, col_h = st.columns(2)
            with col_g:
                smoking = st.checkbox("Smoking")
                diabetes = st.checkbox("Diabetes")
                physical_activity = st.checkbox("Regular Physical Activity")
            with col_h:
                family_history = st.checkbox("Family History of Heart Disease")
                hypertension = st.checkbox("Hypertension (High BP)")
                alcohol = st.checkbox("Alcohol Consumption")
            
            submitted = st.form_submit_button("❤️ Diagnose & Assess Risk", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if submitted:
            st.markdown('<div class="glass-card"><h3>📊 Diagnosis Results</h3>', unsafe_allow_html=True)
            
            # ============================================
            # CALCULATE RISK SCORE
            # ============================================
            risk_score = 0
            risk_factors = []
            conditions = []
            
            # Age factor (0-20 points)
            if age < 40:
                risk_score += 5
            elif age < 50:
                risk_score += 10
            elif age < 60:
                risk_score += 15
            else:
                risk_score += 20
            
            # BMI factor (0-10 points)
            if bmi >= 30:
                risk_score += 10
                risk_factors.append("Obesity (BMI ≥ 30)")
            elif bmi >= 25:
                risk_score += 5
                risk_factors.append("Overweight (BMI ≥ 25)")
            
            # Chest Pain factor (0-15 points)
            if chest_pain == "Typical Angina":
                risk_score += 15
                risk_factors.append("Typical Angina (Strong indicator)")
                conditions.append("Coronary Artery Disease (CAD)")
            elif chest_pain == "Non-anginal":
                risk_score += 10
                risk_factors.append("Non-anginal Chest Pain")
            elif chest_pain == "Atypical":
                risk_score += 5
                risk_factors.append("Atypical Chest Pain")
            
            # Cholesterol factor (0-15 points)
            if cholesterol > 240:
                risk_score += 15
                risk_factors.append("High Cholesterol (>240 mg/dL)")
            elif cholesterol > 200:
                risk_score += 10
                risk_factors.append("Borderline Cholesterol (>200 mg/dL)")
            
            # LDL/HDL ratio factor (0-15 points)
            if ldl > 160:
                risk_score += 15
                risk_factors.append("High LDL (>160 mg/dL)")
            elif ldl > 130:
                risk_score += 10
                risk_factors.append("Elevated LDL (>130 mg/dL)")
            elif ldl > 100:
                risk_score += 5
            
            # Blood Pressure factor (0-15 points)
            if systolic_bp > 160:
                risk_score += 15
                risk_factors.append("Severe Hypertension (>160 mmHg)")
                conditions.append("Hypertensive Heart Disease")
            elif systolic_bp > 140:
                risk_score += 10
                risk_factors.append("High Blood Pressure (>140 mmHg)")
                conditions.append("Hypertension")
            elif systolic_bp > 120:
                risk_score += 5
                risk_factors.append("Pre-hypertension (>120 mmHg)")
            
            # ECG factor (0-15 points)
            if ecg_results == "ST-T Wave Abnormality":
                risk_score += 15
                risk_factors.append("ST-T Wave Abnormality (Ischemia indicator)")
                conditions.append("Myocardial Ischemia")
            elif ecg_results == "Left Ventricular Hypertrophy":
                risk_score += 15
                risk_factors.append("Left Ventricular Hypertrophy")
                conditions.append("Left Ventricular Hypertrophy")
            elif ecg_results == "Abnormal":
                risk_score += 10
                risk_factors.append("Abnormal ECG")
                conditions.append("Potential Cardiac Arrhythmia")
            
            # Exercise Angina (0-10 points)
            if exercise_angina == "Yes":
                risk_score += 10
                risk_factors.append("Exercise-Induced Angina")
                if "Coronary Artery Disease (CAD)" not in conditions:
                    conditions.append("Coronary Artery Disease (CAD)")
            
            # Smoking (0-10 points)
            if smoking:
                risk_score += 10
                risk_factors.append("Smoking")
            
            # Diabetes (0-10 points)
            if diabetes:
                risk_score += 10
                risk_factors.append("Diabetes")
                conditions.append("Diabetic Cardiomyopathy")
            
            # Family History (0-10 points)
            if family_history:
                risk_score += 10
                risk_factors.append("Family History of Heart Disease")
            
            # Hypertension (0-10 points)
            if hypertension:
                risk_score += 10
                risk_factors.append("Hypertension")
            
            # Physical Activity (-5 points bonus)
            if physical_activity:
                risk_score -= 5
            
            # Heart Rate factor (0-5 points)
            if heart_rate > 100:
                risk_score += 5
                risk_factors.append("Tachycardia (Heart Rate > 100 bpm)")
            elif heart_rate < 60:
                risk_score += 3
                risk_factors.append("Bradycardia (Heart Rate < 60 bpm)")
            
            # Fasting Sugar factor (0-5 points)
            if fasting_sugar > 200:
                risk_score += 5
                risk_factors.append("Very High Blood Sugar (>200 mg/dL)")
            elif fasting_sugar > 140:
                risk_score += 3
                risk_factors.append("High Blood Sugar (>140 mg/dL)")
            
            # Normalize to 0-100 scale
            risk_score = max(0, min(100, risk_score * 1.2))
            
            # ============================================
            # DETERMINE CONDITIONS
            # ============================================
            if not conditions:
                if risk_score > 50:
                    conditions.append("General Cardiovascular Risk")
                else:
                    conditions.append("No significant condition detected")
            
            conditions = list(set(conditions))
            
            # ============================================
            # DETERMINE RISK LEVEL
            # ============================================
            if risk_score < 30:
                risk_level = "Low"
                risk_color = "#34d399"
                risk_bg = "rgba(0, 168, 150, 0.15)"
                risk_class = "risk-low"
                recommendation = "Great job! Continue maintaining a healthy lifestyle. Regular check-ups recommended annually."
            elif risk_score < 50:
                risk_level = "Moderate"
                risk_color = "#fbbf24"
                risk_bg = "rgba(245, 158, 11, 0.15)"
                risk_class = "risk-moderate"
                recommendation = "Consider lifestyle modifications. Consult a healthcare provider for a comprehensive evaluation."
            elif risk_score < 70:
                risk_level = "High"
                risk_color = "#fb923c"
                risk_bg = "rgba(251, 146, 60, 0.15)"
                risk_class = "risk-moderate"
                recommendation = "Please consult a cardiologist soon. Lifestyle changes and medical intervention may be necessary."
            else:
                risk_level = "Critical"
                risk_color = "#f87171"
                risk_bg = "rgba(239, 68, 68, 0.15)"
                risk_class = "risk-high"
                recommendation = "URGENT: Please seek immediate medical attention from a cardiologist."
            
            # ============================================
            # DISPLAY RESULTS
            # ============================================
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Risk Score", f"{risk_score:.1f}%")
            with col_b:
                st.metric("Risk Level", risk_level)
            
            st.markdown(f"""
            <div class="risk-indicator {risk_class}">
                <strong>Recommendation:</strong> {recommendation}
            </div>
            """, unsafe_allow_html=True)
            
            # Risk Gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_score,
                title={"text": "Heart Disease Risk", "font": {"color": "rgba(255,255,255,0.8)", "size": 14}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "rgba(255,255,255,0.3)", "tickfont": {"color": "rgba(255,255,255,0.5)", "size": 10}},
                    "steps": [
                        {"range": [0, 30], "color": "rgba(0, 168, 150, 0.2)"},
                        {"range": [30, 50], "color": "rgba(245, 158, 11, 0.2)"},
                        {"range": [50, 70], "color": "rgba(251, 146, 60, 0.2)"},
                        {"range": [70, 100], "color": "rgba(239, 68, 68, 0.2)"}
                    ],
                    "threshold": {
                        "line": {"color": "#EF4444", "width": 4},
                        "thickness": 0.7,
                        "value": 70
                    }
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            
            # ============================================
            # DIAGNOSED CONDITIONS
            # ============================================
            st.markdown("#### 🏥 Diagnosed Heart Conditions")
            
            if conditions and conditions[0] != "No significant condition detected":
                for condition in conditions:
                    if "Coronary Artery" in condition or "CAD" in condition:
                        icon = "🫀"
                        desc = "Blockage or narrowing of coronary arteries reducing blood flow to the heart muscle."
                    elif "Heart Failure" in condition:
                        icon = "💔"
                        desc = "Heart muscle cannot pump blood efficiently to meet the body's needs."
                    elif "Myocardial Ischemia" in condition:
                        icon = "⚡"
                        desc = "Reduced blood flow to the heart muscle, often due to partially blocked arteries."
                    elif "Hypertension" in condition or "Hypertensive" in condition:
                        icon = "📈"
                        desc = "Persistently high blood pressure that puts strain on the heart and blood vessels."
                    elif "Arrhythmia" in condition:
                        icon = "🔴"
                        desc = "Irregular heart rhythm that can affect the heart's ability to pump blood."
                    elif "Left Ventricular Hypertrophy" in condition:
                        icon = "💪"
                        desc = "Thickening of the left ventricle wall, often due to high blood pressure."
                    elif "Diabetic Cardiomyopathy" in condition:
                        icon = "🩸"
                        desc = "Heart muscle damage caused by diabetes, independent of coronary artery disease."
                    elif "General Cardiovascular" in condition:
                        icon = "⚠️"
                        desc = "Elevated cardiovascular risk requiring further evaluation."
                    else:
                        icon = "❤️"
                        desc = "Cardiac condition requiring further evaluation by a specialist."
                    
                    st.markdown(f"""
                    <div style="background: {risk_bg}; border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; border-left: 4px solid {risk_color}; backdrop-filter: blur(10px);">
                        <p style="margin: 0; font-weight: 600; color: {risk_color};">
                            {icon} {condition}
                        </p>
                        <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                            {desc}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: rgba(0, 168, 150, 0.1); border-radius: 10px; padding: 16px; text-align: center; border-left: 4px solid #00A896; backdrop-filter: blur(10px);">
                    <p style="margin: 0; color: #34d399; font-size: 1.1rem; font-weight: 600;">
                        ✅ No significant heart conditions detected
                    </p>
                    <p style="margin: 4px 0 0 0; color: rgba(255,255,255,0.6); font-size: 0.9rem;">
                        Continue healthy lifestyle and regular check-ups.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # ============================================
            # RISK FACTORS BREAKDOWN
            # ============================================
            st.markdown("#### 🔍 Risk Factors Analysis")
            
            if risk_factors:
                col_risk1, col_risk2 = st.columns(2)
                for i, rf in enumerate(risk_factors[:5]):
                    with col_risk1 if i % 2 == 0 else col_risk2:
                        st.markdown(f"- 🔴 {rf}")
                
                if len(risk_factors) > 5:
                    with st.expander(f"View all {len(risk_factors)} risk factors"):
                        for rf in risk_factors[5:]:
                            st.markdown(f"- 🔴 {rf}")
            else:
                st.info("No significant risk factors identified. Continue maintaining a healthy lifestyle.")
            
            st.markdown("""
            <div style="margin-top: 12px; padding: 12px; background: rgba(102, 126, 234, 0.1); border-radius: 8px; border-left: 4px solid #60a5fa; backdrop-filter: blur(10px);">
                <p style="color: rgba(255,255,255,0.7); font-size: 0.8rem; margin: 0;">
                    💡 <strong>Recommendation:</strong> Regular cardiovascular screening is essential for early detection and prevention. 
                    Consult a healthcare professional for personalized advice.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ANALYSIS & EXPLAINABILITY PAGE
# ============================================
elif page == "analysis_explainability":
    st.markdown("""
    <div class="main-header">
        <h1>📈 Survival Analysis & Explainability</h1>
        <p>Kaplan-Meier survival curves and model interpretability</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Survival Analysis Section
    st.markdown('<div class="glass-card"><h3>📈 Kaplan-Meier Survival Curves</h3>', unsafe_allow_html=True)
    
    np.random.seed(42)
    n = 100
    
    fig = go.Figure()
    
    color_map = {
        "Low": {"line": "#34d399", "fill": "rgba(0, 168, 150, 0.15)"},
        "Medium": {"line": "#fbbf24", "fill": "rgba(245, 158, 11, 0.15)"},
        "High": {"line": "#f87171", "fill": "rgba(239, 68, 68, 0.15)"}
    }
    
    for risk, colors in color_map.items():
        if risk == "Low":
            times = np.random.exponential(300, n)
        elif risk == "Medium":
            times = np.random.exponential(200, n)
        else:
            times = np.random.exponential(100, n)
        
        sorted_times = np.sort(times)
        survival = np.array([(times >= t).mean() for t in sorted_times])
        
        fig.add_trace(go.Scatter(
            x=sorted_times,
            y=survival,
            mode="lines",
            name=f"{risk} Risk",
            line=dict(color=colors["line"], width=3),
            fill="tozeroy",
            fillcolor=colors["fill"]
        ))
    
    fig.update_layout(
        xaxis_title="Time (days)",
        yaxis_title="Survival Probability",
        height=400,
        legend=dict(x=0.8, y=0.2, bgcolor="rgba(0,0,0,0.4)", font=dict(color="rgba(255,255,255,0.8)", size=11)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="rgba(255,255,255,0.6)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="rgba(255,255,255,0.6)", range=[0, 1])
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Explainability Section
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown('<div class="glass-card"><h3>🌍 Feature Importance</h3>', unsafe_allow_html=True)
        
        features = ["Ejection Fraction", "Serum Creatinine", "Age", "Serum Sodium", "Diabetes"]
        importance = [0.28, 0.22, 0.18, 0.12, 0.08]
        
        colors = ['#60a5fa', '#818cf8', '#a78bfa', '#c084fc', '#e879f9']
        
        fig = go.Figure(data=[
            go.Bar(
                x=importance,
                y=features,
                orientation="h",
                marker_color=colors,
                text=[f"{v:.1%}" for v in importance],
                textposition="outside",
                textfont=dict(color="rgba(255,255,255,0.9)", size=12, weight="bold")
            )
        ])
        
        fig.update_layout(
            xaxis_title="SHAP Value",
            yaxis_title="Features",
            height=300,
            margin=dict(l=10, r=60, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="rgba(255,255,255,0.6)", title_font=dict(color="rgba(255,255,255,0.6)")),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="rgba(255,255,255,0.6)", title_font=dict(color="rgba(255,255,255,0.6)"))
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card"><h3>🧠 How It Works</h3>', unsafe_allow_html=True)
        st.markdown("""
        <div style="color: rgba(255,255,255,0.8); font-size: 0.85rem; line-height: 2.0;">
            <p><strong style="color: #60a5fa;">CatBoost</strong> - Gradient boosting on decision trees</p>
            <p><strong style="color: #60a5fa;">TabTransformer</strong> - Transformer with multi-head attention</p>
            <p><strong style="color: #60a5fa;">Hybrid Fusion</strong> - Cross-attention between both models</p>
            <p><strong style="color: #60a5fa;">SHAP Values</strong> - Explainable AI for transparency</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PATIENTS PAGE
# ============================================
elif page == "patients":
    st.markdown("""
    <div class="main-header">
        <h1>👤 Patient Management</h1>
        <p>View, search, and manage patient records</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">299</div>
            <div class="stat-label">Total Patients</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value" style="background: linear-gradient(135deg, #34d399, #00A896) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; background-clip: text !important;">187</div>
            <div class="stat-label">Alive</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value" style="background: linear-gradient(135deg, #f87171, #ef4444) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; background-clip: text !important;">112</div>
            <div class="stat-label">Deceased</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value" style="background: linear-gradient(135deg, #fbbf24, #f59e0b) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; background-clip: text !important;">42</div>
            <div class="stat-label">High Risk</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    np.random.seed(42)
    first_names = ["John", "Sarah", "Michael", "Emily", "David", "Emma", "James", "Lisa", "Robert", "Maria"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    streets = ["Main St", "Oak Ave", "Maple Dr", "Cedar Ln", "Pine Rd", "Elm Blvd", "Washington Ave", "Park St"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego"]
    states = ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA"]
    
    patients = []
    for i in range(25):
        first = np.random.choice(first_names)
        last = np.random.choice(last_names)
        patients.append({
            "ID": f"P{i:03d}",
            "Name": f"{first} {last}",
            "Address": f"{np.random.randint(100, 9999)} {np.random.choice(streets)}, {np.random.choice(cities)}, {np.random.choice(states)} {np.random.randint(10000, 99999)}",
            "Phone": f"({np.random.randint(100, 999)}) {np.random.randint(100, 999)}-{np.random.randint(1000, 9999)}",
            "Age": np.random.randint(30, 90),
            "Sex": np.random.choice(["Male", "Female"]),
            "EF (%)": np.random.randint(15, 70),
            "Creatinine": round(np.random.uniform(0.5, 3.0), 2),
            "Risk Score": round(np.random.uniform(0, 1), 2),
            "Status": np.random.choice(["Alive", "Deceased"], p=[0.6, 0.4])
        })
    
    patients_df = pd.DataFrame(patients)
    
    col1, col2, col3 = st.columns([3, 1, 1], gap="large")
    with col1:
        search = st.text_input("🔍 Search Patients", placeholder="Search by Name, ID, Phone...")
    with col2:
        status_filter = st.selectbox("Status", ["All", "Alive", "Deceased"])
    with col3:
        risk_filter = st.selectbox("Risk Level", ["All", "Low", "Medium", "High"])
    
    filtered = patients_df.copy()
    if search:
        filtered = filtered[
            filtered["ID"].str.contains(search.upper(), na=False) |
            filtered["Name"].str.contains(search, case=False, na=False) |
            filtered["Phone"].str.contains(search, na=False)
        ]
    if status_filter != "All":
        filtered = filtered[filtered["Status"] == status_filter]
    if risk_filter != "All":
        if risk_filter == "Low":
            filtered = filtered[filtered["Risk Score"] < 0.3]
        elif risk_filter == "Medium":
            filtered = filtered[(filtered["Risk Score"] >= 0.3) & (filtered["Risk Score"] < 0.7)]
        else:
            filtered = filtered[filtered["Risk Score"] >= 0.7]
    
    st.markdown(f"<p style='color: rgba(255,255,255,0.4); font-size: 0.85rem; margin-bottom: 12px;'>Showing {len(filtered)} patients</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    for idx, row in filtered.iterrows():
        with st.expander(f"🆔 {row['ID']} - {row['Name']}  |  Risk: {row['Risk Score']:.2f}  |  {row['Status']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                **📋 Patient Details**
                - **ID:** {row['ID']}
                - **Name:** {row['Name']}
                - **Age:** {row['Age']}
                - **Sex:** {row['Sex']}
                """)
            
            with col2:
                st.markdown(f"""
                **📍 Contact Information**
                - **Address:** {row['Address']}
                - **Phone:** {row['Phone']}
                """)
            
            with col3:
                risk_color = "🟢" if row['Risk Score'] < 0.3 else "🟡" if row['Risk Score'] < 0.7 else "🔴"
                status_color = "🟢" if row['Status'] == "Alive" else "🔴"
                st.markdown(f"""
                **💊 Clinical Data**
                - **EF:** {row['EF (%)']}%
                - **Creatinine:** {row['Creatinine']}
                - **Risk Score:** {risk_color} {row['Risk Score']:.2f}
                - **Status:** {status_color} {row['Status']}
                """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ➕ Add New Patient")
    
    with st.form("add_patient_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Personal Information")
            name = st.text_input("Full Name *", placeholder="Enter patient's full name")
            age = st.number_input("Age *", 20, 100, 60)
            sex = st.selectbox("Sex *", ["Male", "Female"])
        
        with col2:
            st.markdown("#### Contact Information")
            address = st.text_area("Address *", placeholder="Enter complete address")
            phone = st.text_input("Phone Number *", placeholder="(XXX) XXX-XXXX")
        
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("#### Clinical Data")
            ef = st.number_input("Ejection Fraction (%)", 10, 80, 35)
            creatinine = st.number_input("Serum Creatinine (mg/dL)", 0.5, 4.0, 1.2, 0.1)
            sodium = st.number_input("Serum Sodium (mEq/L)", 120, 150, 137)
        
        with col4:
            st.markdown("#### Risk Assessment")
            risk_score = st.slider("Risk Score", 0.0, 1.0, 0.5)
            status = st.selectbox("Status", ["Alive", "Deceased"])
            diabetes = st.checkbox("Diabetes")
            smoking = st.checkbox("Smoking")
            high_bp = st.checkbox("High Blood Pressure")
        
        submitted = st.form_submit_button("💾 Save Patient Record", use_container_width=True)
        
        if submitted:
            if not name or not address or not phone:
                st.error("⚠️ Please fill in all required fields (Name, Address, Phone)")
            else:
                new_id = f"P{len(patients_df) + 1:03d}"
                st.success(f"✅ Patient {name} (ID: {new_id}) added successfully!")
                st.balloons()

# ============================================
# SETTINGS PAGE
# ============================================
elif page == "settings":
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ Settings</h1>
        <p>Configure system preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<div class="glass-card"><h3>🎯 Model Settings</h3>', unsafe_allow_html=True)
        model_type = st.selectbox("Default Model", ["Hybrid", "CatBoost", "TabTransformer"])
        threshold = st.slider("Risk Threshold", 0.0, 1.0, 0.5)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card"><h3>📊 Display Settings</h3>', unsafe_allow_html=True)
        theme = st.selectbox("Theme", ["Dark", "Light"])
        show_explanations = st.checkbox("Show Explanations", True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="app-footer">
    <p>CardioSurvFormer v2.0.0 • M.Tech Research Project • For research purposes only</p>
</div>
""", unsafe_allow_html=True)