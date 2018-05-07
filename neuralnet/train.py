import os
import numpy
from neuralnet.core import neuralNetwork
import dill as pickle
import settings


class Learn:
    def __init__(self,
                 lrate=float(os.getenv('LEARNING_RATE')),
                 hnodes=int(os.getenv('HIDDEN_NODES')),
                 epochs=int(os.getenv('EPOCHS')),
                 in_nodes=int(os.getenv('INPUT_NODES')),
                 onodes=int(os.getenv('OUTPUT_NODES'))):
        # load default model parameters
        # number of input, hidden and output nodes
        self.__input_nodes = in_nodes
        self.__hidden_nodes = hnodes
        self.__output_nodes = onodes

        # epochs is the number of times the training data set is used
        # for training
        self.__epochs = epochs

        # learning rate
        self.__learning_rate = lrate

    def read_mnist(self):
        # load the mnist training data CSV file into a list
        CONFIG_PATH = os.path.join(settings.ROOT_DIR, os.getenv('TRAIN_PATH'))
        training_data_file = open(CONFIG_PATH, 'r')
        training_data = training_data_file.readlines()
        training_data_file.close()

        return training_data

    def run(self):
        training_data_list = self.read_mnist()

        # create instance of neural network
        n = neuralNetwork(self.__input_nodes, self.__hidden_nodes,
                          self.__output_nodes, self.__learning_rate)

        for e in range(self.__epochs):
            # go through all records in the training data set
            for record in training_data_list:
                # split the record by the ',' commas
                all_values = record.split(',')
                # scale and shift the inputs
                inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
                # create the target output values (all 0.01,
                # except the desired label which is 0.99)
                targets = numpy.zeros(self.__output_nodes) + 0.01
                # all_values[0] is the target label for this record
                targets[int(all_values[0])] = 0.99
                n.train(inputs, targets)
                pass
            pass

        return n

    def setparams(self, hnodes, epochs, lrate):
        self.__hidden_nodes = hnodes
        self.__epochs = epochs
        self.__learning_rate = lrate

    def getparams(self):
        hyper_params = {
            'epoch': self.__epochs,
            'input_nodes': self.__input_nodes,
            'learning_rate': self.__learning_rate,
            'output_nodes': self.__output_nodes,
            'hidden_nodes': self.__hidden_nodes
        }

        return hyper_params


class Model:
    def __init__(self, instance=None, model_name=None):
        if instance is not None:
            self.instance = instance

        if model_name is not None:
            self.model_name = model_name
        else:
            self.model_name = 'default.pki'

    def load(self, model_name=None):
        loaded_model = None
        CONFIG_PATH = os.path.join(settings.ROOT_DIR,
                                   os.getenv('PICKLE_MODEL_PATH'))

        if model_name is not None:
            model_path = CONFIG_PATH + model_name
            print(model_path)
        else:
            model_path = CONFIG_PATH + 'default.pki'

        with open(model_path, 'rb') as file:
            loaded_model = pickle.load(file)
            print('nn ', loaded_model)
        print('mdl.load() ', loaded_model)
        return loaded_model

    def save(self):
        CONFIG_PATH = os.path.join(settings.ROOT_DIR,
                                   os.getenv('PICKLE_MODEL_PATH'))
        model_path = CONFIG_PATH + self.model_name

        with open(model_path, 'wb') as file:
            pickle.dump(self.instance, file)

    def get(self, model_name=None):
        # get from sql
        pass
