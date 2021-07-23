from fastapi import FastAPI
from fastapi import Query       # used to add more details to the query parameters
from fastapi import Path        # used to add more details to the path parameters
from typing import Optional
from fastapi.exceptions import HTTPException     # used to make a query parameter as optional 
from pydantic import BaseModel  # used with the Post method 
app = FastAPI()

'''
Endpoint: An API endpoint is the point of entry in communication channel when two systems are interacting. 
It refers to touchpoints of the communication between an API and a server. 
'''

# Normal Path/Endpoint Example  ======================================================================
@app.get("/")
def home():
    data = {
        "message" : "Hello !!!"
    }
    return data

@app.get("/about")
def about():
    data = {
        "Name" : "Abhishek",
        "Organization" : "CDAC"
    }
    return data



# Path/Endpoint with Parameters Example ======================================================================
car_inventory = {
    1: {
        "name" : "Nexon",
        "company" : "Tata",
        "price" : "12L"
    },
    2: {
        "name" : "Scorpio",
        "company" : "Mahindra",
        "price" : "15L"
    },
    3: {
        "name" : "Creta",
        "company" : "Hyundai",
        "price" : "14L"
    }
}

'''
# Basic example
@app.get("/get-car/{car_id}")
def get_car(car_id: int):
    return car_inventory[car_id]
'''


'''
#Adding more details to path parameters eg. hints/descriptions

@app.get("/get-car/{car_id}")
def get_car(car_id: int = Path(None, description = "The ID of the Car you would like to view")): # Path(default-value, other_parameters)
    return car_inventory[car_id]
'''

#Adding more details to path parameters eg. hints/descriptions
#Adding some constraints to the path parameters say ID should be greater than or less than to some value
@app.get("/get-car/{car_id}")
def get_car(car_id: int = Path(None, description = "The ID of the Car you would like to view", gt = 0, le = 3)): # gt = greater than; lt = less than; le = less than or equals; ge = greater than or equals
    return car_inventory[car_id]



# QUERY PARAMETERS ==============================================================================================
''' 
comes after a question mark (?) sign in URLs usually
eg: "facebook.com/home?redirect=/abhishek&msg=fail"
above example has two query parameters --> redirect and msg
'''


'''
#Basic example : here name parameter is required*
@app.get("/get-car-by-name")
def get_car_by_name(name : str):  

    for item_id in car_inventory:
        if car_inventory[item_id]["name"] == name:
            return car_inventory[item_id]
    return {"Data" : "Not Found !!"}
# access this endpoint like this: 127.0.0.1:8000/get-car-by-name?name=Creta
'''

'''
#Basic example : here [name] parameter is optional
@app.get("/get-car-by-name")
def get_car_by_name(name : str = None):  #added a default value to make it optional

    for item_id in car_inventory:
        if car_inventory[item_id]["name"] == name:
            return car_inventory[item_id]
    return {"Data" : "Not Found !!"}
# access this endpoint like this: 127.0.0.1:8000/get-car-by-name
'''

'''
#Basic example: recommended way of making a parameter as optional as per the FastAPI docs
@app.get("/get-car-by-name")
def get_car_by_name(name : Optional[str] = None):  # this is useful to give better auto-completion for the FastAPI auto documentation feature

    for item_id in car_inventory:
        if car_inventory[item_id]["name"] == name:
            return car_inventory[item_id]
    return {"Data" : "Not Found !!"}
# access this endpoint like this: 127.0.0.1:8000/get-car-by-name?name=Creta
'''

'''
#Basic example: using required* and optional* parameters together   [WRONG - Way]
@app.get("/get-car-by-name")
def get_car_by_name(name : Optional[str] = None, test: int):  #test is just a random parameter taken for example
    # above line will give an error like this : Non-default argument follows default argument (Pylance)
    # because the require parameter [test] is placed after optional parameter [name]
    # for FastAPI it is fine
    # but Python generates an error like this: Non-default argument follows default argument (Pylance)

    for item_id in car_inventory:
        if car_inventory[item_id]["name"] == name:
            return car_inventory[item_id]
    return {"Data" : "Not Found !!"}
# access this endpoint like this: 127.0.0.1:8000/get-car-by-name?name=Creta&test=1
'''
'''
#Basic example: using required* and optional* parameters together   [Correct - Way]
@app.get("/get-car-by-name")
def get_car_by_name(*, name : Optional[str] = None, test: int):  #test is just a random parameter taken for example
    # we can add an asterisk [*] at the very beginning during function definition like above line to resolve positional parameter error
    # otherwise we have to change the positions of parameters such that
    # required parameters should appear before the optional parameters in the function definition
    # i.e like this -->  def get_car_by_name(test: int, name : Optional[str] = None):

    for item_id in car_inventory:
        if car_inventory[item_id]["name"] == name:
            return car_inventory[item_id]
    return {"Data" : "Not Found !!"}
# access this endpoint like this: 127.0.0.1:8000/get-car-by-name?name=Creta&test=1
'''

'''
# Combining PATH parameters and QUERY parameters together =====================================================
@app.get("/get-car-by-name/{car_id}")
def get_car_by_name(*, car_id: int, name : Optional[str] = None, test: int):  #test is just a random parameter taken for example
    # we can add an asterisk [*] at the very beginning during function definition like above line to resolve positional parameter error
    # otherwise we have to change the positions of parameters such that
    # required parameters should appear before the optional parameters in the function definition
    # i.e like this -->  def get_car_by_name(test: int, name : Optional[str] = None):

    for item_id in car_inventory:
        if car_inventory[item_id]["name"] == name:
            return car_inventory[item_id]
    return {"Data" : "Not Found !!"}
# access this endpoint like this: http://127.0.0.1:8000/get-car-by-name/1?test=1&name=Scorpio
'''




# ==========================================
# REQUEST BODY : POST method Examples
# ==========================================


# we can create a model like this to store data efficiently
class Car (BaseModel):
    name: str
    company: str
    price: Optional[str] = None

cars_data = {}

@app.post("/create-item/{item_id}")
def create_item (item_id: int, item: Car):
    if item_id in cars_data:
        return {"Error" : "Item ID already exists !!"}

    cars_data[item_id] = item

    return cars_data[item_id]

@app.get("/get-car-by-name")
def get_car_by_name(name : str):  

    for item_id in cars_data:
        if cars_data[item_id].name == name:
            return cars_data[item_id]
    return {"Data" : "Not Found !!"}




# ==========================================
# UPDATE operation : PUT method Example
# ==========================================


#
class UpdateCar (BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    price: Optional[str] = None


@app.put("/update_item/{item_id}")
def update_item (item_id: int, item: UpdateCar):

    if item_id not in cars_data:
        return {"Error": "Item ID does not exists."}
    if item.name != None:
        cars_data[item_id].name = item.name 

    if item.company != None:
        cars_data[item_id].company = item.company 

    if item.price != None:
        cars_data[item_id].price = item.price 

    return cars_data[item_id]




# ==========================================
# DELETE operation : DELETE method Example
# ==========================================

#deleting an item by taking query parameter
@app.delete("/delete_item")
def delete_item(item_id: int = Query(..., description = "The ID of the item to delete")):
    if item_id not in cars_data:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")

    del cars_data[item_id]

    return {"Success" : "Item deleted !!"}