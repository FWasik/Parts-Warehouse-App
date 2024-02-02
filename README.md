# Parts-Warehouse-App
 
The application was created as a recruitment task. The goal was to create a service, with any Python framework and database 
MongoDB, which would handle the basic functionality of the warehouse.
The application has two types of collections, such as "parts" and "categories." Both collections implement 
basic CRUD functionality. In addition, the application supports the part search function for the part collection as a separate endpoint. 
The application is also containerized using Docker.

As a Python framework, I chose the Django Rest Framework, for me the most familiar and best framework for creating RESTful APIs.
API. As a MongoDB connector, I used mongoengine.

## Table of contents
* [Requirements](#requirements)
* [Technologies](#technologies)
* [Installation](#installation)
* [Application](#application)

## Requirements
Part model:
- serial_number (str): A unique serial number assigned to each part. 
- name (str): The name or model of the part. 
- description (str): A brief description of the part.
- category (str): The category to which the part belongs (e.g., resistor, capacitor, IC). 
- quantity (int): The quantity of the part available in the warehouse.
- price (float): The price of a single unit of the part. 
- location (dict): A dictionary specifying the exact location of the part in the warehouse, including 
sections such as room, bookcase, shelf, cuvee, column, row.

Category model:
- name (str): The name of the category. 
- parent_name (str): If empty, this is a base category. This will be used to create a category tree

Because in NoSQL there are no standard primary key, I set fields like serial_number (for Part model) and
name (for Category model) as lookup_field in relevant endpoints.


1. Ensure that a part cannot be assigned to a base category. 
2. Ensure that a category cannot be removed if there are parts assigned to it. 
3. Ensure that a parent category cannot be removed if it has child categories with parts assigned. 
4. Implement input validation for both collections. 
5. Pay special atention to the 'location' field in the 'parts' dataset, which includes sections such as 
room, bookcase, shelf, cuvee, column, row.
6. Ensure that each part belongs to a category and that a part cannot be in a base category. 
7. Dockerize the application, ensuring that it can be easily deployed and run in a containerized 
environment. 
8. Ensure that the API returns results in JSON format and can be consumed with Postman. 

In addition, I added some additional rules for the application to maintain the consistency of collections in the application:

1. The base category cannot be assigned to an existing category (a problem with the "looping" of categories in the 
tree and difficulties in deletion.)
2. A category cannot be its parent
3. I assumed that in the location field (dictionary), the keys are the names of the locations, and the values represent
the number of parts in each location. Therefore, the sum of the values from the locations must be equal to the quantity.
4. When a category is updated, it is also updated in other categories and parts (just like a name update).
5. All children are also removed when deleting a specific category. (all down the category tree)
6. Unique names for categories

All requirements and rules have been met.


## Technologies
Most important technologies used:
- Python: 3.11.5
- Django: 4.1.13
- mongoengine: 0.27.0
- django-rest-framework-mongoengine: 3.4.1
- djangorestframework: 3.14.0
- pymongo: 3.12.1


## Installation:
To run the application, first of all, you need to pull the image from DockerHub. Run this command:
```
docker pull dilreni2137/parts-warehouse-app-web
```

Next, the container should be started. For security reasons, I have not included the .env file in the container. 
Therefore, they must be added directly in container startup command:
```
docker run -e DB_NAME=<your_db_name> -e DB_USERNAME=<your_username> -e DB_PASSWORD=<your_password> -e DB_HOST=<your_host> -p 8000:8000  dilreni2137/parts-warehouse-app-web
```

### !!! CORRECTION !!! (02.02.2024)

Probably, as I noticed, you can run the container without adding envs to the run command. In that case, use the 
following command. If there are problems, use the command with envs.

```
docker run -p 8000:8000 dilreni2137/parts-warehouse-app-web
```

## Application
### Endpoints
A available endpoints are:

For GET (all objects in collection), POST methods:
* http[]()://localhost:8000/api/warehouse/parts/
* http[]()://localhost:8000/api/warehouse/categories/

For GET (single object), DELETE, PATCH, PUT methods:
* http[]()://localhost:8000/api/warehouse/parts/<part_serial_number>/
* http[]()://localhost:8000/api/warehouse/categories/<category_name>/

For search endpoint there is one method allowed which is GET method:
* http[]()://localhost:8000/api/warehouse/parts-search/?<field_name>=<value_to_filter>

with any number of fields after which filtering will take place. They must be separated by "&" in endpoint.

### Input validation

The input validation for parts is:
- All fields are required. 
- The serial number must be unique.
- A category that does not exist in the database cannot be assigned.
- Quantity must not be less than 0.
- Price must not be less than 0.
- Cannot be assigned to a base category.
- The values in the location dictionary must not be less than 0.
- The location dictionary must have valid location names (room, rack, shelf, tray, column, row) as the key.
- The sum of the values in the location dictionary must be equal to the quantity.

Validation of input data for categories:
- Name must be unique.
- Parent must exist in the database.
- The category cannot be a parent category for itself.
- Base category cannot be assigned to an existing category (when updating).

Search endpoint filters parts based on the value for each field. String fields are filtered by containing a given phrase.
Numeric and dictionary fields are filtered by exact.

