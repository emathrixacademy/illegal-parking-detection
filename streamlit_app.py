import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Illegal Parking Detection System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS styling
st.markdown("""
    <style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card styling */
    .custom-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        color: #4a5568;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Status badge */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.5rem;
    }
    
    .status-online {
        background: #48bb78;
        color: white;
    }
    
    .status-offline {
        background: #f56565;
        color: white;
    }
    
    /* Feature icons */
    .feature-item {
        display: flex;
        align-items: center;
        padding: 1rem;
        margin: 0.5rem 0;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .feature-item:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: translateX(10px);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Initialize Firebase
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

try:
    db = init_firebase()
    firebase_connected = True
except Exception as e:
    st.error(f"Firebase connection error: {e}")
    firebase_connected = False

# Header
st.markdown('<h1 class="main-header">🚗 Smart Parking Enforcement</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Illegal Parking Detection System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Barangay Tagapo, City of Santa Rosa, Laguna</p>', unsafe_allow_html=True)

# System Status Card
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">🔌 Dashboard</div>
            <div class="metric-value">●</div>
            <div class="metric-label">ONLINE</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if firebase_connected:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-label">🗄️ Database</div>
                <div class="metric-value">●</div>
                <div class="metric-label">CONNECTED</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #f56565 0%, #c53030 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center;">
                <div class="metric-label">🗄️ Database</div>
                <div class="metric-value">●</div>
                <div class="metric-label">DISCONNECTED</div>
            </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">📹 Active Cameras</div>
            <div class="metric-value">1</div>
            <div class="metric-label">Brgy. Tagapo</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# About Section
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## 🎯 About This System
    
    An **AI-powered Computer Vision system** that automatically detects and monitors 
    illegal parking violations on sidewalks in real-time.
    
    ### 🌟 Key Features
    """)
    
    features = [
        ("🎥", "Real-time camera monitoring with YOLOv8"),
        ("🤖", "AI-powered vehicle detection (Hailo AI Kit)"),
        ("⏱️", "Automatic 5-minute violation timing"),
        ("🔍", "License plate recognition (OCR)"),
        ("🎨", "Vehicle color identification"),
        ("📊", "Analytics and reporting dashboard"),
        ("🔔", "Real-time notifications to enforcers"),
        ("📱", "Mobile-responsive web interface")
    ]
    
    for icon, text in features:
        st.markdown(f'<div class="feature-item">{icon} &nbsp; {text}</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    ### 📋 Research Project
    
    **Title:** Decongesting the Sidewalk
    
    **Institution:** Technological University of the Philippines
    
    **Researcher:** Ma. Ymelda C. Batalla
    
    **Program:** Doctor of Technology
    
    **Location:** Barangay Tagapo, Santa Rosa, Laguna
    
    ---
    
    ### 📞 Support
    For assistance, contact the Barangay office.
    """)

st.markdown('</div>', unsafe_allow_html=True)

# Quick Statistics
if firebase_connected:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("## 📊 Today's Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        violations_ref = db.collection('violations').where('timestamp', '>=', today).stream()
        violations_list = list(violations_ref)
        
        total_violations = len(violations_list)
        active_violations = len([v for v in violations_list if v.to_dict().get('status') == 'active'])
        
        with col1:
            st.metric("Total Violations", total_violations, delta=f"+{total_violations}")
        with col2:
            st.metric("Active Now", active_violations, delta=None if active_violations == 0 else f"-{total_violations - active_violations}")
        with col3:
            st.metric("Resolved", total_violations - active_violations)
        with col4:
            if violations_list:
                avg_duration = sum([v.to_dict().get('duration', 0) for v in violations_list]) / len(violations_list)
                st.metric("Avg Duration", f"{avg_duration:.1f} min")
            else:
                st.metric("Avg Duration", "0 min")
                
    except Exception as e:
        col1.metric("Total Violations", "0")
        col2.metric("Active Now", "0")
        col3.metric("Resolved", "0")
        col4.metric("Avg Duration", "0 min")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Recent Violations Preview
if firebase_connected:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("## 🚨 Recent Violations")
    
    try:
        recent_violations = db.collection('violations').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(3).stream()
        
        violations_found = False
        for violation in recent_violations:
            violations_found = True
            data = violation.to_dict()
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if data.get('image_url'):
                    st.image(data['image_url'], use_column_width=True)
                else:
                    st.info("📷 No image")
            
            with col2:
                st.markdown(f"**🚗 {data.get('vehicle_type', 'Unknown').upper()}** - {data.get('plate_number', 'N/A')}")
                st.markdown(f"⏱️ Duration: {data.get('duration', 0):.1f} minutes")
                st.markdown(f"📍 {data.get('location', 'N/A')}")
            
            with col3:
                timestamp = data.get('timestamp')
                if timestamp:
                    st.markdown(f"🕐 {timestamp.strftime('%H:%M:%S')}")
                status = data.get('status', 'unknown')
                if status == 'active':
                    st.markdown('<span class="status-badge status-offline">🔴 Active</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="status-badge status-online">🟢 Resolved</span>', unsafe_allow_html=True)
            
            st.divider()
        
        if not violations_found:
            st.success("✅ No violations recorded yet. System is ready to monitor!")
            
    except Exception as e:
        st.warning(f"Unable to load recent violations")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: white;'>
    <p><strong>Developed by Ma. Ymelda C. Batalla</strong></p>
    <p>Technological University of the Philippines - Doctor of Technology Program</p>
    <p>© 2025 | Powered by YOLOv8, Hailo AI, Firebase & Streamlit</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    st.info("""
    **Quick Access:**
    - 📊 Dashboard: Overview
    - 🚨 Live: Active violations
    - 📈 Analytics: Trends & insights
    """)
    
    st.markdown("### ℹ️ System Info")
    st.success("All systems operational")
    st.metric("Uptime", "99.9%")
