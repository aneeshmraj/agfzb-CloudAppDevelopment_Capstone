from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django import forms
import logging
import json
import os
from dotenv import load_dotenv

load_dotenv()

COUCH_URL = os.getenv('COUCH_URL')
IAM_API_KEY = os.getenv('IAM_API_KEY')
NLU_API_KEY = os.getenv('NLU_API_KEY')
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
# Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}    
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            # redirect to course list page
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/aneeshmraj%40yahoo.com_djangoserver-space/dealer/dealer-get.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url,
         COUCH_URL=COUCH_URL,
         IAM_API_KEY=IAM_API_KEY
         )
        context["dealership_list"] = dealerships
        # Return a list of dealers as context
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context={}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/aneeshmraj%40yahoo.com_djangoserver-space/reviews/review-get.json"
        # Get dealers from the URL
        review_details = get_dealer_reviews_from_cf(url,
         COUCH_URL=COUCH_URL,
         IAM_API_KEY=IAM_API_KEY,
         dealerId = dealer_id
         )
        context["reviews_list"] = review_details
        # Concat all reviews        
        return render(request,'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    print("Received:",  request.method )
    if request.method == "POST":
        print("recevied POST")
        form = forms.Form(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            review = dict()
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["review"] = form.cleaned_data['content']
            review["name"] = user.first_name + ' ' + user.last_name
            review["purchase"] = form.cleaned_data['purchasecheck']
            selected_car = form.cleaned_data['car']
            car_models=CarModel.objects.filter(dealer_id=dealer_id)
            car = car_models[selected_car-1]
            print(car)
            review["car_make"] = select_data[0]
            review["car_model"]= select_data[1]
            review["car_year"]= select_data[2]
            review["purchase_date"]=  form.cleaned_data['purchasedate']
            json_payload = dict()
            json_payload["review"] = review
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/aneeshmraj%40yahoo.com_djangoserver-space/reviews/add-review.json"
            response = post_request(url,
                                    json_payload,
                                    COUCH_URL=COUCH_URL,
                                    IAM_API_KEY=IAM_API_KEY)     
        
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    elif request.method == "GET":
        cars = []
        context={}
        context["dealer_id"]=dealer_id
        car_models=CarModel.objects.filter(dealer_id=dealer_id)
        context["cars"]=car_models      
        return render(request,'djangoapp/add_review.html', context)
    else:
        return HTTPResponse("Unsupported request type")

