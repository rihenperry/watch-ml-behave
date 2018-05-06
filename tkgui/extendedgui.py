from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from actions import file_dialog, validate_img


def md_lft_frame_gui(frame, other_frame):
    file_upload = ttk.Button(frame, command=partial(file_dialog, other_frame),
                             text='File')
    validate = ttk.Button(frame, command=validate_img, text='Validate')

    file_upload.grid(row=1, column=1, rowspan=1, sticky=W, padx=130, pady=100)
    validate.grid(row=1, column=2, rowspan=1, columnspan=1, sticky=E, padx=150, pady=100)


def btm_rght_frame_gui(frame):
    lr_slider = ttk.Scale(frame, orient='vertical', length=150, from_=0, to_=128, command='')
    lr_lbl = ttk.Label(frame, text="learning rate")

    epoch_slider = ttk.Scale(frame, orient='vertical', length=150, from_=0, to=128, command='')
    epoch_lbl = ttk.Label(frame, text="epoch")

    hn_slider = ttk.Scale(frame, orient='vertical', length=150, from_=0, to=128, command='')
    hn_lbl = ttk.Label(frame, text="hidden nodes")

    train = ttk.Button(frame, command=validate_img, text='train')

    lr_slider.grid(row=0, column=0, padx=50, pady=30)
    epoch_slider.grid(row=0, column=1, padx=50, pady=30)
    hn_slider.grid(row=0, column=2, padx=50, pady=30)
    train.grid(row=0, column=3, padx=50, pady=43)

    lr_lbl.grid(row=1, column=0, padx=50, pady=33)
    epoch_lbl.grid(row=1, column=1, padx=50, pady=33)
    hn_lbl.grid(row=1, column=2, padx=50, pady=33)
