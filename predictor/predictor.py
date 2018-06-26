from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
import pandas
import numpy
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import pickle
import os


app = Flask(__name__)
CORS(app)

model_position = None
model_position_version = None
model_drink = None
model_drink_version = None


@app.route('/')
def home_route():
    return render_template('models.html', model_drink_version=model_drink_version,
                           model_position_version=model_position_version, available_models=get_available_models())


@app.route('/active')
def active_model_route():
    model_file = request.args.get('file')
    print('Make model active: ' + model_file)

    if 'position' in model_file:
        global model_position_version
        model_position_version = model_file
        global model_position
        model_position = pickle.load(open('models/' + model_file, 'rb'))

    if 'drink' in model_file:
        global model_drink_version
        model_drink_version = model_file
        global model_drink
        model_drink = pickle.load(open('models/' + model_file, 'rb'))

    return redirect('/')


@app.route('/delete')
def delete_model_route():
    model_file = request.args.get('file')
    print('Make model delete: ' + model_file)

    data_file = model_file.replace('_model.sav', '.csv')
    os.remove('models/' + model_file)
    os.remove('data/' + data_file)

    return redirect('/')


@app.route('/upload', methods=['POST'])
def upload_file_route():
    if 'file' not in request.files:
        print('No file part')
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        print('No selected file')
        return redirect('/')
    if file and ('_drink.csv' in file.filename or '_position.csv' in file.filename):
        file.save('data/' + file.filename)

        day = file.filename.replace(
            '_drink.csv', '').replace('_position.csv', '')
        load_function = None
        name = ''
        if 'position' in file.filename:
            load_function = load_data_position
            name = 'position'
        if 'drink' in file.filename:
            load_function = load_data_drink
            name = 'drink'
        train_model(load_function, name, day)

    return redirect('/')


@app.route('/predict/<model_type>')
def predict_route(model_type):
    model = None
    result_array = None
    feature_count = None
    if 'position' == model_type:
        model = model_position
        # Need to keep result_array in sync with visualiser.js or proxy it all
        result_array = ['bar', 'toilet', 'smoke']
        feature_count = 10
    elif 'drink' == model_type:
        model = model_drink
        # Need to keep result_array in sync with visualiser.js or proxy it all
        result_array = ['beer', 'whiteWine', 'redWine', 'water', 'coke']
        feature_count = 2
    else:
        return jsonify({'error': True, 'msg': 'No model type called set for ' + model_type, 'model_type_param': model_type})

    features_string = request.args.get('features')
    if not features_string:
        return jsonify({'error': True, 'msg': 'Features parameter not set', 'model_type_param': model_type})
    featuresArray = features_string.split(',')
    if len(featuresArray) != feature_count:
        return jsonify({'error': True, 'msg': 'Features parameter must have 10 comma separated values', 'model_type_param': model_type})
    features = numpy.reshape(featuresArray, (1, -1))
    result = model.predict(features)
    score = model.predict_proba(features)
    # print(result)
    # print(score)
    return jsonify({
        'result': result_array[int(result[0]) - 1],
        'score': score[0][result[0] - 1]
    })


def get_available_models():
    model_list = os.listdir('models')
    model_list.sort()
    model_datas = []
    for model_file in model_list:
        print(model_file)
        day = model_file.replace('_position_model.sav', '').replace(
            '_drink_model.sav', '')
        load_function = None
        active = False
        model_type = ''
        if 'position' in model_file:
            load_function = load_data_position
            active = model_file == model_position_version
            model_type = 'position'
        if 'drink' in model_file:
            load_function = load_data_drink
            active = model_file == model_drink_version
            model_type = 'drink'
        dataset, y_col = load_function(day)

        X_train, X_validation, Y_train, Y_validation, X, Y, seed = split_out_dataset(
            dataset, y_col)

        loaded_model = pickle.load(open('models/' + model_file, 'rb'))
        result = loaded_model.score(X_validation, Y_validation)
        model_data = {'name': model_file,
                      'shape': str(dataset.shape[0]) + ' rows x ' + str(dataset.shape[1]) + ' columns', 'score': result, 'type': model_type, 'active': active}
        print(model_data)
        model_datas.append(model_data)
    return model_datas


def load_default_models():
    model_list = os.listdir('models')
    print(model_list)

    position_models = [x for x in model_list if 'position' in x]
    if len(position_models) > 0:
        position_models.sort()
        position_model_file = position_models[0]
        global model_position_version
        model_position_version = position_model_file
        global model_position
        model_position = pickle.load(
            open('models/' + position_model_file, 'rb'))

    drink_models = [x for x in model_list if 'drink' in x]
    if len(drink_models) > 0:
        drink_models.sort()
        drink_model_file = drink_models[0]
        global model_drink_version
        model_drink_version = drink_model_file
        global model_drink
        model_drink = pickle.load(
            open('models/' + drink_model_file, 'rb'))


def load_data_position(day):
    # Load data
    print('Load data position')
    url = "data/" + day + "_position.csv"
    names = ['position_1_x', 'position_1_z', 'position_2_x', 'position_2_z', 'position_3_x',
             'position_3_z', 'position_4_x', 'position_4_z', 'position_5_x', 'position_5_z', 'location_text', 'location']
    dataset = pandas.read_csv(url, names=names)
    print(dataset.groupby('location_text').size())
    dataset = dataset.drop(columns='location_text')
    print(dataset)
    print(dataset.shape)
    y_col = dataset.shape[1] - 1
    print('y_col = ' + str(y_col))
    print(dataset.columns)
    return dataset, y_col


def load_data_drink(day):
    # Load data
    print('Load data drink')
    url = "data/" + day + "_drink.csv"
    names = ['position_1_x', 'position_1_z',
             'user_id', 'location_text', 'location']
    dataset = pandas.read_csv(url, names=names)
    print(dataset.groupby('user_id').size())
    print(dataset.groupby('location_text').size())
    dataset = dataset.drop(columns='user_id')
    dataset = dataset.drop(columns='location_text')
    print(dataset)
    print(dataset.shape)
    y_col = dataset.shape[1] - 1
    print('y_col = ' + str(y_col))
    print(dataset.columns)
    return dataset, y_col


def split_out_dataset(dataset, y_col):
    print('Split out dataset')
    array = dataset.values
    X = array[:, 0: y_col]
    Y = array[:, y_col]
    validation_size = 0.20
    seed = 7
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(
        X, Y, test_size=validation_size, random_state=seed)
    return X_train, X_validation, Y_train, Y_validation, X, Y, seed


def validate_argorithms(X_train, Y_train, seed):
    print('Validate algorithms')
    models = []
    # models.append(('LR', LogisticRegression())) # Too slow
    # models.append(('LDA', LinearDiscriminantAnalysis())) # Too slow
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('CART', DecisionTreeClassifier()))
    models.append(('FOR', RandomForestClassifier()))
    # models.append(('NB', GaussianNB())) # Too slow
    # models.append(('SVM', SVC()))  # Too slow

    # Evaluate each model in turn
    scoring = 'accuracy'
    results = []
    names = []
    for name, model in models:
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        cv_results = model_selection.cross_val_score(
            model, X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)


def create_model(model_type, X_train, Y_train):
    print('Create model')
    model = model_type
    model.fit(X_train, Y_train)
    return model


def make_predictions_on_validation_set(model, X_validation, Y_validation):
    print('Make predictions on validation set')
    predictions = model.predict(X_validation)
    print(accuracy_score(Y_validation, predictions))
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))


def train_model(load_function, name, day):
    print('Training model:')

    # Load data
    dataset, y_col = load_function(day)

    # Split - out validation dataset
    X_train, X_validation, Y_train, Y_validation, X, Y, seed = split_out_dataset(
        dataset, y_col)

    # Validate Algorithms
    validate_argorithms(X_train, Y_train, seed)

    # Create model
    model = create_model(KNeighborsClassifier(), X_train, Y_train)

    # Make predictions on validation dataset
    make_predictions_on_validation_set(model, X_validation, Y_validation)

    # Persist model
    filename = 'models/' + day + '_' + name + '_model.sav'
    pickle.dump(model, open(filename, 'wb'))

    # Load model
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.score(X_validation, Y_validation)
    print(result)


if __name__ == '__main__':
    load_default_models()
    app.run(host='0.0.0.0', port=5101)
