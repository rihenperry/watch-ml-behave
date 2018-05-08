from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from actions import file_dialog, validate_img

from actions import lr_knob, epoch_knob, hn_knob, configure


def md_lft_frame_gui(frame, other_frame):
    file_upload = ttk.Button(frame, command=partial(file_dialog, other_frame),
                             text='File')
    validate = ttk.Button(frame, command=validate_img, text='Validate')

    file_upload.grid(row=1, column=1, rowspan=1, sticky=W, padx=130, pady=100)
    validate.grid(row=1, column=2, rowspan=1, columnspan=1, sticky=E, padx=150, pady=100)



def btm_rght_frame_gui(frame):
    lrvar = DoubleVar()
    lrvar.set(0.2)

    lr_lbl = ttk.Label(frame, text="learning rate")
    lr_slider = ttk.Scale(frame, orient='vertical', variable=lrvar.get(), length=150, from_=0.05, to=1, command=lr_knob)
    lr_slider.set(0.2)
    lr_scale_lbl = ttk.Label(frame, textvariable=lrvar.get())

    epochvar = IntVar()
    epochvar.set(1)
    epoch_slider = ttk.Scale(frame, orient='vertical', variable=epochvar.get(), length=150, from_=1, to=25, command=epoch_knob)
    epoch_slider.set(1)
    epoch_lbl = ttk.Label(frame, text="epoch")
    epoch_scale_lbl = ttk.Label(frame, textvariable=epochvar.get())

    hnvar = IntVar()
    hnvar.set(100)
    hn_slider = ttk.Scale(frame, orient='vertical', length=150, variable=hnvar.get(), from_=1, to=600, command=hn_knob)
    hn_slider.set(100)
    hn_lbl = ttk.Label(frame, text="hidden nodes")
    hn_scale_lbl = ttk.Label(frame, textvariable=int(float(hnvar.get())))


    train = ttk.Button(frame, command=partial(configure), text='train')

    lr_slider.grid(row=0, column=0, padx=50, pady=15)
    epoch_slider.grid(row=0, column=1, padx=50, pady=15)
    hn_slider.grid(row=0, column=2, padx=50, pady=15)
    train.grid(row=0, column=3, padx=50, pady=43)

    lr_scale_lbl.grid(row=1, column=0, padx=50, pady=18)
    epoch_scale_lbl.grid(row=1, column=1, padx=50, pady=18)
    hn_scale_lbl.grid(row=1, column=2, padx=50, pady=18)

    lr_lbl.grid(row=2, column=0, padx=50, pady=18)
    epoch_lbl.grid(row=2, column=1, padx=50, pady=18)
    hn_lbl.grid(row=2, column=2, padx=50, pady=18)
