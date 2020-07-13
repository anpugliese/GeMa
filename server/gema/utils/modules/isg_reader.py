import numpy as np
import os
import csv

'''
Geoid header format:
    modelname
    modeltype
    units
    reference
    latmin
    latmax
    lonmin
    lonmax
    deltalat
    deltalon
    nrows
    ncols
    nodata
    ISGformat
'''
#CHANGE THE FOLLOWING LINE TO POINT TO THE LOCAL PATH OF THE GEOID BACK END FOLDER#
path = os.path.dirname(__file__)

#CHANGE THE FOLLOWING LINE TO POINT TO THE LOCAL PATH OF THE GEOID FRONT END FOLDER#
path_geoids = os.path.dirname(__file__) + '/../geoids/'

def populate_bounds():
    print(path)
    geoid_file_names = os.listdir("geoids")
    with open(path + '/bounds.csv', 'w', newline='') as outfile:
        w = csv.writer(outfile)
        for name in geoid_file_names:
            geoid = read_header(name)
            w.writerow([geoid['modelname'], str(geoid['latmin']), str(geoid['latmax']), str(geoid['lonmin']), str(geoid['lonmax']), str(name)])

def get_filename_from_geoid_name(name):
    with open(path + '/bounds.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] == name:
                return row[5]
    return None

def read_header(filename):
    f = open(path_geoids + filename, "r")
    f.readline()
    line = f.readline()
    head = {}
    try:
        while("end_of_head" not in line):
            line = line.replace(" ", "").replace("\n", "")
            if(":" in line):
                lineSplit = line.split(":")
                head[lineSplit[0]] = lineSplit[1]
            else:
                lineSplit = line.split("=")
                head[lineSplit[0]] = float(lineSplit[1])
            
            line = f.readline()
    except:
        return
    return head

def read_geoid(filename):
    f = open(path_geoids + filename, "r")
    f.readline()
    line = f.readline()
    geoid = {}
    while("end_of_head" not in line):
        line = line.replace(" ", "").replace("\n", "")
        if(":" in line):
            lineSplit = line.split(":")
            geoid[lineSplit[0]] = lineSplit[1]
        else:
            lineSplit = line.split("=")
            geoid[lineSplit[0]] = float(lineSplit[1])
        line = f.readline()

    rows = int(geoid['nrows'])
    cols = int(geoid['ncols'])
    geoid["grid"] = np.zeros((rows, cols))
    for i in range(0, rows):
        line = f.readline().split()
        for j in range(0, cols):
            try:
                geoid["grid"][i, j] = line[j] 
            except Exception as e:
                raise e
    return geoid

# To be used only offline
def test_geoids():
    geoid_file_names = os.listdir("C:/Users/juan-/Desktop/Geoids/geoid_service/server/gema/utils/geoids")
    i = 1
    for name in geoid_file_names:
        try:
            print("reading " + name + ", " + str(i))
            read_geoid(name)
        except Exception as e:
            print("----------------------")
            print("Error in geoid " + name)
            print(e)
            print("----------------------")
        i += 1
        