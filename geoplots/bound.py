def set_axis_bound(ax, left, right, lowwer, upper):
    """
    Set the boundaries of the axes.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes to update.
    left : float
        The left bound as a fraction of the current x-range.
    right : float
        The right bound as a fraction of the current x-range.
    lowwer : float
        The lower bound as a fraction of the current y-range.
    upper : float
        The upper bound as a fraction of the current y-range.
    """
    x_left, x_right = ax.get_xlim()
    y_lower, y_upper = ax.get_ylim()
    ax.set_xbound(
        x_left + (x_right - x_left) * left, x_left + (x_right - x_left) * right
    )
    ax.set_ybound(
        y_lower + (y_upper - y_lower) * lowwer, y_lower + (y_upper - y_lower) * upper
    )


def robinson_bound(ax):
    """
    Set the boundaries for a Robinson projection.

    Sets the axes to global extent, turns off axis lines, and sets specific bounds.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes to update.
    """
    ax.set_global()
    ax.axis('off')
    set_axis_bound(ax, 0.13, 0.96, 0.15, 0.99)


def lonlat_bound(ax):
    """
    Set the boundaries and style for a Longitude/Latitude plot.

    Sets the axes to global extent, adds coastlines, and configures ticks.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes to update.
    """
    ax.set_global()
    ax.coastlines(color='#939698', linewidth=1)
    ax.set_xticks([-180, -120, -60, 0, 60, 120, 180])
    ax.set_xticklabels([])
    ax.set_yticks([-60, -30, 0, 30, 60, 90])
    ax.set_yticklabels([])
    ax.tick_params(axis='both', direction='in')
    ax.set_ylim(bottom=-60)
