import numpy as np
import matplotlib as mpl


def rgb2hex(rgb):
    return ['#%02x%02x%02x' % tuple((np.array(i) * 1).astype(int)) for i in rgb]


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=256):
    cmap = mpl.colormaps[cmap] if isinstance(cmap, str) else cmap
    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        f'trunc({cmap.name},{minval:.2f},{maxval:.2f})',
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap
