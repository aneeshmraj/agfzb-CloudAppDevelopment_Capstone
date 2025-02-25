import requests
import json
from .models import CarDealer, CarReview
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

NLU_API_KEY = os.getenv('NLU_API_KEY')

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, apikey=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if apikey:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs,
                                    auth=HTTPBasicAuth('apikey',apikey))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url,payload,**kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                    json=payload,params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,**kwargs)
    print(json_result)
    if json_result:
        # Get the row list in JSON as 
        if "rows" in json_result:
            dealers = json_result["rows"]            
            # For each dealer object
            for dealer in dealers:
                # Get its content in `doc` object
                dealer_doc = dealer["doc"]
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    dealer_id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
                results.append(dealer_obj)
        elif "docs" in json_result:
            dealers = json_result["docs"]
             # For each dealer object
            for dealer_doc in dealers:
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    dealer_id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
                results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    # - Call get_request() with specified arguments
    # - Parse JSON results into a DealerView object list
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,**kwargs)
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["docs"]
        # For each dealer object
        for review_doc in reviews:
            # Get its content in `doc` object
            #review_doc = review["doc"]
            # Create a CarDealer object with values in `doc` object
            
            review_obj = CarReview(name=review_doc["name"], 
                                   review=review_doc["review"],
                                   purchase=review_doc["purchase"],
                                   car_make=review_doc["car_make"],
                                   car_model=review_doc["car_model"], 
                                   car_year=review_doc["car_year"],
                                   dealer_id=review_doc["dealership"])# sentiment=review_doc["sentiment"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(analyze_text):
    # - Call get_request() with specified arguments
    # - Get the returned sentiment label such as Positive or Negative
    # params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    response = get_request('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/81538a51-8f40-47f9-a072-e0a8b411c35b/v1/analyze',
                            apikey=NLU_API_KEY,
                            text= analyze_text,
                            version='2021-08-01',
                            features= 'sentiment'
                           )
    if 'code' in response and response['code'] == 422:
        return 'neutral'
    else:
        return response["sentiment"]["document"]["label"]


