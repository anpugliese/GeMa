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
    def test_conversion_single_point_non_existent(self):
        result = isg_utils.calculate_orthometric_height(self.far_point, 'GEOCOL2004', 'bilinear', 0)
        expect = None
        self.assertEqual(result, expect)

    # Test conversion of a single point of wrong coordinates
    def test_conversion_single_point_bad(self):
        result = isg_utils.calculate_orthometric_height(self.bad_point, 'GEOCOL2004', 'bilinear', 0)
        expect = None
        self.assertEqual(result, expect)

    # Test conversion from orthometric height to ellipsoidal height of a single point of good coordinates
    def test_conversion_single_point_ok_invert(self):
        ok_point_invert = (10.8896, -74.7808, 11.548)
        result = isg_utils.calculate_orthometric_height(ok_point_invert, 'GEOCOL2004', 'bilinear', 1)
        expect = 29.871 # not the same of ok_point because of approximation
        self.assertEqual(result, expect)

    # Test bilinear interpolation function
    def test_interpolation_function_ok(self):
        filename = isg_reader.get_filename_from_geoid_name('GEOCOL2004')
        geoid = isg_reader.read_geoid(filename)
        result = isg_utils.interpolation(self.ok_point, geoid, 'bilinear')
        expect = 18.322658062564187
        self.assertEqual(result, expect)

    # Test bilinear interpolation function for point outside geoid
    def test_interpolation_function_non_existent(self):
        filename = isg_reader.get_filename_from_geoid_name('GEOCOL2004')
        geoid = isg_reader.read_geoid(filename)
        result = isg_utils.interpolation(self.far_point, geoid, 'bilinear')
        expect = None
        self.assertEqual(result, expect)
    
    # Test bilinear interpolation point for point with bad coordinates
    def test_interpolation_function_bad(self):
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

    # Test orthometric height calculation for csv file
    def test_calculations_for_file(self):
        f = open(self.test_file)
        point_list = read_point_file(f)
        result = isg_utils.calculate_orthometric_height_list(point_list, 'EGG2015')
        expect = [
            [-6.081689834590001, 145.391998291, 1609.9536, 'Coordinates not in the geoid'],
            [66.133301,	-18.9167,	3.048,	-54.95],
            [49.950801849365234,	-125.27100372314453,	105.4608,	'Coordinates not in the geoid'],
            [48.74610137939453,	-69.09719848632812,	89.3064, 'Coordinates not in the geoid'],
            [47.81999969482422,	-83.3467025756836,	448.056, 'Coordinates not in the geoid'],
            [48.52000045776367,	-72.2656021118164,	178.6128, 'Coordinates not in the geoid'],
            [45.445099,	9.27674,	107.5944,	67.476],
            [32.5143055556,	-1.98305555556,	1106.424,	1066.209],
            [37.8567008972168,	-93.99909973144531,	283.7688, 'Coordinates not in the geoid'],
            [36.662799835205,	-121.60600280762,	25.908,	'Coordinates not in the geoid']
        ]
        self.assertEqual(result, expect)

    # Test list of available geoids for csv file
    def test_geoids_available_for_file(self):
        f = open(self.test_file)
        point_list = read_point_file(f)
        result = isg_utils.available_geoids_list(point_list)
        print(result)
        expect = [
            "AGP", "AGP2007", "EGG2008", "EGG2015", "EGG97", "EGG97Q", "G96SSS", "G99SS", "GEOID03u", "GEOID09u", 
            "GEOID12Bu", "GEOID90", "GEOID93", "GEOID96", "GEOID96u", "GEOID99u", "GEOMED", "GGEOID2016", "GGF97", 
            "ICEGEOID2011", "ITALGEO83", "ITALGEO90", "ITG2009", "MORGEO", "PNG08", "PNG94", "USAGEOID12A", 
            "USAUSGG2012", "USGG2003u", "USGG2009u", "USGG2012u"
        ]
        self.assertEqual(result, expect)

    


if __name__ == '__main__':
    unittest.main()
