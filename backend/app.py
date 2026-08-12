from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "CardioSurvFormer API is running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="CardioSurvFormer - Clinical Decision Support",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS - PASTE ALL CSS HERE
# ============================================
st.markdown("""
<style>
    /* ============================================
       ALL YOUR CSS GOES HERE
       ============================================ */
    
    /* Import Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Color Palette & Global Styles */
    :root {
        --gradient-primary: linear-gradient(135deg, #0D47A1, #1565C0);
        --color-primary-dark: #0D47A1;
        --color-primary: #1565C0;
        --color-primary-light: #64B5F6;
        --color-accent: #E3F2FD;
        --color-text: #1A2332;
        --color-text-light: #5A6C7D;
        --color-background: #F4F7FC;
        --color-white: #FFFFFF;
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Inter', sans-serif;
        background-color: var(--color-background);
        color: var(--color-text);
    }
    
    /* Main container */
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Header */
    .main-header {
        background: var(--gradient-primary);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(13, 71, 161, 0.15);
    }
    .main-header h1 {
        font-size: 2rem;
        font-weight: 700;
        color: var(--color-white);
        margin: 0;
    }
    .main-header p {
        color: rgba(255,255,255,0.8);
        font-size: 1rem;
        margin: 4px 0 0 0;
    }
    
    /* Cards */
    .card {
        background: var(--color-white);
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        padding: 20px 24px;
        margin-bottom: 16px;
        border: 1px solid #EAEEF4;
        transition: box-shadow 0.2s ease;
    }
    .card:hover {
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    .card h3 {
        color: var(--color-primary-dark);
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 12px 0;
    }
    
    /* Stats */
    .stat-card {
        background: var(--color-white);
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
        border: 1px solid #EAEEF4;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }
    .stat-card .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--color-primary-dark);
    }
    .stat-card .stat-label {
        color: var(--color-text-light);
        font-size: 0.85rem;
        margin-top: 2px;
    }
    
    /* Sidebar */
    .sidebar-title {
        text-align: center;
        padding: 16px 0;
    }
    .sidebar-title .logo {
        font-size: 2.5em;
    }
    .sidebar-title h2 {
        color: var(--color-primary-dark);
        margin: 4px 0 2px 0;
        font-size: 1.2rem;
    }
    .sidebar-title p {
        color: var(--color-text-light);
        font-size: 0.7rem;
    }
    .sidebar-divider {
        width: 40px;
        height: 2px;
        background: var(--gradient-primary);
        margin: 8px auto;
        border-radius: 2px;
    }
    .sidebar-footer {
        position: fixed;
        bottom: 20px;
        left: 20px;
        right: 20px;
        padding: 12px 16px;
        background: var(--color-white);
        border-radius: 10px;
        border: 1px solid #EAEEF4;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    .sidebar-footer .status {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .sidebar-footer .status-dot {
        width: 6px;
        height: 6px;
        background: #10b981;
        border-radius: 50%;
        display: inline-block;
    }
    .sidebar-footer .status-text {
        color: var(--color-text-light);
        font-size: 0.65rem;
    }
    .sidebar-footer .version {
        color: var(--color-text-light);
        font-size: 0.55rem;
        margin-top: 2px;
        opacity: 0.6;
    }
    
    /* Badges */
    .badge {
        padding: 3px 12px;
        border-radius: 16px;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-success { background: #D1FAE5; color: #065F46; }
    .badge-warning { background: #FEF3C7; color: #92400E; }
    .badge-danger { background: #FEE2E2; color: #991B1B; }
    
    /* Buttons */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(13, 71, 161, 0.3);
    }
    
    /* Activity items */
    .activity-item {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #F0F2F5;
        font-size: 0.9rem;
    }
    .activity-item:last-child {
        border-bottom: none;
    }
    .activity-patient {
        color: var(--color-text);
        font-weight: 500;
    }
    .activity-event {
        color: var(--color-text-light);
    }
    .activity-time {
        color: var(--color-text-light);
        font-size: 0.75rem;
    }
    
    /* Footer */
    .app-footer {
        text-align: center;
        padding: 16px;
        margin-top: 24px;
        border-top: 1px solid #EAEEF4;
    }
    .app-footer p {
        color: var(--color-text-light);
        font-size: 0.75rem;
        margin: 0;
    }
    
    /* Reduce Streamlit default margins */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 1400px !important;
    }
    
    /* Fix column gaps */
    .stColumns {
        gap: 16px !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #D1D5DB;
    }
    .stSelectbox > div > div {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)
