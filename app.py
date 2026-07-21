# app.py
import logging
import streamlit as st
import pandas as pd
import plotly.express as px
from config.settings import OPENAI_API_KEY
from Services.openai_service import generate_strategy
from Services.pdf_service import PDFService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Premium Killer Mock Brief (in Ukrainian to test Cyrillic PDF rendering)
st.set_page_config(
    page_title="BriefToLaunch MVP",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark Premium CSS Injection
st.markdown("""
    <style>
    /* Main body background & text colors */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    }
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #58a6ff !important;
        font-weight: 600;
    }
    /* Container styling */
    div[data-testid="stForm"] {
        border: 1px solid #30363d !important;
        background-color: #161b22 !important;
        border-radius: 6px;
        padding: 20px;
    }
    div[data-testid="metric-container"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 6px;
    }
    /* Custom buttons */
    .stButton>button {
        background-color: #21262d !important;
        color: #58a6ff !important;
        border: 1px solid #30363d !important;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #30363d !important;
        border-color: #8b949e !important;
    }
    /* Download button */
    .stDownloadButton>button {
        background-color: #238636 !important;
        color: #ffffff !important;
        border: 1px solid #2ea043 !important;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        width: 100%;
    }
    .stDownloadButton>button:hover {
        background-color: #2ea043 !important;
    }
    /* Textareas and inputs */
    textarea {
        background-color: #0d1117 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 BriefToLaunch")
st.subheader("Elite Cynical CMO Campaign Strategy MVP")

# Check if strategy exists in session state
if "strategy" not in st.session_state:
    st.session_state.strategy = None

# Two-column layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📝 Brand Brief Input")
    
    # API Key Handling
    api_key_input = st.text_input(
        "OpenAI API Key (Optional if set in `.env` / Environment)",
        type="password",
        value=OPENAI_API_KEY or "",
        placeholder="sk-proj-..."
    )
    
    brief_text = st.text_area(
        "Paste Raw Notes or Brand Brief",
        value=DEFAULT_BRIEF,
        height=400
    )
    
    if st.button("Generate Strategy Campaign"):
        final_key = api_key_input or OPENAI_API_KEY
        if not final_key:
            st.error("Error: OpenAI API Key is missing. Enter it above or add it to `.env`.")
        else:
            with st.spinner("Cynical CMO is writing your campaign strategy..."):
                try:
                    strategy = generate_strategy(brief_text, custom_api_key=final_key)
                    st.session_state.strategy = strategy
                    st.success("Strategy compiled successfully!")
                except Exception as e:
                    st.error(f"Failed to generate strategy: {e}")

with col2:
    st.markdown("### 📊 Compiled Campaign Output")
    
    strategy = st.session_state.strategy
    if strategy:
        # Title and positioning
        st.markdown(f"#### 🏷️ Campaign Name: **{strategy.campaign_name}**")
        st.info(f"**Positioning Statement:** {strategy.positioning}")
        
        # Target Audience Info
        st.markdown("---")
        st.markdown(f"👤 **Persona Nickname:** `{strategy.target_audience.cynical_nickname}`")
        st.write(f"**Demographics:** {strategy.target_audience.demographics}")
        st.write(f"**Lifestyle & Psychographics:** {strategy.target_audience.lifestyle_psychographics}")
        
        # Channels expanders
        st.markdown("---")
        st.markdown("🛠️ **Channel Activations**")
        for ch in strategy.channels:
            with st.expander(ch.channel_name):
                for step in ch.steps:
                    st.write(f"- {step}")
        
        # NGO Integration
        st.markdown("---")
        st.markdown(f"🤝 **CSR Integration ({strategy.csr.ngo_name})**")
        st.write(strategy.csr.integration_concept)
        
        # Plotly budget share pie chart & data table
        st.markdown("---")
        st.markdown("💰 **Budget Allocation & KPIs**")
        
        budget_data = []
        for b in strategy.budget:
            budget_data.append({
                "Operational Item": b.operational_item,
                "Percentage Share (%)": b.percentage_share,
                "Quantifiable KPI": b.quantifiable_kpi
            })
            
        df = pd.DataFrame(budget_data)
        
        # Render Plotly Pie Chart
        fig = px.pie(
            df,
            names="Operational Item",
            values="Percentage Share (%)",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Teal
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e6edf3",
            showlegend=True,
            margin=dict(t=10, b=10, l=10, r=10),
            height=260
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Render Table
        st.table(df)
        
        # Compile PDF and provide download button
        try:
            pdf_path = "strategy_output.pdf"
            PDFService.generate_report(strategy, pdf_path)
            
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
                
            st.download_button(
                label="📥 Download Marketing Strategy PDF",
                data=pdf_bytes,
                file_name="strategy_output.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error compiling PDF file: {e}")
    else:
        st.markdown("_Input a campaign brief on the left and hit compile to display the strategy data here._")
