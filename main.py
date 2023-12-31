from fastapi import FastAPI, HTTPException
from typing import List, Optional
import psycopg2
from pydantic import BaseModel
from typing import Tuple
import os

app = FastAPI()

DATABASE_URL = os.environ.get('DATABASE_URL', "postgresql://postgres:admin@localhost:5432/melp_db")


class Restaurant(BaseModel):
    id: str
    rating: int
    name: str
    site: str
    email: str
    phone: str
    street: str
    city: str
    state: str
    lat: float
    lng: float


class RestaurantStatistics(BaseModel):
    count: int
    avg: float
    std: float


@app.get("/")
def root():
    return {"Dear EDT Team": "Welcome to the Melp API!"}


@app.get("/restaurants/", response_model=List[Restaurant])
def read_restaurants():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Restaurants;")
            rows = cur.fetchall()
            return [Restaurant(id=row[0], rating=row[1], name=row[2], site=row[3], email=row[4], phone=row[5], 
                               street=row[6], city=row[7], state=row[8], lat=row[9], lng=row[10]) for row in rows]


@app.get("/restaurants/{restaurant_id}", response_model=Restaurant)
def read_restaurant(restaurant_id: str):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Restaurants WHERE id = %s;", (restaurant_id,))
            row = cur.fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="Restaurant not found")
            return Restaurant(id=row[0], rating=row[1], name=row[2], site=row[3], email=row[4], phone=row[5], 
                              street=row[6], city=row[7], state=row[8], lat=row[9], lng=row[10])


@app.post("/restaurants/", response_model=Restaurant)
def create_restaurant(restaurant: Restaurant):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO Restaurants (id, rating, name, site, email, phone, street, city, state, lat, lng) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                (restaurant.id, restaurant.rating, restaurant.name, restaurant.site, restaurant.email, restaurant.phone, 
                 restaurant.street, restaurant.city, restaurant.state, restaurant.lat, restaurant.lng)
            )
            conn.commit()
            return restaurant


@app.put("/restaurants/{restaurant_id}", response_model=Restaurant)
def update_restaurant(restaurant_id: str, restaurant: Restaurant):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE Restaurants 
                SET rating = %s, name = %s, site = %s, email = %s, phone = %s, 
                    street = %s, city = %s, state = %s, lat = %s, lng = %s 
                WHERE id = %s
                RETURNING id;
                """,
                (restaurant.rating, restaurant.name, restaurant.site, restaurant.email, restaurant.phone, 
                 restaurant.street, restaurant.city, restaurant.state, restaurant.lat, restaurant.lng, restaurant_id)
            )
            updated_row = cur.fetchone()
            if updated_row is None:
                raise HTTPException(status_code=404, detail="Restaurant not found")
            return restaurant


@app.delete("/restaurants/{restaurant_id}", response_model=dict)
def delete_restaurant(restaurant_id: str):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Restaurants WHERE id = %s RETURNING id;", (restaurant_id,))
            deleted_row = cur.fetchone()
            if deleted_row is None:
                raise HTTPException(status_code=404, detail="Restaurant not found")
            return {"status": "Restaurant deleted successfully"}


@app.get("/restaurants/statistics/")
def get_statistics(latitude: float, longitude: float, radius: float):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            # Find restaurants within the specified radius
            query = """
            SELECT 
                COUNT(*), 
                AVG(rating), 
                STDDEV(rating)
            FROM 
                Restaurants 
            WHERE 
                ST_DWithin(geom, ST_MakePoint(%s, %s)::geography, %s);
            """
            cur.execute(query, (longitude, latitude, radius))
            result = cur.fetchone()
            count, avg, std = result

            # Return results in the required JSON format
            return {
                "count": count,
                "avg": float(avg) if avg is not None else None,
                "std": float(std) if std is not None else None
            }
        

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
