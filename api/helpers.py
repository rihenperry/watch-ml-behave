import numpy
import itertools
import scipy
import scipy.misc
import scipy.special
import PIL
from PIL import Image

from settings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from neuralnet.train import Model

live_model = {}


# make a particular model active and set it as current model
def activate_nn_model(model_name=None):
    global live_model

    if model_name is None and 'default.pki' in live_model:
        print('model {} is already loaded'.format('default.pki'))
    elif model_name in live_model:
        print('model {} is already loaded'.format(model_name))
    else:
        if model_name is None:
            live_model = {}  # empty dict by mutation, I know its bad
            mdl = Model()
            live_model['default.pki'] = mdl.load()
            print('model {} loaded'.format(live_model))
        else:
            mdl = Model(None, model_name)
            live_model[model_name] = mdl.load(model_name)
            print('model {} loaded'.format(live_model))


# get active model instance
def get_active_model():
    return live_model


# check for allowed file type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# prepare the image to test by doing some cleaning on it
# rescale the image and return 784 values
def preprocess_img(img_blob, filename):
    img = Image.open(img_blob)
    img = img.resize((28, 28), PIL.Image.ANTIALIAS)
    file_path = UPLOAD_FOLDER + 'resized.' + (filename
                                              .rsplit('.', 1)[1].lower())
    img.save(file_path)

    img_array = scipy.misc.imread(file_path, flatten=True)

    # reshape from 28x28 to list of 784 values, invert values
    img_data = 255.0 - img_array.reshape(784)

    # then scale data to range from 0.01 to 1.0
    img_data = (img_data / 255.0 * 0.99) + 0.01
    print("min = ", numpy.min(img_data))
    print("max = ", numpy.max(img_data))

    return img_data


# query the neural net
def predict(image_sample):
    n = get_active_model()

    # query the network and extract max arg
    raw_op = n['default.pki'].query(image_sample)
    label = numpy.int64(numpy.argmax(raw_op)).item()

    md_array = numpy.array(raw_op).tolist()
    merged = itertools.chain.from_iterable(md_array)
    percentiles = [round(numpy.float64(x).item(), 2) for x in merged]
    print('label {}, network output ={}'.format(label, percentiles))

    return dict(label=label, stats=percentiles)
