.. _options_dialog-label:

Options Dialog
==============

The options dialog is used to set the settings for the plugin. It can be accessed by clicking on **Plugins** ->
**GeoContext** -> **Options**. Here is a quick explanation of the available options:

- **API configuration**:
    - *Endpoint URL*: Base URL used to request data;
    - *Schema configuration*: URL used to retrieve the docs schema.
- **Global settings**:
    - *Request CRS*: This should be set to the coordinate system on which the requests need to be made. Coordinates will therefore be transformed to this CRS when required. Available CRSs:
    - WGS84 (EPSG:4326).
- **Panel settings**:
    - *Decimal places*: The number of decimal plcaes which will be used for numberic values when performing panel requests;
    - *Automatically clear table*: If enabled, everytime a user clicks in the canvas for a location request, the table will be cleared. If disabled the request values will stack in the table. The 'Clear table' button can still be used to clear the table.
- **Processing tool settings**:
    - *Decimal places*: The number of decimal places which will be used for numeric values when storing the results in the point layer attribute table.

   .. image:: /images/options_dialog.png
      :align: center
      :scale: 50 %
