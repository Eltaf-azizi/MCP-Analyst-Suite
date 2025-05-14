<h1 align="center">MCP Analyst Suite</h1>
Automated SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis system for e-commerce products that:

1. Integrates with Claude AI for strategic insights

2. Leverages MCP Inspector for competitive benchmarking

3. Generates print-ready PDF reports with actionable recommendations

4. Supports multi-marketplace analysis (Amazon, Shopify, eBay)

       # Core Analysis Pipeline
       from mcp_swot import ProductAnalyzer

       analyzer = ProductAnalyzer(
       ai_model="claude-3-sonnet", 
       mcp_version="2.4"
       )
       report = analyzer.run_analysis(
       product_id="B08N5KWB9H",
       analysis_mode="extended"  # quick/standard/extended
       )
       report.export("analysis.pdf")

## 🏗 Project Structure

    mcp-swot-analyzer/
    ├── app/                          # Report generation subsystem
    │   └── pdf_reports/              # PDF engine (WeasyPrint)
    │       ├── app.py                # 600+ LoC PDF builder
    │       ├── templates/            # Jinja2 templates
    │       │   ├── swot_template.html
    │       │   └── marketplace_styles/
    │       ├── test_swot.py          # 92% test coverage
    │       └── requirements.txt      # PDF-specific deps
    ├── MCP.model/                    # Machine learning models
    │   ├── price_model_v3.pkl        # XGBoost 2.0
    │   └── review_sentiment.h5       # TensorFlow 2.15
    ├── tools/                        # Core analysis logic
    │   ├── __init__.py
    │   ├── mcp_swot.py               # Main 2000+ LoC
    │   └── data_connectors/          # Marketplace adapters
    │       ├── amazon_api.py         # SP-API wrapper
    │       └── shopify_scraper.py    # Playwright-based
    ├── pyproject.toml                # Poetry config
    ├── .python-version               # 3.12.1
    └── main.py                       # CLI interface

## 🌟 Key Features

### 1. AI-Powered SWOT Analysis
 - Claude 3 Integration


       from claude_handler import SWOTGenerator
                     
       swot = SWOTGenerator(api_key=os.getenv('CLAUDE_KEY'))
       analysis = swot.generate(
       product_data=product_json,
       language="en",  # 12 languages supported
       tone="professional"  # casual/professional
       )

### 2. Competitive Intelligence (MCP Inspector)
![deepseek_mermaid_20250514_77e174](https://github.com/user-attachments/assets/ddb231ae-b1f6-442c-9ed3-45a1a775b8d3)

