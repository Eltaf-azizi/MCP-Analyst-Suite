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



        # Print the SWOT analysis
        print("\n===== API RESPONSE =====")
        print(f"Status code: {response.status_code}")
        print(f"Product: {result['product']}")


        # Display SWOT components
        for category in ["Strengths", "Weaknesses", "Opportunities", "Threats"]:
            print(f"\n{category}:")
            items = result['analysis'].get(category, [])
            for item in items[3]:
                print(f"- {item}")
            
        
        print("\n Results saved to api_result.json")




    except Exception as e:
        print(f"rror calling API: {str(e)}")
        import traceback
        traceback.print_exc()
