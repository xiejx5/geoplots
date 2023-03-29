import numpy as np
import matplotlib as mpl


def rgb2hex(rgb):
    return ['#%02x%02x%02x' % tuple((np.array(i) * 1).astype(int)) for i in rgb]


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=256):
    cmap = mpl.colormaps[cmap] if isinstance(cmap, str) else cmap
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        f'trunc({cmap.name},{minval:.2f},{maxval:.2f})',
        cmap(np.linspace(minval, maxval, n)))
    return cmap


def boundary_cmap(colors, bounds):
    colors = [c if isinstance(c, str) else rgb2hex(c) for c in colors]
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'boundary_cmap', list(zip(np.linspace(0, 1, len(colors)), colors)))
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    return cmap, norm
