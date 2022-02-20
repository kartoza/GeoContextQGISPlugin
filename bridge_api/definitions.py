# coding=utf-8
"""This module contains definitions used by Bridge API Interface.
"""

# JUST EXAMPLES FOR NOW, WILL UPDATE

# Map type families definition
base_reference_map = {
    'key': 'base-reference-map',
    'endpoint': 'base-reference-map'
}
difference_map = {
    'key': 'difference-map',
    'endpoint': 'difference-map'
}

# Map types definition

# Difference map
DIFFERENCE_INSEASON_NDVI = {
    'key': 'DIFFERENCE_INSEASON_NDVI',
    'name': 'DIFFERENCE_INSEASON_NDVI',
    'map_family': difference_map
}

# NDVI (Normalized Difference Vegetation Index)
# https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index
INSEASON_NDVI = {
    'key': 'INSEASON_NDVI',
    'name': 'INSEASON_NDVI',
    'map_family': base_reference_map,
    'description': 'Provides the in-season Normalized Difference '
                   'Vegetation Index.',
    'difference_map': DIFFERENCE_INSEASON_NDVI
}

ARCHIVE_MAP_PRODUCTS = [
    INSEASON_NDVI,
]

BASIC_INSEASON_MAP_PRODUCTS = [
    INSEASON_NDVI,
]

DIFFERENCE_MAPS = [
    DIFFERENCE_INSEASON_NDVI,
]
