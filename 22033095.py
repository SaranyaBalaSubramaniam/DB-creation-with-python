# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 16:32:36 2023

@author: ADMIN
"""
import csv
import random
from faker import Faker
import sqlite3
import os

fake = Faker()

# Function to generate random ordinal data
def generate_ordinal_data():
    ratings = ["Low", "Medium", "High"]
    return random.choice(ratings)

# Function to generate random nominal data
def generate_nominal_data():
    categories = ["Electronics", "Clothing", "Home Appliances"]
    return random.choice(categories)

# Function to generate random ratio data
def generate_ratio_data():
    return round(random.uniform(10.0, 500.0), 2)

# Function to generate random interval data
def generate_interval_data():
    return random.randint(1, 10)

# Set the current working directory to the script's directory
script_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_directory)

# Generate Products data
products_data = []
for product_id in range(1, 1001):
    category = generate_nominal_data()
    price = generate_ratio_data()
    stock_quantity = random.randint(20, 100)
    product_rating = generate_ordinal_data()
    customer_id = fake.uuid4()  # Adding customer_id
    
    product = {
        "product_id": product_id,
        "product_name": fake.word(),
        "category": category,
        "price": price,
        "stock_quantity": stock_quantity,
        "product_rating": product_rating,
        "customer_id": customer_id,
    }
    products_data.append(product)

# Generate Sales data
sales_data = []
for sale_id in range(1, 1001):
    customer_name = fake.name()
    sale_date = fake.date_this_year()
    customer_id = fake.uuid4()  # Adding customer_id
    
    sale = {
        "sale_id": sale_id,
        "customer_id": customer_id,
        "customer_name": customer_name,
        "sale_date": sale_date,
    }
    sales_data.append(sale)

# Generate Sales Details data (Child Table)
sales_details_data = []
for sale_id in range(1, 1001):
    product_id = random.randint(1, 1000)
    quantity_sold = random.randint(1, 10)
    
    sales_details = {
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity_sold": quantity_sold,
    }
    sales_details_data.append(sales_details)

# Define CSV file names with full paths
products_csv_file = os.path.join(script_directory, "products_data.csv")
sales_csv_file = os.path.join(script_directory, "sales_data.csv")
sales_details_csv_file = os.path.join(script_directory, "sales_details_data.csv")

# Write data to CSV files
with open(products_csv_file, mode="w", newline="") as file:
    fieldnames = ["product_id", "product_name", "category", "price", "stock_quantity", "product_rating", "customer_id"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products_data)

with open(sales_csv_file, mode="w", newline="") as file:
    fieldnames = ["sale_id", "customer_id", "customer_name", "sale_date"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(sales_data)

with open(sales_details_csv_file, mode="w", newline="") as file:
    fieldnames = ["sale_id", "product_id", "quantity_sold"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(sales_details_data)

# Function to create SQLite database and import data from CSV files
def create_sales_database(products_csv, sales_csv, sales_details_csv, database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Create 'products' table if it does not exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
    if not cursor.fetchone():
        with open(products_csv, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            columns = ', '.join(header)
            cursor.execute(f'CREATE TABLE products ({columns})')
            cursor.executemany(f'INSERT INTO products VALUES ({", ".join(["?"] * len(header))})', reader)

    # Create 'sales' table if it does not exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales'")
    if not cursor.fetchone():
        with open(sales_csv, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            columns = ', '.join(header)
            cursor.execute(f'CREATE TABLE sales ({columns})')
            cursor.executemany(f'INSERT INTO sales VALUES ({", ".join(["?"] * len(header))})', reader)

    # Create 'sales_details' table if it does not exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales_details'")
    if not cursor.fetchone():
        with open(sales_details_csv, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            columns = ', '.join(header)
            cursor.execute(f'CREATE TABLE sales_details ({columns})')
            cursor.executemany(f'INSERT INTO sales_details VALUES ({", ".join(["?"] * len(header))})', reader)

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Create the 'sales_database.db' and import data
create_sales_database(products_csv_file, sales_csv_file, sales_details_csv_file, 'sales_database.db')
