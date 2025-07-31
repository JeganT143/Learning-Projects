-- Create table
CREATE TABLE pets (
pet_id SERIAL PRIMARY KEY,
name VARCHAR(50) NOT NULL,
species VARCHAR(30) NOT NULL,
magical_power VARCHAR(100),
age INTEGER,
price DECIMAL(8,2),
is_available BOOLEAN DEFAULT TRUE
);

-- Add data 
INSERT INTO 
pets(name, species, magical_power, age, price, is_available )
VALUES('Sparkles','Unicorn','Healing magic','150','1000.00',TRUE);

SELECT * FROM pets;

-- Adding more pets
INSERT INTO pets (name, species, magical_power, age, price, is_available)
VALUES
('Flamewings', 'Dragon', 'Fire breathing', 200 , 5000.00, TRUE),
('Whiskers','Cat', 'Invisibility', 3 , 50.00, TRUE),
('Hooty', 'Owl', 'Wisdom spells', 25, 150, FALSE ),
('Splash', 'Mermaid', 'Water Control', 18, 800, TRUE);

-- see all pets
SELECT * FROM pets;

-- See only names and species
SELECT name, species FROM pets;

-- See pets that cost less then 200
SELECT name, species, price
FROM pets
WHERE price < 200 ;

-- See available pets only

SELECT name, species, magical_power
FROM pets
WHERE is_available = TRUE;

-- See pets orderd by price
SELECT name, species, price
FROM pets
ORDER BY price;






