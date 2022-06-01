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
import pyqtgraph as pg
from pyqtgraph import PlotWidget, exporters
import sys  # We need sys so that we can pass argv to QApplication
import os
import random

from bridge_api.default import (
    PLOT_LINE_WIDTH,
    PLOT_LIMITS_BUFFER
)

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'GeoContextQGISPlugin_plot.ui'))


class PlotDialog(QDialog, FORM_CLASS):
    """Dialog for showing the results of the plugin creation process."""
    def __init__(self, list_of_tables, current_tab, tab_names, parent=None):
        super(PlotDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        self.setupUi(self)

        self.list_of_tables = list_of_tables
        self.tab_names = tab_names

        # Limitations used for the graph view
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None

        index = 0
        for name in self.tab_names:
            if index == current_tab:
                # The graph will be plotted with the currently selected tab data
                # So enable it in the checkable combobox
                self.cbPlots.addItemWithCheckState(name, 2)
            else:
                # All other cases will be disabled, but can be enabled by the user
                self.cbPlots.addItemWithCheckState(name, 0)
            index = index + 1

        self.cbPlots.setDefaultText("No selection")
        self.plot_file_output.setFilter("*.png")

        self.set_plot_themes()

        current_table = self.list_of_tables[current_tab]
        r, g, b = self.random_rgb()
        pen = pg.mkPen((r, g, b), width=PLOT_LINE_WIDTH)
        self.create_plot(current_table, pen)

        self.set_connectors()

    def set_connectors(self):
        self.btnExport.clicked.connect(self.export_btn_click)
        self.cbPlots.checkedItemsChanged.connect(self.combobox_plots_change)

    def combobox_plots_change(self):
        # Clears the plot
        self.widgetPlot.clear()

        # Resets the limitations used for the graph view
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None

        # Plots each of the checked items
        checked_list = self.cbPlots.checkedItems()
        for item in checked_list:
            index = self.tab_names.index(item)
            table = self.list_of_tables[index]

            r, g, b = self.random_rgb()
            pen = pg.mkPen((r, g, b), width=PLOT_LINE_WIDTH)
            self.create_plot(table, pen)

    def export_btn_click(self):
        exporter = pg.exporters.ImageExporter(self.widgetPlot.plotItem)
        exporter.export(self.plot_file_output.filePath())

    def set_plot_themes(self):
        # pg.setConfigOption('background', 'r')
        # pg.setConfigOption('foreground', 'g')

        # win = pg.GraphicsLayoutWidget()
        # win.setBackground('w')

        # graph background
        viewbox = self.widgetPlot.getViewBox()
        viewbox.setBackgroundColor((255, 255, 255))

        viewbox.setBorder(pen=pg.mkPen((82, 235, 52), width=5))

    def update_view_limits(self, x_value, y_value):
        # Checks if the values has been initialized yet
        if self.x_min is None:
            # Sets the values the first time
            self.x_min = x_value
            self.x_max = x_value

            self.y_min = y_value
            self.y_max = y_value
        else:
            # Updates the value where required
            if x_value < self.x_min:
                self.x_min = x_value
            if x_value > self.x_max:
                self.x_max = x_value

            if y_value < self.y_min:
                self.y_min = y_value
            if y_value > self.y_max:
                self.y_max = y_value

    def set_view_limits(self):
        viewbox = self.widgetPlot.getViewBox()

        print("x min: " + str(self.x_min))
        print("x max: " + str(self.x_max))
        print("y min: " + str(self.y_min))
        print("y max: " + str(self.y_max))

        if self.x_min > 0:
            x_min_buf = self.x_min - (self.x_min * PLOT_LIMITS_BUFFER)
        else:
            x_min_buf = self.x_min + (self.x_min * PLOT_LIMITS_BUFFER)

        if self.x_max > 0:
            x_max_buf = self.x_max + (self.x_max * PLOT_LIMITS_BUFFER)
        else:
            x_max_buf = self.x_max - (self.x_max * PLOT_LIMITS_BUFFER)

        if self.y_min > 0:
            y_min_buf = self.y_min - (self.y_min * PLOT_LIMITS_BUFFER)
        else:
            y_min_buf = self.y_min + (self.y_min * PLOT_LIMITS_BUFFER)

        if self.y_max > 0:
            y_max_buf = self.y_max + (self.y_max * PLOT_LIMITS_BUFFER)
        else:
            y_max_buf = self.y_max - (self.y_max * PLOT_LIMITS_BUFFER)

        viewbox.setLimits(
            xMin=x_min_buf,
            xMax=x_max_buf,
            yMin=y_min_buf,
            yMax=y_max_buf,
            #maxXRange=[x_min_buf, x_max_buf],
            #maxYRange=[y_min_buf, y_max_buf]
        )

    def random_rgb(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        return r, g, b

    def create_plot(self, table, pen):
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

            self.update_view_limits(i, float(value))

            i = i + 1

        # Plots the line
        self.widgetPlot.plot(plot_range, plot_values, pen=pen)

        self.set_view_limits()
