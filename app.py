import os
import base64
from datetime import datetime
from flask import Flask, json, jsonify, request


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
    data = request.json
    if not data or 'product_name' not in data:
        return jsonify({"error": "Product name is required"}), 400
    

    product_name = data['product_name']
    try:
        # Get full analysis with chart
        analysis_result = ecommerce_swot_analyzer(product_name)


        # Save analysis result to local directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = product_name.replace(" ", "_").replace("/", "_")
        result_filename = f"{safe_name}_swot_{timestamp}.json"
        result_path = os.path.join(RESULTS_DIR, result_filename)


        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=4)

        
        # Save the analysis in a PDF
        pdf_filename = f"{safe_name}_swot_{timestamp}.pdf"
        pdf_path = os.path.join(PDF_DIR, pdf_filename)
        generate_pdf_report(analysis_result, pdf_path)


        analysis_result['local_file'] = result_path
        analysis_result['pdf_file'] = pdf_path

        return jsonify(analysis_result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



def generate_pdf_report(data, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.call(200, 10, f"SWOT Analysis Report", ln=True, align='C')


    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, f"Product: {data['product']}", ln=True)
    pdf.set_font("Arial", size=12)


    summary = data.get("summary", {})