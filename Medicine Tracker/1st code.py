Python 3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import math
import requests

# --- Haversine Distance Formula ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in KM
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# --- Sample seller data ---
sellers = []

def add_seller(shop_name, lat, lon, medicines):
    sellers.append({
        'shop_name': shop_name,
        'lat': lat,
        'lon': lon,
        'medicines': medicines  # Dictionary {medicine_name: price}
    })

# --- Add sample sellers ---
add_seller("Green Pharmacy", 28.6139, 77.2090, {"Paracetamol": 20, "Aspirin": 30})
add_seller("Health Plus", 28.5355, 77.3910, {"Paracetamol": 22, "Ibuprofen": 25})
add_seller("MediWorld", 28.7041, 77.1025, {"Aspirin": 35, "Ibuprofen": 28, "Paracetamol": 19})

# --- Geocode address to lat/lon ---
def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json'
    }
    headers = {
        'User-Agent': 'MedicineFinderApp/1.0 (your_email@example.com)'  # Replace with your info
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    else:
...         return None, None
... 
... # --- Find medicine nearby ---
... def find_medicine_nearby(user_lat, user_lon, medicine_name, max_distance_km=10):
...     found_shops = []
...     for seller in sellers:
...         if medicine_name in seller['medicines']:
...             distance = haversine(user_lat, user_lon, seller['lat'], seller['lon'])
...             if distance <= max_distance_km:
...                 found_shops.append({
...                     "shop_name": seller['shop_name'],
...                     "distance_km": round(distance, 2),
...                     "price": seller['medicines'][medicine_name]
...                 })
... 
...     return sorted(found_shops, key=lambda x: x['distance_km'])
... 
... # --- Main Execution ---
... if __name__ == "__main__":
...     print("=== Find Nearby Medicine Shops ===")
...     med = input("Enter medicine name: ").strip()
...     address = input("Enter your full address: ").strip()
... 
...     user_lat, user_lon = geocode_address(address)
... 
...     if user_lat is None:
...         print("❌ Could not locate your address. Please try again with more detail.")
...     else:
...         results = find_medicine_nearby(user_lat, user_lon, med)
... 
...         if results:
...             print(f"\n🩺 Shops near you with '{med}':")
...             for shop in results:
...                 print(f" - {shop['shop_name']} ({shop['distance_km']} km) - ₹{shop['price']}")
...         else:
...             print(f"\nNo shops found within 10 km that have '{med}'.")
