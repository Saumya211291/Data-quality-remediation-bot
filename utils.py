import os
import warnings
from dotenv import load_dotenv

# Load environment variables early so any module-level config can read them
load_dotenv()

# Suppress the FutureWarning about google.generativeai deprecation
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")

import google.generativeai as genai
import pandas as pd

# The previous implementation loaded static Word/Excel files to provide context.
# Since users now upload their own CSV, we no longer need those files.  Define
# empty context strings for compatibility.
WORD_CONTEXT = ""
EXCEL_CONTEXT = ""

# configure SDK and model (use env var fallback)
# Read API key robustly (strip quotes if present) and configure
raw_key = os.getenv("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")
API_KEY = None
if raw_key:
    API_KEY = raw_key.strip().strip('"').strip("'")

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        print(f"Warning: failed to configure genai with provided key: {e}")
else:
    print("No GOOGLE_API_KEY found. Please set GOOGLE_API_KEY in environment or .env file.")

MODEL_NAME = os.getenv("GENAI_MODEL", "gemini-2.5-flash")

MODEL = None
try:
    MODEL = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    print(f"Failed to load model {MODEL_NAME}: {e}")
#Function to extract data from text...
def generate_response(prompt: str, additional_context: str | None = None) -> str:
    """Generate a response using the generative model.

    - *prompt* is the user's question or instruction.
    - *additional_context* can contain extra text (e.g. CSV rows) that should
      be included in the prompt; if provided it will be appended and the static
      Excel/Word contexts will still be included.
    """
    if MODEL is None:
        return f"Model not loaded ({MODEL_NAME}). Check GOOGLE_API_KEY, GENAI_MODEL and account access."
    try:
        # build base prompt with known contexts
        base = (
            "You are an assistant with access to the following data sources:\n"
            f"Execel Data: {EXCEL_CONTEXT}\n"
            f"Word Data: {WORD_CONTEXT}\n"
        )
        if additional_context:
            base += f"Additional Data: {additional_context}\n"
        base += f"Your task is to answer the user's question based on the provided data sources.\nUser's question: {prompt}"
        response = MODEL.generate_content(base)
        # ensure attribute exists and use correct strip()
        return getattr(response, "text", str(response)).strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Analyze a dataframe of failed records and produce a detailed remediation report
# The CSV is expected to have fields that indicate which table/resource failed along
# with other context. Gemini will be asked to review each row and describe the issue
# and a suggested fix.
def analyze_failed_records(df: pd.DataFrame) -> str:
    """Generate a detailed report for each failed record in the provided DataFrame."""
    if MODEL is None:
        return f"Model not loaded ({MODEL_NAME}). Check GOOGLE_API_KEY, GENAI_MODEL and account access."
    try:
        csv_text = df.to_csv(index=False)
        prompt = (
            "You are a data-quality assistant. You will receive a CSV of failed records. "
            "For each row, identify which resource or table has failed, describe the issue, "
            "and explain how to fix it. Please output a clear, detailed paragraph per record.\n\n"
            f"Here are the records:\n{csv_text}"
        )
        response = MODEL.generate_content(prompt)
        return getattr(response, "text", str(response)).strip()
    except Exception as e:
        return f"An error occurred: {e}"


