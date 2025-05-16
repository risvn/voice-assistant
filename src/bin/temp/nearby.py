import overpy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Create Overpass API instance
api = overpy.Overpass()

# Create Nominatim geocoder instance (OpenStreetMap's reverse geocoding service)
geolocator = Nominatim(user_agent="OpenStreetMapReverseGeocoder")

# Set center location (lat, lon)
latitude = 17.4309087  
longitude = 78.4418388
radius = 3000  # in meters

# Overpass query to fetch cafes and hospitals
query = f"""
(
  node
    ["amenity"="cafe"]
    (around:{radius},{latitude},{longitude});
);
out center;
"""

print("Querying Overpass API...")
result = api.query(query)

# Combine nodes into one list
places = result.nodes

# Limit to top 5 results
places = places[:5]

num=1
if not places:
    print("No cafes or hospitals found nearby.")
else:
    print(f"\nFound {len(places)} places:")

    for node in places:
        # Get the name and amenity
        name = node.tags.get("name", "Unnamed")
        amenity = node.tags.get("amenity", "unknown")
        
        # Get the coordinates of the place
        lat, lon = node.lat, node.lon

        # Reverse geocode to get address from lat, lon
        location = geolocator.reverse((lat, lon), language="en")
        address = location.address if location else "Address not found"

        # Calculate relative distance from the center point
        center_coords = (latitude, longitude)
        place_coords = (lat, lon)
        distance = geodesic(center_coords, place_coords).km  # Distance in km

        print(f"{num}  {amenity.capitalize()}: {name} at Address: {address}")
        print(f"   Distance from center: {distance:.2f} km")
        num+=1
# (Optional) Save to CSV
import csv
with open("osm_nearby_places_with_address.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Amenity", "Name", "Address", "Latitude", "Longitude", "Distance (km)"])
    for node in places:
        lat, lon = node.lat, node.lon
        location = geolocator.reverse((lat, lon), language="en")
        address = location.address if location else "Address not found"
        distance = geodesic((latitude, longitude), (lat, lon)).km
        writer.writerow([
            node.tags.get("amenity", ""),
            node.tags.get("name", ""),
            address,
            lat,
            lon,
            distance
        ])
print("\nSaved results to osm_nearby_places_with_address.csv")

