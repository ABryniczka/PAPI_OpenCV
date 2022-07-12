import math

def Calc_horizon_distance(lat1,lon1,lat2,lon2):
    R = 6371 # Radius of the earth in km
    dLat = deg2rad(lat2-lat1)  #deg2rad below
    dLon = deg2rad(lon2-lon1) 
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)); 
    d = R * c * 1000 # Distance in m
    return d

def deg2rad(deg):
  return deg * (math.PI/180)

  '''
  This script calculates great-circle distances 
  between the two points – that is, the shortest distance over 
  the earth's surface – using the 'Haversine' formula.

  https://en.wikipedia.org/wiki/Haversine_formula
  '''
