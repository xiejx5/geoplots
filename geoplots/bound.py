def set_axis_bound(ax, left, right, lowwer, upper):
    x_left, x_right = ax.get_xlim()
    y_lower, y_upper = ax.get_ylim()
    ax.set_xbound(x_left + (x_right - x_left) * left,
                  x_left + (x_right - x_left) * right)
    ax.set_ybound(y_lower + (y_upper - y_lower) * lowwer,
                  y_lower + (y_upper - y_lower) * upper)


def robinson_bound(ax):
    set_axis_bound(ax, 0.13, 0.96, 0.15, 0.99)
