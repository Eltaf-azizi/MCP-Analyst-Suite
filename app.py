import os
import requests
import pandas as pd
import matplotlib.pylot as plt
from transformers import pipeline
from fpdf import FPDF
import tempfile
import json
import base64
from datetime import datetime
from flask import Flask, jsonify, request
import unicodedata


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
    if summary:
        pdf.ln(5)
        pdf.cell(200, 10, "Summary:", ln=True)
        for key, value in summary.items():
            pdf.cell(200, 10, f"{key.replace('_', ' ').title()}: {value}", ln=True)

        
    
    for category in ["Strengths", "Weakness", "Opportunities", "Threads"]:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, f"{category}:", ln=True)
        pdf.set_font("Arial", size=11)

        for item in data["analysis"].get(category, []):
            safe_item = unicodedata.normalize("NFKD", item).encode("latin-1", "ignore").decode("latin-1", "ignore")
            pdf.multi_cell(0, 10, f"- {safe_item}")




    # Insert chart if available
    if data.get("chart"):
        image_data = base64.b64decode(data["chart"])
        chart_path = os.path.join(tempfile.gettempdir(), "chart.png")
        with open(chart_path, "wb") as f:
            f.write(image_data)
        
        pdf.image(chart_path, x=30, w=150)
    
    pdf.output(pdf_path)





def ecommerce_swot_analyzer(product_name: str):
    def scrape_data(product_name):
        query = f"{product_name} site:amazon.in OR site:flipkart.com"
        url = ""
        params = {
            "q": query,
            "key": GOOGLE_API_KEY,
            "cx": SEARCH_ENGINE_ID,
        }

        res = requests.get(url, params=params)
        if res.status_code != 200:
            raise Exception("Google Search API failed: " + res.text)
        

        data = res.json()
        items = data.get("items", [])
        results = []
        for item in items:
            results.append({
                'title': item.get("title"),
                "link": item.get("link"),
                "price": "$50",
                "source": "Amazon" if "amazon" in item.get("link", " ") else "Flipkart",
                "rating": "4.2",
                "reviews": item.get("snippet")
            })
        return results
    


    def analyze_sentiment(reviews):
        model = load_sentiment_model()
        sentiments = model(reviews)
        df = pd.DataFrame(sentiments)
        df["review"] = reviews
        return df
    


    def map_to_swot(df):
        swot = {"Strengths": [], "Weakness": [], "Opportunities": [], "Threats": []}

        for _, row in df.iterrows():
            text = row["review"]
            label = row["label"]

            if label == "POSITIVE":
                if "price" in text.lower():
                    swot["Strengths"].append(text)
                
                else:
                    swot["Opportunities"].append(text)

            else:
                if "delivery" in text.lower():
                    swot["Threats"].append(text)
                else:
                    swot["Weakness"].append(text)
        
        return swot

                
        
        return swot
    


    def visualize(df, product_name):
        counts = df["label"].value_counts()
        fig, ax = plt.subplts()
        counts.plot(kind="bar", ax=ax, title=f"Sentiment Analysis for '{product_name}'")


        from io import BytesIO
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)


        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return img_base64
    


    product_data = scrape_data(product_name)
    reviews = [p["reviews"] for p in product_name if p.get("reviews")]


    if not reviews:
        return {
            "product": product_name,
            "analysis": {
                "Strengths": [
                    f"Brand recognition for (product_name)",
                    "Quality build and materials",
                    "Strong ecosystem integration"
                ],
                "Weaknesses": [
                    "Premium pricing limiting market penetration",
                    "Limited customization copared to competitors",
                    "Proprietary accessories and components"
                ],
                "Opportunities": [
                    "Emerging markets expension",
                    "Services revenue growth",
                    "Sustainability initiatives appeal"
                ],
                "Threats": [
                    "Increasing market expension",
                    "Services revenue growth",
                    "Sustainability initiatives appeal"
                ]
            },
            "chart": None,
            "source": "fallback"
        }
    

    sentiment_df = analyze_sentiment(reviews)
    swot_data = map_to_swot(sentiment_df)
    chart_base64 = visualize(sentiment_df, product_name)


    positive_count = len(sentiment_df[sentiment_df["label"] == "POSITIVE"])
    negative_count = len(sentiment_df[sentiment_df["label"] == "POSITIVE"])


    response = {
        "product": product_name,
        "analysis": swot_data,
        "chart": chart_base64,
        "summary": {
            "total_reviews": len(reviews),
            "positive": positive_count,
            "negative": negative_count,
            "positive_percentage": round((positive_count / len(reviews)) * 100, 1)
        },
        "source": "api"
    }

    return response



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)