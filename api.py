import flask
from flask import request
from flask import jsonify
import pickle
import numpy as np
from flask_cors import CORS

model = pickle.load(open('RFCovidModel.pkl', 'rb'))
app = flask.Flask(__name__)
CORS(app)
# app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Hey There</h1><p>This is main function for the covid API, yet do not works.</p>"


@app.route('/covid/calculate', methods=['POST'])
def calculate_covid():
    if not request.json or not 'gender' or not 'age' or not 'wbc' or not 'platelets' or not 'neutrophils' or not 'lymphocyte' or not 'monocytes' or not 'eosinophils' or not 'basophils' or not 'ast' or not 'alt' or not 'alp' or not 'ggt' or not 'ldh' in request.json:
        return jsonify({'error': 1, 'message': 'insufficient data', 'data': {}}), 200

    covid_data = [request.json['gender'],request.json['age'],request.json['wbc'],request.json['platelets'],request.json['neutrophils'],request.json['lymphocyte'],request.json['monocytes'],request.json['eosinophils'],request.json['basophils'],request.json['ast'],request.json['alt'],request.json['alp'],request.json['ggt'],request.json['ldh']]
    print(covid_data)
    int_features = [float(x) for x in covid_data]
    print(int_features)
    final_features = [np.array(covid_data)]
    print(final_features)
    # prediction = model.predict(final_features)
    prediction = model.predict_proba(final_features)
    alpha = 0.80
    beta = 0.4
    print(prediction)
   # finalProb=[]
    for i in prediction:
        print(i)
     # print("list: i is:",i)
        if i[1] > alpha and i[1] > i[0]:
            ele = i[1]
           # print("positive")
            add = 1
            finalProb = add
            # finalLabelProb.append(add)

        elif i[0] > beta and i[0] > i[1]:
           # print("negative")
            add = 0
            finalProb = add
            # finalLabelProb.append(add)
        else:
            #print("abstention incurred")
            add = 2
            # remove prob with target as 2
            finalProb = add

    output = finalProb
    # also display output from 'prediction' variable
    return jsonify({'prediction': format(output)}), 200


app.run()
