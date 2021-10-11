#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.query import Query
from requests import ConnectionError, ReadTimeout, RequestException
import requests
import sys

def main(dict):
    print(dict)
    service = Cloudant.iam(None, dict["IAM_API_KEY"], url=dict["COUCH_URL"], connect=True)
    db = service['reviews']
    try:
        selector = {'dealership': {'$eq':int(dict["dealerId"])}}
        docs = db.get_query_result(selector)
        reviews = []
        for doc in docs:
            reviews.append(doc)
        return {"docs":reviews}
    except CloudantException as ce:
        print("Method failed")
        print(" - status code: " + str(ce.code))
        print(" - error message: " + ce.message)
    except ConnectionError as cerr:
        print("Connection error occurred:")
        print(cerr)
    except ReadTimeout as rt:
        # The server did not send any data in the allotted amount of time.
        print("Read timed out:")
        print(rt)
    except RequestException as re:
        # Handle other request failures
        print("Request Exception:")
        print(re)

#add review

def main1(dict):
    print(dict)
    service = Cloudant.iam(None, dict["IAM_API_KEY"], url=dict["COUCH_URL"], connect=True)
    db = service['reviews']
    try:        
        # Create a document using the Database API
        my_document = db.create_document(dict["review"])
        # Check that the document exists in the database
        if my_document.exists():
           return {"text": "Review successfully added."}
    
    except ConnectionError as cerr:
        print("Connection error occurred:")
        print(cerr)
    except ReadTimeout as rt:
        # The server did not send any data in the allotted amount of time.
        print("Read timed out:")
        print(rt)
    except RequestException as re:
        # Handle other request failures
        print("Request Exception:")
        print(re)
   
