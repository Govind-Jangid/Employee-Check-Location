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
    company = frappe.db.get_list("Company",{"name":doc.custom_company}['custom_latitude',"custom_longitude","custom_buffer_distance"])
    latitude = company[0]['custom_latitude']
    longitude = company[0]['custom_longitude']
    buffer_distance_in_km = company[0]['custom_buffer_distance'] if company[0]['custom_buffer_distance']>0 else 0
    
    # user coordinates
    user_latiude = doc.latitude
    user_longitude = doc.longitude
    
   
    # Get buffered polygon around live location
    if latitude and longitude:
        buffered_polygon = get_polygon_around_location(latitude, longitude)

        hyde_park = Polygon(buffered_polygon).buffer(buffer_distance_in_km)
        
        
        someone_inside = Point(user_latiude, user_longitude)
        
        is_inside_or_not = hyde_park.contains(someone_inside)
        
        if not is_inside_or_not:
            frappe.throw(_("You are outside of office Location"))
    else:
        frappe.throw(_("Please Set Latiude and Longitude In Comapany Setting"))
    
   
