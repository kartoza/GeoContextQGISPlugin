"""This module contains default values used by the plugin.
"""

# This is default Kartoza API URL endpoint
API_DEFAULT_URL = "https://staging.geocontext.kartoza.com/api/v2/"

# Registry keys
SERVICE = {
    'name': 'Service',
    'key': 'service'
}
GROUP = {
    'name': 'Group',
    'key': 'group'
}
COLLECTION = {
    'name': 'Collection',
    'key': 'collection'
}

COORDINATE_SYSTEM = "EPSG:4326"

# JSON response variables
VALUE_JSON = 'value'
KEY_JSON = 'key'
NAME_JSON = 'name'
SERVICE_JSON = 'services'
GROUP_JSON = 'groups'
COLLECTION_JSON = 'collections'

# Processing tool parameters names
TOOL_INPUT_POINT_LAYER = 'Input point layer'
TOOL_REGISTRY = 'Registry'
TOOL_KEY = 'Key'
TOOL_FIELD_NAME = 'Field name'
TOOL_OUTPUT_POINT_LAYER = 'Output point layer'

# Graphs
PLOT_LINE_WIDTH = 2
PLOT_LIMITS_BUFFER = 0.01  # Increase graph limits: {Value} + {Value} * PLOT_LIMITS_BUFFER

# Docking widget table
TABLE_DATA_TYPE = {
    'table': 'Data type',
    'file': 'data_type'
}
TABLE_VALUE = {
    'table': 'Value',
    'file': 'value'
}
TABLE_LONG = {
    'table': 'Longitude',
    'file': 'long'
}
TABLE_LAT = {
    'table': 'Latitude',
    'file': 'lat'
}
