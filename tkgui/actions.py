import requests
import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

from graphing import update_prediction_graph, update_model_performance_graph, update_lr_vs_p, update_epoch_vs_p, update_hn_vs_p

imglabel = None
img_name = None
img_fname = ""


def file_dialog(top_frame_lft):
    global label
    global img_name
    global img_fname

    dir_path = os.getcwd()
    img_name = askopenfilename(initialdir=dir_path,
                               filetypes=[("Image files", "*.jpg *.png")],
                               title="Choose a file")

    # image = PhotoImage(file=img_name)
    im = Image.open(img_name)
    img_fname = im.filename
    resize_im = im.resize((200, 200), Image.ANTIALIAS)
    alt_im = ImageTk.PhotoImage(resize_im)
    imglabel = Label(top_frame_lft, image=alt_im, width=220, height=220)
    imglabel.photo = alt_im
    imglabel.grid(row=0, column=3, columnspan=2, padx=260, pady=2, sticky=(W,E))


def validate_img():
    if img_name is not None:
        print(img_name)

        validate_url = 'http://127.0.0.1:8080/api/predict/0/img' 
        files = {'file': open(img_name, 'rb')}

        r = requests.post(validate_url, files=files)
        # print(r.json())
        update_prediction_graph(r.json())
    else:
        pass


def load_model(var):
    # var = lmenu.entrycget(index, 'label')
    load_url = 'http://127.0.0.1:8080/api/model/' + str(var)
    print('requesting url {0}'.format(load_url))

    loaded_obj = requests.get(load_url).json()
    print('active model {0}'.format(loaded_obj))


global lr, epoch, hn


def lr_knob(val):
    global lr
    lr = round(float(val), 2)


def epoch_knob(val):
    global epoch
    epoch = int(float(val))


def hn_knob(val):
    global hn
    hn = int(float(val))


def configure():
    print(lr, epoch, hn)
    training_url = 'http://127.0.0.1:8080/api/model/tune'

    payload = {'lr': lr, 'epoch': epoch, 'hn': hn}
    r = requests.post(training_url, data=payload)
    print(r.json())

    update_model_performance_graph(r.json())
    update_lr_vs_p(r.json())
    update_epoch_vs_p(r.json())
    update_hn_vs_p(r.json())


def save_model():
    import uuid
    save_url = 'http://127.0.0.1:8080/api/model/save'

    name = uuid.uuid4().hex
    payload = {'model_name': name[:5]}
    r = requests.post(save_url, data=payload)
    print(r.json())
