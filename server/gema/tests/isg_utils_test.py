import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import utils.modules.isg_utils as isg_utils
import utils.modules.isg_reader as isg_reader

def read_point_file(file):    
    point_list = []
    f = file
    
  
    while True: 
        line = f.readline()
        if not line:  
            break
        line = str(line).strip("\\rn'b")
        line_split = line.split(",")
        point_list.append([float(line_split[0]), float(line_split[1]), float(line_split[2])])
    
    f.close() 
    return point_list

class TestIsgUtils(unittest.TestCase):

    # Airport Ernesto Cortissoz in Barranquilla, Colombia
    ok_point = (10.8896, -74.7808, 29.8704)

    # Point in the middle of the ocean
    far_point = (-39.963555, 79.005367, 123)

    # Bad point 
    bad_point = (12121212.963555, -131212.005367, 123)

    # test file
    test_file = 'airports.csv'

    # Test available geoids for a single point contained in the geoid
    def test_single_point_ok(self):
        expected = ['GEOCOL2004', 'GEOID2015', 'QGEOCOL2004', 'SOUTHAMERICA']
        result = isg_utils.available_geoids(self.ok_point)
        self.assertEqual(result, expected)

    # Test available geoids for a single point that is not contained in the geoid
    def test_single_point_non_existent(self):
        expected = []
        result = isg_utils.available_geoids(self.far_point)
        self.assertEqual(result, expected)

    # Test available geoids for a single point with wrong coordinates
    def test_single_point_error(self):
        expected = []
        result = isg_utils.available_geoids(self.bad_point)
        self.assertEqual(result, expected)
    
    # Test indices of the quadrants of a single point in a geoid
    def test_get_quadrant(self): 
        filename = isg_reader.get_filename_from_geoid_name('GEOCOL2004')
        geoid = isg_reader.read_geoid(filename)
        result = isg_utils.getQuadrant(self.ok_point, geoid)
        expect = ((476,156),(476,157),(477,156),(477,157))
        self.assertEqual(result, expect)
    
    # Test correct conversion of a single point
    def test_conversion_single_point_ok(self):
        result = isg_utils.calculate_orthometric_height(self.ok_point, 'GEOCOL2004', 'bilinear', 0)
        expect = 11.548
        self.assertEqual(result, expect)
    
    # Test correct conversion of a single point
    def test_interpolation_single_point_non_existent(self):
        result = isg_utils.calculate_orthometric_height(self.far_point, 'GEOCOL2004', 'bilinear', 0)
        expect = None
        self.assertEqual(result, expect)

    def test_interpolation_single_point_bad(self):
        result = isg_utils.calculate_orthometric_height(self.bad_point, 'GEOCOL2004', 'bilinear', 0)
        expect = None
        self.assertEqual(result, expect)

    def test_interpolation_single_point_ok_invert(self):
        ok_point_invert = (10.8896, -74.7808, 11.548)
        result = isg_utils.calculate_orthometric_height(ok_point_invert, 'GEOCOL2004', 'bilinear', 1)
        expect = 29.871 # not the same of ok_point because of approximation
        self.assertEqual(result, expect)

    def test_interpolation_function_ok(self):
        filename = isg_reader.get_filename_from_geoid_name('GEOCOL2004')
        geoid = isg_reader.read_geoid(filename)
        result = isg_utils.interpolation(self.ok_point, geoid, 'bilinear')
        expect = 18.322658062564187
        self.assertEqual(result, expect)

    def test_interpolation_function_non_existent(self):
        filename = isg_reader.get_filename_from_geoid_name('GEOCOL2004')
        geoid = isg_reader.read_geoid(filename)
        result = isg_utils.interpolation(self.far_point, geoid, 'bilinear')
        expect = None
        self.assertEqual(result, expect)
    
    def test_interpolation_function_far(self):
        filename = isg_reader.get_filename_from_geoid_name('GEOCOL2004')
        geoid = isg_reader.read_geoid(filename)
        result = isg_utils.interpolation(self.bad_point, geoid, 'bilinear')
        expect = None
        self.assertEqual(result, expect)

    # Test for a point that is in the last quadrant of the geoid
    def test_extremal_value(self):
        #Airport in Kazijistan - extremal value in the Europe geoid
        extremal_point = (37.988, 69.805, 698.9064)
        result = isg_utils.calculate_orthometric_height(extremal_point, 'EGG2015', 'bilinear', 0)
        expect = 707.032
        self.assertEqual(result, expect)

    def test_geoids_for_file(self):
        f = open(self.test_file)
        point_list = read_point_file(f)
        print(point_list)
    


if __name__ == '__main__':
    unittest.main()
