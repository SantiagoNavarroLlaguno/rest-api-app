-- Update the geom values using lat and lng
UPDATE Restaurants SET geom = ST_SetSRID(ST_MakePoint(lng, lat), 4326);

-- Create an index on the geom column for faster spatial queries
CREATE INDEX idx_restaurants_geom ON Restaurants USING gist(geom);
