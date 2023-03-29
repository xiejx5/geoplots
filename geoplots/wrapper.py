import matplotlib.pyplot as plt
from geoplots._const import params
from matplotlib.transforms import Bbox


def init(figsize, widths=None, heights=None, wspace=0, hspace=0,
         left=0.005, right=0.995, bottom=0.005, top=0.995, **kwargs):
    plt.rcParams.update(params)
    fig = plt.figure(figsize=figsize, **kwargs)
    ncols = 1 if widths is None else len(widths)
    nrows = 1 if heights is None else len(heights)
    grids = fig.add_gridspec(ncols=ncols, nrows=nrows,
                             width_ratios=widths, wspace=wspace,
                             height_ratios=heights, hspace=hspace,
                             left=left, right=right, bottom=bottom, top=top)
    return fig, grids


def title(ax, label=None, **kwargs):
    axes_list = [axes for axes in ax.figure.axes if 'colorbar' not in axes.get_label()]
    if label is None:
        kwargs['fontweight'] = kwargs.pop('fontweight', 'bold')
        label = chr(96 + len(axes_list))
    elif isinstance(label, int):
        kwargs['fontweight'] = kwargs.pop('fontweight', 'bold')
        label = chr(97 + label)
        ax.title.get_size()
    kwargs['fontsize'] = kwargs.pop('fontsize', ax.title.get_size())
    kwargs['loc'] = kwargs.pop('loc', 'left')
    kwargs['y'] = kwargs.pop('y', 1)
    kwargs['pad'] = kwargs.pop('pad', 6)
    bbox = ax.get_tightbbox()
    x, _ = ax.transAxes.inverted().transform([bbox.x0, bbox.y0])
    kwargs['x'] = kwargs.pop('x', x)
    ax.set_title(label, **kwargs)


def highlight(ax, label, color='red'):
    if label in [t.get_text() for t in ax.get_xticklabels()]:
        ticklabels = ax.get_xticklabels()
    else:
        ticklabels = ax.get_yticklabels()

    idx = [t.get_text() for t in ticklabels].index(label)
    ticklabels[idx].set_color(color)
    ticklabels[idx].set_weight("bold")


def colorbar(ax, mappable=None, width='1%', height='80%', pad='1%', reverse=False, **kwargs):
    """
    Add a new axes on a given side of the main axes.

    Parameters
    ----------
    width : float or str
        Size of the inset axes to create. If a float is provided, it is
        the size in inches, e.g. *width=1.3*. If a string is provided, it is
        the size in relative units, e.g. *width='40%%'*.
    height : float or str
        Same to width
    pad : float or str
        Padding between the axes.
    inverse : bool
        whether append to left or top
    """
    mappable = ax.images[0] if mappable is None else mappable
    w = float(width.strip('%')) / 100 if isinstance(width, str) else width
    h = float(height.strip('%')) / 100 if isinstance(height, str) else height
    pad = float(pad.strip('%')) / 100 if isinstance(pad, str) else pad

    # must get_position() first to get tightbbox
    ll, bb, ww, hh = ax.get_position().bounds
    bbox = ax.transAxes.inverted().transform(ax.get_tightbbox())
    (x0, y0), (x1, y1) = bbox
    if w < h and not reverse:
        location = 'right'
        bounds = [x1 + pad, (1 - h) / 2, w, h]
    elif w >= h and not reverse:
        location = 'bottom'
        bounds = [(1 - w) / 2, y0 - pad - h, w, h]
    elif w < h and reverse:
        location = 'left'
        bounds = [x0 - pad - w, (1 - h) / 2, w, h]
    elif w >= h and reverse:
        location = 'top'
        bounds = [(1 - w) / 2, y1 + pad, w, h]

    kwargs['orientation'] = kwargs.pop('orientation', None)
    if kwargs['orientation'] is None:
        kwargs['location'] = location

    # cax = ax.inset_axes(bounds) cannot set_position
    bbox = ax.transAxes.transform(Bbox.from_bounds(*bounds))
    cax = ax.figure.add_axes(Bbox(ax.figure.transFigure.inverted().transform(bbox)).bounds)
    cb = ax.figure.colorbar(mappable=mappable, cax=cax, **kwargs)
    cb.outline.set_visible(False)
    cax.tick_params(left=False, right=False, bottom=False, top=False, pad=2)
    cax.set_label('colorbar')
    ax.cax = cax
    return cb


def tight(ax, label=None):
    if hasattr(ax, 'cax'):
        cax = ax.cax
        ax.add_child_axes(cax)
        bbox0 = ax.figure.transFigure.inverted().transform(ax.get_tightbbox())
        ax.child_axes.remove(cax)
        bbox1 = ax.figure.transFigure.inverted().transform(ax.get_tightbbox())
    else:
        cax = None

    ax.set_anchor('N')
    ll, bb, ww, hh = ax.get_position().bounds
    bbox = ax.figure.transFigure.inverted().transform(ax.get_tightbbox())
    (x0, y0), (x1, y1) = bbox
    dx0, dy0 = ll - x0, bb - y0
    dx1, dy1 = x1 - (ll + ww), y1 - (bb + hh)

    # cax offset
    if cax:
        delta = bbox0 - bbox1
        if delta[1, 0] != 0:
            loc = 'right'
            dx1 += abs(delta[1, 0])
        elif delta[0, 0] != 0:
            loc = 'left'
            dx0 += abs(delta[0, 0])
        elif delta[0, 1] != 0:
            loc = 'bottom'
            dy0 += abs(delta[0, 1])
        elif delta[1, 1] != 0:
            loc = 'top'
            dy1 += abs(delta[1, 1])

    # tight ax
    if ax.get_aspect() != 'auto':
        dy0 = min(dy0, hh / ww * (dx0 + dx1) - dy1)
    ax.set_position([ll + dx0, bb + dy0, ww - dx0 - dx1, hh - dy0 - dy1])

    # move cax
    if cax:
        l, b, w, h = cax.get_position().bounds
        ratio = h / hh if loc in ['right', 'left'] else w / ww
        ll, bb, ww, hh = ax.get_position().bounds
        if loc == 'right':
            cax.set_position([l - dx1, bb + (1 - ratio) / 2 * hh, w, ratio * hh])
        elif loc == 'left':
            cax.set_position([l + dx0, bb + (1 - ratio) / 2 * hh, w, ratio * hh])
        elif loc == 'bottom':
            cax.set_position([ll + (1 - ratio) / 2 * ww, b + (bbox - bbox1)[0, 1] + dy0, ratio * ww, h])
        elif loc == 'top':
            cax.set_position([ll + (1 - ratio) / 2 * ww, b + (bbox - bbox1)[0, 1] - dy1, ratio * ww, h])

    # add label to title
    if label is None:
        if ax.get_title():
            title(ax)
    elif isinstance(label, bool):
        if label:
            title(ax)
    elif isinstance(label, str):
        if label:
            title(ax, label=label)
    else:
        title(ax, label=label)
