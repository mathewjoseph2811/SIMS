# SIMS
Simple Inventory Management System using Django Rest Framework

A brief description of your application, its purpose, and what problem it solves.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)


## Features

- User authentication using JWT.
- CRUD operations for item/inventory management.
- Caching for improved performance.

## Technologies Used

- Django
- Django REST Framework
- Redis
- PostgreSQL
- JWT for authentication

## Installation

Follow these steps to set up the application locally:

1. **Clone the repository:**
   ```bash
   git clone git@github.com:mathewjoseph2811/SIMS.git
   cd SIMS
   
2. **Create a virtual environment:**

	python3 -m venv sims_env
	
	source venv/bin/activate
	
	pip install -r requirements.txt
	
	requirements.txt included in the project directory
	
3. **Create database/ migrating tables:**

	You can create a database using : createdb -U admin -h localhost sims_db
	
	Migrate all tables to the database using:
	
	python manage.py makemigrations
	python manage.py migrate
	
	
	create super user using:
	
	python manage.py createsuperuser
	
	Note: you can also populate the sample database usign sql query attached in the project directory
	
**Run the development server:**

	python manage.py runserver



**Login**
	Endpoint: /token/
	Method: POST
	Sample Login Raw Data:
	
		{
		  "username": "admin",
		  "password": "123456"
		}
	
	Response:
		
		{
		  "refresh": "refresh_token",
		  "access": "access_token"
		}
		
## API Documentation		
**headers for authentication** (Authentication required for all CRUD operations)
Headers:
	http

	Authorization: Bearer your_access_token
	
**Create an Item**

Endpoint: /item/
Method: POST
Sample Request Body:
json

	{
	  "vchr_item_code": "ITEM1",
	  "vchr_item_name": "test item",
	  "txt_description": "test",
	  "dbl_price": "3",
	  "int_quantity": "1"
	}
	
**Update an Item**

Endpoint: /item/{id}/
Method: PUT
Sample Request Body:
json

	{
	  "vchr_item_code": "ITEM1",
	  "vchr_item_name": "test item",
	  "txt_description": "test",
	  "dbl_price": "3",
	  "int_quantity": "1"
	}
	
**View an Item**

Endpoint: /item/{id}/
Method: GET



**Delete an Item**

Endpoint: /item/{id}/
Method: DELETE



##Examples
**Example: Create an Item**

	curl -X POST "http://localhost:8000/item/" \
	-H "Authorization: Bearer your_access_token" \
	-H "Content-Type: application/json" \
	-d '{
	  "vchr_item_code": "ITEM1",
	  "vchr_item_name": "test item",
	  "txt_description": "test",
	  "dbl_price": "3",
	  "int_quantity": "1"
	}'


**Example: Update an Item**

	curl -X PUT "http://localhost:8000/item/1/" \
	-H "Authorization: Bearer your_access_token" \
	-H "Content-Type: application/json" \
	-d '{
	  "vchr_item_code": "ITEM1",
	  "vchr_item_name": "updated item",
	  "txt_description": "updated test",
	  "dbl_price": "5",
	  "int_quantity": "2"
	}'
	
	
**Example: Delete an Item**

	curl -X DELETE "http://localhost:8000/item/1/" -H "Authorization: Bearer your_access_token"
	
	
**Example: View an Item**

	curl -X GET "http://localhost:8000/item/1/" -H "Authorization: Bearer your_access_token"

