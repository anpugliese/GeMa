import numpy as np
import isg_reader
import isg_utils

geoid = isg_reader.readfile("bolivia.isg")

q1, q2, q3, q4 = isg_utils.getQuadrant(-22.5, -68, geoid)