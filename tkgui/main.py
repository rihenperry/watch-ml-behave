import requests
from tkinter import *
from tkinter import ttk

import extendedgui
from graphing import prediction_graph, model_performance_graph
from graphing import lr_p_graph, epoch_p_graph, hn_p_graph


# -- root window
root = Tk()
root.title('Handwritten Digit Classifier and Model Trainer')
# root.geometry('{}x{}'.format(600, 300))

# from inside root window
# f_style = ttk.Style()
# f_style.configure('Main.TFrame', background='#000000')

Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)

master_frame = ttk.Frame(root, width=1300, height=700)
master_frame.grid(row=0, column=0, sticky=(N, S, E, W))
# frame = ttk.Frame(masterwidget, borderwidth=5, width=600, height=300)
# end of root window


# create main containers
# create all of the main containers
# s = ttk.Style()
# s.configure('Tool.TFrame', background='#d4d5d6')

top_lft_frame = ttk.Frame(master_frame, relief="groove", borderwidth=2, width=750, height=232)
simple_frame = ttk.Frame(root)
mid_lft_frame = ttk.Frame(master_frame, relief="groove", borderwidth=2, width=750, height=232)
mid_lft_frame.rowconfigure(0, weight=1)
mid_lft_frame.rowconfigure(1, weight=3)
mid_lft_frame.rowconfigure(2, weight=3)
mid_lft_frame.columnconfigure(0, weight=1)
mid_lft_frame.columnconfigure(1, weight=3)
mid_lft_frame.columnconfigure(2, weight=3)
extendedgui.md_lft_frame_gui(mid_lft_frame, top_lft_frame)

bottom_lft_frame = ttk.Frame(master_frame, relief="groove", width=750, height=232)
prediction_graph(bottom_lft_frame)


top_rht_frame = ttk.Frame(master_frame, relief="groove", borderwidth=2, width=750, height=232)
model_performance_graph(top_rht_frame)

mid_rht_frame = ttk.Frame(master_frame, relief="groove", borderwidth=2, width=750, height=232)

lr_vs_p_frame = ttk.Frame(mid_rht_frame, relief="groove", borderwidth=1, width=250, height=232)
lr_p_graph(lr_vs_p_frame)

epoch_vs_p_frame = ttk.Frame(mid_rht_frame, relief="groove", borderwidth=1, width=250, height=232)
epoch_p_graph(epoch_vs_p_frame)

hn_vs_p_frame = ttk.Frame(mid_rht_frame, relief="groove", borderwidth=1, width=250, height=232)
hn_p_graph(hn_vs_p_frame)

bottom_rht_frame = ttk.Frame(master_frame, relief="groove", borderwidth=2, width=750, height=290)
bottom_rht_frame.rowconfigure(0, weight=1)
bottom_rht_frame.rowconfigure(1, weight=3)
bottom_rht_frame.columnconfigure(0, weight=1)
bottom_rht_frame.columnconfigure(1, weight=3)
bottom_rht_frame.columnconfigure(2, weight=3)
bottom_rht_frame.columnconfigure(3, weight=3)
extendedgui.btm_rght_frame_gui(bottom_rht_frame)

# use grid manager to position frame and widgets
# layout the main containers

top_lft_frame.grid(row=0, column=0, padx=2.5, pady=2.5, sticky=(N,W))
mid_lft_frame.grid(row=1, column=0, padx=2.5, sticky=W)
bottom_lft_frame.grid(row=2, column=0, padx=2.5, pady=2.5, sticky=(S,W))

top_rht_frame.grid(row=0, columnspan=1, column=3, padx=2.5, pady=2.5, sticky=(N,E))

mid_rht_frame.grid(row=1, columnspan=1, column=3, padx=2.5, sticky=E)
lr_vs_p_frame.grid(row=0, column=0, padx=0.5, pady=0.5, sticky=W)
epoch_vs_p_frame.grid(row=0, column=1, padx=0.5, pady=0.5, sticky=(W,E))
hn_vs_p_frame.grid(row=0, column=2, padx=0.5, pady=0.5, sticky=E)

bottom_rht_frame.grid(row=2, columnspan=1, column=3, padx=2.5, pady=2.5, sticky=(S,E))

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

master_frame.columnconfigure(0, weight=3)
master_frame.columnconfigure(1, weight=3)
master_frame.columnconfigure(2, weight=3)
master_frame.columnconfigure(3, weight=3)
master_frame.rowconfigure(0, weight=3)
master_frame.rowconfigure(1, weight=3)

# end of grid manager

# include a menu bar
menubar = Menu(root)

# menu options
optmenu = Menu(menubar, tearoff=0)
optmenu.add_command(label='save model', command=None)
optmenu.add_command(label='load model', command=None)
optmenu.add_command(label='exit', command=root.quit)
menubar.add_cascade(label='options', menu=optmenu)

root.config(menu=menubar)
# end of menu bar
# end of resizing window

# start main event loop
if __name__ == '__main__':
    init_url = 'http://127.0.0.1:8080/api/'
    print('init request url {0}'.format(init_url))

    r = requests.get(init_url)
    print(r.json())

    root.mainloop()
