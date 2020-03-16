import numpy as np

def readfile(filename):
    f = open(filename, "r")
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
            geoid["grid"][i, j] = line[j]   
    return geoid

