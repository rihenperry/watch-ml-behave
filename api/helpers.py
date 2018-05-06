import numpy
import itertools
import scipy
import scipy.misc
import scipy.special
import PIL
from PIL import Image

from settings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from neuralnet.train import Model, Learn
from neuralnet import test

live_model = {}
current_tuning = {}


# make a particular model active and set it as current model
def activate_nn_model(model=None):
    global live_model
    model_name = None

    if type(model) == dict:
        model_name = list(model.keys())[0]
    else:
        model_name = model

    if model_name is None and 'default.pki' in live_model:
        print('model {0} is already loaded'.format('default.pki'))
    elif model_name in live_model and (model_name != 'current.pki'):
        print('model {0} is already loaded'.format(model_name))
    else:
        if model_name is None:
            live_model = {}  # empty dict by mutation, I know its bad
            mdl = Model()
            live_model['default.pki'] = mdl.load()
            print('model {0} loaded'.format(live_model))
        elif type(model) == dict:
            live_model = {}
            live_model = model
            print('model {0} loaded'.format(live_model))
        else:
            live_model = {}
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
    current_model = list(n.keys())[0]
    raw_op = n[current_model].query(image_sample)
    label = numpy.int64(numpy.argmax(raw_op)).item()

    md_array = numpy.array(raw_op).tolist()
    merged = itertools.chain.from_iterable(md_array)
    percentiles = [round(numpy.float64(x).item(), 2) for x in merged]
    print('label {}, network output ={}'.format(label, percentiles))

    return dict(label=label, stats=percentiles)


def set_current_tuning(obj):
    global current_tuning
    current_tuning = obj


def get_current_tuning():
    return current_tuning


def tuneD(lr, hn, epoch):
    lrn = Learn(lr, hn, epoch)
    n = lrn.run()
    test.run(n)
    accuracy = test.results()

    return {
        'lr': lr,
        'hidden_nodes': hn,
        'epoch': epoch,
        'accuracy': accuracy,
        'current.pki': n,
        'lr_vs_p': (str(lr) + ',' + str(accuracy)),
        'epoch_vs_p': (str(epoch) + ',' + str(accuracy)),
        'hn_vs_p': (str(hn) + ',' + str(accuracy))
    }
