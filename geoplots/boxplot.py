from matplotlib.patches import Polygon


def stylize_boxplot(bp, colors):
    """
    Apply custom styles to a boxplot.

    Parameters
    ----------
    bp : dict
        The dictionary returned by `matplotlib.pyplot.boxplot`.
    colors : list
        A list of colors to apply to the boxes and whiskers.
    """
    for i, box in enumerate(bp['boxes']):
        # set color for each box
        box.set_linewidth(0)
        boxCoords = list(zip(box.get_xdata(), box.get_ydata()))
        boxPolygon = Polygon(boxCoords, facecolor=colors[i], linewidth=0)
        bp['whiskers'][0].axes.add_patch(boxPolygon)
        box.set_color(colors[i])

        # we have two whiskers!
        bp['whiskers'][i * 2].set_color(colors[i])
        bp['whiskers'][i * 2 + 1].set_color(colors[i])
        bp['whiskers'][i * 2].set_linewidth(1)
        bp['whiskers'][i * 2 + 1].set_linewidth(1)
        # top and bottom fliers
        if len(bp['fliers']) > 0:
            bp['fliers'][i].set(
                markerfacecolor=colors[i],
                marker='o',
                alpha=0.75,
                markersize=2,
                markeredgecolor='none',
            )
        bp['medians'][i].set_color('black')
        bp['medians'][i].set_linewidth(1)
        # and 4 caps to remove
        xdata = bp['caps'][i * 2].get_xdata()
        dx = (xdata[1] - xdata[0]) / 4
        bp['caps'][i * 2].set(
            color=colors[i],
            linewidth=1,
            xdata=bp['caps'][i * 2].get_xdata() + (dx, -dx),
        )
        bp['caps'][i * 2 + 1].set(
            color=colors[i],
            linewidth=1,
            xdata=bp['caps'][i * 2 + 1].get_xdata() + (dx, -dx),
        )
