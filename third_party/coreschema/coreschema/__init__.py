import sys
import os

# Directory for third party modules
third_party_path = os.path.abspath(os.path.abspath(os.path.abspath(os.path.join(os.path.dirname(__file__)))))
if third_party_path not in sys.path:
    sys.path.append(third_party_path)

from coreschema.coreschema.schemas import (
    Object, Array, Integer, Number, String, Boolean, Null,
    Enum, Anything, Ref, RefSpace,
    Union, Intersection, ExclusiveUnion, Not
)
from coreschema.coreschema.encodings.html import render_to_form


__version__ = '0.0.4'

__all__ = [
    Object, Array, Integer, Number, String, Boolean, Null,
    Enum, Anything, Ref, RefSpace,
    Union, Intersection, ExclusiveUnion, Not,
    render_to_form
]
