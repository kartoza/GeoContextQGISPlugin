# coding=utf-8
"""
Help dialog implementation.

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt5.QtWidgets import QDialog, QTableWidget
from qgis.PyQt import uic, QtWidgets
from qgis.PyQt.QtCore import pyqtSignal, QUrl, QVariant
import sys  # We need sys so that we can pass argv to QApplication
import os

from utilities.utilities import (
    get_request_crs,
    create_vector_file
)
from qgis.core import (
    QgsProject,
    QgsSettings,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsPointXY,
    QgsVectorLayer,
    QgsField,
    QgsFeature,
    QgsGeometry
)
from bridge_api.default import (
    API_DEFAULT_URL,
    SERVICE,
    GROUP,
    COLLECTION,
    VALUE_JSON,
    SERVICE_JSON,
    GROUP_JSON,
    COLLECTION_JSON,
    TABLE_DATA_TYPE,
    TABLE_VALUE,
    TABLE_LONG,
    TABLE_LAT,
    COORDINATE_SYSTEM
)

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'GeoContextQGISPlugin_table.ui'))


class TableDialog(QDialog, FORM_CLASS):
    """Dialog for showing the results of the plugin creation process."""
    def __init__(self, list_tables, list_names, parent=None):
        super(TableDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        self.setupUi(self)

        self.list_tables = list_tables
        self.list_names = list_names

        self.table_output_file.setFilter("*.gpkg;;*.csv")
        self.create_table()

        self.set_connectors()

    def set_connectors(self):
        self.cbTableTabs.currentIndexChanged.connect(self.tab_combobox_change)
        self.tabTables.currentChanged.connect(self.tab_changed)

        self.btnExport.clicked.connect(self.export_btn_click)

    def export_btn_click(self):
        """Export the contents of the docking widget's table to a
        geopackage (gpkg).
        """
        output_file = self.table_output_file.filePath()  # Output file provided by the user
        output_dir = os.path.dirname(output_file)  # Folder directory of the output

        index = self.tabTables.currentIndex()
        table = self.list_tables[index]  # QTableWidget

        # Checks whether the table has any contents
        num_rows = table.rowCount()
        if num_rows <= 0:
            # File will not be created
            print("Export not performed: ", "Table has no contents!")
            return

        # Checks if the folder path exists
        if os.path.exists(output_dir):
            # Exports the table data
            success, msg = self.export_table(output_file, table)
            if not success:
                # Prints an error message if the output file could not be created
                self.iface.messageBar().pushCritical("Cannot create file: ", msg)
        else:
            # Shows an error message if the folder path does not exist
            print("Output directory does not exist: ")

    def tab_changed(self):
        tab_index = self.tabTables.currentIndex()
        cb_index = self.cbTableTabs.currentIndex()

        if tab_index != cb_index:
            self.cbTableTabs.setCurrentIndex(tab_index)
        else:
            # This will happen when the change were a result of the combobox selection
            return

    def tab_combobox_change(self):
        tab_index = self.tabTables.currentIndex()
        cb_index = self.cbTableTabs.currentIndex()

        if tab_index != cb_index:
            self.tabTables.setCurrentIndex(cb_index)
        else:
            # This will happen when the change were a result of a tab selection
            return

    def create_table(self):
        index = 0
        for table in self.list_tables:
            name = self.list_names[index]

            tab_index = self.tabTables.addTab(table, name)
            self.cbTableTabs.addItem(name)

            index = index + 1

    def export_table(self, output_file, table):
        """Exports the table contents of the docking widget.

        :param output_file: Directory and output file name (gpkg)
        :type output_file: str

        :param table: Pointer to the table from which data will be retrieved
        :type table: QTableWidget

        :returns: success, msg
        :rtype: boolean, string
        """
        new_layer = QgsVectorLayer("Point", "temporary_points", "memory")
        layer_provider = new_layer.dataProvider()

        # Adds the new attributes fields to the layer
        new_layer.startEditing()
        list_attributes = [
            QgsField(TABLE_DATA_TYPE['file'], QVariant.String),
            QgsField(TABLE_VALUE['file'], QVariant.String),
            QgsField(TABLE_LONG['file'], QVariant.Double),
            QgsField(TABLE_LAT['file'], QVariant.Double)]
        layer_provider.addAttributes(list_attributes)
        new_layer.updateFields()
        new_layer.commitChanges()

        row_cnt = table.rowCount()
        # Loops through each of the table entries
        i = table.rowCount() - 1  # Current ID
        while i >= 0:
            key = table.item(i, 0).text()  # Data source
            value = table.item(i, 1).text()  # Value at the point
            x = float(table.item(i, 2).text())  # Longitude
            y = float(table.item(i, 3).text())  # Latitude

            # Creates the new feature and updates its attributes
            new_layer.startEditing()
            new_point = QgsPointXY(x, y)
            new_feat = QgsFeature()
            new_feat.setAttributes([key, value, x, y])
            new_feat.setGeometry(QgsGeometry.fromPointXY(new_point))
            layer_provider.addFeatures([new_feat])
            new_layer.commitChanges()

            i = i - 1

        target_crs = QgsCoordinateReferenceSystem(COORDINATE_SYSTEM)
        success, created_layer, msg = create_vector_file(new_layer, output_file, target_crs)

        return success, msg
