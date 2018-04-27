from tkinter import *
from tkinter import ttk
import matplotlib
import numpy

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.use('TkAgg')


btm_lft_frame = None
ax = None
bars = None
canvas = None

def prediction_graph(layout_position=None, result=None):
    global btm_lft_frame, ax, canvas, bars

    if layout_position is not None:
        btm_lft_frame = layout_position

    f = Figure(figsize=(7.5, 3), dpi=100, facecolor='black', edgecolor='green')
    ax = f.add_subplot(111)
    data = []

    if result is None:
        data = [0 for x in range(10)]
    else:
        data = [(elm*100) for elm in result['stats']]

    ind = numpy.arange(0, 10)  # the x locations for the groups
    width = .3

    bars = ax.bar(ind, data, width, color='green', align='center')
    ax.xaxis.set_ticks(ind)
    ax.yaxis.set_ticks([(10*x) for x in range(11)])
    ax.spines['bottom'].set_color('green')
    ax.spines['left'].set_color('green')
    ax.tick_params(axis='x', colors='green')
    ax.tick_params(axis='y', colors='green')
    ax.set_facecolor("#000000")
    ax.set_title('prediction analysis')
    ax.title.set_color('green')
    ax.set_xlabel('labels')
    ax.xaxis.label.set_color('green')
    ax.set_ylabel('accuracy')
    ax.yaxis.label.set_color('green')
    ax.set_xticklabels(ind)
    canvas = FigureCanvasTkAgg(f, master=btm_lft_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side="left", fill="both", expand=True)


def update_prediction_graph(result):
    global bars
    bars.remove()
    ind = numpy.arange(0, 10)  # the x locations for the groups
    # refresh_data = [0 for x in range(10)]
    width = .5

    # ax.bar(ind, refresh_data, width, color='green', align='center')
    # ax.yaxis.set_ticks([(10*x) for x in range(11)])
    # canvas.draw()

    orgnl_data = [(elm*100) for elm in result['stats']]
    bars = ax.bar(ind, orgnl_data, width, color='green', align='center')
    ax.yaxis.set_ticks([(10*x) for x in range(11)])
    canvas.draw()

def model_performance_graph():
    pass


def model_parameter_response_graph():
    pass
