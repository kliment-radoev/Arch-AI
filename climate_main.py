from geopy.geocoders import Nominatim

from temperature import temperatures
from wind import wind_parameters

place = input("Please enter a place whose climate you want to check in the format 'City, Country? : \n"
              "(If there is no data for the specified city, you can enter the nearest large city) \n")

years = int(input('How many years back do you want to get data for?: \n'
                  '(Note that public weather data in Python format is not very old\n'
                  'and is not necessarily available for every city around the globe) \n'))


def get_coordinates(address):
    geolocator = Nominatim(user_agent="myapplication")
    location = geolocator.geocode(address)
    return location.latitude, location.longitude


# print the coordinates of the address
def print_coordinates(address):
    lat, lon = get_coordinates(address)
    coor_list = [place, lat, lon]
    print()
    print(coor_list[0])
    print("Latitude: ", lat)
    print("Longitude: ", lon, "\n")

    return coor_list


city_coords = print_coordinates(place)

temperatures(city_coords, years)
wind_parameters(place, years)
