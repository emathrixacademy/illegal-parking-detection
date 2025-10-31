import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

st.set_page_config(page_title="Live Violations", page_icon="🚨", layout="wide")

# Same styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: #ffffff;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .header-container {
        background: linear-gradient(135deg, #5b21b6 0%, #7c3aed 100%);
        text-align: center;
        padding: 2.5rem 2rem;
        margin: -2rem -2rem 2rem -2rem;
        border-radius: 0 0 24px 24px;
    }
    
    .page-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .page-subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 400;
    }
    
    .clean-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        border: 1px solid #e5e7eb;
    }
    
    .violation-card {
        background: white;
        border: 2px solid #fee2e2;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .violation-card:hover {
        border-color: #fca5a5;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.1);
    }
    
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
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #5b21b6 0%, #7c3aed 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .stButton>button {
        background: #7c3aed;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        background: #6d28d9;
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

db = init_firebase()

# Header
st.markdown("""
    <div class="header-container">
        <div class="page-title">🚨 Live Violations Monitoring</div>
        <div class="page-subtitle">Real-time monitoring of active parking violations</div>
    </div>
""", unsafe_allow_html=True)

# Refresh button
if st.button("🔄 Refresh"):
    st.rerun()

st.info("🔄 Click refresh button to see latest violations", icon="ℹ️")

st.markdown("<br>", unsafe_allow_html=True)

# Get active violations (simplified query)
try:
    all_violations = db.collection('violations').stream()
    violations_list = []
    
    for violation in all_violations:
        data = violation.to_dict()
        if data.get('status') == 'active':
            violations_list.append((violation.id, data))
    
    # Sort by timestamp
    violations_list.sort(key=lambda x: x[1].get('timestamp', datetime.min), reverse=True)
    
    violations_found = False
    for violation_id, data in violations_list:
        violations_found = True
        
        st.markdown('<div class="violation-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
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
            color = data.get('color', 'N/A')
            duration = data.get('duration', 0)
            location = data.get('location', 'N/A')
            
            st.markdown(f"### 🚗 {vehicle}")
            st.markdown(f"**Plate Number:** {plate}")
            st.markdown(f"**Color:** {color}")
            st.markdown(f"**⏱️ Duration:** {duration:.1f} minutes")
            st.markdown(f"**📍 Location:** {location}")
            
            timestamp = data.get('timestamp')
            if timestamp:
                st.markdown(f"**🕐 Time:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        with col3:
            st.markdown('<div class="badge badge-active" style="font-size: 1rem; padding: 0.5rem 1rem;">🔴 ACTIVE</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("✅ Mark as Resolved", key=violation_id):
                db.collection('violations').document(violation_id).update({
                    'status': 'resolved',
                    'resolved_at': datetime.now()
                })
                st.success("Violation marked as resolved!")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if not violations_found:
        st.markdown("""
            <div class="clean-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">✅</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #10b981; margin-bottom: 0.5rem;">No Active Violations!</div>
                <div style="font-size: 1rem; color: #6b7280;">All clear at this time. System is monitoring.</div>
            </div>
        """, unsafe_allow_html=True)
        st.balloons()
        
except Exception as e:
    st.error(f"Error loading violations: {e}")
