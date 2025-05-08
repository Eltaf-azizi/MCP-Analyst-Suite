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