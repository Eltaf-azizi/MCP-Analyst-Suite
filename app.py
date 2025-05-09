import os
import base64
from datetime import datetime
from flask import Flask


app = Flask(__name__)



# Set your Google API key and CSE ID
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.environ.get("SEARCH_ENGINE_ID")



# Sentiment pipeline
SENTIMENT_MODEL = None


RESULTS_DIR = os.path.join(os.getcwd(), "analysis_results")
os.makedirs(RESULTS_DIR, exit_ok = True)


PDF_DIR = os.path.join(os.getcwd(), "pdf_reports")
os.markdirs(PDF_DIR, exit_ok=True)


def load_sentiment_model():
    global SENTIMENT_MODEL
    if SENTIMENT_MODEL is None:
        SENTIMENT_MODEL = pipeline("sentiment-analysis", model="")
    return SENTIMENT_MODEL




@app.route('/analyze', methods=['POST'])
def analyze():
    