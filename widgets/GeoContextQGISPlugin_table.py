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

from PyQt5.QtWidgets import QDialog
from qgis.PyQt import uic, QtWidgets
import sys  # We need sys so that we can pass argv to QApplication
import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'GeoContextQGISPlugin_table.ui'))


class TableDialog(QDialog, FORM_CLASS):
    """Dialog for showing the results of the plugin creation process."""
    def __init__(self, list_tables, parent=None):
        super(TableDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        self.setupUi(self)

        self.list_tables = list_tables

        self.create_table()

    def create_table(self):
        # Creates a new tab
        #table_widget = QtWidgets.QTableWidget()
        for table in self.list_tables:
            i = self.tabTables.addTab(table, "test")
