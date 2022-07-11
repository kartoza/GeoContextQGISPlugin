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
from qgis.PyQt import uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'GeoContextQGISPlugin_plot.ui'))


class PlotDialog(QDialog, FORM_CLASS):
    """Dialog for showing the results of the plugin creation process."""
    def __init__(self, table, parent=None):
        super(PlotDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        self.setupUi(self)

        self.create_plot(table)

    def create_plot(self, table):
        """Exports the table contents of the docking widget.

        :param output_file: Directory and output file name (gpkg)
        :type output_file: str

        :param table: Pointer to the table from which data will be retrieved
        :type table: QTableWidget

        :returns: success, msg
        :rtype: boolean, string
        """

        row_cnt = table.rowCount()
        # Loops through each of the table entries
        i = 0  # Current ID
        plot_range = []
        plot_values = []
        while i < row_cnt:
            key = table.item(i, 0).text()  # Data source
            value = table.item(i, 1).text()  # Value at the point
            x = float(table.item(i, 2).text())  # Longitude
            y = float(table.item(i, 3).text())  # Latitude

            plot_range.append(i)
            plot_values.append(float(value))

            i = i + 1

        print("BEFORE PLOT")

        self.widgetPlot.plot(plot_range, plot_values)

        print("AFTER")
