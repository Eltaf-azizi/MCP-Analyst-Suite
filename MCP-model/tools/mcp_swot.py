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
        

        # Check if successful
        response.raise_for_status()


        # Parse the json response
        result = response.json()


        # Save result to a file (excluding the chart which can be large)
        result_copy = result.copy()
        
        if 'chart' in result_copy:
            result_copy['chart'] = "<<base64 image data removed for display>>"


        with open('api_result.json', 'w') as f:
            json.dump(result_copy, f, indent=2)

