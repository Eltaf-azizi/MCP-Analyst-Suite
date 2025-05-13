import os
import json
import requests



def test_api_endpoint():
    """
    Test the SWOT analysis API endpoint
    """
    # API endpoint
    api_url = "http://127.0.0.1:5000/analyze"


    # Product to test
    product_name = "iphone 15"

    print(f"Testing API for: {product_name}")

    try:
        # Make the API request
        response = requests.post(
            api_url,
            json = {"product_name": product_name},
            headers = {"Content-Type": "application/json"}
        )