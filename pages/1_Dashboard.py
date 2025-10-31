import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Same clean styling
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
    
    .clean-card:hover {
        box-shadow: 0 4px 12px rgba(91, 33, 182, 0.1);
        border-color: #c4b5fd;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #7c3aed;
        display: inline-block;
    }
    
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
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
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
        <div class="page-title">📊 Dashboard Overview</div>
        <div class="page-subtitle">Comprehensive violation statistics and insights</div>
    </div>
""", unsafe_allow_html=True)

# Date filter
col1, col2 = st.columns([3, 1])
with col1:
    date_filter = st.date_input("📅 Select Date", datetime.now())
with col2:
    if st.button("🔄 Refresh Data"):
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Get violations for selected date
start_time = datetime.combine(date_filter, datetime.min.time())
end_time = datetime.combine(date_filter, datetime.max.time())

try:
    violations_ref = db.collection('violations').where('timestamp', '>=', start_time).where('timestamp', '<=', end_time).stream()
    violations_list = [v.to_dict() for v in violations_ref]
    
    # Summary metrics
    st.markdown('<div class="clean-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📈 Daily Summary</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(violations_list)
    active = len([v for v in violations_list if v.get('status') == 'active'])
    resolved = total - active
    avg_duration = sum([v.get('duration', 0) for v in violations_list]) / total if total > 0 else 0
    
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
                <div class="metric-label">Active</div>
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
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Vehicle type breakdown
    if violations_list:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">🚗 Violations by Vehicle Type</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        vehicle_counts = {}
        for v in violations_list:
            vtype = v.get('vehicle_type', 'unknown')
            vehicle_counts[vtype] = vehicle_counts.get(vtype, 0) + 1
        
        with col1:
            st.bar_chart(vehicle_counts)
        
        with col2:
            for vtype, count in vehicle_counts.items():
                st.markdown(f"""
                    <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #7c3aed;">
                        <span style="font-weight: 600; color: #111827;">{vtype.title()}</span>
                        <span style="float: right; color: #7c3aed; font-weight: 700;">{count}</span>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Detailed table
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📋 Detailed Violations</div>', unsafe_allow_html=True)
        df = pd.DataFrame(violations_list)
        if not df.empty:
            st.dataframe(
                df[['timestamp', 'vehicle_type', 'plate_number', 'duration', 'status']], 
                use_container_width=True,
                hide_index=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.markdown("""
            <div class="clean-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📭</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #111827;">No violations recorded for this date</div>
                <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">Select a different date to view violations</div>
            </div>
        """, unsafe_allow_html=True)
        
except Exception as e:
    st.error(f"Error loading data: {e}")
