\COPY Restaurants(id, rating, name, site, email, phone, street, city, state, lat, lng) FROM 'C:\Users\SNL\projects\melp_app\data\restaurantes.csv' WITH CSV HEADER;

-- NOTE: Ensure the path above points to the location of your CSV file. Adjust if necessary.
-- NOTE: After running this script, run the '03_optimization.sql' script to optimize the database for spatial queries.
