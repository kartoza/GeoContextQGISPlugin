.. _processing_tool-label:

Processing tool
===============

To open the processing tool for the plugin, the user can go to 'Plugins' -> 'GeoContext'.
Here is an example of the menu:

   .. image:: /images/plugin_menu.png
      :align: center
      :scale: 50 %

The processing tool can be accessed via the GeoContext menu, as illustrated in the 'Plugin menu and toolbar'
section. This tool allows the user to provide a point vector file as input to perform requests with. A request
will be performed for each of the points contained by the vector layer. Any points with no geometry will be ignored.
Here is a quick explanation on the parameters of the tool:

- Point layer: This is the input layer which contains the points for which requests will be made. This can only be a point vector layer;
- Selected features only: If the user has selected features of the input layer, the processing will only perform on the selection;
- Endpoint URL: Base URL used to perform requests. This can be changed in the options;
- Schema configuration: The link used to retrieve the schema docs. This can be changed in the options;
- Registry: The registry type, either 'Service', 'Group', or 'Collection';
- Key: The key name. This name will be used to retrieve the key ID, which in turn is used to perform the request;
- Field name/prefix: This is the field name/prefix for the field(s) which will be added. At least one character needs to be provided;
- Output point file: The newly created file. Can either be geopackage (gpkg) or shapefile (shp); and
- Open output file after running algorithm: If the processing is successful the newly created point file will be added to the QGIS map canvas.

   .. image:: /images/plugin_menu.png
      :align: center
      :scale: 50 %

Results from processing tool
----------------------------

The figure which follows show the extracted elevation values for points. This has been obtained using 'Service'
registry type.

   .. image:: /images/result_service_elevation.png
      :align: center
      :scale: 50 %

Notable is that the attribute table which follows contains a large number of added values/attributes. This is because
the request were done on a 'Collection', in this case on 'Global climate collection' - the results therefore
contains several attributes, e.g. bioclimatic conditions, rainfall, temperature, etc.

   .. image:: /images/result_collection_climate.png
      :align: center
      :scale: 50 %
