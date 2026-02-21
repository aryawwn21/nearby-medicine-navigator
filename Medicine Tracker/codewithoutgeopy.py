import tkinter as tk
from tkinter import messagebox
import os
import math

# ------------------- Setup folders -------------------
os.makedirs("users", exist_ok=True)
os.makedirs("history", exist_ok=True)

# ------------------- Known Locations -------------------
# Predefined city coordinates (can add more as needed)
city_coordinates = {
    "delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "bangalore": (12.9716, 77.5946),
    "bengaluru": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "hyderabad": (17.3850, 78.4867),
    "pune": (18.5204, 73.8567),
    "jaipur": (26.9124, 75.7873),
    "lucknow": (26.8467, 80.9462)
}

# ------------------- Medicine Sellers -------------------
sellers = []

def add_seller(shop_name, city, medicines):
    lat, lon = city_coordinates[city.lower()]
    sellers.append({
        "shop_name": shop_name,
        "lat": lat,
        "lon": lon,
        "medicines": medicines
    })

# Add sellers mapped to cities
add_seller("Green Pharmacy - Delhi", "delhi", {"Paracetamol": 20, "Aspirin": 30})
add_seller("HealthPlus - Mumbai", "mumbai", {"Paracetamol": 19, "Ibuprofen": 25})
add_seller("MediCare - Bangalore", "bangalore", {"Aspirin": 32, "Ibuprofen": 27})
add_seller("Apollo Health - Chennai", "chennai", {"Paracetamol": 21, "Cetrizine": 15})

# ------------------- Distance Formula -------------------
def haversine(lat1, lon1, lat2, lon2):
    """Calculate great-circle distance between two points"""
    R = 6371  # Earth radius in km
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

# ------------------- Get City Coordinates -------------------
def get_city_coordinates(address):
    """Match entered address with known cities"""
    address = address.lower().strip()
    for city in city_coordinates:
        if city in address:
            return city_coordinates[city]
    return (None, None)

# ------------------- GUI -------------------
class MedicineApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Medicine Finder")
        self.username = None
        self.login_frame()

    # ------------------- Login Screen -------------------
    def login_frame(self):
        self.clear_frame()

        tk.Label(self.master, text="Username").pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        tk.Label(self.master, text="Password").pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        tk.Button(self.master, text="Sign In", command=self.sign_in).pack(pady=5)
        tk.Button(self.master, text="Sign Up", command=self.sign_up).pack()

    def sign_in(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        file_path = f"users/{user}.txt"

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                stored_pwd = f.read().strip()
            if pwd == stored_pwd:
                self.username = user
                self.search_frame()
            else:
                messagebox.showerror("Error", "Incorrect password.")
        else:
            messagebox.showerror("Error", "User not found.")

    def sign_up(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        file_path = f"users/{user}.txt"

        if os.path.exists(file_path):
            messagebox.showerror("Error", "User already exists.")
        else:
            with open(file_path, "w") as f:
                f.write(pwd)
            with open(f"history/{user}_history.txt", "w") as f:
                f.write("")
            messagebox.showinfo("Success", "Account created successfully.")

    # ------------------- Search Screen -------------------
    def search_frame(self):
        self.clear_frame()

        tk.Label(self.master, text=f"Welcome, {self.username}").pack(pady=5)

        tk.Label(self.master, text="Medicine").pack()
        self.med_entry = tk.Entry(self.master)
        self.med_entry.pack()

        tk.Label(self.master, text="Your Area & City").pack()
        self.addr_entry = tk.Entry(self.master)
        self.addr_entry.pack()

        tk.Button(self.master, text="Search", command=self.search_medicine).pack(pady=5)

        self.results = tk.Text(self.master, height=10, width=60)
        self.results.pack(pady=5)

        tk.Label(self.master, text="Search History:").pack()
        self.history = tk.Text(self.master, height=10, width=60)
        self.history.pack()
        self.load_history()

    def search_medicine(self):
        medicine = self.med_entry.get().strip()
        address = self.addr_entry.get().strip()

        if not medicine or not address:
            messagebox.showerror("Error", "Please enter both medicine and address.")
            return

        lat, lon = get_city_coordinates(address)
        self.results.delete("1.0", tk.END)

        if not lat:
            self.results.insert(tk.END, "❌ City not recognized. Try again (e.g., 'Mumbai').\n")
            return

        matches = []
        for shop in sellers:
            if medicine in shop["medicines"]:
                dist = haversine(lat, lon, shop["lat"], shop["lon"])
                if dist <= 10:  # Within 10 km
                    matches.append(f"{shop['shop_name']} - ₹{shop['medicines'][medicine]} ({round(dist,2)} km)")

        if matches:
            self.results.insert(tk.END, "✅ Nearby Shops:\n")
            for match in matches:
                self.results.insert(tk.END, match + "\n")
        else:
            self.results.insert(tk.END, "No nearby shops found.\n")

        # Save to history file
        with open(f"history/{self.username}_history.txt", "a") as f:
            f.write(f"{medicine} in {address}\n")
        self.load_history()

    def load_history(self):
        self.history.delete("1.0", tk.END)
        try:
            with open(f"history/{self.username}_history.txt", "r") as f:
                self.history.insert(tk.END, f.read())
        except FileNotFoundError:
            pass

    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# ------------------- Run the App -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MedicineApp(root)
    root.mainloop()
