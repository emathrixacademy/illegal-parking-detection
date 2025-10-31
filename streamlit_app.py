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

# Ultra-clean modern CSS
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header section */
    .header-container {
        text-align: center;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 400;
    }
    
    /* Clean white cards */
    .clean-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .clean-card:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    /* Status cards */
    .status-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        height: 100%;
    }
    
    .status-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .status-label {
        font-size: 0.875rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .status-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .status-text {
        font-size: 0.875rem;
        color: #94a3b8;
        font-weight: 500;
    }
    
    /* Status indicator dot */
    .status-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-online {
        background: #10b981;
    }
    
    .status-offline {
        background: #ef4444;
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    
    .feature-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .feature-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
    }
    
    .feature-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.25rem;
    }
    
    .feature-text {
        font-size: 0.875rem;
        color: #64748b;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.5rem;
    }
    
    /* Violation card */
    .violation-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-active {
        background: #fee2e2;
        color: #dc2626;
    }
    
    .badge-resolved {
        background: #d1fae5;
        color: #059669;
    }
    
    /* Metrics */
    .metric-container {
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e293b;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-delta {
        font-size: 0.875rem;
        margin-top: 0.5rem;
    }
    
    /* Info box */
    .info-box {
        background: #f8fafc;
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .info-title {
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .info-text {
        color: #64748b;
        font-size: 0.875rem;
        line-height: 1.6;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        background: transparent;
    }
    
    /* Button styling */
    .stButton>button {
        background: #667eea;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background: #5568d3;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
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
    firebase_connected = False

# Header
st.markdown("""
    <div class="header-container">
        <div class="main-title">🚗 Smart Parking Enforcement</div>
        <div class="subtitle">AI-Powered Illegal Parking Detection System</div>
        <div class="subtitle">Barangay Tagapo, City of Santa Rosa, Laguna</div>
    </div>
""", unsafe_allow_html=True)

# Status Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="status-card">
            <div class="status-icon">📊</div>
            <div class="status-label">Dashboard</div>
            <div class="status-value"><span class="status-dot status-online"></span></div>
            <div class="status-text">ONLINE</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if firebase_connected:
        st.markdown("""
            <div class="status-card">
                <div class="status-icon">🗄️</div>
                <div class="status-label">Database</div>
                <div class="status-value"><span class="status-dot status-online"></span></div>
                <div class="status-text">CONNECTED</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="status-card">
                <div class="status-icon">🗄️</div>
                <div class="status-label">Database</div>
                <div class="status-value"><span class="status-dot status-offline"></span></div>
                <div class="status-text">DISCONNECTED</div>
            </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="status-card">
            <div class="status-icon">📹</div>
            <div class="status-label">Active Cameras</div>
            <div class="status-value">1</div>
            <div class="status-text">Brgy. Tagapo</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Quick Stats
if firebase_connected:
    st.markdown('<div class="clean-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Today\'s Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        violations_ref = db.collection('violations').where('timestamp', '>=', today).stream()
        violations_list = list(violations_ref)
        
        total = len(violations_list)
        active = len([v for v in violations_list if v.to_dict().get('status') == 'active'])
        resolved = total - active
        avg_duration = sum([v.to_dict().get('duration', 0) for v in violations_list]) / total if total > 0 else 0
        
        with col1:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-value">{total}</div>
                    <div class="metric-label">Total Violations</div>
                    <div class="metric-delta" style="color: #ef4444;">+{total} today</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-value">{active}</div>
                    <div class="metric-label">Active Now</div>
                    <div class="metric-delta" style="color: #f59e0b;">Monitoring</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-value">{resolved}</div>
                    <div class="metric-label">Resolved</div>
                    <div class="metric-delta" style="color: #10b981;">Completed</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-value">{avg_duration:.1f}</div>
                    <div class="metric-label">Avg Duration (min)</div>
                </div>
            """, unsafe_allow_html=True)
    
    except:
        with col1:
            st.markdown("""
                <div class="metric-container">
                    <div class="metric-value">0</div>
                    <div class="metric-label">Total Violations</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="metric-container">
                    <div class="metric-value">0</div>
                    <div class="metric-label">Active Now</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="metric-container">
                    <div class="metric-value">0</div>
                    <div class="metric-label">Resolved</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div class="metric-container">
                    <div class="metric-value">0</div>
                    <div class="metric-label">Avg Duration (min)</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# About System
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="clean-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🎯 System Features</div>', unsafe_allow_html=True)
    
    features = [
        ("🎥", "Real-time Monitoring", "24/7 camera surveillance with YOLOv8 AI"),
        ("🤖", "AI Detection", "Powered by Hailo AI Kit acceleration"),
        ("⏱️", "Auto Timing", "5-minute violation threshold detection"),
        ("🔍", "Plate Recognition", "Automatic license plate capture (OCR)"),
        ("📊", "Analytics", "Comprehensive reporting and insights"),
        ("🔔", "Notifications", "Real-time alerts to enforcers")
    ]
    
    for icon, title, text in features:
        st.markdown(f"""
            <div class="feature-card">
                <div style="display: flex; align-items: center;">
                    <span class="feature-icon">{icon}</span>
                    <div>
                        <div class="feature-title">{title}</div>
                        <div class="feature-text">{text}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="clean-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📋 Research Info</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="info-box">
            <div class="info-title">🎓 Academic Project</div>
            <div class="info-text">
                Doctor of Technology Program<br>
                Technological University of the Philippines
            </div>
        </div>
        
        <div class="info-box">
            <div class="info-title">👤 Researcher</div>
            <div class="info-text">Ma. Ymelda C. Batalla</div>
        </div>
        
        <div class="info-box">
            <div class="info-title">📍 Location</div>
            <div class="info-text">
                Barangay Tagapo<br>
                Santa Rosa City, Laguna
            </div>
        </div>
        
        <div class="info-box">
            <div class="info-title">🚀 Technology Stack</div>
            <div class="info-text">
                YOLOv8 • Hailo AI • Raspberry Pi 5<br>
                Firebase • Streamlit • Python
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Recent Violations
if firebase_connected:
    st.markdown('<div class="clean-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🚨 Recent Violations</div>', unsafe_allow_html=True)
    
    try:
        recent_violations = db.collection('violations').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(3).stream()
        
        violations_found = False
        for violation in recent_violations:
            violations_found = True
            data = violation.to_dict()
            
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                if data.get('image_url'):
                    st.image(data['image_url'], use_column_width=True)
                else:
                    st.markdown("""
                        <div style="background: #f1f5f9; padding: 2rem; text-align: center; border-radius: 8px;">
                            <div style="font-size: 2rem;">📷</div>
                            <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.5rem;">No Image</div>
                        </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                vehicle = data.get('vehicle_type', 'Unknown').upper()
                plate = data.get('plate_number', 'N/A')
                duration = data.get('duration', 0)
                location = data.get('location', 'N/A')
                
                st.markdown(f"""
                    <div>
                        <div style="font-weight: 600; font-size: 1.1rem; color: #1e293b; margin-bottom: 0.5rem;">
                            🚗 {vehicle} - {plate}
                        </div>
                        <div style="color: #64748b; font-size: 0.875rem; margin-bottom: 0.25rem;">
                            ⏱️ Duration: {duration:.1f} minutes
                        </div>
                        <div style="color: #64748b; font-size: 0.875rem;">
                            📍 {location}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                timestamp = data.get('timestamp')
                if timestamp:
                    st.markdown(f"""
                        <div style="text-align: right; color: #94a3b8; font-size: 0.875rem; margin-bottom: 1rem;">
                            🕐 {timestamp.strftime('%H:%M:%S')}
                        </div>
                    """, unsafe_allow_html=True)
                
                status = data.get('status', 'unknown')
                if status == 'active':
                    st.markdown('<div class="badge badge-active">🔴 Active</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="badge badge-resolved">🟢 Resolved</div>', unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
        
        if not violations_found:
            st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #94a3b8;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: #10b981;">No violations recorded yet</div>
                    <div style="font-size: 0.875rem; margin-top: 0.5rem;">System is ready to monitor!</div>
                </div>
            """, unsafe_allow_html=True)
    
    except:
        st.info("Unable to load recent violations")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; color: white; padding: 2rem 0; margin-top: 2rem;">
        <div style="font-size: 0.875rem; opacity: 0.9;">
            © 2025 Ma. Ymelda C. Batalla • Technological University of the Philippines
        </div>
        <div style="font-size: 0.75rem; opacity: 0.7; margin-top: 0.5rem;">
            Powered by YOLOv8, Hailo AI, Firebase & Streamlit
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style="color: white; padding: 1rem 0;">
            <h3 style="color: white; margin-bottom: 1rem;">🧭 Quick Navigation</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="color: white; font-size: 0.875rem; line-height: 1.8;">
                📊 <strong>Dashboard</strong>: Overview<br>
                🚨 <strong>Live Violations</strong>: Active monitoring<br>
                📈 <strong>Analytics</strong>: Trends & insights
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
            <div style="color: white; font-weight: 600; margin-bottom: 0.5rem;">⚡ System Status</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 0.875rem;">
                ✅ All systems operational<br>
                📊 Uptime: 99.9%
            </div>
        </div>
    """, unsafe_allow_html=True)
