# install needed libraries if not installed
# pip install overpy

import overpy

# Create Overpass API instance
api = overpy.Overpass()

# Set center location
latitude = 17.4309087  
longitude = 78.4418388
radius = 3000  # in meters

# Overpass QL query
query = f"""
(
  node
    ["amenity"="resturents"]
    (around:{radius},{latitude},{longitude});
  node
    ["amenity"="college"]
    (around:{radius},{latitude},{longitude});
);
out center;
"""

print("Querying Overpass API...")
result = api.query(query)

# Combine nodes into one list
places = result.nodes

if not places:
    print("No cafes or hospitals found nearby.")
else:
    print(f"\nFound {len(places)} places:")
    for node in places:
        name = node.tags.get("name", "Unnamed")
        amenity = node.tags.get("amenity", "unknown")
        print(f" - {amenity.capitalize()}: {name} at lat={node.lat:.6f}, lon={node.lon:.6f}")

# (Optional) Save to CSV
import csv
with open("osm_nearby_places.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Amenity", "Name", "Latitude", "Longitude"])
    for node in places:
        writer.writerow([
            node.tags.get("amenity", ""),
            node.tags.get("name", ""),
            node.lat,
            node.lon
        ])
print("\nSaved results to osm_nearby_places.csv")

