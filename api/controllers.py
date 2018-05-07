# make flask imports
from flask import jsonify, request
from werkzeug.utils import secure_filename
# from flask import request, redirect, url_for

# import app object and db container
from . import db
from . import endpoint
from . import helpers

# import ORM models
from api.models import HyperParams, ModelGraphData
from neuralnet.train import Model


@endpoint.route('/', methods=["GET"])
def index():
    # initialize gui
    # load the default model and
    # return model's hyperparameters and graph data
    helpers.activate_nn_model()
    active_model = helpers.get_active_model()
    data = list()
    hypers = HyperParams.query.all()

    for hyper in hypers:
        item = {
            'model_id': hyper.id,
            'created_at': hyper.created_at,
            'lr': hyper.lr,
            'epoch': hyper.epoch,
            'hidden_nodes': hyper.hidden_nodes,
            'model_name': hyper.model_name,
            'accuracy': hyper.accuracy,
            'graph_id': hyper.graph_plot.id,
            'lr_vs_p': hyper.graph_plot.lr_vs_p,
            'epoch_vs_p': hyper.graph_plot.epoch_vs_p,
            'hn_vs_p': hyper.graph_plot.hn_vs_p
        }
        data.append(item)

    return jsonify(data=data, current_model=list(active_model.keys())[0]), 200


# loads a specific model
@endpoint.route('/model/<int:model_id>', methods=["GET"])
def loadmodel(model_id):
    # load given ml model profile into tkinter gui
    hyper = HyperParams.query.get(model_id)

    if hyper is not None:
        helpers.activate_nn_model(hyper.model_name)
        response = {
            'model_id': hyper.id,
            'created_at': hyper.created_at,
            'lr': hyper.lr,
            'epoch': hyper.epoch,
            'hidden_nodes': hyper.hidden_nodes,
            'model_name': hyper.model_name,
            'accuracy': hyper.accuracy,
            'graph_id': hyper.graph_plot.id,
            'lr_vs_p': hyper.graph_plot.lr_vs_p,
            'epoch_vs_p': hyper.graph_plot.epoch_vs_p,
            'hn_vs_p': hyper.graph_plot.hn_vs_p
        }
        return jsonify(loaded=response), 200
    else:
        msg = 'model with id {0} not found'.format(model_id)
        return jsonify(msg=msg), 404


@endpoint.route('/model/all', methods=["GET"])
def allmodel():
    bag = {}
    models = HyperParams.query.with_entities(HyperParams.id,
                                             HyperParams.model_name,
                                             HyperParams.created_at)

    for model in models:
        bag[model.id] = {
            'name': model.model_name,
            'created_at': model.created_at
        }

    return jsonify(model_list=bag), 200


@endpoint.route('/model/tune', methods=['POST'])
def modeltune():
    # upon receiving tuning data, name the model using given name
    # train nn with new config by running it in subprocess
    # once done, save it to current_tuning
    # set as active model
    # return status and model data
    obj = helpers.tuneD(float(request.form['lr']),
                        int(request.form['hn']),
                        int(request.form['epoch']))

    helpers.set_current_tuning(obj)
    helpers.activate_nn_model({'current.pki': obj['current.pki']})

    current_model = obj
    current_model.pop('current.pki', None)
    current_model['model_name'] = 'current.pki'
    return jsonify(live_model=current_model), 200


@endpoint.route('/model/save', methods=['POST'])
def savemodel():
    # check if model name exists in db if not save else say already exist
    # get current_tuning config and dump it to database
    model_name = request.form['model_name']
    model_name += '.pki'
    obj = helpers.get_current_tuning()
    brain_label = list(helpers.get_active_model().keys())[0]
    brain = helpers.get_active_model()[brain_label]
    obj['model_name'] = model_name

    hyper = HyperParams(lr=obj['lr'],
                        epoch=obj['epoch'],
                        hidden_nodes=obj['hidden_nodes'],
                        model_name=obj['model_name'],
                        accuracy=obj['accuracy'])
    graph = ModelGraphData(hyper_parameters=hyper,
                           lr_vs_p=obj['lr_vs_p'],
                           epoch_vs_p=obj['epoch_vs_p'],
                           hn_vs_p=obj['hn_vs_p'])
    db.session.add(graph)
    db.session.commit()

    m = Model(brain, model_name)
    m.save()
    helpers.set_current_tuning({})
    helpers.activate_nn_model(obj['model_name'])

    return jsonify(saved_model=obj), 200


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
