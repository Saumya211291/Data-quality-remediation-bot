import streamlit as st
from dotenv import load_dotenv
import pandas as pd

# THIS MUST BE THE FIRST ST COMMAND
st.set_page_config(
    page_title="Data Quality Remediation Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# BRANDING (Add it here)
#st.logo("/Users/khajasaifanmulla/Desktop/Projects/run.gif", link="https://lloydstechnologycentre.com/")

with st.sidebar:
    # This ensures your horizontal logo fills the sidebar width
    st.image("/Users/khajasaifanmulla/Desktop/Projects/ltclogo2.jpg",link="https://lloydstechnologycentre.com/", use_container_width=True)
    
    # Optional: Add a subtle version or "Internal Use" tag for Org standards
    st.caption("v1.2.0 | Enterprise Edition")
    st.divider() 
    
    # --- Rest of your sidebar inputs go here ---
    st.subheader("🚀 Quick Start Guide")
    st.markdown("""
    1. **Upload**: Drop a CSV into the main panel.
    2. **Analyze**: AI identifies data quality errors.
    3. **Review**: Check the generated remediation report.
    4. **Download**: Save results as Text.
    """)
    st.divider()
    #uploaded_file = st.file_uploader("Upload DQ File", type=['csv', 'xlsx'])

# 2. EXACT CSS FOR GREEN-TO-BLACK GRADIENT
st.markdown("""
    <style>
    /* 1. The Main Gradient: #006400 (Dark Green) to #000000 (Black) */
    .stApp {
        background: linear-gradient(180deg, #005400 0%, #002b21 35%, #000000 100%) !important;
        background-attachment: fixed;
    }

    /* 2. Text Visibility - Using a crisp 'Mint White' for readability */
    h1, h2, h3, h4, h5, h6, p, span, label, div[data-testid="stMarkdownContainer"] {
        color: #f0fff4 !important;
    }

    /* 3. Professional Sidebar - Darkened to let the logo pop */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.8) !important;
        border-right: 1px solid #006400;
    }

    /* 4. Data Table/Dataframe Styling for Dark Mode */
    [data-testid="stDataFrameResizerGui"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }

    /* 5. Inputs and Buttons - Matching the #006400 Green */
    .stButton>button {
        background-color: #006400 !important;
        color: white !important;
        border: 1px solid #22c55e !important;
        border-radius: 4px;
        font-weight: 600;
    }

    .stTextInput>div>div>input {
        background-color: #001a14 !important;
        color: white !important;
        border: 1px solid #006400 !important;
    }

    /* Remove the default Streamlit header shadow */
    header {
        background-color: rgba(0,0,0,0) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Load .env early so module-level imports (like utils) can read GOOGLE_API_KEY
load_dotenv()

from utils import *


def main():
    # dotenv already loaded at import time
    
    st.title("Data Quality Remediation Bot💁 ")
    st.subheader("Upload your data quality failed record file ")


    # let user upload a CSV of failed records
    # file upload and storage of context
    uploaded_file = st.file_uploader("Upload failed records CSV", type="csv")

    if uploaded_file is not None:
        try:
            df_failed = pd.read_csv(uploaded_file)
            st.write("### Uploaded records (first 5 rows)", df_failed.head())

            # save csv text in session state so it can be referenced later
            st.session_state.failed_csv = df_failed.to_csv(index=False)

            with st.spinner("Generating remediation report..."):
                report = analyze_failed_records(df_failed)
                st.text_area("Detailed remediation report", report, height=400)

            # --- DOWNLOAD BUTTON STARTS HERE ---
                st.download_button(
                    label="📥 Download Remediation Report",
                    data=report,
                    file_name="remediation_report.txt",
                    mime="text/plain"
                )
                # --- DOWNLOAD BUTTON ENDS HERE ---
            st.success("Report generated ✅")
        except Exception as e:
            st.error(f"Failed to read or process file: {e}")

    # keep previous text input as optional chat interface
    st.write("---")
    user_input = st.text_input("Or ask a data-quality question...?")
    submit = st.button("Submit")
    if submit and user_input:
        with st.spinner('Processing your request...'):
            extra = st.session_state.get('failed_csv')
            response = generate_response(user_input, additional_context=extra)
            st.write(response)
        st.success("Hope I was able to help you...❤️")


#Invoking main function
if __name__ == '__main__':
    main()
