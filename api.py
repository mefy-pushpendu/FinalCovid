import flask
from flask import request
from flask import jsonify
import pickle
import numpy as np
from flask_cors import CORS

covid_model = pickle.load(open('RFCovidModel.pkl', 'rb'))
heart_model = pickle.load(open('RF.pkl', 'rb'))
model = pickle.load(open('done.pkl', 'rb'))
model1=pickle.load(open('noWaist.pkl','rb'))
model2=pickle.load(open('noTrigs983.pkl','rb'))
model3=pickle.load(open('both.pkl','rb'))

app = flask.Flask(__name__)
CORS(app)
# app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Hey There</h1><p>This is main function for the covid API, yet do not works.</p>"


@app.route('/covid/calculate', methods=['POST'])
def calculate_covid():
    if not request.json or not 'gender' or not 'age' or not 'wbc' or not 'platelets' or not 'neutrophils' or not 'lymphocyte' or not 'monocytes' or not 'eosinophils' or not 'basophils' or not 'crp' or not 'ast' or not 'alt' or not 'alp' or not 'ggt' or not 'ldh' in request.json:
        return jsonify({'error': 1, 'message': 'insufficient data', 'data': {}}), 200

    covid_data = [request.json['gender'], request.json['age'], request.json['wbc'], request.json['platelets'], request.json['neutrophils'], request.json['lymphocyte'], request.json['monocytes'],
                  request.json['eosinophils'], request.json['basophils'], request.json['crp'], request.json['ast'], request.json['alt'], request.json['alp'], request.json['ggt'], request.json['ldh']]
    print(covid_data)
    int_features = [float(x) for x in covid_data]
    print(int_features)
    final_features = [np.array(covid_data)]
    print(final_features)
    prediction = covid_model.predict_proba(final_features)
    alpha = 0.70
    beta = 0.70
   # finalProb=
    for i in prediction:
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

    output = []

    output.append(finalProb)
    output.append(prediction[0])
    print("OUTPUT")
    print(output)
    # output.append(prediction[0])
    # also display output from 'prediction' variable
    return jsonify({'prediction': {
        'positive': format(output[1])[0],
        'negetive': format(output[1][0])
    }}), 200


@app.route('/heart/calculate', methods=['POST'])
def calculate_heart():
    if not request.json or not 'age' or not 'gender' or not 'chest_pain_type' or not 'bp' or not 'chol' or not 'fbs' or not 'eks' or not 'hr' or not 'agina' or not 'depre' or not 'slope' in request.json:
        return jsonify({'error': 1, 'message': 'insufficient data', 'data': {}}), 200

    heart_data = [request.json['age'], request.json['gender'], request.json['chest_pain_type'], request.json['bp'], request.json['chol'],
                  request.json['fbs'], request.json['eks'], request.json['hr'], request.json['agina'], request.json['depre'], request.json['slope']]

    int_features = [float(x) for x in heart_data]
    final_features = [np.array(int_features)]

   # prediction = model.predict_proba(final_features)
    prediction = heart_model.predict(final_features)

    output = prediction[0]
    if output < 0.5:
        output1 = 'Normal'
    elif output > 0.5:
        output1 = '10yr CHD risk'

    # output.append(prediction[0])
    # also display output from 'prediction' variable
    return jsonify({'prediction': format(output1)}), 200


@app.route('/diabetes/calculate', methods=['POST'])
def calculate_diabetes():
    if not request.json or not 'gender' or not 'age' or not 'bmi' or not 'waist' or not 'sysbp' or not 'diabp' or not 'albcr' or not 'choles' or not 'glucose' or not 'trigs' or not 'a1c' or not 'serumGlucose' in request.json:
        return jsonify({'error': 1, 'message': 'insufficient data', 'data': {}}), 200

    diabetes_data = [request.json['gender'], request.json['age'], request.json['bmi'], request.json['waist'], request.json['sysbp'],
                  request.json['diabp'], request.json['albcr'], request.json['choles'], request.json['glucose'], request.json['trigs'], request.json['a1c'], request.json['serumGlucose']]

    int_features = [float(x) for x in diabetes_data]
    int_features1=[]
    for i in int_features:
        #for male, it is zero
        if i != 100:
            int_features1.append(i)
        
    final_features = [np.array(int_features1)]
    
    if int_features[3]==100 and int_features[9]==100:
        prediction = model3.predict(final_features)
    elif int_features[9]==100:
        prediction = model2.predict(final_features)
    elif int_features[3]==100:
        prediction = model1.predict(final_features)
    else:
        prediction = model.predict(final_features)


    output = prediction[0]
    if output==0:
        output1='Normal'
    elif output==1:
        output1='Diabetic'
    elif output==2:
        output1='Pre-Diabetic'    

    # output.append(prediction[0])
    # also display output from 'prediction' variable
    return jsonify({'prediction': format(output1)}), 200


app.run()
