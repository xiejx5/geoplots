import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def heatmap(df, ax=None, row_labels=None, col_labels=None, **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if row_labels is None:
        row_labels = list(df.index)
    elif isinstance(row_labels, dict):
        row_labels = [row_labels[i] for i in df.index]

    if col_labels is None:
        col_labels = list(df.columns)
    elif isinstance(col_labels, dict):
        col_labels = [col_labels[i] for i in df.columns]

    # Plot the heatmap
    im = ax.imshow(df.values, **kwargs)

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(df.shape[1]), labels=col_labels,
                  fontweight='bold', fontname='consolas')
    ax.set_yticks(np.arange(df.shape[0]), labels=row_labels,
                  fontweight='bold', fontname='consolas')

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(df.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(df.shape[0] + 1) - .5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.tick_params(length=0)

    return im


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors="black", bounds=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a bounds,
        the second for those above.  Optional.
    bounds
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the bounds to the images color range
    if bounds is None:
        bounds = [-np.inf, np.inf]
    norm = mpl.colors.BoundaryNorm(bounds, len(bounds) - 1)

    if isinstance(textcolors, str):
        textcolors = [textcolors for i in range(len(bounds) - 1)]

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = mpl.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[norm(data[i, j])])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts
