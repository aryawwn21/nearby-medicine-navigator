#  Medicine Finder App

A Python-based application that helps users locate nearby pharmacies and check medicine availability using location-based search.

---

## Project Overview

The Medicine Finder App allows users to search for medicines and find nearby pharmacies that have them in stock.
It uses distance calculation and location matching to display the nearest sellers along with pricing.

This project is useful for quickly finding essential medicines in nearby areas.

---

## Features

✔ User login & signup system
✔ Medicine search by location
✔ Nearby pharmacy detection
✔ Distance calculation using Haversine formula
✔ Search history tracking
✔ Simple GUI interface (Tkinter)
✔ Optional database integration (MySQL)

---

## Technologies Used

* Python
* Tkinter (GUI)
* Geolocation APIs
* Haversine Distance Algorithm
* MySQL (optional database)
* File handling for user data

---

## Project Structure

```
Medicine-Finder-App/
│
├── medicinenavigator.py
├── codewithoutgeopy.py
├── Mysql connection.py
├── users/
├── history/
└── README.md
```

---

##  Installation & Setup

### 1️⃣ Clone the repository

git clone https://github.com/yourusername/medicine-finder-app.git

### 2️⃣ Navigate to the folder

cd medicine-finder-app

### 3️⃣ Install required libraries

pip install requests geopy mysql-connector-python

### 4️⃣ Run the application

python medicinenavigator.py

---

## How It Works

1. User logs into the application
2. Enters the medicine name and location
3. App converts location into coordinates
4. Distance is calculated using the Haversine formula
5. Nearby pharmacies within a fixed radius are displayed

---

## Database Setup (Optional)

If using MySQL:

CREATE DATABASE medicine_finder;

Update database credentials inside the MySQL connection file before running.

---

## Objective

To develop a location-based system that helps users quickly locate nearby pharmacies and check medicine availability.

---

##  Author

**Aryan Chawla**
B.Tech Electronics & Communication Engineering

---

## License

This project is licensed under the MIT License.
