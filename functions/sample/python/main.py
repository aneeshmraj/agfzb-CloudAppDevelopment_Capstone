#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from requests import ConnectionError, ReadTimeout, RequestException, ValueError
import requests


def getAllReviewsForDealership(dict,dealerId):   

    authenticator = IAMAuthenticator(dict["COUCH_URL"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(dict["IAM_API_KEY"])

    try:
        # Invoke a Cloudant method request
        response = service.post_search(
                                        db='reviews',
                                        query='dealership:'+dealerId
                                        ).get_result()

        return response
    
    except ApiException as ae:
        print("Method failed")
        print(" - status code: " + str(ae.code))
        print(" - error message: " + ae.message)
    if ("reason" in ae.http_response.json()):
        print(" - reason: " + ae.http_response.json()["reason"])
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
    except ValueError as ve:
        print("Invalid argument value:\n" + ve.message)


def postReviewForDealership(dict,review):   

    authenticator = IAMAuthenticator(dict["COUCH_URL"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(dict["IAM_API_KEY"])
    review = review["review"]
    add_review = Document(
                    id=review["id"],
                    name=review["name"],
                    dealership=review["dealership"],
                    review=review["review"],
                    purchase=review["purchase"],
                    another=review["another"],
                    purchase_date=review["purchase_date"],
                    car_make=review["car_make"],
                    car_model=review["car_model"],
                    car_year=review["car_year"])

    try:        

        response = service.post_document(db='reviews',
                                         document=add_review).get_result()

        return response
    
    except ApiException as ae:
        print("Method failed")
        print(" - status code: " + str(ae.code))
        print(" - error message: " + ae.message)
    if ("reason" in ae.http_response.json()):
        print(" - reason: " + ae.http_response.json()["reason"])
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
    except ValueError as ve:
        print("Invalid argument value:\n" + ve.message)