import itertools
import numpy as np
import matplotlib as mpl
from matplotlib.text import Text
from matplotlib.patches import Patch


# reverse order: flip(legend_elements, ncol), flip(labels, ncol)
def flip(items, ncol):
    """
    Flatten a list of items by flipping them column-wise.

    Parameters
    ----------
    items : list
        The list of items to flip.
    ncol : int
        The number of columns.

    Returns
    -------
    itertools.chain
        An iterator over the flipped items.
    """
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])


# Text legend: obj_0 = AnyObject("T", "#e41a1c")
class AnyObject(object):
    """
    A placeholder object for creating custom text legends.

    Parameters
    ----------
    text : str
        The text to display.
    color : str
        The color of the text.
    """

    def __init__(self, text, color):
        self.text = text
        self.color = color


# 'handler_map': {obj_0: AnyObjectHandler()}
class AnyObjectHandler(object):
    """
    Handler for AnyObject to draw text in the legend.
    """

    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        patch = Text(
            x=x0 + width / 2,
            y=height / 2 - y0,
            text=orig_handle.text,
            color=orig_handle.color,
            verticalalignment='center',
            horizontalalignment='center',
            multialignment=None,
            fontproperties=None,
            linespacing=None,
            rotation_mode=None,
            fontsize=20,
            family='consolas',
        )
        handlebox.add_artist(patch)
        return patch


# categorical legend: USA_Baseflow fig2_gages.py
def cat_legend(values, cmap, vmin=None, vmax=None, **style_kwds):
    """
    Create a categorical legend.

    Parameters
    ----------
    values : list or numpy.ndarray
        The values to map to colors.
    cmap : str or matplotlib.colors.Colormap
        The colormap used.
    vmin : float, optional
        Minimum value for normalization.
    vmax : float, optional
        Maximum value for normalization.
    **style_kwds
        Additional keyword arguments.

    Returns
    -------
    list
        A list of matplotlib.patches.Patch objects.
    """
    values = np.asarray(values)
    categories = sorted(set(values))
    valuemap = dict((k, v) for (v, k) in enumerate(categories))
    values = np.array([valuemap[k] for k in values])
    mn = values[~np.isnan(values)].min() if vmin is None else vmin
    mx = values[~np.isnan(values)].max() if vmax is None else vmax

    norm = mpl.colors.Normalize(vmin=mn, vmax=mx)
    n_cmap = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)

    patches = []
    for value, cat in enumerate(categories):
        patches.append(Patch(color=n_cmap.to_rgba(value), linewidth=1))
    return patches
