import streamlit as st
import joblib
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Sales Predictor",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for clean visual styling
st.markdown("""
    <style>
    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2563EB, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .header-subtitle {
        color: #6B7280;
        font-size: 1.05rem;
        margin-bottom: 1.8rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2.8rem !important;
        color: #2563EB !important;
        font-weight: 800 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Cache model loading to optimize performance
@st.cache_resource
def load_model():
    return joblib.load('linear_regression_model.sav')

model = load_model()

# Header Section
st.markdown('<div class="header-title">📈 Uncapped Live Sales Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Enter any media spending amount without limit to calculate real-time forecasts.</div>', unsafe_allow_html=True)

# Layout Setup
left_col, right_col = st.columns([1.1, 0.9], gap="large")

with left_col:
    st.subheader("🎯 Ad Budget Allocation ($)")
    st.caption("Type or step any numeric amount without upper limits:")
    
    # TV Input (Uncapped)
    tv = st.number_input(
        '📺 TV Advertising Spend ($)', 
        min_value=0.0, 
        max_value=None, 
        value=100.0, 
        step=10.0, 
        format="%.2f"
    )
    
    # Radio Input (Uncapped)
    radio = st.number_input(
        '📻 Radio Advertising Spend ($)', 
        min_value=0.0, 
        max_value=None, 
        value=20.0, 
        step=5.0, 
        format="%.2f"
    )
    
    # Newspaper Input (Uncapped)
    newspaper = st.number_input(
        '📰 Newspaper Advertising Spend ($)', 
        min_value=0.0, 
        max_value=None, 
        value=30.0, 
        step=5.0, 
        format="%.2f"
    )

# --- LIVE PREDICTION & CALCULATIONS ---
input_data = pd.DataFrame([{
    'TV': tv,
    'Radio': radio,
    'Newspaper': newspaper
}])

predicted_sales = model.predict(input_data)[0]
total_budget = tv + radio + newspaper

with right_col:
    st.subheader("📊 Real-Time Forecast")
    
    # Primary KPI Card
    st.metric(
        label="Predicted Sales",
        value=f"${predicted_sales:,.2f}"
    )
    
    st.divider()
    
    # Budget Analysis Summary
    st.markdown("**Budget Overview**")
    m1, m2 = st.columns(2)
    m1.metric("Total Budget", f"${total_budget:,.2f}")
    
    roas = (predicted_sales / total_budget) if total_budget > 0 else 0.0
    m2.metric("Estimated ROAS", f"{roas:.2f}x")
    
    # Dynamic Budget Percentages
    if total_budget > 0:
        st.write("---")
        st.write("**Budget Breakdown:**")
        tv_pct = (tv / total_budget) * 100
        radio_pct = (radio / total_budget) * 100
        news_pct = (newspaper / total_budget) * 100
        
        st.caption(f"**TV:** {tv_pct:.1f}% | **Radio:** {radio_pct:.1f}% | **Newspaper:** {news_pct:.1f}%")
        st.progress(min(tv / total_budget, 1.0))
