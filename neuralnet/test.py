import os
import numpy
import settings
from neuralnet.train import Model
# test the neural network

# scorecard for how well the network performs, initially empty
scorecard = []


def read_mnist_testdata():
    # load the mnist test data CSV file into a list
    CONFIG_PATH = os.path.join(settings.ROOT_DIR, os.getenv('TEST_PATH'))
    test_data_file = open(CONFIG_PATH, 'r')
    test_data = test_data_file.readlines()
    test_data_file.close()
    return test_data


def run(neural=None):
    test_data_list = read_mnist_testdata()
    if neural is not None:
        n = neural
    else:
        mdl = Model()
        n = mdl.load()

    # go through all the records in the test data set
    for record in test_data_list:
        # split the record by the ',' commas
        all_values = record.split(',')
        # correct answer is first value
        correct_label = int(all_values[0])
        # scale and shift the inputs
        inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        # query the network
        outputs = n.query(inputs)
        # the index of the highest value corresponds to the label
        label = numpy.argmax(outputs)
        # append correct or incorrect to list
        if (label == correct_label):
            # network's answer matches correct answer, add 1 to scorecard
            scorecard.append(1)
        else:
            # network's answer doesn't match correct answer, add 0 to scorecard
            scorecard.append(0)
            pass

        pass


def results():
    # calculate the performance score, the fraction of correct answers
    scorecard_array = numpy.asarray(scorecard)
    performance = scorecard_array.sum() / scorecard_array.size
    print("performance = ", performance)

    return performance
