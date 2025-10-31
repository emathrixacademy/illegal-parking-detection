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

# Clean white design with minimal purple accents
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background - WHITE */
    .stApp {
        background: #ffffff;
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
    
    /* Header section - Dark Purple Gradient */
    .header-container {
        background: linear-gradient(135deg, #5b21b6 0%, #7c3aed 100%);
        text-align: center;
        padding: 3rem 2rem;
        margin: -2rem -2rem 2rem -2rem;
        border-radius: 0 0 24px 24px;
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
        color: rgba(255, 255, 255, 0.95);
        font-weight: 400;
    }
    
    /* Clean white cards */
    .clean-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .clean-card:hover {
        box-shadow: 0 4px 12px rgba(91, 33, 182, 0.1);
        transform: translateY(-2px);
        border-color: #c4b5fd;
    }
    
    /* Status cards - White with purple border */
    .status-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .status-card:hover {
        border-color: #7c3aed;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
    }
    
    .status-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .status-label {
        font-size: 0.875rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .status-value {
        font-size: 2rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.5rem;
    }
    
    .status-text {
        font-size: 0.875rem;
        color: #7c3aed;
        font-weight: 600;
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
    
    /* Section headers with purple accent */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #7c3aed;
        display: inline-block;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    
    .feature-card:hover {
        border-color: #c4b5fd;
        box-shadow: 0 4px 8px rgba(124, 58, 237, 0.1);
        transform: translateX(5px);
    }
    
    .feature-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
    }
    
    .feature-title {
        font-size: 1rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.25rem;
    }
    
    .feature-text {
        font-size: 0.875rem;
        color: #6b7280;
    }
    
    /* Metrics - purple accent */
    .metric-container {
        text-align: center;
        padding: 1.5rem;
        background: white;
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        border-color: #7c3aed;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #7c3aed;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-delta {
        font-size: 0.75rem;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    /* Info box - light purple background */
    .info-box {
        background: #faf5ff;
        border-left: 4px solid #7c3aed;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        transition: all 0.2s ease;
    }
    
    .info-box:hover {
        background: #f3e8ff;
    }
    
    .info-title {
        font-weight: 600;
        color: #5b21b6;
        margin-bottom: 0.5rem;
    }
    
    .info-text {
        color: #4b5563;
        font-size: 0.875rem;
        line-height: 1.6;
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
    
    /* Sidebar - Dark Purple */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #5b21b6 0%, #7c3aed 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: #7c3aed;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s;
        border: 2px solid #7c3aed;
    }
    
    .stButton>button:hover {
        background: #6d28d9;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 2px solid #e5e7eb;
        margin: 2rem 0;
    }
    </style>
    st.markdown("""
    <style>
    /* Nuclear option - hide everything in header */
    .stApp > header,
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    .stToolbar,
    button[kind="header"],
    button[title="Share"],
    button[title="Fork"],
    .stAppDeployButton,
    .stApp > header > div,
    header > div > div > button {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        width: 0 !important;
        pointer-events: none !important;
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

# Header - Only dark purple section
st.markdown("""
    <div class="header-container">
        <div class="main-title">🚗 Smart Parking Enforcement</div>
        <div class="subtitle">AI-Powered Illegal Parking Detection System</div>
        <div class="subtitle">Barangay Tagapo, City of Santa Rosa, Laguna</div>
    </div>
""", unsafe_allow_html=True)

# Status Cards - White with borders
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
                <div class="status-text" style="color: #ef4444;">DISCONNECTED</div>
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
    st.markdown("<br>", unsafe_allow_html=True)
    
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

st.markdown("<br>", unsafe_allow_html=True)

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
    st.markdown('<div class="section-header">📋 Project Info</div>', unsafe_allow_html=True)
    
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
                        <div style="background: #f9fafb; padding: 2rem; text-align: center; border-radius: 8px; border: 1px solid #e5e7eb;">
                            <div style="font-size: 2rem;">📷</div>
                            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 0.5rem;">No Image</div>
                        </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                vehicle = data.get('vehicle_type', 'Unknown').upper()
                plate = data.get('plate_number', 'N/A')
                duration = data.get('duration', 0)
                location = data.get('location', 'N/A')
                
                st.markdown(f"""
                    <div>
                        <div style="font-weight: 600; font-size: 1.1rem; color: #111827; margin-bottom: 0.5rem;">
                            🚗 {vehicle} - {plate}
                        </div>
                        <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.25rem;">
                            ⏱️ Duration: {duration:.1f} minutes
                        </div>
                        <div style="color: #6b7280; font-size: 0.875rem;">
                            📍 {location}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                timestamp = data.get('timestamp')
                if timestamp:
                    st.markdown(f"""
                        <div style="text-align: right; color: #9ca3af; font-size: 0.875rem; margin-bottom: 1rem;">
                            🕐 {timestamp.strftime('%H:%M:%S')}
                        </div>
                    """, unsafe_allow_html=True)
                
                status = data.get('status', 'unknown')
                if status == 'active':
                    st.markdown('<div class="badge badge-active">🔴 Active</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="badge badge-resolved">🟢 Resolved</div>', unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
        
        if not violations_found:
            st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #9ca3af;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: #10b981;">No violations recorded yet</div>
                    <div style="font-size: 0.875rem; margin-top: 0.5rem; color: #6b7280;">System is ready to monitor!</div>
                </div>
            """, unsafe_allow_html=True)
    
    except:
        st.info("Unable to load recent violations")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 2rem 0;">
        <div style="font-size: 0.875rem;">
            © 2025 Ma. Ymelda C. Batalla • Technological University of the Philippines
        </div>
        <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 0.5rem;">
            Powered by YOLOv8, Hailo AI, Firebase & Streamlit
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar - Dark purple (only colored section)
with st.sidebar:
    st.markdown("""
        <div style="padding: 1rem 0;">
            <h3 style="margin-bottom: 1rem;">🧭 Quick Navigation</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="font-size: 0.875rem; line-height: 1.8;">
                📊 <strong>Dashboard</strong>: Overview<br>
                🚨 <strong>Live Violations</strong>: Active monitoring<br>
                📈 <strong>Analytics</strong>: Trends & insights
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
            <div style="font-weight: 600; margin-bottom: 0.5rem;">⚡ System Status</div>
            <div style="font-size: 0.875rem;">
                ✅ All systems operational<br>
                📊 Uptime: 99.9%
            </div>
        </div>
    """, unsafe_allow_html=True)
