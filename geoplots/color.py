import numpy as np
import matplotlib as mpl


def rgb2hex(rgb):
    """
    Convert RGB values to hexadecimal color strings.

    Parameters
    ----------
    rgb : list of lists/tuples or numpy.ndarray
        Array of RGB values (0-1 or 0-255).

    Returns
    -------
    list
        List of hexadecimal color strings.
    """
    return ['#%02x%02x%02x' % tuple((np.array(i) * 1).astype(int)) for i in rgb]


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=256):
    """
    Truncate a colormap to a specific range.

    Parameters
    ----------
    cmap : str or matplotlib.colors.Colormap
        The colormap to truncate.
    minval : float, optional
        The lower bound of the new colormap (default is 0.0).
    maxval : float, optional
        The upper bound of the new colormap (default is 1.0).
    n : int, optional
        The number of discrete colors in the new colormap (default is 256).

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        The truncated colormap.
    """
    cmap = mpl.colormaps[cmap] if isinstance(cmap, str) else cmap
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        f'trunc({cmap.name},{minval:.2f},{maxval:.2f})',
        cmap(np.linspace(minval, maxval, n)),
    )
    return cmap


def boundary_cmap(colors, bounds):
    """
    Create a colormap and norm for discrete intervals.

    Parameters
    ----------
    colors : list
        List of colors (names, hex, or RGB).
    bounds : list
        List of boundaries for the discrete intervals.

    Returns
    -------
    tuple
        (cmap, norm) where cmap is the colormap and norm is the BoundaryNorm.
    """
    colors = [c if isinstance(c, str) else rgb2hex(c) for c in colors]
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'boundary_cmap', list(zip(np.linspace(0, 1, len(colors)), colors))
    )
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    return cmap, norm
