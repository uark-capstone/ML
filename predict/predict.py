from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import json


def load_data(file_name):
    with open(file_name, 'r') as data_file:
        data = json.load(data_file) 
        input_data = data['input_data']
        output_data = data['output_data']

    data_file.close();
    print(input_data)

    print(output_data)

    return (input_data, output_data)


def train_model(input, output):
    model = LogisticRegression(solver='lbfgs', max_iter=100000)
    model.fit(input, output)

    acc = accuracy_score(output, model.predict(input))
    print('Accuracy: ' + str(acc))
    return model


def train_and_predict(data_file, input):
    input_data, output_data = load_data(data_file)
    model = train_model(input_data, output_data)

    return model.predict(input)

# new_input = [[80.96, 7.49, 9.37, 0, 0, 0]]
# new_output = model.predict(new_input)

# print(new_input, new_output)