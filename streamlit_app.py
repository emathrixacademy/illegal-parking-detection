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

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Firebase
@st.cache_resource
def init_firebase():
    """Initialize Firebase connection"""
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

# Initialize database
try:
    db = init_firebase()
    firebase_connected = True
except Exception as e:
    st.error(f"Firebase connection error: {e}")
    firebase_connected = False

# Header
st.title("🚗 Illegal Parking Detection System")
st.markdown("### Decongesting the Sidewalk - Barangay Tagapo, City of Santa Rosa, Laguna")
st.markdown("---")

# Welcome message
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## Welcome to the Monitoring System
    
    This system uses **Computer Vision** and **IoT** technology to automatically detect 
    and monitor illegal parking violations on sidewalks in real-time.
    
    **Features:**
    - 🎥 Real-time camera monitoring
    - 🤖 AI-powered vehicle detection (YOLOv8 with Hailo AI Kit)
    - ⏱️ Automatic violation timing (5-minute threshold)
    - 📸 License plate recognition
    - 📊 Analytics and reporting
    - 🔔 Real-time notifications
    
    **Research Project:**
    - **Title:** Decongesting the Sidewalk: A Computer Vision-Based IoT Application
    - **Location:** Barangay Tagapo, City of Santa Rosa, Laguna
    - **Institution:** Technological University of the Philippines
    """)

with col2:
    st.info("""
    **System Status**
    
    🟢 Dashboard: Online
    """)
    
    if firebase_connected:
        st.success("🟢 Database: Connected")
    else:
        st.error("🔴 Database: Disconnected")
    
    st.metric("Active Cameras", "1")
    st.metric("Location", "Brgy. Tagapo")

st.markdown("---")

# Quick stats
if firebase_connected:
    st.subheader("📊 Quick Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        # Get today's violations
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        violations_ref = db.collection('violations').where('timestamp', '>=', today).stream()
        violations_list = list(violations_ref)
        
        total_violations = len(violations_list)
        active_violations = len([v for v in violations_list if v.to_dict().get('status') == 'active'])
        
        col1.metric("Total Violations Today", total_violations)
        col2.metric("Active Violations", active_violations)
        col3.metric("Resolved Today", total_violations - active_violations)
        
        if violations_list:
            avg_duration = sum([v.to_dict().get('duration', 0) for v in violations_list]) / len(violations_list)
            col4.metric("Average Duration", f"{avg_duration:.1f} min")
        else:
            col4.metric("Average Duration", "0 min")
            
    except Exception as e:
        col1.metric("Total Violations Today", "0")
        col2.metric("Active Violations", "0")
        col3.metric("Resolved Today", "0")
        col4.metric("Average Duration", "0 min")

# Recent violations preview
st.markdown("---")
st.subheader("🚨 Recent Violations")

if firebase_connected:
    try:
        recent_violations = db.collection('violations').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(5).stream()
        
        violations_found = False
        for violation in recent_violations:
            violations_found = True
            data = violation.to_dict()
            
            with st.container():
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    if data.get('image_url'):
                        st.image(data['image_url'], width=200)
                    else:
                        st.info("📷 No image available")
                
                with col2:
                    st.markdown(f"**Vehicle:** {data.get('vehicle_type', 'Unknown').upper()}")
                    st.markdown(f"**Plate Number:** {data.get('plate_number', 'N/A')}")
                    st.markdown(f"**Duration:** {data.get('duration', 0):.1f} minutes")
                    st.markdown(f"**Location:** {data.get('location', 'N/A')}")
                
                with col3:
                    timestamp = data.get('timestamp')
                    if timestamp:
                        st.markdown(f"**Time:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                    status = data.get('status', 'unknown')
                    if status == 'active':
                        st.error("🔴 Active")
                    else:
                        st.success("🟢 Resolved")
                
                st.divider()
        
        if not violations_found:
            st.info("📭 No violations recorded yet. The system is ready to monitor!")
            st.balloons()
            
    except Exception as e:
        st.warning(f"Unable to load recent violations: {e}")
else:
    st.warning("⚠️ Database connection required to view violations")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Developed by Ma. Ymelda C. Batalla</strong></p>
    <p>Technological University of the Philippines - Doctor of Technology Program</p>
    <p>February 2023</p>
</div>
""", unsafe_allow_html=True)

# Navigation hint
st.sidebar.success("Select a page above to explore different sections.")
st.sidebar.info("""
**Navigation:**
- 📊 Dashboard: Overview and statistics
- 🚨 Live Violations: Real-time monitoring
- 📈 Analytics: Historical data and trends
""")
