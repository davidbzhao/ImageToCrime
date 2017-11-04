#download the google map image from url
import urllib.request
import math

def downloadMapImage(latitude, longitude, key, fileName, width=640, height=640, zoom=17):
    f = open(fileName, "wb")
    f.write(urllib.request.urlopen('https://maps.googleapis.com/maps/api/staticmap?center='                                    + str(latitude) +','+ str(longitude) + '&zoom=17&size=' +                                    str(width) + 'x' + str(height) + '&maptype=satellite&key=' + key)                                    .read())
    f.close()
    



def getPicWidthMeters(latitude, pic_width_pixels, zoom): 
    meters_per_pixel = 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom) 
    pic_width_meters = meters_per_pixel * pic_width_pixels
    return pic_width_meters



# get coordinates of 2nd point, given a starting point, distance moved, and either moving east/west
# latitude and longitude must be given in DEGREES
# returns coordinates of new point in DEGREES
def getSecondPointMovingEW(lat1, long1, distance, west= True): 
    radius = 6371000 # radius of earth in meters  
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)
    p1 = math.sin(distance/(2*radius))
    p2 = math.cos(lat1)
    quotient = p1/p2
    delta_longitude = 2*math.asin(quotient)
    if west:
        long2 = long1 - delta_longitude
    else:
        long2 = long1 + delta_longitude
    
    return math.degrees(long2)



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
key = "" 
latitude = 41.878114
longitude = -87.6298
zoom = 17
width = 640
height = 640
# downloadMapImage(latitude, longitude, key, "testimg1.png")


distanceFromCenter = getPicWidthMeters(latitude, width, zoom)
longitude = getSecondPointMovingEW(latitude, longitude, distanceFromCenter, west=False)
print(distanceFromCenter)
downloadMapImage(latitude, longitude, key, "testimg1.png")
f = open("testimg2.png", "wb")
f.write(urllib.request.urlopen('https://maps.googleapis.com/maps/api/staticmap?center='                                + str(latitude) +','+ str(longitude) + '&zoom=17&&size=640x640&maptype=satellite&key=' + key)                                .read())
f.close()

