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
from PyQt5.QtGui import QColor
from qgis.PyQt import uic
import pyqtgraph as pg
from pyqtgraph import PlotWidget, exporters
import sys  # We need sys so that we can pass argv to QApplication
import os
import random
import math

from bridge_api.default import (
    PLOT_LINE_WIDTH,
    PLOT_LIMITS_BUFFER
)

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'GeoContextQGISPlugin_plot.ui'))


class PlotDialog(QDialog, FORM_CLASS):
    """Dialog for showing the results of the plugin creation process."""
    def __init__(self, list_of_tables, current_tab, parent=None):
        super(PlotDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        self.setupUi(self)

        self.list_of_tables = list_of_tables
        self.list_names = self.create_plot_names(self.list_of_tables)

        # Used to avoid calling triggers when not needed
        self.updating_plots = False
        self.cb_selection_changing = False
        self.colour_changing = False
        self.width_changing = False

        # Limitations used for the graph view
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None

        self.dict_settings = self.default_line_settings(self.list_names)
        self.cbLines.clear()

        # Colours is used to set current line display colour
        red = None
        green = None
        blue = None

        index = 0
        for name in self.list_names:
            if index == current_tab:
                # The graph will be plotted with the currently selected tab data
                # So enable it in the checkable combobox
                self.cbPlots.addItemWithCheckState(name, 2)

                current_color = self.dict_settings.get(name)
                red = current_color.get('red')
                green = current_color.get('green')
                blue = current_color.get('blue')

                self.cbColourLines.setColor(QColor(red, green, blue))

            else:
                # All other cases will be disabled, but can be enabled by the user
                self.cbPlots.addItemWithCheckState(name, 0)
            index = index + 1

        self.cbPlots.setDefaultText("No selection")
        self.plot_file_output.setFilter("*.png")

        self.set_plot_themes()

        # Plots the currently selected tab data
        # Other tabs are still disabled at this point
        current_table = self.list_of_tables[current_tab]
        pen = pg.mkPen((red, green, blue), width=PLOT_LINE_WIDTH, symbol='o', symbolPen='b', symbolSize=10)
        name = self.create_plot(current_table, pen)
        self.cbLines.addItem(name)
        self.widgetPlot.setTitle('')  # Title can be changed by the user
        self.widgetPlot.addLegend()

        self.set_connectors()

    def set_connectors(self):
        # Buttons
        self.btnExport.clicked.connect(self.export_btn_click)
        self.cbTitle.stateChanged.connect(self.title_tick_box)
        self.cbXaxis.stateChanged.connect(self.x_axis_tick_box)
        self.cbYaxis.stateChanged.connect(self.y_axis_tick_box)

        # Text boxes
        self.lnTitle.textChanged.connect(self.title_update)
        self.lnXaxis.textChanged.connect(self.x_axis_title_update)
        self.lnYaxis.textChanged.connect(self.y_axis_title_update)

        # Plots
        self.cbPlots.checkedItemsChanged.connect(self.combobox_plots_change)
        self.cbLines.currentIndexChanged.connect(self.combobox_selection_changes)
        self.cbColourLines.colorChanged.connect(self.colour_changed)
        self.sbLineWidth.valueChanged.connect(self.width_changed)

    def title_tick_box(self):
        state = self.cbTitle.isChecked()
        self.lnTitle.setEnabled(state)

        if state:
            title = self.lnTitle.text()
            self.widgetPlot.setTitle(title)
        else:
            self.widgetPlot.setTitle('')

    def x_axis_tick_box(self):
        state = self.cbXaxis.isChecked()
        self.lnXaxis.setEnabled(state)

        if state:
            x_axis = self.lnXaxis.text()
            self.widgetPlot.setLabel('bottom', x_axis)
        else:
            self.widgetPlot.setLabel('bottom', '')

    def y_axis_tick_box(self):
        state = self.cbYaxis.isChecked()
        self.lnYaxis.setEnabled(state)

        if state:
            y_axis = self.lnYaxis.text()
            self.widgetPlot.setLabel('left', y_axis)
        else:
            self.widgetPlot.setLabel('left', '')

    def title_update(self):
        title = self.lnTitle.text()
        self.widgetPlot.setTitle(title)

    def x_axis_title_update(self):
        x_axis = self.lnXaxis.text()
        self.widgetPlot.setLabel('bottom', x_axis)

    def y_axis_title_update(self):
        y_axis = self.lnYaxis.text()
        self.widgetPlot.setLabel('left', y_axis)

    def combobox_selection_changes(self):
        # This is set so that the colour change will not call the update plots method
        self.cb_selection_changing = True

        key = self.cbLines.currentText()
        if key is not None and key != '':
            settings = self.dict_settings.get(key)
            if settings is not None:
                r = settings.get('red')
                g = settings.get('green')
                b = settings.get('blue')
                width = settings.get('width')

                self.cbColourLines.setColor(QColor(r, g, b))
                self.sbLineWidth.setValue(width)
        else:
            self.cbColourLines.setColor(QColor(255, 255, 255))
            self.sbLineWidth.setValue(0.00)

        self.cb_selection_changing = False

    def combobox_plots_change(self):
        self.update_plots()

    def colour_changed(self):
        self.colour_changing = True

        colour = self.cbColourLines.color()
        red = colour.red()
        green = colour.green()
        blue = colour.blue()

        key = self.cbLines.currentText()
        self.set_dict_colour(key, red, green, blue)

        # This check is done to avoid performing a plot change when its
        # already happening, or if it's another line being selected
        if not self.updating_plots and not self.cb_selection_changing:
            self.update_plots()

        self.colour_changing = False

    def width_changed(self):
        self.width_changing = True

        if not self.cb_selection_changing:
            new_width = self.sbLineWidth.value()
            key = self.cbLines.currentText()
            self.set_dict_width(key, new_width)

            self.update_plots()

        self.width_changing = False

    def export_btn_click(self):
        exporter = pg.exporters.ImageExporter(self.widgetPlot.plotItem)
        exporter.export(self.plot_file_output.filePath())

    def update_plots(self):
        # This is set so that the colour change will not call the update plots method
        self.updating_plots = True

        self.widgetPlot.clear()

        if not self.colour_changing and not self.width_changing:
            self.cbLines.clear()

        # Resets the limitations used for the graph view
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None

        # Plots each of the checked items
        checked_list = self.cbPlots.checkedItems()
        for item in checked_list:
            index = self.list_names.index(item)
            table = self.list_of_tables[index]

            settings = self.dict_settings.get(item)
            r = settings.get('red')
            g = settings.get('green')
            b = settings.get('blue')
            width = settings.get('width')

            # line = plt.plot(x, y, pen=pg.mkPen('r', width=6), symbol='o', symbolPen='b', symbolSize=20)

            pen = pg.mkPen((r, g, b), width=width, symbol='o', symbolPen='b', symbolSize=10)
            name = self.create_plot(table, pen)

            if not self.colour_changing and not self.width_changing:
                self.cbLines.addItem(name)

        self.widgetPlot.addLegend()

        self.updating_plots = False

    def set_plot_themes(self):
        # Sets the widget settings
        self.widgetPlot.setBackground((255, 255, 255))
        self.widgetPlot.showGrid(x=True, y=True, alpha=0.3)

        # Sets the graph settings
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

        # Applies limitation buffers to the x-axis and y-axis
        # This value can be changed in default
        x_min_buf = self.x_min - (abs(self.x_min) * PLOT_LIMITS_BUFFER)
        x_max_buf = self.x_max + (abs(self.x_max) * PLOT_LIMITS_BUFFER)
        y_min_buf = self.y_min - (abs(self.y_min) * PLOT_LIMITS_BUFFER)
        y_max_buf = self.y_max + (abs(self.y_max) * PLOT_LIMITS_BUFFER)

        viewbox.setLimits(
            xMin=x_min_buf,
            xMax=x_max_buf,
            yMin=y_min_buf,
            yMax=y_max_buf,
        )

    def random_rgb(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        return r, g, b

    def create_plot_names(self, list_tables):
        list_names = []
        for table in list_tables:
            name = table.item(0, 0).text()
            list_names.append(name)

        return list_names

    def default_line_settings(self, list_keys):
        dict_settings = {}
        for key in list_keys:
            r, g, b = self.random_rgb()
            dict_settings[key] = {
                'red': r,
                'green': g,
                'blue': b,
                'width': PLOT_LINE_WIDTH
            }
        return dict_settings

    def set_dict_colour(self, key, red, green, blue):
        if key != '' and key is not None:
            settings = self.dict_settings.get(key)
            width = settings.get('width')

            self.dict_settings[key] = {
                'red': red,
                'green': green,
                'blue': blue,
                'width': width
            }

    def set_dict_width(self, key, width):
        if key != '' and key is not None:
            settings = self.dict_settings.get(key)
            red = settings.get('red')
            green = settings.get('green')
            blue = settings.get('blue')

            self.dict_settings[key] = {
                'red': red,
                'green': green,
                'blue': blue,
                'width': width
            }

    def create_plot(self, table, pen):
        row_cnt = table.rowCount()
        # Loops through each of the table entries/values
        i = 0  # Current ID
        plot_range = []
        plot_values = []
        key = ''
        while i < row_cnt:
            key = table.item(i, 0).text()  # Data source or name
            value = table.item(i, 1).text()  # Value at the point
            x = float(table.item(i, 2).text())  # Longitude
            y = float(table.item(i, 3).text())  # Latitude

            plot_range.append(i)
            plot_values.append(float(value))

            self.update_view_limits(i, float(value))

            i = i + 1

        # Plots the line
        plot_item = self.widgetPlot.plot(
            plot_range,
            plot_values,
            pen=pen,
            name=key
        )

        # View set to new limits
        self.set_view_limits()

        return key
