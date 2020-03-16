import numpy as np

def getQuadrant(lat, lng, geoid):
    min_lat = geoid['latmin']
    delta_lat = geoid['deltalat']
    min_lng = geoid['lonmin']
    delta_lng = geoid['deltalon']
    
    i_up = int((lat - min_lat) / delta_lat)
    if i_up == geoid['nrows']: i_up = i_up - 1
    i_down = i_up + 1

    j_left = int((lng - min_lng) / delta_lng)
    if j_left == geoid['ncols']: j_left = j_left - 1
    j_right = j_left + 1
    
    return (i_up, j_left), (i_up, j_right), (i_down, j_left), (i_down, j_right)