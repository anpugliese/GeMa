import numpy as np
import isg_reader
import isg_utils

p = (-22.5, -68, 456)

geoid = isg_reader.readfile("bolivia.isg")

q1, q2, q3, q4 = isg_utils.getQuadrant(p, geoid)

Np = isg_utils.interpolation(p, q1, q2, q3, q4, geoid, 'bilinear')
print(Np)

H = isg_utils.orthometric_height(p, Np)

print(H)