Python 3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import mysql.connector

# --- Connect to MySQL ---
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",        # Replace with your MySQL username
        password="your_password",    # Replace with your MySQL password
        database="medicine_finder"   # Ensure this DB exists or create it
    )

# --- Create Tables ---
def create_tables():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sellers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        shop_name VARCHAR(255),
        latitude DOUBLE,
        longitude DOUBLE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seller_id INT,
        medicine_name VARCHAR(255),
        price DOUBLE,
        FOREIGN KEY (seller_id) REFERENCES sellers(id)
    )
    """)

    db.commit()
    db.close()

# --- Insert Seller + Medicines ---
def add_seller(shop_name, lat, lon, medicines):
    db = connect_db()
    cursor = db.cursor()

    # Insert into sellers
    cursor.execute("INSERT INTO sellers (shop_name, latitude, longitude) VALUES (%s, %s, %s)",
                   (shop_name, lat, lon))
    seller_id = cursor.lastrowid

    # Insert medicines
    for med_name, price in medicines.items():
        cursor.execute("INSERT INTO medicines (seller_id, medicine_name, price) VALUES (%s, %s, %s)",
                       (seller_id, med_name, price))

    db.commit()
    db.close()
... 
... # --- Search Sellers by Medicine ---
... def find_sellers_by_medicine(medicine_name):
...     db = connect_db()
...     cursor = db.cursor(dictionary=True)
... 
...     query = """
...     SELECT s.shop_name, s.latitude, s.longitude, m.price
...     FROM sellers s
...     JOIN medicines m ON s.id = m.seller_id
...     WHERE m.medicine_name = %s
...     """
...     cursor.execute(query, (medicine_name,))
...     results = cursor.fetchall()
... 
...     db.close()
...     return results
... 
... # --- Example Usage ---
... if __name__ == "__main__":
...     create_tables()
... 
...     # Add sellers (sample data)
...     add_seller("Green Pharmacy", 28.6139, 77.2090, {"Paracetamol": 20, "Aspirin": 30})
...     add_seller("MediWorld", 28.7041, 77.1025, {"Paracetamol": 19, "Ibuprofen": 25})
... 
...     # Search for medicine
...     search = input("Enter medicine to search: ")
...     sellers = find_sellers_by_medicine(search)
... 
...     if sellers:
...         print(f"Sellers with '{search}':")
...         for shop in sellers:
...             print(f" - {shop['shop_name']} at ₹{shop['price']} (Lat: {shop['latitude']}, Lon: {shop['longitude']})")
...     else:
...         print("No sellers found with that medicine.")
CREATE DATABASE medicine_finder;

