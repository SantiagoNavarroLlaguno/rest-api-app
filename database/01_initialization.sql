DROP TABLE IF EXISTS Restaurants;

CREATE TABLE Restaurants (
    id TEXT PRIMARY KEY,       -- Unique Identifier of Restaurant
    rating INTEGER CHECK (rating >= 0 AND rating <= 4),  -- Number between 0 and 4
    name TEXT,                 -- Name of the restaurant
    site TEXT,                 -- Url of the restaurant
    email TEXT,
    phone TEXT,
    street TEXT,
    city TEXT,
    state TEXT,
    lat FLOAT,                 -- Latitude
    lng FLOAT                  -- Longitude
);

ALTER TABLE Restaurants ADD COLUMN geom geography(POINT, 4326);

-- NOTE: After running this script, run the '02_importdata.sql' script to import data from the provided CSV file.
