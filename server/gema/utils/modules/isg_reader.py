import numpy as np
import os
import csv

path = "gema/utils/modules/"
path_geoids = "gema/utils/geoids/"

def populate_bounds():
    geoid_file_names = os.listdir("geoids")
    with open(path + 'bounds.csv', 'w', newline='') as outfile:
        w = csv.writer(outfile)
        for name in geoid_file_names:
            geoid = read_header('geoids/'+name)
            w.writerow([geoid['modelname'], str(geoid['latmin']), str(geoid['latmax']), str(geoid['lonmin']), str(geoid['lonmax']), str(name)])

def get_filename_from_geoid_name(name):
    with open(path + 'bounds.csv') as csv_file:
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
        #print(head['modelname'])
        print(filename)
        return
    return head

def read_geoid(filename):
    f = open(path_geoids + filename, "r")
    f.readline()
    line = f.readline()
    geoid = {}
    '''
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
            except:
                print(geoid['modelname'])
                print(filename)
                print(str(rows) + ',' + str(cols))
                print("Unexpected error:" + str(i) + ',' + str(j))
                print(len(line))
                return
    return geoid

import csv