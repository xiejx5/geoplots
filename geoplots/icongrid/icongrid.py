#!/usr/bin/python
# -*-coding: utf-8 -*-
import numpy as np
from matplotlib.pyplot import cm
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Patch
import matplotlib.font_manager as fm
from matplotlib.text import Text
from matplotlib.legend_handler import HandlerBase
import copy
import os
from itertools import product


def ceil(a, b):
    """
    Just like math.ceil
    """
    return int(a // b + bool(a % b))


def array_resize(array, length, array_len=None):
    """
    Resize array to given length. If the array is shorter than given length, repeat the array; If the array is longer
    than the length, trim the array.
    :param array: array
    :param length: target length
    :param array_len: if length of original array is known, pass it in here
    :return: axtended array
    """
    if not array_len:
        array_len = len(array)
    return array * (length // array_len) + array[:length % array_len]


_FONT_PATH = os.path.dirname(__file__)
FONT_FOLDER = {
    'brands': os.path.join(_FONT_PATH, 'icons', 'fa-brands-400.ttf'),
    'solid': os.path.join(_FONT_PATH, 'icons', 'fa-solid-900.ttf'),
    'regular': os.path.join(_FONT_PATH, 'icons', 'fa-regular-400.ttf')
}

class TextLegend(object):
    def __init__(self, text, color, **kwargs):
        self.text = text
        self.color = color
        self.kwargs = kwargs


class TextLegendHandler(HandlerBase):
    def __init__(self, font_file):
        super().__init__()
        self.font_file = FONT_FOLDER[font_file]

    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
        x = xdescent + width / 2.0
        y = ydescent + height / 2.0
        kwargs = {
            'horizontalalignment': 'center',
            'verticalalignment': 'center',
            'color': orig_handle.color,
            'fontproperties': fm.FontProperties(fname=self.font_file, size=fontsize)
        }
        kwargs.update(orig_handle.kwargs)
        annotation = Text(x, y, orig_handle.text, **kwargs)
        return [annotation]

    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        kwargs = {
            'horizontalalignment': 'center',
            'verticalalignment': 'center',
            'color': orig_handle.color,
            'fontproperties': fm.FontProperties(fname=self.font_file, size=fontsize)
        }
        kwargs.update(orig_handle.kwargs)
        patch = Text(x=x0 + width / 2, y=height / 2 - y0,
                     text=orig_handle.text, **kwargs)
        handlebox.add_artist(patch)
        return patch


class Waffle(Figure):
    """

    A custom Figure class to make waffle charts.

    :param values: Numerical value of each category. If it is a dict, the keys would be used as labels.
    :type values: list|dict

    :param rows: The number of lines of the waffle chart. This is required if plots is not assigned.
    :type rows: int

    :param columns: The number of columns of the waffle chart.
        If it is not None, the total number of blocks would be decided through rows and columns. [Default None]
    :type columns: int

    :param colors: A list of colors for each category. Its length should be the same as values.
        Default values are from Set2 colormap.
    :type colors: list[str]|tuple[str]

    :param labels: The name of each category.
        If the values is a dict, this parameter would be replaced by the keys of values.
    :type labels: list[str]|tuple[str]

    :param legend: Parameters of matplotlib.pyplot.legend in a dict.
        E.g. {'loc': '', 'bbox_to_anchor': (,), ...}
        See full parameter list in https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html
    :type legend: dict

    :param icon_legend: Whether to use icon but not color bar in legend. [Default False]
    :type icon_legend: bool

    :param interval_ratio_x: Ratio of distance between blocks on X to block's width. [Default 0.2]
    :type interval_ratio_x: float

    :param interval_ratio_y: Ratio of distance between blocks on Y to block's height. [Default 0.2]
    :type interval_ratio_y: float

    :param block_aspect: The ratio of block's width to height. [Default 1]
    :type block_aspect: float

    :param cmap_name: Name of colormaps for default color, if colors is not assigned.
        See full list in https://matplotlib.org/examples/color/colormaps_reference.html [Default 'Set2']
    :type cmap_name: str

    :param title: Parameters of matplotlib.axes.Axes.set_title in a dict.
        E.g. {'label': '', 'fontdict': {}, 'loc': ''}
        See full parameter list in https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_title.html
    :type title: dict

    :param icons: Icon name of Font Awesome. If it is a string, all categories use the same icon;
        If it's a list or tuple of icons, the length should be the same as values.
        See the full list of Font Awesome on http://fontawesome.io/icons/ [Default None]
    :type icons: str|list[str]|tuple[str]

    :param icon_set: ('BRANDS', 'REGULAR', 'SOLID')
        The set of icons to be used. Visit https://fontawesome.com/cheatsheet to see which icons belong to which set.
        [Default 'SOLID']
    :type icon_set: str

    :param icon_size: Fint size of the icons. The default size is not fixed and depends on the block size.
    :type icon_size: int

    :param plot_anchor: {'C', 'SW', 'S', 'SE', 'E', 'NE', 'N', 'NW', 'W'}
        The alignment method of subplots.
        See details in https://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.set_anchor.html
        [Default 'W']
    :type plot_anchor: str

    :param plots: Location and parameters of Waffle class for subplots in a dict,
        with format like {loc: {subplot_args: values, }, }.
        loc is a 3-digit integer. If the three integers are I, J, and K,
        the subplot is the Ith plot on a grid with J rows and K columns.
        The parameters of subplots are the same as Waffle class parameters, excluding plots itself.
        Nested subplots is not supported.
        If any parameter of subplots is not assigned, it use the same parameter in Waffle class as default value.
    :type plots: dict
    :param plot_direction: {'NW', 'SW', 'NE', 'SE'}, the default value is SW.
    Change the starting location plotting the blocks
    'NW' means plots start at upper left and end at lower right.
    For 'SW', plots start at lower left and end at upper right.
    For 'NE', plots start at upper right and end at lower left.
    For 'SE', plots start at lower right and end at upper left.
    :type plot_direction: str
    """

    _direction_values = {
        'NW': {
            'column_order': 1,
            'row_order': -1,
        },
        'SW': {
            'column_order': 1,
            'row_order': 1,
        },
        'NE': {
            'column_order': -1,
            'row_order': 1,
        },
        'SE': {
            'column_order': -1,
            'row_order': -1,
        },
    }

    def __init__(self, *args, **kwargs):
        self.fig_args = {
            'values': kwargs.pop('values', []),
            'rows': kwargs.pop('rows', None),
            'columns': kwargs.pop('columns', None),
            'colors': kwargs.pop('colors', None),
            'labels': kwargs.pop('labels', None),
            'legend': kwargs.pop('legend', {}),
            'icon_legend': kwargs.pop('icon_legend', False),
            'interval_ratio_x': kwargs.pop('interval_ratio_x', 0.2),
            'interval_ratio_y': kwargs.pop('interval_ratio_y', 0.2),
            'block_aspect': kwargs.pop('block_aspect', 1),
            'cmap_name': kwargs.pop('cmap_name', 'Set2'),
            'title': kwargs.pop('title', None),
            'icons': kwargs.pop('icons', None),
            'icon_size': kwargs.pop('icon_size', None),
            'icon_set': kwargs.pop('icon_set', 'SOLID'),
            'plot_anchor': kwargs.pop('plot_anchor', 'W'),
            'plot_direction': kwargs.pop('plot_direction', 'SW'),
            'rotation': kwargs.pop('rotation', None),
            'show_num': kwargs.pop('show_num', False),
            'marker': kwargs.pop('icons', None),
            'marker_args': kwargs.pop('marker_args', {}),
            'rectangle_args': kwargs.pop('rectangle_args', {}),
            'nan': kwargs.pop('nan', None),
            'x_offset': kwargs.pop('x_offset', 0),
            'y_offset': kwargs.pop('y_offset', 0),
        }
        self.plots = kwargs.pop('plots', None)
        self.cover_plots = kwargs.pop('cover_plots', None)

        # # If plots is empty, make a single waffle chart
        # if self.plots is None:
        #     self.plots = {111: self.fig_args}

        Figure.__init__(self, *args, **kwargs)

        if self.plots is not None:
            for loc, setting in self.plots.items():
                self._waffle(loc, **copy.deepcopy(setting))
        if self.cover_plots is not None:
            for loc, setting in self.cover_plots:
                self._waffle(loc, **copy.deepcopy(setting))

        # Adjust the layout
        # self.set_tight_layout(True)

    def _waffle(self, loc, **kwargs):
        # _pa is the arguments for this single plot
        self._pa = kwargs

        # Append figure args to plot args
        plot_fig_args = copy.deepcopy(self.fig_args)
        for arg, v in plot_fig_args.items():
            if arg not in self._pa:
                self._pa[arg] = v

        element = np.delete(np.unique(self._pa['values']),
                            np.where(np.unique(self._pa['values']) == self._pa['nan'])[0])
        self.values_len = element.shape[0]

        # Build a color sequence if colors is empty
        if self._pa['colors'] is not None:
            if isinstance(self._pa['colors'], dict):
                self._pa['colors'] = {i: self._pa['colors'][i]
                                      for i in element}
            else:
                self._pa['colors'] = {i: self._pa['colors']
                                      for i in element}
        else:
            default_colors = cm.get_cmap(self._pa['cmap_name']).colors
            default_color_num = cm.get_cmap(self._pa['cmap_name']).N
            self._pa['colors'] = dict(zip(element,
                                          array_resize(array=default_colors, length=self.values_len, array_len=default_color_num)))

        rectangle_args = {}
        for k, v in self._pa['rectangle_args'].items():
            if isinstance(v, dict):
                rectangle_args[k] = {i: self._pa['rectangle_args'][k][i] for i in element}
            else:
                rectangle_args[k] = {i: self._pa['rectangle_args'][k] for i in element}
        if not any(i in rectangle_args.keys() for i in
                   ['color', 'edgecolor', 'facecolor', 'ec', 'fc']):
            rectangle_args['color'] = self._pa['colors']

        if isinstance(self._pa['values'], dict):
            if not self._pa['labels']:
                self._pa['labels'] = self._pa['values'].keys()
            self._pa['values'] = list(self._pa['values'].values())

        if self._pa['labels'] and len(self._pa['labels']) != self.values_len:
            raise ValueError("Length of labels doesn't match the values.")

        if self._pa['icons']:
            from .fontawesome_mapping import icons

            if self._pa['icon_set'] not in icons.keys():
                raise KeyError('icon_set should be one of {}'.format(
                    ', '.join(icons.keys())))

            # If icons is a string, convert it into a list of same icon. It's length is the label's length
            # '\uf26e' -> ['\uf26e', '\uf26e', '\uf26e', ]
            if isinstance(self._pa['icons'], str):
                self._pa['icons'] = {i: self._pa['icons']
                                     for i in element}

            if len(self._pa['icons']) < self.values_len:
                raise ValueError("Length of icons doesn't match the values.")

            self._pa['icons'] = {i: icons[self._pa['icon_set']]
                                 [self._pa['icons'][i]] for i in element}

        if self._pa['rotation']:
            self._pa['rotation'] = {i: self._pa['rotation'][i]
                                    for i in element}

        if isinstance(loc, tuple):
            self.ax = self.add_subplot(*loc, aspect='equal')
        else:
            self.ax = self.get_axes()[int(loc)]

        # Alignment of subplots
        self.ax.set_anchor(self._pa['plot_anchor'])

        # if column number is not given, use the values as number of blocks
        self._pa['rows'], self._pa['columns'] = self._pa['values'].shape[:2]

        # Absolute height of the plot
        figure_height = 1
        block_y_length = figure_height / (
            self._pa['rows'] + self._pa['rows'] *
            self._pa['interval_ratio_y'] - self._pa['interval_ratio_y']
        )
        block_x_length = self._pa['block_aspect'] * block_y_length

        # Define the limit of X, Y axis
        self.ax.axis(
            xmin=0,
            xmax=(
                self._pa['columns'] + self._pa['columns'] *
                self._pa['interval_ratio_x'] - self._pa['interval_ratio_x']
            ) * block_x_length,
            ymin=0,
            ymax=figure_height
        )

        # Default font size
        if self._pa['icons']:
            x, y = self.ax.transData.transform([(0, 0), (0, block_x_length)])
            prop = fm.FontProperties(
                fname=FONT_FOLDER[self._pa['icon_set']],
                size=self._pa['icon_size'] or int((y[1] - x[1]) / 16 * 12)
            )
        elif self._pa['show_num']:
            x, y = self.ax.transData.transform([(0, 0), (0, block_x_length)])
            prop = fm.FontProperties(
                family='consolas',
                size=self._pa['icon_size'] or int((y[1] - x[1]) / 16 * 12)
            )

        # Plot blocks
        x_full = (1 + self._pa['interval_ratio_x']) * block_x_length
        y_full = (1 + self._pa['interval_ratio_y']) * block_y_length

        plot_direction = self._pa['plot_direction'].upper()

        try:
            column_order = self._direction_values[plot_direction]['column_order']
            row_order = self._direction_values[plot_direction]['row_order']
        except KeyError:
            raise KeyError(
                "plot_direction should be one of 'NW', 'SW', 'NE', 'SE'")

        iter_cell = ((col, row) for col, row in product(range(self._pa['columns'])[::column_order], range(self._pa['rows'])[::row_order]) if
                     self._pa['values'][self._pa['rows'] - 1 - row, col] != self._pa['nan'])
        for col, row in iter_cell:
            x = x_full * col
            y = y_full * row

            if self._pa['icons']:
                rotation_arg = None
                if self._pa['rotation']:
                    rotation_arg = self._pa['rotation'][self._pa['values']
                                                        [self._pa['rows'] - 1 - row, col]]
                self.ax.text(
                    x=x + block_x_length * (1 / 2 + self._pa['x_offset']),
                    y=y + block_y_length * (1 / 2 + self._pa['y_offset']),
                    s=self._pa['icons'][self._pa['values']
                                        [self._pa['rows'] - 1 - row, col]],
                    color=self._pa['colors'][self._pa['values']
                                             [self._pa['rows'] - 1 - row, col]],
                    fontproperties=prop,
                    horizontalalignment='center',
                    verticalalignment='center',
                    rotation=rotation_arg,
                )
            elif self._pa['show_num']:
                self.ax.text(
                    x=x + block_x_length * (1 / 2 + self._pa['x_offset']),
                    y=y + block_y_length * (1 / 2 + self._pa['y_offset']),
                    s=str(self._pa['values']
                          [self._pa['rows'] - 1 - row, col]),
                    color=self._pa['colors'][self._pa['values']
                                             [self._pa['rows'] - 1 - row, col]],
                    fontproperties=prop,
                    horizontalalignment='center',
                    verticalalignment='center'
                )
            elif self._pa['marker']:
                self.ax.plot(
                    x + block_x_length * (1 / 2 + self._pa['x_offset']),
                    y + block_y_length * (1 / 2 + self._pa['y_offset']),
                    color=self._pa['colors'][self._pa['values']
                                             [self._pa['rows'] - 1 - row, col]],
                    marker=self._pa['marker'][self._pa['values']
                                              [self._pa['rows'] - 1 - row, col]],
                    **self._pa['marker_args']
                )
            else:
                temp_args = {k: v[self._pa['values'][self._pa['rows'] - 1 - row, col]]
                             for k, v in rectangle_args.items()}
                self.ax.add_artist(
                    Rectangle(xy=(x, y), width=block_x_length, clip_on=False,
                              height=block_y_length, **temp_args))

        # Add title
        if self._pa['title'] is not None:
            self.ax.set_title(**self._pa['title'])

        # Add legend
        if self._pa['labels'] or 'labels' in self._pa['legend']:
            if self._pa['icons'] and self._pa['icon_legend']:
                self._pa['legend']['handles'] = [
                    TextLegend(color=c, text=i) for c, i in zip(self._pa['colors'], self._pa['icons'])
                ]
                self._pa['legend']['handler_map'] = {
                    TextLegend: TextLegendHandler(self._pa['icon_set'])}
            # elif not self._pa['legend'].get('handles'):
            elif 'handles' not in self._pa['legend']:
                self._pa['legend']['handles'] = [
                    Patch(color=c, label=str(l)) for c, l in zip(self._pa['colors'], self._pa['labels'])
                ]

            # labels is an alias of legend['labels']
            if 'labels' not in self._pa['legend'] and self._pa['labels']:
                self._pa['legend']['labels'] = self._pa['labels']

            if 'handles' in self._pa['legend'] and 'labels' in self._pa['legend']:
                self.ax.legend(**self._pa['legend'])

        # Remove borders, ticks, etc.
        self.ax.axis('off')

    def remove(self):
        pass
