import matplotlib.pyplot as plt
from geoplots._const import params


def init(figsize, widths=None, heights=None, wspace=0, hspace=0,
         left=0.005, right=0.995, bottom=0.005, top=0.995, **kwargs):
    plt.rcParams.update(params)
    f = plt.figure(figsize=figsize, **kwargs)
    ncols = 1 if widths is None else len(widths)
    nrows = 1 if heights is None else len(heights)
    gs = f.add_gridspec(ncols=ncols, nrows=nrows,
                        width_ratios=widths, wspace=wspace,
                        height_ratios=heights, hspace=hspace,
                        left=left, right=right, bottom=bottom, top=top)
    return f, gs


def tight(ax):
    ll, bb, ww, hh = ax.get_position().bounds
    bbox = ax.get_tightbbox()
    x, y = ax.figure.transFigure.inverted().transform([bbox.x0, bbox.y0])
    dx, dy = ll - x, bb - y
    ax.set_position([ll + dx, bb + dy, ww - dx, hh - dy])


def title(ax, label=None, **kwargs):
    label = chr(96 + len(ax.figure.axes)) if label is None else label
    label = chr(97 + label) if isinstance(label, int) else label
    kwargs['loc'] = kwargs.pop('loc', 'left')
    kwargs['y'] = kwargs.pop('y', 1)
    kwargs['pad'] = kwargs.pop('pad', 6)
    bbox = ax.get_tightbbox()
    x, _ = ax.transAxes.inverted().transform([bbox.x0, bbox.y0])
    kwargs['x'] = kwargs.pop('x', x)
    ax.set_title(label, **kwargs)
