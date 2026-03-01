import streamlit as st
from dotenv import load_dotenv
import pandas as pd

# Load .env early so module-level imports (like utils) can read GOOGLE_API_KEY
load_dotenv()

from utils import *


def main():
    # dotenv already loaded at import time
    
    st.set_page_config(page_title="Data Quality Remediation Bot", page_icon="🤖")
    st.title("Data Quality Remediation Bot💁 ")
    st.subheader("upload your data quality failed record file ")


    # let user upload a CSV of failed records
    # file upload and storage of context
    uploaded = st.file_uploader("Upload failed records CSV", type="csv")

    if uploaded is not None:
        try:
            df_failed = pd.read_csv(uploaded)
            st.write("### Uploaded records (first 5 rows)", df_failed.head())

            # save csv text in session state so it can be referenced later
            st.session_state.failed_csv = df_failed.to_csv(index=False)

            with st.spinner("Generating remediation report..."):
                report = analyze_failed_records(df_failed)
                st.text_area("Detailed remediation report", report, height=400)

            st.success("Report generated ✅")
        except Exception as e:
            st.error(f"Failed to read or process file: {e}")

    # keep previous text input as optional chat interface
    st.write("---")
    user_input = st.text_input("Or ask a data-quality question")
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
