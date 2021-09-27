from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='make')
    
    description = models.CharField(max_length=1000)
    
    def __init__(self, name, description):
        # name
        self.name = name
        # description
        self.description = description
        
    def __str__(self):
        return "Car Name: " + self.name + "," + \
               "Description: " + self.description




# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    CAR_TYPE = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON')
    ]
    name = models.CharField(null=False, max_length=30, default='model')
    year = models.DateField(null=True)
    dealer_id = models.IntegerField(default=0)
    car_type = models.CharField(max_length=5, choices=CAR_TYPE, default=SEDAN)
    make =  models.ForeignKey(CarMake, on_delete=models.CASCADE)
    
    def __init__(self, name, dealer_id, car_type, year):
        # name
        self.name = name
        # description
        self.dealer_id = dealer_id
        # type
        self.car_type = car_type
        #year
        self.year = year

        
    def __str__(self):
        return "Car model: " + self.name + "," + \
               "type:" + self.car_type + ","+ \
               "year" + self.year + "," + \
               "dealer" + self.dealer 



# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(models.Model):
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)
    long = models.CharField(max_length=100)
    short_name = models.CharField(null=False, max_length=30, default='short name')
    st = models.CharField(max_length=10)
    zip = models.CharField(max_length=20)
    dealer_id = models.IntegerField(default=0)

    def __init__(self, address, city, full_name, dealer_id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.dealer_id = dealer_id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
