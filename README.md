# cs699_project
Python webscraping and result posted in website


1. Using FastApi for exposing an API throuhg which the data in postgres can be accessed by the static website
2. Using FastApi static files to host the static website and using the javascript in the html to access the data in postgresql using the exposed api.

# code to start the fast api server
    uvicorn apis:app --reload