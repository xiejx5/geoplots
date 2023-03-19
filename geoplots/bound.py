def set_axis_bound(ax, left, right, lowwer, upper):
    x_left, x_right = ax.get_xlim()
    y_lower, y_upper = ax.get_ylim()
    ax.set_xbound(x_left + (x_right - x_left) * left,
                  x_left + (x_right - x_left) * right)
    ax.set_ybound(y_lower + (y_upper - y_lower) * lowwer,
                  y_lower + (y_upper - y_lower) * upper)


def robinson_bound(ax):
    ax.set_global()
    ax.axis('off')
    set_axis_bound(ax, 0.13, 0.96, 0.15, 0.99)


def lonlat_bound(ax):
    ax.set_global()
    ax.coastlines(color='#939698', linewidth=1)
    ax.set_xticks([-180, -120, -60, 0, 60, 120, 180])
    ax.set_xticklabels([])
    ax.set_yticks([-60, -30, 0, 30, 60, 90])
    ax.set_yticklabels([])
    ax.tick_params(axis="both", direction="in")
    ax.set_ylim(bottom=-60)
