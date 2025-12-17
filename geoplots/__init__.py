import os
import matplotlib.font_manager as fm

_font_dir = os.path.join(os.path.dirname(__file__), 'fonts')
for font_file in os.listdir(_font_dir):
    if font_file.endswith('.ttf'):
        fm.fontManager.addfont(os.path.join(_font_dir, font_file))

from geoplots._const import *
from geoplots.wrapper import *
from geoplots.cartopy import *
from geoplots.bound import *
from geoplots.legend import *
from geoplots.boxplot import *
from geoplots.heatmap import *
from geoplots.icongrid import *
from geoplots.color import *
