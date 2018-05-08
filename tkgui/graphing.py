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
p_x_stack = []
p_y_stack = []
p_x_stack_display = []
saved_stack_count = 0
f = None


def model_performance_graph(xy_cords=None, result=None):
    global topmost_rht_frame, ax_line, canvas_line, lines, p_x_stack, p_y_stack, p_x_stack_display, f, saved_stack_count

    if xy_cords is not None:
        topmost_rht_frame = xy_cords

    for graph in result['data']:
        f_name = graph['model_name'].split('.')[0]
        p_x_stack_display.append(f_name)
        p_x_stack.append(graph['model_id'])
        p_y_stack.append(graph['accuracy'])
        saved_stack_count += 1

    f = plt.figure(figsize=(7.8, 2.4), dpi=95, facecolor='black',
                   edgecolor='green')
    ax_line = f.add_subplot(111)

    width = .3
    lines = ax_line.errorbar(p_x_stack, p_y_stack, width, color='c')

    ax_line.yaxis.set_ticks([(elm/10) for elm in range(0, 11)])
    ax_line.set_xticks(p_x_stack)
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
    ax_line.set_xticklabels(p_x_stack_display)
    # ax_line.grid('on')
    canvas_line = FigureCanvasTkAgg(f, master=topmost_rht_frame)
    canvas_line.draw()
    canvas_line.get_tk_widget().pack(side="left", fill="both", expand=True)


def update_model_performance_graph(result):
    global ax_line, p_x_stack, p_y_stack, lines, p_x_stack_display, f, saved_stack_count
    lines.remove()

    width = .5

    if (saved_stack_count != len(p_x_stack)):
        p_x_stack.pop(len(p_x_stack) - 1)
        p_y_stack.pop(len(p_y_stack) - 1)
        p_x_stack_display.pop(len(p_x_stack_display) - 1)

    extract = result['live_model']
    f_name = extract['model_name'].split('.')[0]
    p_x_stack_display.append(f_name)

    model_id = max(p_x_stack) + 1
    p_x_stack.append(model_id)
    p_y_stack.append(extract['accuracy'])

    lines = ax_line.errorbar(p_x_stack, p_y_stack, width, color='c')
    ax_line.set_xticklabels(p_x_stack_display)

    f.canvas.draw()
    f.canvas.flush_events()
    canvas_line.draw()


lrp_ax = None
lrp_canvas = None
lrp_lines = None
lrp_frame = None
lrp_f = None
lrp_x_stack = []
lrp_y_stack = []
lrp_saved_stack_count = 0


def lr_p_graph(xy_cords=None, result=None):
    global lrp_frame, lrp_ax, lrp_canvas, lrp_lines, lrp_ax, lrp_x_stack, lrp_y_stack, lrp_f, lrp_saved_stack_count

    if xy_cords is not None:
        lrp_frame = xy_cords

    for graph in result['data']:
        lr = round(float(graph['lr_vs_p'].split(',')[0]), 2)
        p = float(graph['lr_vs_p'].split(',')[1])
        lrp_x_stack.append(lr)
        lrp_y_stack.append(p)
        lrp_saved_stack_count += 1

    lrp_f = plt.figure(figsize=(3, 2.5), dpi=80, facecolor='black',
                       edgecolor='green')
    lrp_ax = lrp_f.add_subplot(111)

    width = .3

    print(lrp_x_stack)
    print(lrp_y_stack)
    lrp_lines = lrp_ax.plot(lrp_x_stack, lrp_y_stack, width, linestyle='dashed', color='c',
                            marker='o')
    # lrp_ax.set_yticklabels([(elm) for elm in range(0, 11)])
    lrp_ax.set_yticks([(elm/10) for elm in range(0, 11)])
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
    # lrp_ax.set_xticklabels([(elm) for elm in range(0, 11)])
    lrp_ax.set_xticks([(elm/10) for elm in range(0, 11)])
    # ax_line.grid('on')
    lrp_canvas = FigureCanvasTkAgg(lrp_f, master=lrp_frame)
    lrp_canvas.draw()
    lrp_canvas.get_tk_widget().pack(side="right", fill="both", expand=True)


def update_lr_vs_p(result):
    global lrp_ax, lrp_x_stack, lrp_y_stack, lrp_lines, lrp_f, lrp_saved_stack_count, lrp_canvas
    ln = lrp_lines.pop(0)
    ln.remove()
    # lrp_lines.remove()

    width = .5

    if (lrp_saved_stack_count != len(lrp_x_stack)):
        lrp_x_stack.pop(len(lrp_x_stack) - 1)
        lrp_y_stack.pop(len(lrp_y_stack) - 1)

    extract = result['live_model']

    lr = round(float(extract['lr_vs_p'].split(',')[0]), 2)
    p = float(extract['lr_vs_p'].split(',')[1])
    lrp_x_stack.append(lr)
    lrp_y_stack.append(p)

    lrp_lines = lrp_ax.plot(lrp_x_stack, lrp_y_stack, width, linestyle='dashed', color='c', marker='o')

    lrp_f.canvas.draw()
    lrp_f.canvas.flush_events()
    lrp_canvas.draw()


epochp_ax = None
epochp_canvas = None
epochp_lines = None
epochp_frame = None
epoch_x_stack = []
epoch_y_stack = []
epoch_f = None
epoch_saved_stack_count = 0

def epoch_p_graph(xy_cords=None, result=None):
    global epochp_frame, epochp_ax, epochp_canvas, epochp_lines, epoch_saved_stack_count, epoch_x_stack, epoch_y_stack, epoch_f

    if xy_cords is not None:
        epochp_frame = xy_cords

    for graph in result['data']:
        epoch = int(graph['epoch_vs_p'].split(',')[0])
        p = float(graph['epoch_vs_p'].split(',')[1])
        epoch_x_stack.append(epoch)
        epoch_y_stack.append(p)
        epoch_saved_stack_count += 1

    epoch_f = plt.figure(figsize=(3, 2.5), dpi=80, facecolor='black',
                   edgecolor='green')
    epochp_ax = epoch_f.add_subplot(111)

    width = .3

    epochp_lines = epochp_ax.plot(epoch_x_stack, epoch_y_stack, width, linestyle='dashed', color='c',
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
    epochp_canvas = FigureCanvasTkAgg(epoch_f, master=epochp_frame)
    epochp_canvas.draw()
    epochp_canvas.get_tk_widget().pack(side="right", fill="both", expand=True)


def update_epoch_vs_p(result):
    global epochp_ax, epoch_x_stack, epoch_y_stack, epochp_lines, epoch_f, epoch_saved_stack_count, epochp_canvas
    ln = epochp_lines.pop(0)
    ln.remove()
    # lrp_lines.remove()

    width = .5

    if (epoch_saved_stack_count != len(epoch_x_stack)):
        epoch_x_stack.pop(len(epoch_x_stack) - 1)
        epoch_y_stack.pop(len(epoch_y_stack) - 1)

    extract = result['live_model']

    epoch = round(float(extract['epoch_vs_p'].split(',')[0]), 2)
    p = float(extract['epoch_vs_p'].split(',')[1])
    epoch_x_stack.append(epoch)
    epoch_y_stack.append(p)

    epochp_lines = epochp_ax.plot(epoch_x_stack, epoch_y_stack, width, linestyle='dashed', color='c', marker='o')

    epoch_f.canvas.draw()
    epoch_f.canvas.flush_events()
    epochp_canvas.draw()


hnp_ax = None
hnp_canvas = None
hnp_lines = None
hnp_frame = None
hnp_x_stack = []
hnp_y_stack = []
hnp_f = None
hnp_saved_stack_count = 0


def hn_p_graph(xy_cords=None, result=None):
    global hnp_frame, hnp_ax, hnp_canvas, hnp_lines, hnp_x_stack, hnp_y_stack, hnp_f, hnp_saved_stack_count

    if xy_cords is not None:
        hnp_frame = xy_cords

    for graph in result['data']:
        hn = int(graph['hn_vs_p'].split(',')[0])
        p = float(graph['hn_vs_p'].split(',')[1])
        hnp_x_stack.append(hn)
        hnp_y_stack.append(p)
        hnp_saved_stack_count +=1

    hnp_f = plt.figure(figsize=(3, 2.5), dpi=80, facecolor='black',
                   edgecolor='green')
    hnp_ax = hnp_f.add_subplot(111)

    width = .3

    hnp_lines = hnp_ax.plot(hnp_x_stack, hnp_y_stack, width, linestyle='dashed', color='c',
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
    hnp_canvas = FigureCanvasTkAgg(hnp_f, master=hnp_frame)
    hnp_canvas.draw()
    hnp_canvas.get_tk_widget().pack(side="right", fill="both", expand=True)


def update_hn_vs_p(result):
    global hnp_ax, hnp_x_stack, hnp_y_stack, hnp_lines, hnp_f, hnp_saved_stack_count, hnp_canvas
    ln = hnp_lines.pop(0)
    ln.remove()

    width = .5

    if (hnp_saved_stack_count != len(hnp_x_stack)):
        hnp_x_stack.pop(len(hnp_x_stack) - 1)
        hnp_y_stack.pop(len(hnp_y_stack) - 1)

    extract = result['live_model']

    hnp = round(float(extract['hn_vs_p'].split(',')[0]), 2)
    p = float(extract['hn_vs_p'].split(',')[1])
    hnp_x_stack.append(hnp)
    hnp_y_stack.append(p)

    hnp_lines = hnp_ax.plot(hnp_x_stack, hnp_y_stack, width, linestyle='dashed', color='c', marker='o')

    hnp_f.canvas.draw()
    hnp_f.canvas.flush_events()
    hnp_canvas.draw()

