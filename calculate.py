import numpy as np
import isg_reader
import isg_utils

p = (-22.5, -68, 456) #bolivia
p2 = (7.042560, -75.121684, 29) #colombia
p3 = (-27.177390, -64.054582, 93) #argentina
p4 = (45.471976, 9.168189, 13) #italia

#isg_reader.populate_bounds()

p = p4

#print(isg_utils.available_geoids(p))

geoid = isg_reader.read_geoid("geoids/EGG2015_20170713.isg")

#q1, q2, q3, q4 = isg_utils.getQuadrant(p, geoid)

Np = isg_utils.interpolation(p, geoid, 'bilinear')
if Np == None:
    print('out of bounds')

H = isg_utils.orthometric_height(p, Np)
print(H)
