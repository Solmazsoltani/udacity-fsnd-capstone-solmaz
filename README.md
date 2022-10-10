# Sells Agency Project
Udacity Full-Stack Web Developer Nanodegree Program Capstone Project

## Project Motivation
The Sells Agency Project models a company that is responsible for creating Autos and managing and assigning Buyers to those Autos. You are an Executive Producer within the company and are creating a system to simplify and streamline your process. 


This project is simply a workspace for practicing and showcasing different set of skills related with web development. These include data modelling, API design, authentication and authorization and cloud deployment.

## Getting Started

The project adheres to the PEP 8 style guide and follows common best practices, including:

* Variable and function names are clear.
* Endpoints are logically named.
* Code is commented appropriately.
* Secrets are stored as environment variables.


### Key Dependencies & Platforms

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [Auth0](https://auth0.com/docs/) is the authentication and authorization system we'll use to handle users with different roles with more secure and easy ways

- [PostgreSQL](https://www.postgresql.org/) this project is integrated with a popular relational database PostgreSQL, though other relational databases can be used with a little effort.

- [Heroku](https://www.heroku.com/what) is the cloud platform used for deployment


### Running Locally

#### Installing Dependencies

##### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Once you have your virtual environment setup and running, install dependencies by running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Database Setup
With Postgres running, restore a database using the `capstone.psql` file provided. In terminal run:

``` CLI ``` you should be in the Directory of your psql file for example cd C:\Users\nx018125\Documents\GitHub\udacity-fsnd-capstone-solmaz

in CLI should be written :

     psql -U postgres


create database  is a command line utility which you can run from bash and not from psql. To create a database from psql, use the create database statement like so:

create database [databasename];
Note: be sure to always end your SQL statements with ;


create database [databasename];


create database capstone;

then u should come out by crt + c

then open CLI and 
you should be in the Directory of your psql file for example cd C:\Users\nx018125\Documents\GitHub\udacity-fsnd-capstone-solmaz

psql capstone < capstone.psql postgres


#### Running Tests

To run the tests, run
```bash
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone.psql
python test_app.py
```

Optionally, you can use `run_test.sh` script.

#### Auth0 Setup

You need to setup an Auth0 account.

Environment variables needed: (setup.sh)

```bash
export AUTH0_DOMAIN="xxxxxxxxxx.auth0.com" # Choose your tenant domain
export ALGORITHMS="RS256"
export API_AUDIENCE="capstone" # Create an API in Auth0
```

##### Roles

Create three roles for users under `Users & Roles` section in Auth0

* Sell Assistant
	* Can view Autos and Auto Buyers
* Sell Manager
	* All permissions a Sell Assistant has and…
	* Add or delete an Buyer from the database
	* Modify Buyers or Autos
* Executive Producer
	* All permissions a Sell Manager has and…
	* Add or delete a Car from the database

##### Permissions

Following permissions should be created under created API settings.

* `view:Buyers`
* `view:Autos`
* `delete:Buyers`
* `post:Buyers`
* `update:Buyers`
* `update:Autos`
* `post:Autos`
* `delete:Autos`

##### Set JWT Tokens in `auth_config.json`

Use the following link to create users and sign them in. This way, you can generate 

```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```

#### Launching The App

1. Initialize and activate a virtualenv:

   ```
   py -m venv env
   .\env\Scripts\activate
   
   ```

2. Install the dependencies:

    ```
    pip install -r requirements.txt
    ```
3. Configure database path to connect local postgres database in `models.py`

    ```python
    database_path = "postgres://{}/{}".format('localhost:5432', 'capstone')
    ```
**Note:** For default postgres installation, default user name is `postgres` with no password. Thus, no need to speficify them in database path. You can also omit host and post (localhost:5432). But if you need, you can use this template:

```
postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
```
For more details [look at the documentation (31.1.1.2. Connection URIs)](https://www.postgresql.org/docs/9.3/libpq-connect.html)

4. Setup the environment variables for Auth0 under `setup.sh` running:
	```bash
	source ./setup.sh 
	```
5.  To run the server locally, execute:

    ```bash
    export FLASK_APP=flaskr
    export FLASK_DEBUG=True
    export FLASK_ENVIRONMENT=debug
    flask run --reload
    ```

    Optionally, you can use `run.sh` script.

## API Documentation

### Models
There are two models:
* Auto
	* name
	* produce_date
* Buyer
	* name
	* age
	* gender

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 422: Not Processable 
- 500: Internal Server Error

### Endpoints


#### GET /Autos 
* Get all Autoss

* Require `view:Autos` permission

* **Example Request:** `curl 'http://localhost:5000/Autos'`

* **Expected Result:**
    ```json
	{
		"Autos": [
			{
			"Buyers": [
				{
				"age": 54,
				"gender": "M",
				"id": 1,
				"Auto_id": 2,
				"name": "Tom Hanks"
				},
				{
				"age": 45,
				"gender": "M",
				"id": 4,
				"Auto_id": 2,
				"name": "Robert Downey, Jr."
				},
				{
				"age": 45,
				"gender": "F",
				"id": 5,
				"Auto_id": 2,
				"name": "Julia Roberts"
				}
			],
			"id": 2,
			"release_date": "Fri, 04 May 2012 00:00:00 GMT",
			"title": "Yahşi Batı"
			},
			...
		],
		"success": true
    }
    ```
	
#### GET /Buyers 
* Get all Buyers

* Requires `view:Buyers` permission

* **Example Request:** `curl 'http://localhost:5000/Buyers'`

* **Expected Result:**
    ```json
	{
		"Buyers": [
			{
			"age": 45,
			"gender": "M",
			"id": 6,
			"Auto_id": 1,
			"name": "Cem Yılmaz"
			},
			{
			"age": 54,
			"gender": "M",
			"id": 1,
			"Auto_id": 2,
			"name": "Tom Hanks"
			},
			{
			"age": 44,
			"gender": "M",
			"id": 2,
			"Auto_id": 3,
			"name": "Brad Pitt"
			}
		],
		"success": true
	}
	```
	
#### POST /Autos
* Creates a new Auto.

* Requires `post:Autos` permission

* Requires the title and release date.

* **Example Request:** (Create)
    ```bash
	curl --location --request POST 'http://localhost:5000/Autos' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"title": "Pek Yakında",
			"release_date": "19-02-2020"
		}'
    ```
    
* **Example Response:**
    ```bash
	{
		"success": true
	}
    ```

#### POST /Buyers
* Creates a new Buyer.

* Requires `post:Buyers` permission

* Requires the name, age and gender of the Buyer.

* **Example Request:** (Create)
    ```json
	curl --location --request POST 'http://localhost:5000/Buyers' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"name": "Cem Yılmaz",
			"age": "45",
			"gender": "M"
        }'
    ```
    
* **Example Response:**
    ```json
	{
		"success": true
    }
    ```

#### DELETE /Autos/<int:Auto_id>
* Deletes the Auto with given id 

* Require `delete:Autos` permission

* **Example Request:** `curl --request DELETE 'http://localhost:5000/Autos/1'`

* **Example Response:**
    ```json
	{
		"deleted": 1,
		"success": true
    }
    ```
    
#### DELETE /Buyers/<int:Buyer_id>
* Deletes the Buyer with given id 

* Require `delete:Buyers` permission

* **Example Request:** `curl --request DELETE 'http://localhost:5000/Buyers/1'`

* **Example Response:**
    ```json
	{
		"deleted": 1,
		"success": true
    }
    ```

#### PATCH /Autos/<Auto_id>
* Updates the Auto where <Auto_id> is the existing Auto id

* Require `update:Autos` permission

* Responds with a 404 error if <Auto_id> is not found

* Update the corresponding fields for Auto with id <Auto_id>

* **Example Request:** 
	```json
    curl --location --request PATCH 'http://localhost:5000/Autos/1' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"title": "Eyvah eyvah 2"
        }'
  ```
  
* **Example Response:**
    ```json
	{
		"success": true, 
		"updated": {
			"id": 1, 
			"release_date": "Wed, 04 May 2016 00:00:00 GMT", 
			"title": "Eyvah eyvah 2"
		}
    }
    ```
	
#### PATCH /Buyers/<Buyer_id>
* Updates the Buyer where <Buyer_id> is the existing Buyer id

* Require `update:Buyers`

* Responds with a 404 error if <Buyer_id> is not found

* Update the given fields for Buyer with id <Buyer_id>

* **Example Request:** 
	```json
    curl --location --request PATCH 'http://localhost:5000/Buyers/1' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"name": "Tom Hanks"
        }'
  ```
  
* **Example Response:**
    ```json
	{
		"success": true, 
		"updated": {
			"age": 54, 
			"gender": "M", 
			"id": 1, 
			"name": "Tom Hanks"
		}
	}
	```
