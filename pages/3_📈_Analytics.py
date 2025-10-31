import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

# Initialize Firebase
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

st.title("📈 Analytics & Insights")
st.markdown("Historical data and trends analysis")
st.markdown("---")

# Date range filter
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=7))
with col2:
    end_date = st.date_input("End Date", datetime.now())

# Get violations
try:
    start_time = datetime.combine(start_date, datetime.min.time())
    end_time = datetime.combine(end_date, datetime.max.time())
    
    violations_ref = db.collection('violations').where('timestamp', '>=', start_time).where('timestamp', '<=', end_time).stream()
    violations_list = [v.to_dict() for v in violations_ref]
    
    if violations_list:
        df = pd.DataFrame(violations_list)
        
        # Convert timestamp to datetime
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        
        # Daily violations trend
        st.subheader("📊 Daily Violations Trend")
        daily_counts = df.groupby('date').size().reset_index(name='count')
        fig = px.line(daily_counts, x='date', y='count', title='Violations per Day', markers=True)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Vehicle type distribution
            st.subheader("🚗 Vehicle Type Distribution")
            vehicle_counts = df['vehicle_type'].value_counts()
            fig = px.pie(values=vehicle_counts.values, names=vehicle_counts.index, title='By Vehicle Type', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Hourly distribution
            st.subheader("⏰ Violations by Hour")
            hourly_counts = df.groupby('hour').size().reset_index(name='count')
            fig = px.bar(hourly_counts, x='hour', y='count', title='Violations by Hour of Day')
            st.plotly_chart(fig, use_container_width=True)
        
        # Duration analysis
        st.subheader("⏱️ Duration Analysis")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Average Duration", f"{df['duration'].mean():.1f} min")
        col2.metric("Maximum Duration", f"{df['duration'].max():.1f} min")
        col3.metric("Minimum Duration", f"{df['duration'].min():.1f} min")
        col4.metric("Total Violations", len(df))
        
        # Top violators (if plate numbers available)
        st.subheader("🚨 Most Frequent Violators")
        if 'plate_number' in df.columns:
            top_violators = df['plate_number'].value_counts().head(10)
            st.bar_chart(top_violators)
        
    else:
        st.info("📭 No violations recorded in selected date range")
        
except Exception as e:
    st.error(f"Error loading analytics: {e}")
```

4. Click **"Commit changes"**

---

### **File 6: requirements.txt**

1. Click **"Add file"** → **"Create new file"**
2. **Filename:** `requirements.txt`
3. **Paste this:**
```
streamlit==1.29.0
firebase-admin==6.3.0
pandas==2.1.4
plotly==5.18.0
Pillow==10.1.0
