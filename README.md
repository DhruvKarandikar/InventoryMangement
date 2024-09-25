This is an backend of inventory Management  where a product can be interacted along with the features of having the End to end user Authentication.
There are User services and Inventory services overall 5 API are made to interact with the database.

As the Databse Postgresql is used and please make sure you have hardcoded you own values of database name and password

For running the project make an python env file to have all the library used to in the project 
- python3 -m venv env
- python -m venv env
 
For activating the env file use:
- terminal - .\env\Scripts\activate
- unix or OS - use source to connect

Installing the libraries useafter activating the environment:
- pip install -r requirements.txt

After connecting to the postgresqldatabase and hardciding the database name and password
to migrate into the database
-python manage.py migrate 

run command to run server
-python manage.py runserver


API are UI are handled on the swagger settings:
go the url: /v1/inventory_management/swagger

On postman: to interact on with API swagger is not needed 
/v1/inventory_management/api_name

Interact with the API: 5 API 
signup an user and then login a user to have the access token 
pass the access token value with Bearer <space> <accesstoken> into the swagger setting locked icon to interact with inventory management API 


Features:
-End to end JWT Token authentication
-swagger settings for UI purpose
-Generic API functions made to ease in creating the API 

