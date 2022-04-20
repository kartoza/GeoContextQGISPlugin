.. _docking_panel-label:

Docking panel
=============

The toolbar can be used to open the GeoContext docking panel. The panel allows the user to select point locations using
the cursor. The figure which follows indicate the GeoContext toolbar (highlighted in red).

   .. image:: /images/toolbar.png
      :align: center
      :scale: 50 %

This panel can be opened when clicking on the toolbar button. When the panel has been opened, the user can select a point
location using the cursor. The coordinates of the point location will be retrieved, which will then be used to perform
a request for the selected registry type and key name. Here is a quick explanation of each of the panel features:

- *Registry*: Can be either 'Service', 'Group', or 'Collection';
- *Key*: The key name of the data the user wants to retrieve. The key name is used to retrieve the key ID, which is then used to perform the request;
- *Information table*: Shows details related to the selected registry type and key;
- *Longitude*: This is the x-coordinate of the selected location;
- *Latitude*: This is the y-coordinate of the selected location;
- *Cursor*: Can be used to enable or disable the canvas point tool cursor. The user won't be to select points using the cursor if this is disabled;
- *Fetch*: Does a request for the location, and selected data;
- *Results table*: Results from the performed request;
- *Export*: Exports the table contents to a geopackage file (gpkg); and
- *Clear*: Clears the table of any content.

   .. image:: /images/panel.png
      :align: center
      :scale: 50 %
