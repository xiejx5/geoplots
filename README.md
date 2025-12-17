# Geoplots

A library for geographic plotting and visualization, built on top of Matplotlib and Cartopy.

## Installation

You can install the package using `pip`:

```bash
pip install geoplots
```

## Usage

### Initialization

Initialize a figure with a custom grid:

```python
from geoplots import wrapper

fig, grids = wrapper.init(figsize=(10, 6), widths=[1, 2], heights=[1, 1])
```

### Geographical Plots

Create plots with specific boundaries:

```python
import matplotlib.pyplot as plt
from geoplots import bound
import cartopy.crs as ccrs

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111, projection=ccrs.Robinson())
bound.robinson_bound(ax)
```

### Icon Grids (Waffle Charts)

Create waffle charts with icons:

```python
from geoplots.icongrid import Waffle

data = {'Cats': 30, 'Dogs': 25, 'Birds': 10}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=data,
    legend={'loc': 'upper left', 'bbox_to_anchor': (1.1, 1)}
)
```