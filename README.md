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

### 3. Dynamic PDF Reporting  
- **Output Formats**: PDF/A-3, PDF/UA  
- **Resolution**: 300 DPI (print-ready)  
- **Color Profiles**: CMYK, Pantone support  
- **Security**: Password protection, Watermarking  


## 🚀 Installation
### System Requirements

 - Minimum: 4 vCPU, 8GB RAM, 10GB SSD

 - Recommended: 8 vCPU, 16GB RAM, NVMe storage


       # With Poetry (recommended)
       poetry install --with prod, dev
       
       # With pip
       pip install -r requirements/production.txt



## ⚙️ Configuration
### Environment Variables

       # .env.production
       CLAUDE_API_KEY=sk-ant-prod-abc123
       MCP_API_ENDPOINT=https://api.mcp-inspector.com/v3
       PDF_COMPRESSION_LEVEL=6  # 0-9

## YAML Configuration

       # config/analysis.yaml
       analysis:
         depth: extended
         markets: ["amazon_us", "shopify"]
         risk_factors:  
           - price_volatility
           - review_velocity
       
       pdf:
         branding:
           logo_url: "https://yourdomain.com/logo.png"
           primary_color: "#3a86ff"


## 📊 Sample Report Structure

       1. EXECUTIVE SUMMARY
          - Product Rating: 4.7/5 (Top 15%)
          - Price Competitiveness: 8.2/10
       
       2. SWOT MATRIX
          [Strengths]
          - 30% faster shipping than competitors
          - Verified authenticity badge
       
          [Opportunities]  
          - Untapped German market (25% price premium)
       
       3. RECOMMENDATIONS
          - Bundle with complementary products (+12% conversion)
          - Optimize for "giftable" keywords

## � Testing & Validation
### Test Coverage

| MODULE         | UNIT TESTS | INTEGRATION | LOAD TEST    |
|----------------|------------|-------------|--------------|
| `mcp_swot.py`  | 89%        | 72%         | 100 RPS      |
| `pdf_reports/` | 100%       | N/A         | 50 PDFs/min  |

       # Run full test suite
       pytest --cov=app --cov=tools --cov-report=html


## 🙌 Contributing
Found a bug? Want to add a feature? Contributions are welcome!

1. Fork the repository.
2. Create a new branch.
3. Submit a pull request with your improvements.


<h3 align="center">Happy Coding!</h3>
