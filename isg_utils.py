import numpy as np

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


def interpolation(p, p1, p2, p3, p4, geoid, type='bilinear'):
    min_lat = geoid['latmin']
    delta_lat = geoid['deltalat']
    min_lng = geoid['lonmin']
    delta_lng = geoid['deltalon']
    grid = geoid['grid']

   
    lat1 = min_lat + delta_lat*p1[0]
    lng1 = min_lng + delta_lng*p1[1]
    lat2 = min_lat + delta_lat*p2[0]
    lng2 = min_lng + delta_lng*p2[1]
    lat3 = min_lat + delta_lat*p3[0]
    lng3 = min_lng + delta_lng*p3[1]
    lat4 = min_lat + delta_lat*p4[0]
    lng4 = min_lng + delta_lng*p4[1]



    if type == 'bilinear': 
        A = np.array([[lat1, lng1, lat1*lng1, 1],
                      [lat2, lng2, lat2*lng2, 1], 
                      [lat3, lng3, lat3*lng3, 1],
                      [lat4, lng4, lat4*lng4, 1]]) 

        B = np.array([grid[p1], grid[p2], grid[p3], grid[p4]]) 
        x = np.linalg.solve(A, B) 
        print(x)

        Np = x[0]*p[0]+ x[1]*p[1] + x[2]*p[0]*p[1] + x[3]

        return Np


def orthometric_height(p, Np):
    return p[2] - Np

