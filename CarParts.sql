-- Clean the database
DROP TABLE IF EXISTS Part_in_Order;
DROP TABLE IF EXISTS Supplier;
DROP TABLE IF EXISTS Brand;
DROP TABLE IF EXISTS Part;
DROP TABLE IF EXISTS Part_for_Car;
DROP TABLE IF EXISTS Part_Supplier;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Customer_Statut;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Car_Manufacturer;
DROP TABLE IF EXISTS Car;
DROP TABLE IF EXISTS Part_Maker;

-- Create the Schema
CREATE TABLE IF NOT EXISTS Customer_Statut(
            statut_id INT NOT NULL PRIMARY KEY,
            statut VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Customer(
            customer_id INT NOT NULL PRIMARY KEY,
            statut_id INT NOT NULL,
            individual_or_organization VARCHAR(50) NOT NULL,
            organisation_name varchar(50),
            individual_first_name varchar(50),
            individual_last_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Orders(
            order_id INT NOT NULL PRIMARY KEY,
            customer_id INT NOT NULL,
            amount_due INT NOT NULL
            );
         
CREATE TABLE IF NOT EXISTS Car_Manufacturer(
            car_manufacturer_id INT NOT NULL PRIMARY KEY,
            name VARCHAR(50) NOT NULL
            );
           
CREATE TABLE IF NOT EXISTS Car(
            car_id INT NOT NULL PRIMARY KEY,
            car_manufacturer_id INT NOT NULL,
            date_of_manufacture DATE NOT NULL,
            model VARCHAR(50) NOT NULL
            );
           
CREATE TABLE IF NOT EXISTS Supplier(
            supplier_id INT NOT NULL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            street_address VARCHAR(50) NOT NULL,
            town VARCHAR(50) NOT NULL,
            country VARCHAR(50) NOT NULL,
            postcode INT NOT NULL,
            phone VARCHAR(50) NOT NULL
);
           
CREATE TABLE IF NOT EXISTS Brand(
            brand_id INT NOT NULL PRIMARY KEY,
            name VARCHAR(50) NOT NULL
);
           
CREATE TABLE IF NOT EXISTS Part_Maker(
            part_maker_id INT NOT NULL PRIMARY KEY,
            name VARCHAR(50) NOT NULL
);
           
CREATE TABLE IF NOT EXISTS Part(
        part_id INT NOT NULL PRIMARY KEY,
        brand_id INT NOT NULL,
        supplier_id INT NOT NULL,
        part_group_id INT NOT NULL,
        part_maker_id INT NOT NULL,
        part_name VARCHAR(50) NOT NULL,
        main_supplier_name VARCHAR(50) NOT NULL,
        price_to_us INT NOT NULL,
        price_to_customer INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Part_for_Car(
            car_id INT NOT NULL,
            part_id INT NOT NULL
);
           
CREATE TABLE IF NOT EXISTS Part_Supplier(
        part_supplier_id INT NOT NULL PRIMARY KEY,
        part_id INT NOT NULL,
        supplier_id INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Part_in_Order(
            part_in_order_id INT NOT NULL,
            order_id INT NOT NULL,
            part_supplier_id INT NOT NULL,
            actual_sale_price INT NOT NULL,
            quantity INT NOT NULL
);
