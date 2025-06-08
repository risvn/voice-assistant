import overpy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import argparse

def find_places(place_type="cafe"):
    # Create Overpass API instance
    api = overpy.Overpass()

    # Create Nominatim geocoder instance (OpenStreetMap's reverse geocoding service)
    geolocator = Nominatim(user_agent="OpenStreetMapReverseGeocoder")

    # Set center location (lat, lon)
    latitude = 17.4309087
    longitude = 78.4418388
    radius = 3000  # in meters

    # Overpass query to fetch specified amenity type
    query = f"""
    (
      node
        ["amenity"="{place_type}"]
        (around:{radius},{latitude},{longitude});
    );
    out center;
    """

    print("Querying Overpass API...")
    result = api.query(query)

    # Combine nodes into one list
    places = result.nodes

    # Limit to top 5 results
    places = places[:3]

    num = 1
    if not places:
        print(f"No {place_type}s found nearby.")
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
            num += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find nearby places using Overpass API.")
    parser.add_argument("place", type=str, help="Type of place to search for (e.g., cafe, hospital, atm)")
    args = parser.parse_args()

    find_places(args.place)
