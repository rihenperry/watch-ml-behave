from tkinter import *
from tkinter import ttk
import matplotlib
import numpy

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

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


topmost_rht_frame = None
ax_line = None
canvas_line = None
lines = None


def model_performance_graph(xy_cords=None, result=None):
    global topmost_rht_frame, ax_line, canvas_line, lines

    if xy_cords is not None:
        topmost_rht_frame = xy_cords

    x_stack = []
    x_stack_display = []
    y_stack = []

    for graph in result['data']:
        f_name = graph['model_name'].split('.')[0]
        x_stack_display.append(f_name)
        x_stack.append(graph['model_id'])
        y_stack.append(graph['accuracy'])

    f = plt.figure(figsize=(7.8, 2.4), dpi=95, facecolor='black',
                   edgecolor='green')
    ax_line = f.add_subplot(111)

    width = .3
    lines = ax_line.errorbar(x_stack, y_stack, width, color='c')

    ax_line.yaxis.set_ticks([(elm/10) for elm in range(0, 11)])
    ax_line.set_xticks(x_stack)
    ax_line.spines['bottom'].set_color('c')
    ax_line.spines['left'].set_color('c')
    ax_line.tick_params(axis='x', colors='c')
    ax_line.tick_params(axis='y', colors='c')
    ax_line.set_facecolor("#000000")
    ax_line.set_title('performance comparison')
    ax_line.title.set_color('c')
    ax_line.grid(color='w', linestyle='dotted', axis='y', linewidth=0.5)
    ax_line.set_xlabel('model versions')
    ax_line.xaxis.label.set_color('c')
    ax_line.set_ylabel('accuracy')
    ax_line.yaxis.label.set_color('c')
    ax_line.set_xticklabels(x_stack_display)
    # ax_line.grid('on')
    canvas_line = FigureCanvasTkAgg(f, master=topmost_rht_frame)
    canvas_line.draw()
    canvas_line.get_tk_widget().pack(side="left", fill="both", expand=True)


def update_model_performance_graph():
    pass


lrp_ax = None
lrp_canvas = None
lrp_lines = None
lrp_frame = None


def lr_p_graph(xy_cords=None, result=None):
    global lrp_frame, lrp_ax, lrp_canvas, lrp_lines

    if xy_cords is not None:
        lrp_frame = xy_cords

    x_stack = []
    y_stack = []

    for graph in result['data']:
        lr = round(float(graph['lr_vs_p'].split(',')[0]), 2)
        p = float(graph['lr_vs_p'].split(',')[1])
        x_stack.append(lr)
        y_stack.append(p)

    f = plt.figure(figsize=(3, 2.5), dpi=80, facecolor='black',
                   edgecolor='green')
    lrp_ax = f.add_subplot(111)

    width = .3

    lrp_lines = lrp_ax.plot(x_stack, y_stack, width, linestyle='dashed', color='c',
                            marker='o')
    ax_line.set_yticklabels([(elm/10) for elm in range(0, 11)])
    lrp_ax.spines['bottom'].set_color('c')
    lrp_ax.spines['left'].set_color('c')
    lrp_ax.tick_params(axis='x', colors='c')
    lrp_ax.tick_params(axis='y', colors='c')
    lrp_ax.set_facecolor("#000000")
    lrp_ax.set_title('learning rate vs p')
    lrp_ax.title.set_color('c')
    lrp_ax.grid(color='w', linestyle='dotted', linewidth=0.5)
    lrp_ax.set_ylabel('performance')
    lrp_ax.xaxis.label.set_color('c')
    lrp_ax.yaxis.label.set_color('c')
    lrp_ax.set_xticklabels([(elm/10) for elm in range(0, 11)])
    # ax_line.grid('on')
    lrp_canvas = FigureCanvasTkAgg(f, master=lrp_frame)
    lrp_canvas.draw()
    lrp_canvas.get_tk_widget().pack(side="right", fill="both", expand=True)


epochp_ax = None
epochp_canvas = None
epochp_lines = None
epochp_frame = None


def epoch_p_graph(xy_cords=None, result=None):
    global epochp_frame, epochp_ax, epochp_canvas, epochp_lines

    if xy_cords is not None:
        epochp_frame = xy_cords

    x_stack = []
    y_stack = []

    for graph in result['data']:
        epoch = int(graph['epoch_vs_p'].split(',')[0])
        p = float(graph['epoch_vs_p'].split(',')[1])
        x_stack.append(epoch)
        y_stack.append(p)

    f = plt.figure(figsize=(3, 2.5), dpi=80, facecolor='black',
                   edgecolor='green')
    epochp_ax = f.add_subplot(111)

    width = .3

    epochp_lines = epochp_ax.plot(x_stack, y_stack, width, linestyle='dashed', color='c',
                                  marker='o')

    epochp_ax.xaxis.set_ticks([(5*elm) for elm in range(0, 5)])
    epochp_ax.yaxis.set_ticks([(elm/10) for elm in range(0, 11)])
    epochp_ax.spines['bottom'].set_color('c')
    epochp_ax.spines['left'].set_color('c')
    epochp_ax.tick_params(axis='x', colors='c')
    epochp_ax.tick_params(axis='y', colors='c')
    epochp_ax.set_facecolor("#000000")
    epochp_ax.set_title('epoch vs p')
    epochp_ax.title.set_color('c')
    epochp_ax.grid(color='w', linestyle='dotted', linewidth=0.5)
    epochp_ax.set_ylabel('performance')
    epochp_ax.xaxis.label.set_color('c')
    epochp_ax.yaxis.label.set_color('c')
    # ax_line.grid('on')
    epochp_canvas = FigureCanvasTkAgg(f, master=epochp_frame)
    epochp_canvas.draw()
    epochp_canvas.get_tk_widget().pack(side="right", fill="both", expand=True)


hnp_ax = None
hnp_canvas = None
hnp_lines = None
hnp_frame = None


def hn_p_graph(xy_cords=None, result=None):
    global hnp_frame, hnp_ax, hnp_canvas, hnp_lines

    if xy_cords is not None:
        hnp_frame = xy_cords

    x_stack = []
    y_stack = []

    for graph in result['data']:
        hn = int(graph['hn_vs_p'].split(',')[0])
        p = float(graph['hn_vs_p'].split(',')[1])
        x_stack.append(hn)
        y_stack.append(p)

    f = plt.figure(figsize=(3, 2.5), dpi=80, facecolor='black',
                   edgecolor='green')
    hnp_ax = f.add_subplot(111)

    width = .3

    hnp_lines = hnp_ax.plot(x_stack, y_stack, width, linestyle='dashed', color='c',
                            marker='o')
    hnp_ax.xaxis.set_ticks([(100*elm) for elm in range(0, 7)])
    hnp_ax.yaxis.set_ticks([(elm/10) for elm in range(0, 11)])
    hnp_ax.spines['bottom'].set_color('c')
    hnp_ax.spines['left'].set_color('c')
    hnp_ax.tick_params(axis='x', colors='c')
    hnp_ax.tick_params(axis='y', colors='c')
    hnp_ax.set_facecolor("#000000")
    hnp_ax.set_title('hidden nodes vs p')
    hnp_ax.title.set_color('c')
    hnp_ax.grid(color='w', linestyle='dotted', linewidth=0.5)
    hnp_ax.set_ylabel('performance')
    hnp_ax.xaxis.label.set_color('c')
    hnp_ax.yaxis.label.set_color('c')
    # ax_line.grid('on')
    hnp_canvas = FigureCanvasTkAgg(f, master=hnp_frame)
    hnp_canvas.draw()
    hnp_canvas.get_tk_widget().pack(side="right", fill="both", expand=True)



