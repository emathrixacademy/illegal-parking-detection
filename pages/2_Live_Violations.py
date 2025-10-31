import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

st.set_page_config(page_title="Live Violations", page_icon="🚨", layout="wide")

# Initialize Firebase
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

st.title("🚨 Live Violations Monitoring")
st.markdown("Real-time monitoring of active parking violations")
st.markdown("---")

# Refresh button
if st.button("🔄 Refresh"):
    st.rerun()

st.info("🔄 Click refresh button to see latest violations")

# Get active violations
try:
    active_violations = db.collection('violations').where('status', '==', 'active').order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
    
    violations_found = False
    for violation in active_violations:
        violations_found = True
        data = violation.to_dict()
        
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if data.get('image_url'):
                    st.image(data['image_url'], use_column_width=True)
                else:
                    st.info("📷 No image")
            
            with col2:
                st.markdown(f"### {data.get('vehicle_type', 'Unknown').upper()}")
                st.markdown(f"**🚗 Plate:** {data.get('plate_number', 'N/A')}")
                st.markdown(f"**🎨 Color:** {data.get('color', 'N/A')}")
                st.markdown(f"**⏱️ Duration:** {data.get('duration', 0):.1f} minutes")
                st.markdown(f"**📍 Location:** {data.get('location', 'N/A')}")
                
                timestamp = data.get('timestamp')
                if timestamp:
                    st.markdown(f"**🕐 Time:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            
            with col3:
                st.error("🔴 ACTIVE VIOLATION")
                
                if st.button("✅ Mark as Resolved", key=violation.id):
                    db.collection('violations').document(violation.id).update({
                        'status': 'resolved',
                        'resolved_at': datetime.now()
                    })
                    st.success("Violation marked as resolved!")
                    st.rerun()
            
            st.divider()
    
    if not violations_found:
        st.success("✅ No active violations at this time!")
        st.balloons()
        
except Exception as e:
    st.error(f"Error loading violations: {e}")
