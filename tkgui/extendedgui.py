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
    pass
