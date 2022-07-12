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
    create_vector_file,
    export_table
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
            success, msg = export_table(output_file, table)
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
