import streamlit as st
import joblib
import pandas as pd

# Page Configuration - Must be the first Streamlit command
st.set_page_config(
    page_title="Sales Predictor",
    page_icon="📈",
    layout="wide"
)

# Custom Styling for modern UI
st.markdown("""
    <style>
    /* Gradient Accent Header */
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
        margin-bottom: 2rem;
    }
    
    /* Styled Prediction Metric Card */
    div[data-testid="stMetricValue"] {
        font-size: 2.8rem !important;
        color: #2563EB !important;
        font-weight: 800 !important;
    }
    
    /* Sub-cards styling */
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Load model with caching to avoid re-loading on every UI update
@st.cache_resource
def load_model():
    return joblib.load('linear_regression_model.sav')

model = load_model()

# Header Section
st.markdown('<div class="header-title">📈 Live Sales Prediction Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Adjust ad spend channels to calculate predicted revenue in real time.</div>', unsafe_allow_html=True)

# Layout Setup: Left column for inputs, right column for live predictions & breakdowns
left_col, right_col = st.columns([1.1, 0.9], gap="large")

with left_col:
    st.subheader("🎯 Media Spending ($)")
    st.caption("Drag the sliders or type exact values below:")
    
    # TV Input
    tv = st.slider('📺 TV Advertising', min_value=0.0, max_value=300.0, value=100.0, step=0.1, help="Spending budget on TV ads")
    
    # Radio Input
    radio = st.slider('📻 Radio Advertising', min_value=0.0, max_value=50.0, value=20.0, step=0.1, help="Spending budget on Radio ads")
    
    # Newspaper Input
    newspaper = st.slider('📰 Newspaper Advertising', min_value=0.0, max_value=120.0, value=30.0, step=0.1, help="Spending budget on Newspaper ads")

# --- LIVE PREDICTION LOGIC ---
# Construct DataFrame for inference
input_data = pd.DataFrame([{
    'TV': tv,
    'Radio': radio,
    'Newspaper': newspaper
}])

# Calculate Live Prediction
predicted_sales = model.predict(input_data)[0]
total_budget = tv + radio + newspaper

with right_col:
    st.subheader("📊 Forecast Summary")
    
    # Primary KPI Card
    st.metric(
        label="Predicted Sales ($)",
        value=f"${predicted_sales:,.2f}"
    )
    
    st.divider()
    
    # Additional Insights & Budget Breakdown
    st.markdown("**Budget Distribution**")
    m1, m2 = st.columns(2)
    m1.metric("Total Ad Spend", f"${total_budget:,.2f}")
    
    # Return on Ad Spend (ROAS) estimation
    roas = (predicted_sales / total_budget) if total_budget > 0 else 0
    m2.metric("Estimated ROAS", f"{roas:.2f}x")
    
    # Percentage Breakdown Progress Indicators
    if total_budget > 0:
        st.write("---")
        st.write("**Share of Voice:**")
        st.caption(f"**TV:** {tv/total_budget*100:.1f}% | **Radio:** {radio/total_budget*100:.1f}% | **Newspaper:** {newspaper/total_budget*100:.1f}%")
        st.progress(tv / total_budget)
