# Melp App REST API

Melp is a revolutionary application designed to provide users with relevant information about restaurants. This repository provides a REST API backend that supports CRUD operations for restaurant data and computes statistical data based on spatial queries.

## Prerequisites

- Python 3.x
- FastAPI
- Pydantic
- PostgreSQL (with PostGIS extension for spatial queries)
- Uvicorn (for running the FastAPI app)
- Heroku (for deployment)
- Postman (for testing the API)
- GitHub (code repository)

## Setup & Installation

1. Clone this repository:

git clone https://github.com/SantiagoNavarroLlaguno/rest-api-app

2. Navigate to the project directory:

cd melp_app

3. Install the required dependencies:

pip install -r requirements.txt

4. Ensure you have a running PostgreSQL instance with PostGIS extension and import the initial database schema and data using the provided SQL scripts.

5. Run the application:

uvicorn main:app --reload

## API Endpoints

1. **CRUD operations for Restaurants**
   - `GET /restaurants` - Retrieve a list of all restaurants.
   - `GET /restaurants/{restaurant_id}` - Retrieve details of a specific restaurant.
   - `POST /restaurants` - Add a new restaurant.
   - `PUT /restaurants/{restaurant_id}` - Update a restaurant's details.
   - `DELETE /restaurants/{restaurant_id}` - Delete a specific restaurant.

2. **Statistics Endpoint**
   - `GET /restaurants/statistics?latitude=x&longitude=y&radius=z` - Retrieve statistical data for restaurants within a specified radius of a given latitude and longitude.

## Testing

A Postman collection is provided for testing the API endpoints:

https://TBD

## Deployment

The application is deployed on Heroku. You can access the live API at:

https://TBD

## Bonus

- **Good use of Git**: Check the commit history for organized and meaningful commits.
- **API Documentation**: FastAPI provides automatic interactive API documentation. Visit `/docs` on the deployed application to access it.
- **HTTP Verbs**: This API adheres to the standards for HTTP verb usage.
- **Programming Practices**: The code is organized, modular, and follows PEP 8 style guidelines for Python.
