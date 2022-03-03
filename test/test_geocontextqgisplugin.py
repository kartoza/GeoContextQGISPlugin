from __future__ import print_function

from builtins import str
from builtins import range
__author__ = 'Divan Vermeulen <divan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '12/01/2021'
__license__ = "GPL"
__copyright__ = ''

import os
import unittest

from qgis.core import QgsProject, QgsCoordinateTransform, QgsPoint, QgsCoordinateReferenceSystem, QgsVectorLayer

from GeoContextQGISPlugin import (
    is_float,
    apply_decimal_places_to_float_panel,
    apply_decimal_places_tofloat_tool,
    get_canvas_crs,
    get_request_crs,
    transform_point_coordinates,
    transform_xy_coordinates,
    convert_multipart_to_singlepart,
    process_points_layer,
    point_request_panel,
    point_request_dialog,
    canvas_click,
    create_new_field,
)

#from utilities_for_testing import get_qgis_app

#QGIS_APP = get_qgis_app()

# For tests only to ensure sentry logging is on
# Normaly this is configured via QSettings
#os.environ['SENTRY'] = '1'

# These needs to be set prior to processing as its required by some tests
ENDPOINT_URL = "https://staging.geocontext.kartoza.com/api/v2/"
SCHEMA_CONFIG = "https://geocontext.kartoza.com/docs"

# Directories used for testing
TEMP_DIR = os.path.join(
    os.path.expanduser('~'),
    'temp',
    'geocontext-qgis-plugin')
__file__ = "C:/Users/Divan/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/GeoContextQGISPlugin/test/"
DATA_TEST_DIR = os.path.join(os.path.dirname(__file__), 'data')


def duplicate_layer(input_layer, geom_type):
    """Duplicates a layer to memory.

    :param input_layer: Directory of the input layer
    :type input_layer: String

    :param geom_type: Geometry type of the layer. Point, Polygon, or Polyline
    :type geom_type: String

    :returns: Returns the coordinate system set in the options dialog.
    :rtype: QgsCoordinateReferenceSystem
    """

    layer = QgsVectorLayer(input_layer, geom_type, "ogr")
    attr = layer.dataProvider().fields().toList()
    feats = [feat for feat in layer.getFeatures()]

    dup_layer = QgsVectorLayer(
        geom_type +
        "?crs=epsg:4326",
        "duplicated_layer",
        "memory")
    dup_layer_data = dup_layer.dataProvider()
    dup_layer_data.addAttributes(attr)
    dup_layer.updateFields()
    dup_layer_data.addFeatures(feats)

    return dup_layer


# noinspection PyUnresolvedReferences,PyStatementEffect
class TestGeocontextMethods(unittest.TestCase):
    """Class for testing the geocontext plugin."""

    def test_is_float(self):
        """The is_float method checks if a string can be converted to a float. This method
        checks whether this is done correctly for a float string, integer string and a text string.
        """

        # Tests a float type. This should return True
        value_str_float = "1.333252525"
        expected = True
        result = is_float(value_str_float)
        msg = "Expected %s but got %s for %s" % (
            str(expected), str(result), value_str_float)
        self.assertEqual(expected, result, msg)

        # Tests an integer type. This should return False
        value_str_int = '5'
        expected = False
        result = is_float(value_str_int)
        msg = "Expected %s but got %s for %s" % (
            str(expected), str(result), value_str_int)
        self.assertEqual(expected, result, msg)

        # Tests a text string, this should return False
        value_str_text = "hello world"
        expected = False
        result = is_float(value_str_text)
        msg = "Expected %s but got %s for %s" % (
            str(expected), str(result), value_str_text)
        self.assertEqual(expected, result, msg)

    def test_apply_decimal_places_panel(self):
        """The apply_decimal_places_to_float_panel method rounds the provided numeric value.
        This method checks if the expected rounding is performed by those methods.
        """

        rounding_factor = 3

        # Test if a float is correctly rounded
        value_float = "5.2349"
        expected = "5.235"
        result = apply_decimal_places_to_float_panel(
            value_float, rounding_factor)
        msg = "Expected %s but got %s for %s" % (
            str(expected), str(result), value_float)
        self.assertEqual(expected, result, msg)

        # An integer should not change
        value_int = "10"
        expected = "10"
        result = apply_decimal_places_to_float_panel(
            value_int, rounding_factor)
        msg = "Expected %s but got %s for %s" % (
            str(expected), str(result), value_int)
        self.assertEqual(expected, result, msg)

        # A string should not change
        value_string = "hello world"
        expected = "hello world"
        result = apply_decimal_places_to_float_panel(
            value_string, rounding_factor)
        msg = "Expected %s but got %s for %s" % (
            str(expected), str(result), value_string)
        self.assertEqual(expected, result, msg)

    def test_apply_decimal_places_tool(self):
        """The apply_decimal_places_to_float_tool method rounds the provided numeric value.
        This method checks if the expected rounding is performed by those methods.
        """

        rounding_factor = 3

        # Test if a float is correctly rounded
        value_float = "5.2349"
        expected = "5.235"
        result = apply_decimal_places_to_float_tool(
            value_float, rounding_factor)
        msg = "Expected %s but got %s for %s" % (
            str(expected), str(result), value_float)
        self.assertEqual(expected, result, msg)

        # An integer should not change
        value_int = "10"
        expected = "10"
        result = apply_decimal_places_to_float_tool(value_int, rounding_factor)
        msg = "Expected %s but got %s for %s" % (
            str(expected), str(result), value_int)
        self.assertEqual(expected, result, msg)

        # A string should not change
        value_string = "hello world"
        expected = "hello world"
        result = apply_decimal_places_to_float_tool(
            value_string, rounding_factor)
        msg = "Expected %s but got %s for %s" % (
            str(expected), str(result), value_string)
        self.assertEqual(expected, result, msg)

    def test_get_crs(self):
        print("unsure how to test this")

    def test_get_request_crs(self):
        print("unsure how to test this")

    def test_transform_point_coordinates(self):
        """The transform_point_coordinates method projects a provided point to that of the target crs.
        This method checks if this is done correctly. Two point sets are tested: LO19 and Albers equal
        area conic.
        """

        # LO19 coordinates
        coor_x = 35849.01050597087
        coor_y = 3707901.257585528
        pt = QgsPoint(coor_x, coor_y)

        # WGS84 coordinates
        expected_x = 18.614221314233806
        expected_y = -33.496683441230125

        crs_wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")  # WGS84
        crs_lo19 = QgsCoordinateReferenceSystem("EPSG:2048")  # Lo19

        result = transform_point_coordinates(pt, crs_lo19, crs_wgs84)

        result_x = result.x()
        msg = "Expected %s but got %s for %s" % (
            str(expected_x), str(result_x), " x-coordinate")
        self.assertEqual(expected_x, result_x, msg)

        result_y = result.y()
        msg = "Expected %s but got %s for %s" % (
            str(expected_y), str(result_y), " y-coordinate")
        self.assertEqual(expected_y, result_y, msg)

        # Albers equal area conic projection (Africa)
        coor_x = -601965.4575143828
        coor_y = -3799932.048690163
        pt = QgsPoint(coor_x, coor_y)

        expected_x = 19.10091791681273
        expected_y = -33.59383770600347

        crs_wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")  # WGS84
        crs_albers = QgsCoordinateReferenceSystem("ESRI:102022")  # Albers

        result = transform_point_coordinates(pt, crs_albers, crs_wgs84)

        result_x = result.x()
        msg = "Expected %s but got %s for %s" % (
            str(expected_x), str(result_x), " x-coordinate")
        self.assertEqual(expected_x, result_x, msg)

        result_y = result.y()
        msg = "Expected %s but got %s for %s" % (
            str(expected_y), str(result_y), " y-coordinate")
        self.assertEqual(expected_y, result_y, msg)

    def test_transform_xy_coordinates(self):
        """The transform_xy_coordinates method projects provided xy-coordinates to that of the target crs.
        This method checks if this is done correctly. Two point sets are tested: LO19 and Albers equal
        area conic.
        """

        # LO19 coordinates
        coor_x = 35849.01050597087
        coor_y = 3707901.257585528

        # WGS84 coordinates
        expected_x = 18.614221314233806
        expected_y = -33.496683441230125

        crs_wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")  # WGS84
        crs_lo19 = QgsCoordinateReferenceSystem("EPSG:2048")  # Lo19

        result_x, result_y = transform_point_coordinates(
            coor_x, coor_y, crs_lo19, crs_wgs84)

        msg = "Expected %s but got %s for %s" % (
            str(expected_x), str(result_x), " x-coordinate")
        self.assertEqual(expected_x, result_x, msg)

        msg = "Expected %s but got %s for %s" % (
            str(expected_y), str(result_y), " y-coordinate")
        self.assertEqual(expected_y, result_y, msg)

        # Albers equal area conic projection (Africa)
        coor_x = -601965.4575143828
        coor_y = -3799932.048690163

        expected_x = 19.10091791681273
        expected_y = -33.59383770600347

        crs_wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")  # WGS84
        crs_albers = QgsCoordinateReferenceSystem("ESRI:102022")  # Albers

        result_x, result_y = transform_point_coordinates(
            coor_x, coor_y, crs_albers, crs_wgs84)

        msg = "Expected %s but got %s for %s" % (
            str(expected_x), str(result_x), " x-coordinate")
        self.assertEqual(expected_x, result_x, msg)

        msg = "Expected %s but got %s for %s" % (
            str(expected_y), str(result_y), " y-coordinate")
        self.assertEqual(expected_y, result_y, msg)

    def test_convert_multipart_to_singlepart(self):
        """The convert_multipart_to_singlepart function converts all multipoints stored in a
        layer to singlepart. Each point will be an individual feature. This test checks if the provided
        layer has the same number of features as expected after a multipoint layer has been coverted.
        """

        layer_duplicate = duplicate_layer(
            DATA_TEST_DIR +
            "/wgs84/points_multipoint_wgs84.gpkg",
            "Multipoint")

        convert_multipart_to_singlepart(layer_duplicate)

        expected = 20  # Number of features expected after conversion
        # Number of feature for converted layer
        feat_count = layer_duplicate.featureCount()
        msg = "Expected %s but got %s for %s" % (str(expected), str(
            feat_count), " for multipart to singlepart conversion")
        self.assertEqual(expected, feat_count, msg)

    def test_process_points_layer(self):
        """The process_points_layer method does requests for each of the points provided in a layer and
        outputs the result to a newly created file based on the parameters provided by the user.
        This method tests whether processing is done correctly and the output files are as it should be.
        """

        # Service registry option test
        layer_dir = DATA_TEST_DIR + "/wgs84/points_wgs84.gpkg"
        layer_point = duplicate_layer(layer_dir, "Point")
        selected_features = False
        registry = "Service"
        key_name = "altitude"  # DEM altitude of South Africa
        field_name = "TEST_field"
        output_file = TEMP_DIR + "service_test.gpkg"
        load_output_file = False

        process_points_layer(
            layer_point,
            selected_features,
            registry,
            key_name,
            field_name,
            output_file,
            load_output_file)
        result_layer = QgsVectorLayer(output_file, "service_test.gpkg")

        feat_count = result_layer.featureCount()
        expected = 16
        msg = "Expected %s but got %s for %s" % (
            str(expected), str(feat_count), " for singlepart processing")
        self.assertEqual(expected, feat_count, msg)

        result_field_name = field_name
        list_expected = [
            168,
            88,
            27,
            195,
            1219,
            899,
            183,
            183,
            122,
            91,
            152,
            396,
            99,
            274,
            146,
            158]

        index_expected = 0
        for feat in result_layer.getFeatures():
            result_field_index = feat.fieldNameIndex(result_field_name)
            list_attributes = feat.attributes()
            result_value = list_attributes(result_field_index)
            expected = list_expected[index_expected]

            msg = "Expected %s but got %s for %s" % (
                str(expected), str(result_value), " when processing " + layer_dir)
            self.assertEqual(str(expected), str(result_value), msg)

            index_expected = index_expected + 1

        # Group registry option test
        registry = "Group"
        key_name = "rainfall_group"
        output_file = TEMP_DIR + "group_test.gpkg"
        layer_dir = DATA_TEST_DIR + "/projected/points_multipoint_lo19.gpkg"
        layer_point = duplicate_layer(layer_dir, "Point")

        process_points_layer(
            layer_point,
            selected_features,
            registry,
            key_name,
            field_name + "_",
            output_file,
            load_output_file)
        result_layer = QgsVectorLayer(output_file, "group_test.gpkg")

        feat_count = result_layer.featureCount()
        expected = 12
        msg = "Expected %s but got %s for %s" % (
            str(expected), str(feat_count), " for multipart processing")
        self.assertEqual(expected, feat_count, msg)

        result_field_name = field_name + "_monthly_precipitation_january"
        list_expected = [13, 13, 13, 13, 13, 12, 16, 19, 19, 17, 15, 17]

        index_expected = 0
        for feat in result_layer.getFeatures():
            result_field_index = feat.fieldNameIndex(result_field_name)
            list_attributes = feat.attributes()
            result_value = list_attributes(result_field_index)
            expected = list_expected[index_expected]

            msg = "Expected %s but got %s for %s" % (
                str(expected), str(result_value), " when processing " + layer_dir)
            self.assertEqual(str(expected), str(result_value), msg)

            index_expected = index_expected + 1

        # Collection registry option test
        registry = "Collection"
        key_name = "global_climate_collection"
        output_file = TEMP_DIR + "collection_test.gpkg"
        layer_dir = DATA_TEST_DIR + "/wgs84/points_wgs84_broken_geom.gpkg"
        layer_point = duplicate_layer(layer_dir, "Point")

        process_points_layer(
            layer_point,
            selected_features,
            registry,
            key_name,
            field_name + "_",
            output_file,
            load_output_file)
        result_layer = QgsVectorLayer(output_file, "collection_test.gpkg")

        feat_count = result_layer.featureCount()
        expected = 10
        msg = "Expected %s but got %s for %s" % (str(expected), str(
            feat_count), " for singlepart, broken geometry processing")
        self.assertEqual(expected, feat_count, msg)

        result_field_name = field_name + "_yearly_bioclimatic_variables_01"
        list_expected = [
            17.129,
            17.217,
            None,
            17.688,
            None,
            17.483,
            17.746,
            17.462,
            17.542,
            17.996]

        index_expected = 0
        for feat in result_layer.getFeatures():
            result_field_index = feat.fieldNameIndex(result_field_name)
            list_attributes = feat.attributes()
            result_value = list_attributes(result_field_index)
            expected = list_expected[index_expected]

            msg = "Expected %s but got %s for %s" % (
                str(expected), str(result_value), " when processing " + layer_dir)
            self.assertEqual(str(expected), str(result_value), msg)

            index_expected = index_expected + 1

    def test_point_request_panel(self):
        """The point_request_panel method does a point request received by the docking panel
        when the user clicks in the QGIS canvas. This method tests that method for each of the
        registry types: Service, Group and Collection
        """

        # Service
        x = 18.866224412852137
        y = -33.592286339921415
        registry = "Service"
        key = "monthly_max_temperature_september"

        data = point_request_panel(x, y, registry, key, ENDPOINT_URL)
        result_value = data['value']
        expected = 20.9

        msg = "Expected %s but got %s for %s" % (str(expected), str(
            result_value), " when performing a panel request")
        self.assertEqual(str(expected), str(result_value), msg)

        # Group
        x = 18.918032080206356
        y = -33.540173724197835
        registry = "Group"
        key = "monthly_precipitation_group"

        data = point_request_panel(x, y, registry, key, ENDPOINT_URL)
        list_dict_services = data["services"]  # Service files for a group
        list_expected = [22, 23, 32, 53, 83, 94, 100, 82, 44, 22, 16, 15]

        index_expected = 0
        for dict_service in list_dict_services:
            result_value = dict_service['value']
            expected = list_expected[index_expected]

            msg = "Expected %s but got %s for %s" % (str(expected), str(
                result_value), " when performing a panel request")
            self.assertEqual(str(expected), str(result_value), msg)

            index_expected = index_expected + 1

        # Collection
        x = 19.070338116250714
        y = -33.57988917992912
        registry = "Collection"
        key = "sa_land_cover_land_use_collection"

        data = point_request_panel(x, y, registry, key, ENDPOINT_URL)
        # Each group contains a list of the 'Service' data associated with the
        # group
        list_dict_groups = data["groups"]
        list_expected = [81.9, 213, 277, "Protected Area",
                         5, 4, "FRs 9  Swartland Shale Renosterveld"]

        index_expected = 0
        for dict_group in list_dict_groups:
            # Service files for a group
            list_dict_services = dict_group["services"]
            for dict_service in list_dict_services:
                result_value = dict_service['value']
                expected = list_expected[index_expected]

                index_expected = index_expected + 1

                msg = "Expected %s but got %s for %s" % (str(expected), str(
                    result_value), " when performing a panel request")
                self.assertEqual(str(expected), str(result_value), msg)

    def test_point_request_dialog(self):
        """The point_request_dialog method does a point request received by the processing tool
        when the user clicks in the QGIS canvas. This method tests that method for each of the
        registry types: Service, Group and Collection.
        """

        # Service
        x = 18.866224412852137
        y = -33.592286339921415
        registry = "Service"
        key = "monthly_max_temperature_september"

        data = point_request_dialog(x, y, registry, key, ENDPOINT_URL)
        result_value = data['value']
        expected = 20.9

        msg = "Expected %s but got %s for %s" % (str(expected), str(
            result_value), " when performing a panel request")
        self.assertEqual(str(expected), str(result_value), msg)

        # Group
        x = 18.918032080206356
        y = -33.540173724197835
        registry = "Group"
        key = "monthly_precipitation_group"

        data = point_request_dialog(x, y, registry, key, ENDPOINT_URL)
        list_dict_services = data["services"]  # Service files for a group
        list_expected = [22, 23, 32, 53, 83, 94, 100, 82, 44, 22, 16, 15]

        index_expected = 0
        for dict_service in list_dict_services:
            result_value = dict_service['value']
            expected = list_expected[index_expected]

            msg = "Expected %s but got %s for %s" % (str(expected), str(
                result_value), " when performing a panel request")
            self.assertEqual(str(expected), str(result_value), msg)

            index_expected = index_expected + 1

        # Collection
        x = 19.070338116250714
        y = -33.57988917992912
        registry = "Collection"
        key = "sa_land_cover_land_use_collection"

        data = point_request_dialog(x, y, registry, key, ENDPOINT_URL)
        # Each group contains a list of the 'Service' data associated with the
        # group
        list_dict_groups = data["groups"]
        list_expected = [81.9, 213, 277, "Protected Area",
                         5, 4, "FRs 9  Swartland Shale Renosterveld"]

        index_expected = 0
        for dict_group in list_dict_groups:
            # Service files for a group
            list_dict_services = dict_group["services"]
            for dict_service in list_dict_services:
                result_value = dict_service['value']
                expected = list_expected[index_expected]

                index_expected = index_expected + 1

                msg = "Expected %s but got %s for %s" % (str(expected), str(
                    result_value), " when performing a panel request")
                self.assertEqual(str(expected), str(result_value), msg)

    def test_canvas_click(self):
        print("unsure how to perform this test")

    def test_create_new_field(self):
        """The create_new_field method adds a new field to the attribute of the
        provided feature. This method tests if the field are correctly added to
        the feature.
        """

        layer_dir = DATA_TEST_DIR + "/wgs84/points_multipoint_wgs84.gpkg"
        layer_duplicate = duplicate_layer(layer_dir, "Point")
        for feat in layer_duplicate.getFeatures():
            index_new_field = create_new_field(
                layer_duplicate, feat, "testing_field")

            result = feat.fieldNameIndex(index_new_field)
            msg = "Expected True but got False when testing the create_new_field method."
            self.assertTrue(result, msg)


if __name__ == '__main__':
    unittest.main()
