-- Create table for User
CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create table for Host
CREATE TABLE Host (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id)
);

-- Create table for Guest
CREATE TABLE Guest (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id)
);

-- Create table for Place
CREATE TABLE Place (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    address VARCHAR(255),
    city_id INT NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    number_of_rooms INT,
    number_of_bathrooms INT,
    price_per_night FLOAT,
    max_guests INT,
    host_id INT NOT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES City(id),
    FOREIGN KEY (host_id) REFERENCES Host(id)
);

-- Create table for Amenities
CREATE TABLE Amenities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    place_id INT NOT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES Place(id)
);

-- Create table for Country
CREATE TABLE Country (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create table for State
CREATE TABLE State (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country_id INT NOT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (country_id) REFERENCES Country(id)
);

-- Create table for City
CREATE TABLE City (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    state_id INT NOT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (state_id) REFERENCES State(id)
);

-- Create table for Review
CREATE TABLE Review (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    place_id INT NOT NULL,
    feedback TEXT,
    rating INT,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (place_id) REFERENCES Place(id)
);

-- SQL script to insert initial data


-- Insert initial data for Country
INSERT INTO Country (name) VALUES ('USA'), ('Canada');

-- Insert initial data for State
INSERT INTO State (name, country_id) VALUES ('California', 1), ('New York', 1), ('Ontario', 2);

-- Insert initial data for City
INSERT INTO City (name, state_id) VALUES ('San Francisco', 1), ('Los Angeles', 1), ('Toronto', 3);

-- Insert initial data for User
INSERT INTO User (first_name, last_name, email, password) VALUES 
('John', 'Doe', 'john.doe@example.com', 'password123'),
('Jane', 'Smith', 'jane.smith@example.com', 'password123');

-- Insert initial data for Host
INSERT INTO Host (user_id) VALUES (1), (2);

-- Insert initial data for Place
INSERT INTO Place (name, description, address, city_id, latitude, longitude, number_of_rooms, number_of_bathrooms, price_per_night, max_guests, host_id) VALUES 
('Cozy Cottage', 'A cozy cottage in the countryside', '123 Country Lane', 1, 37.7749, -122.4194, 3, 2, 100.00, 4, 1),
('Urban Apartment', 'A modern apartment in the city', '456 Urban Road', 2, 34.0522, -118.2437, 2, 1, 150.00, 2, 2);

-- Insert initial data for Amenities
INSERT INTO Amenities (name, place_id) VALUES 
('WiFi', 1),
('Pool', 1),
('Parking', 2);

-- Insert initial data for Review
INSERT INTO Review (user_id, place_id, feedback, rating) VALUES 
(1, 1, 'Great place, very cozy!', 5),
(2, 2, 'Modern and clean, loved it!', 4);
