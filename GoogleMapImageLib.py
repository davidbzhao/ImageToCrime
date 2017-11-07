#download the google map image from url
import urllib.request
import requests
import math

def is_within_city(latitude, longitude, city_name, key):
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(latitude) + "," + str(longitude) + "&key=" + key
    response = requests.get(url)
    response.raise_for_status()
    if (response.json()['status'] == 'ZERO_RESULTS'):
        return False
    elif (response.json()['status'] != "OK"):
        raise BaseException("Something wrong happened when reverse-geocoding this location:", latitude , longitude, "This is the error received", response.json()['status'])

    address = response.json()["results"][0]["formatted_address"]
    city = address.split(",")[1].strip()
    return city == city_name

def download_satelite_image(latitude, longitude, key, fileName, width=640, height=640, zoom=17):
    f = open(fileName, "wb")
    f.write(urllib.request.urlopen('https://maps.googleapis.com/maps/api/staticmap?center='+ str(latitude) +','+ str(longitude) + '&zoom=17&size=' +str(width) + 'x' + str(height) + '&maptype=satellite&key=' + key).read())
    f.close()
    
def download_map_image(latitude, longitude, key, fileName, width=640, height=640, zoom=17):
    f = open(fileName, "wb")

    f.write(urllib.request.urlopen('https://maps.googleapis.com/maps/api/staticmap?center=' + str(latitude) + ',' + str(longitude) + '&zoom=17&&size=640x640&style=element:labels|visibility:off&key=' + key).read())
    f.close()


def get_pic_width_meters(latitude, pic_width_pixels, zoom):
    meters_per_pixel = 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom) 
    pic_width_meters = meters_per_pixel * pic_width_pixels
    return pic_width_meters



# get coordinates of 2nd point, given a starting point, distance moved, and either moving east/west
# latitude and longitude must be given in DEGREES
# returns coordinates of new point in DEGREES
def get_second_point(lat1, long1, distance, direction):
    ' direction: int: 1 = north, 2 = east, 3 = south, 4 = west'
    ret_value = {1: get_second_point_moving_NS(lat1, long1, distance, False),
                 2: get_second_point_moving_EW(lat1, long1, distance, False),
                 3: get_second_point_moving_NS(lat1, long1, distance, True),
                 4: get_second_point_moving_EW(lat1, long1, distance, True)
                 }
    return ret_value[direction]

def get_second_point_moving_EW(lat1, long1, distance, west= True):
    radius = 6371000 # radius of earth in meters  
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)
    p1 = math.sin(distance/(2*radius))
    p2 = math.cos(lat1)
    quotient = p1/p2
    delta_longitude = 2*math.asin(quotient)
    # print("inside fnctin", math.degrees(delta_longitude))
    # print()
    if west:
        long2 = long1 - delta_longitude
    else:
        long2 = long1 + delta_longitude
    lat2 = math.degrees(lat1) # doesn't change
    long2 = math.degrees(long2)
    return lat2, long2


def get_second_point_moving_NS(lat1, long1, distance, south=True):
    radius = 6371000  # radius of earth in meters
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)
    delta_latitude = distance/radius
    if south:
        lat2 = lat1 - delta_latitude
    else:
        lat2 = lat1 + delta_latitude
    lat2 = math.degrees(lat2)
    long2 = math.degrees(long1) # doesn't change
    return lat2, long2

# Inaccurate 2nd Coordinate Calculation 
#theta measured counterclockwise from due east
# go straight east 
# theta = 0;
# dx = distanceFromCenter*math.cos(theta) 
# dy = distanceFromCenter*math.sin(theta) #dx, dy same units as R

# delta_longitude = dx/(111320*math.cos(latitude))  # dx, dy in meters
# delta_latitude = dy/110540                   # result in degrees long/lat

# longitude += delta_longitude
# latitude  += delta_latitude



# Testing 
# key = "AIzaSyAVcfKag3qQqMrw-I3Lwg0c-UsOj1nx4UI"
# latitude = 41.878114
# longitude = -87.6298
# zoom = 17
# width = 640
# height = 640
# # downloadMapImage(latitude, longitude, key, "testimg1.png")
#
#
# distance_from_center = get_pic_width_meters(latitude, width, zoom)
# latitude, longitude = getSecondPointMovingEW(latitude, longitude, distanceFromCenter, west=False)
# print(distanceFromCenter)
# download_satelite_image(latitude, longitude, key, "testimg1.png")
# f = open("testimg2.png", "wb")
# f.write(urllib.request.urlopen('https://maps.googleapis.com/maps/api/staticmap?center='+ str(latitude) +','+ str(longitude) + '&zoom=17&&size=640x640&style=element:labels|visibility:off&key=' + key).read())
# f.close()

