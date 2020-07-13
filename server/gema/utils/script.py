import os
script_dir = os.path.dirname(__file__)

import sys
print(sys.path)

print(script_dir)

import modules.isg_reader as isg_reader

isg_reader.populate_bounds()