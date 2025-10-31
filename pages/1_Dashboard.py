import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Initialize Firebase
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

st.title("📊 Dashboard Overview")
st.markdown("---")

# Date filter
col1, col2 = st.columns([3, 1])
with col1:
    date_filter = st.date_input("Select Date", datetime.now())
with col2:
    if st.button("🔄 Refresh Data"):
        st.rerun()

# Get violations for selected date
start_time = datetime.combine(date_filter, datetime.min.time())
end_time = datetime.combine(date_filter, datetime.max.time())

try:
    violations_ref = db.collection('violations').where('timestamp', '>=', start_time).where('timestamp', '<=', end_time).stream()
    violations_list = [v.to_dict() for v in violations_ref]
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(violations_list)
    active = len([v for v in violations_list if v.get('status') == 'active'])
    resolved = total - active
    avg_duration = sum([v.get('duration', 0) for v in violations_list]) / total if total > 0 else 0
    
    col1.metric("Total Violations", total, delta=f"+{total} today")
    col2.metric("Active", active, delta="-" + str(resolved) + " resolved")
    col3.metric("Resolved", resolved)
    col4.metric("Avg Duration", f"{avg_duration:.1f} min")
    
    st.markdown("---")
    
    # Vehicle type breakdown
    if violations_list:
        st.subheader("🚗 Violations by Vehicle Type")
        vehicle_counts = {}
        for v in violations_list:
            vtype = v.get('vehicle_type', 'unknown')
            vehicle_counts[vtype] = vehicle_counts.get(vtype, 0) + 1
        
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(vehicle_counts)
        with col2:
            for vtype, count in vehicle_counts.items():
                st.metric(vtype.title(), count)
        
        # Detailed table
        st.subheader("📋 Detailed Violations")
        df = pd.DataFrame(violations_list)
        st.dataframe(df[['timestamp', 'vehicle_type', 'plate_number', 'duration', 'status']], use_container_width=True)
    
    else:
        st.info("📭 No violations recorded for this date")
        
except Exception as e:
    st.error(f"Error loading data: {e}")
