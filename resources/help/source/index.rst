
GeoContext QGIS plugin documentation
======================================

A QGIS plugin which retrieves data for a geographic position. Data is fetched from
a GeoContext data server which can make use of WMS and WFS. The plugin allows the user to
click in the QGIS map canvas, which will fetch the information for the location. Results are
shown in a table. Another feature of the plugin is a processing tool. The tool retrieves
values for each point in a point layer. Results are stored in the attribute in a newly created
layer. If any transformation are required it is automatically done by the plugin. The following
data option are available:

- Service: A single dataset (e.g. rainfall for January, temperature for December, etc.);
- Group: Service datasets of the type (e.g. rainfall, temperature, etc.); and
- Collection: All groups of the same category (e.g. climate)

This plugin is Free and Open Source Software and is released under the GPL V2.
See the LICENSE file included with the plugin (and in this repository) for
more information about this license.

Contents:

.. toctree::
   :maxdepth: 2

   installation
   docking_panel
   processing_tool
   account_dialog
   options_dialog
   plugin_tests

Contributing
------------

If you would like to contribute an enhancement, bug fix, translation etc. to
this plugin, please make a fork of the repository on Github at:

https://github.com/kartoza/GeoContextQGISPlugin

Then make your improvements and make a Github pull request. Please follow
the existing coding conventions if you want us to include your changes.

This plugin was implemented by:
...............................

**Kartoza (Pty) Ltd.**
https://kartoza.com/

**Tim Sutton**
tim@kartoza.com
