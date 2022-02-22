"""Utilities module."""

import os
import sys

from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsProject,
                       QgsSettings,
                       QgsVectorFileWriter,
                       QgsVectorLayer,
                       QgsField,
                       QgsCoordinateTransform,
                       QgsPointXY,
                       QgsFeature,
                       QgsCoordinateReferenceSystem)

# Core API module
from coreapi.client import Client
from coreapi import exceptions as coreapi_exceptions


def get_canvas_crs(iface):
    """Returns the coordinate system of the canvas (e.g. EPSG:4326 (WGS84)).

    :returns: The coordinate system of the QGIS canvas.
    :rtype: QgsCoordinateReferenceSystem
    """

    map_canvas = iface.mapCanvas()  # QgsMapCanvas
    crs = map_canvas.mapSettings().destinationCrs()  # QgsCoordinateReferenceSystem

    return crs


def get_request_crs():
    """Transforms the XY coordinates to the WGS84 coordinate system (EPSG:4326).

    :returns: Returns the coordinate system set in the options dialog.
    :rtype: QgsCoordinateReferenceSystem
    """

    # Gets the coordinate system set by the user. Defaults to WGS84
    # NOTE: At the moment only WGS84 is selectable
    settings = QgsSettings()
    request_crs = settings.value('geocontext-qgis-plugin/request_crs', "WGS84 (EPSG:4326)", type=str)

    if request_crs == "WGS84 (EPSG:4326)":  # WGS84 coordinate system
        return QgsCoordinateReferenceSystem("EPSG:4326")
    else:  # Unknown coordinate system
        return


def transform_point_coordinates(point, cur_crs, target_crs):
    """Transforms point coordinates to the target coordinate system.

    :param point: The point which will be transformed
    :type point: QgsPoint

    :param cur_crs: The current coordinate system of the coordinates
    :type cur_crs: QgsCoordinateReferenceSystem

    :param target_crs: The target coordinate system to which the coordinates will be transformed to
    :type target_crs: QgsCoordinateReferenceSystem

    :returns: The transformed point.
    :rtype: QgsPointXY
    """

    transform_context = QgsProject.instance().transformContext()
    xform = QgsCoordinateTransform(cur_crs, target_crs, transform_context)

    pt = xform.transform(QgsPointXY(point.x(), point.y()))  # Transformed point

    return pt


def transform_xy_coordinates(x, y, cur_crs, target_crs):
    """Transforms the XY coordinates to the target coordinate system.

    :param x: The longitude coordinate value
    :type x: Float

    :param y: The latitude coordinate value
    :type y: Float

    :param cur_crs: The current coordinate system of the coordinates
    :type cur_crs: QgsCoordinateReferenceSystem

    :param target_crs: The target coordinate system to which the coordinates will be transformed to
    :type target_crs: QgsCoordinateReferenceSystem

    :returns: The XY coordinates in WGS84.
    :rtype: Float
    """

    transform_context = QgsProject.instance().transformContext()
    xform = QgsCoordinateTransform(cur_crs, target_crs, transform_context)

    pt = xform.transform(QgsPointXY(x, y))  # Transformed point
    x = pt.x()
    y = pt.y()

    return x, y


def is_float(value):
    """Checks whether a string value can be converted to a float

    :param value: The string value to be checked
    :type value: str

    :returns: True if the value can be converted to a float; False if not
    :rtype: Boolean
    """

    try:
        float(value)
        return True
    except ValueError:
        return False


def apply_decimal_places_to_float_panel(value, rounding_factor):
    """Applies the rounding factor the provided value. This method retrieves the rounding factor
    set for the docking panel in the options dialog.

    :param value: The string value to be checked
    :type value: String or numeric

    :param rounding_factor: The factor used for when the value is rounded
    :type rounding_factor: Integer

    :returns: Value rounded using the rounding factor if float; otherwise the origin value is returned
    :rtype: String
    """

    if value is not None:
        if value.isdigit():  # Integer
            return value  # Number has no decimal values
        else:  # Either string or float
            if is_float(value):  # Float
                value_float = float(value)
                value_rounded = round(value_float, rounding_factor)
                value_str = str(value_rounded)

                return value_str

    return value  # String, therefore no rounding required


def apply_decimal_places_to_float_tool(value, rounding_factor):
    """Applies the rounding factor the provided value. This method retrieves the rounding factor
    set for the processing tool in the options dialog.

    :param value: The string value to be checked
    :type value: String or numeric

    :param rounding_factor: The factor used for when the value is rounded
    :type rounding_factor: Integer

    :returns: Value rounded using the rounding factor if float; otherwise the origin value is returned
    :rtype: String
    """

    if value is not None:
        if value.isdigit():  # Integer
            return value  # Number has no decimal values
        else:  # Either string or float
            if is_float(value):  # Float
                value_float = float(value)
                value_rounded = round(value_float, rounding_factor)
                value_str = str(value_rounded)

                return value_str

    return value  # String, therefore no rounding required


def point_request_dialog(x, y, registry, key, api_url):
    """Return the value rettrieved from the ordered dictionary containing the requested data
    from the server. This method is used by the processing dialog of the plugin.

    This method requests the data from the server for the given point coordinates.

    :param x: Longitude coordinate
    :type x: Numeric

    :param y: Latitude coordinate
    :type y: Numeric

    :param registry: Registry option selected by the user
    :type registry: String

    :param key: Key of the requested data
    :type key: Sorted dictionary

    :param api_url: Endpoint URL provided by the user
    :type api_url: String

    :returns: The data retrieved for the request for the provided location
    :rtype: OrderedDict
    """

    # Performs the request from the server based on the above information
    client = Client()

    url_request = api_url + "query?" + 'registry=' + registry.lower() + '&key=' + key + '&x=' + str(x) + '&y=' + str(y) + '&outformat=json'
    data = client.get(url_request)

    return data


def process_point(input_point, registry, key_name, field_name):
    """
    This method processes a point layer provided by the user.
    The methods takes the point layer provided by the user, and then
    requests the selected registry/key in the processing dialog.
    A new file is created which stores the original attributes with the
    newly requested data. The method will only process the selected features
    if enabled by the user, and the layer can also be loaded into QGIS once
    processing is done.

    :param input_point: The point layer which will be processed.
    :type input_point: QgsPoint

    :param registry: The registry option selected by the user
    :type registry: String

    :param key_name: Key of the requested data
    :type key_name: String

    :param field_name: The fieldname or prefix which will be used for the new attribute fields
    :type field_name: String

    :param layer_crs: Coordinate system used by the input point
    :type layer_crs: QgsCoordinate

    :param target_crs: Coordinate system required by the API
    :type target_crs: QgsCoordinate
    """

    settings = QgsSettings()
    rounding_factor = settings.value('geocontext-qgis-plugin/dec_places_tool', 3, type=int)
    api_url = settings.value('geocontext-qgis-plugin/url')  # Base URL. Set in the options dialog

    # input_type = input_points.wkbType()  # Vector type for input
    # if input_type == 4:  # If a multipoint layer, otherwise skipped
    #     self.convert_multipart_to_singlepart(input_new)  # Splits all multipart features into singlepart features

    # The user selected the 'Service' registry option
    if registry == 'Service':
        print("service")
    elif registry == 'Group':
        print("group")
    elif registry == 'Collection':
        print('Collection')
    else:
        print("Unknown registry")


def create_vector_file(input_layer, output_layer, layer_crs):
    """
    Creates a new geopackage from an existing layer.

    :param input_layer: The point layer which will be copied.
    :type input_layer: QgsVectorLayer

    :param output_layer: Output directory and filename
    :type output_layer: String

    :param layer_crs: Coordinate system for output vector file
    :type layer_crs: QgsCoordinateReferenceSystem
    """
    status_index, msg = QgsVectorFileWriter.writeAsVectorFormat(input_layer, output_layer, 'UTF-8', layer_crs)
    if status_index == 2:  # File already exists and cannot be overwritten (locked)
        error_msg = "File creation error: " + msg
        return error_msg


def convert_multipart_to_singlepart(mp_layer):
    """If a vector file has multiple parts for a feature, each part is split into a feature.
    This is done so that each point can have its own attribute data, as the parts might be at different
    coordinates. The provided layer will directly be edited and no longer required multipart features
    will be removed.

    This method is aimed at point layers for this plugin, but will work for other multipart vector types.

    :param mp_layer: A vector layer.
    :type mp_layer: QgsVectorLayer
    """

    feature_count = mp_layer.featureCount()  # Total number of feature of the layer
    features_to_remove = []  # Multipart features which will be removed when split into multiple features

    # Skips this step if the layer is empty
    if feature_count > 0:
        mp_layer.startEditing()  # Editing is performed on the mp_layer
        for mp_feat in mp_layer.getFeatures():  # All features
            geom = mp_feat.geometry()  # Feature geometry
            if geom.isMultipart():  # Checked if the geometry is multipart
                new_features = []
                temp_feature = QgsFeature(mp_feat)  # Clone of the feature
                features_to_remove.append(mp_feat.id())  # Feature will be removed

                for mp_part in geom.asGeometryCollection():  # Adds each part as a separate feature
                    temp_feature.setGeometry(mp_part)
                    new_features.append(QgsFeature(temp_feature))
                mp_layer.addFeatures(new_features)  # Adds the new features to the layer

        # Removes all of the multipart features which has been split into separate features
        for feat_to_remove_id in features_to_remove:
            mp_layer.deleteFeature(feat_to_remove_id)

        # Gives each singlepart feature a unique ID (fid/oid)
        new_index = 0
        for new_feat in mp_layer.getFeatures():
            mp_layer.changeAttributeValue(new_feat.id(), 0, new_index)

            new_index = new_index + 1

        mp_layer.commitChanges()  # Applies the changes to the layer


def create_new_field(input_layer, input_feat, field_name):
    """Return index of the field in the input layer attribute table.

    :param input_layer: Layer being processed.
    :type input_layer: QgsVectorLayer

    :param input_feat: Used to retrieve the field index
    :type input_feat: QgsFeature

    :param field_name: Field name which needs to be retrieved
    :type field_name: String

    :returns: The index of the field name, -1 if the attribute table does not contain the field
    :rtype: Integer
    """

    field_index = input_feat.fieldNameIndex(field_name)
    if field_index == -1:  # Checks if the field does not exist in the attribute table
        input_layer.startEditing()
        new_field = QgsField(field_name, QVariant.String)
        input_layer.addAttribute(new_field)
        input_layer.updateFields()
        input_layer.commitChanges()
        field_index = input_feat.fieldNameIndex(field_name)
    return field_index
