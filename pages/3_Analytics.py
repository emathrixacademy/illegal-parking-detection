import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

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
    
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #7c3aed;
        display: inline-block;
    }
    
    .metric-box {
        background: #faf5ff;
        border: 2px solid #e9d5ff;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .metric-box-value {
        font-size: 2rem;
        font-weight: 800;
        color: #7c3aed;
        margin-bottom: 0.5rem;
    }
    
    .metric-box-label {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #5b21b6 0%, #7c3aed 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
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
        <div class="page-title">📈 Analytics & Insights</div>
        <div class="page-subtitle">Historical data and trends analysis</div>
    </div>
""", unsafe_allow_html=True)

# Date range filter
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=7))
with col2:
    end_date = st.date_input("End Date", datetime.now())

st.markdown("<br>", unsafe_allow_html=True)

# Get violations
try:
    start_time = datetime.combine(start_date, datetime.min.time())
    end_time = datetime.combine(end_date, datetime.max.time())
    
    violations_ref = db.collection('violations').where('timestamp', '>=', start_time).where('timestamp', '<=', end_time).stream()
    violations_list = [v.to_dict() for v in violations_ref]
    
    if violations_list:
        df = pd.DataFrame(violations_list)
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        
        # Duration summary
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">⏱️ Duration Analysis</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-box-value">{df['duration'].mean():.1f}</div>
                    <div class="metric-box-label">Average Duration (min)</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-box-value">{df['duration'].max():.1f}</div>
                    <div class="metric-box-label">Maximum Duration (min)</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-box-value">{df['duration'].min():.1f}</div>
                    <div class="metric-box-label">Minimum Duration (min)</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-box-value">{len(df)}</div>
                    <div class="metric-box-label">Total Violations</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Daily trend
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📊 Daily Violations Trend</div>', unsafe_allow_html=True)
        daily_counts = df.groupby('date').size().reset_index(name='count')
        fig = px.line(daily_counts, x='date', y='count', title='Violations per Day', markers=True)
        fig.update_traces(line_color='#7c3aed', marker=dict(size=8, color='#7c3aed'))
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="clean-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">🚗 Vehicle Type Distribution</div>', unsafe_allow_html=True)
            vehicle_counts = df['vehicle_type'].value_counts()
            fig = px.pie(values=vehicle_counts.values, names=vehicle_counts.index, title='By Vehicle Type', hole=0.4)
            fig.update_traces(marker=dict(colors=['#7c3aed', '#a78bfa', '#c4b5fd']))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="clean-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">⏰ Violations by Hour</div>', unsafe_allow_html=True)
            hourly_counts = df.groupby('hour').size().reset_index(name='count')
            fig = px.bar(hourly_counts, x='hour', y='count', title='Violations by Hour of Day')
            fig.update_traces(marker_color='#7c3aed')
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Top violators
        if 'plate_number' in df.columns:
            st.markdown('<div class="clean-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">🚨 Most Frequent Violators</div>', unsafe_allow_html=True)
            top_violators = df['plate_number'].value_counts().head(10)
            st.bar_chart(top_violators)
            st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.markdown("""
            <div class="clean-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📭</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #111827;">No violations recorded in selected date range</div>
                <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">Try selecting a different date range</div>
            </div>
        """, unsafe_allow_html=True)
        
except Exception as e:
    st.error(f"Error loading analytics: {e}")
