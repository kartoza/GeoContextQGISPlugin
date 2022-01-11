# coding: utf-8
import sys
import os

# Directory for third party modules
third_party_path = os.path.abspath(os.path.abspath(os.path.abspath(os.path.join(os.path.dirname(__file__), 'third_party'))))
if third_party_path not in sys.path:
    sys.path.append(third_party_path)

from itypes import itypes


class BaseTransport(itypes.Object):
    schemes = None

    def transition(self, link, decoders, params=None, link_ancestors=None, force_codec=False):
        raise NotImplementedError()  # pragma: nocover
