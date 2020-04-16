import numpy as np
import os
import csv
from .isg_reader import get_filename_from_geoid_name, read_geoid

# Point p = (lat, lng, h)
# geoid object has a grid attribute with the geoid ondulation at each interval

path = "gema/utils/modules/"

def getQuadrant(p, geoid):
    min_lat = geoid['latmin']
    delta_lat = geoid['deltalat']
    min_lng = geoid['lonmin']
    delta_lng = geoid['deltalon']
    lat = p[0]
    lng = p[1]
 
    i_up = int((lat - min_lat) / delta_lat)
    if i_up == geoid['nrows']: i_up = i_up - 1
    i_down = i_up + 1

    j_left = int((lng - min_lng) / delta_lng)
    if j_left == geoid['ncols']: j_left = j_left - 1
    j_right = j_left + 1
    
    return (i_up, j_left), (i_up, j_right), (i_down, j_left), (i_down, j_right)


def interpolation(p, geoid, type_='bilinear'):
    p1,p2,p3,p4 = getQuadrant(p, geoid)
    # Interpolation of geoid ondulation on a given point p
    min_lat = geoid['latmin']
    delta_lat = geoid['deltalat']
    min_lng = geoid['lonmin']
    delta_lng = geoid['deltalon']
    grid = geoid['grid'] 
    no_data = geoid['nodata']

    lat1 = min_lat + delta_lat*p1[0]
    lng1 = min_lng + delta_lng*p1[1]
    lat2 = min_lat + delta_lat*p2[0]
    lng2 = min_lng + delta_lng*p2[1]
    lat3 = min_lat + delta_lat*p3[0]
    lng3 = min_lng + delta_lng*p3[1]
    lat4 = min_lat + delta_lat*p4[0]
    lng4 = min_lng + delta_lng*p4[1]

    if grid[p1] == no_data or grid[p2] == no_data or grid[p3] == no_data or grid[p4] == no_data:
        # No data at one of the interpolation points -> the point has no data corresponding
        # that point
        return None

    if type_ == 'bilinear': 
        A = np.array([[lat1, lng1, lat1*lng1, 1],
                      [lat2, lng2, lat2*lng2, 1], 
                      [lat3, lng3, lat3*lng3, 1],
                      [lat4, lng4, lat4*lng4, 1]]) 

        B = np.array([grid[p1], grid[p2], grid[p3], grid[p4]]) 
        x = np.linalg.solve(A, B) 

        Np = x[0]*p[0]+ x[1]*p[1] + x[2]*p[0]*p[1] + x[3]
        return Np

def orthometric_height(p, Np):
    # Calculates ortometric heigth from a geoid ondulation Np and a point
    return p[2] - Np

def calculate_orthometric_height(p, geoid_name, type_='bilinear'):
    try:
        filename = get_filename_from_geoid_name(geoid_name)
        geoid = read_geoid(filename)
        Np = interpolation(p, geoid, type_)
        if Np is None:
            raise Exception("Np is None")
        h = orthometric_height(p, Np)
        return h
    except Exception as e:
        print(e)
        return None
    
def available_geoids(p):
    # bounds csv = (geoid_name, min_lat, max_lat, min_lon, max_lon, file_name)
    # Returns list of names of available geoids in format (geoid_name, file_name)
    available_geoids = []
    #print(os.listdir())
    with open(path + 'bounds.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            # min_lat <= lat_p <= max_lat
            # min_lng <= lng_p <= max_lng
            if p[0] >= float(row[1]) and p[0] <= float(row[2]) and p[1] >= float(row[3]) and p[1] <= float(row[4]):
                row = (row[0])
                available_geoids.append(row) 
    return available_geoids    
