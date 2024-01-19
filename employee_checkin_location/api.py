from shapely.geometry import Point,Polygon
from geopy.geocoders import Nominatim
import geopandas as gpd
import frappe
from frappe import _


def get_polygon_around_location(latitude, longitude):
    # Create a geolocator object
    geolocator = Nominatim(user_agent="polygon_correction_app")

    # Define the coordinates
    location = (latitude, longitude)
    
    # Get the address information for the given coordinates
    address = geolocator.reverse(location, language='en')
  

    # Extract the bounding box coordinates from the address
    bounding_box = address.raw['boundingbox']

    # Convert bounding box coordinates to floats
    min_lat, max_lat, min_lon, max_lon = map(float, bounding_box)
   
    hyde_park_coordinates = [
    (latitude, longitude),
    (min_lat, min_lon),
    (max_lat, max_lon),
    (latitude, longitude),
    ]

    return hyde_park_coordinates



def get_user_location(doc, method=None):
    
    # Comapany address coordinates
    latitude = 17.4357646
    longitude = 78.4568369
    buffer_distance_in_km = 0.05
    
    # user coordinates
    user_latiude = doc.latitude
    user_longitude = doc.longitude

    # Get buffered polygon around live location
    buffered_polygon = get_polygon_around_location(latitude, longitude)

    hyde_park = Polygon(buffered_polygon).buffer(buffer_distance_in_km)
    
    
    someone_inside = Point(user_latiude, user_longitude)
    
    is_inside_or_not = hyde_park.contains(someone_inside)
    
    if not is_inside_or_not:
        frappe.throw(_("You are outside of office Location"))
    
   
