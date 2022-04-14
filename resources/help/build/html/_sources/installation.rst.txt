.. _installation-label:

Installation
============

There are three approaches to installing the GeoContext plugin.

QGIS plugin manager
-------------------
This will be the easiest way to install the plugin:

1. Click on **Plugins** -> **Manage and install plugins** in QGIS;
2. Click on the **All** tab;
3. Type **geocontext** in the search bar; and
4. Click **Install plugin**.

   .. image:: /images/qgis_plugin_install.png
      :align: center

ZIP file
--------

A zip file of the plugin can be downloaded and installed as follows:

1. Go to the pluging gitHub repository: https://github.com/kartoza/GeoContextQGISPlugin;
2. Click on **Code** -> **Download ZIP**;

   .. image:: /images/github_repo_zip.png
      :align: center

3. In QGIS, click on **Plugins** -> **Manage and install plugins**;
4. Click on the **Install from ZIP** tab;
5. Select the plugin ZIP file; and
6. Click **Install plugin**.

   .. image:: /images/qgis_plugin_zip.png
      :align: center

Repository clone
----------------

The user can also directly clone the repository and manually copy it to the QGIS plugin folder:

1. Clone the reposity using git: *git clone https:////github.com//kartoza//GeoContextQGISPlugin*;
2. Go to the QGIS plugins folder. It should be similar to *C:\Users\USERNAME\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\GeoContextQGISPlugin*, where USERNAME is your Windows username;
3. Copy the cloned folder to the plugins folder; and
4. Enable the plugin in the QGIS Plugin manager. A QGIS restart might be required.
