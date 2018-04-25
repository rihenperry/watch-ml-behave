# make flask imports
from flask import jsonify, request, Response
from werkzeug.utils import secure_filename
# from flask import request, redirect, url_for

# import app object and db container
from . import app
from . import endpoint
from . import helpers

# import ORM models
# from api.models import HyperParams, ModelGraphData


@endpoint.route('/', methods=["GET"])
def index():
    import json
    # initialize gui
    # load the default model and
    # return model's hyperparameters and graph data
    helpers.activate_nn_model()
    active_model = helpers.get_active_model()

    return jsonify(model=list(active_model.keys())[0]), 200


# loads a specific model
@endpoint.route('/<string:model_name>', methods=["GET"])
def loadmodel(model_name='defaults'):
    # load given ml model profile into tkinter gui
    msg = 'Model {0}'.format(model_name)
    return jsonify(msg=msg), 200


@endpoint.route('/predict/<string:model_id>/img', methods=["POST"])
def validate(model_id=0):
    # 1. check for image extension
    # 1.1 If not png type then convert to png
    # 2. rescale the image to 28X28 pixel and to 784 values
    # 3. convert those 784 values between 0.01 to 1.0
    # query the nn and conclude
    print('model in use {0}, model id {1}'.format(
                     helpers.get_active_model(),
                     model_id))

    if 'file' not in request.files:
        return jsonify({
            'text': 'file not found'
        }), 404

    file = request.files['file']

    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return jsonify({
            'text': 'no selected file'
        }), 403

    if file and helpers.allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # call preprocess func
        img_data = helpers.preprocess_img(file, filename)

        # call predict function over the file
        output_data = helpers.predict(img_data)

        return jsonify(label=output_data['label'],
                       stats=output_data['stats']), 200
    else:
        return jsonify({
            'text': 'file not secure'
        }), 403
