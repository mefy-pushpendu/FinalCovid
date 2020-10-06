import numpy as np
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
import pickle
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
model = pickle.load(open('Final.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():
    '''
    For rendering results on HTML GUI
    '''
    if("text" == "M"):
        text = 1
    else:
        text =0

    data = request.get_json()

    # int_f eatures = [float(x) for x in request.form.values()]
    final_features = [np.array(data['userdata'])]
    print(final_features)
    prediction = model.predict(final_features)

    output  = round(prediction[0], 13)

    # return render_template('index1.html', prediction_text='The Patient is {}'.format(output))
    return json.dumps({'score':format(output)})

if __name__ == "__main__":
    app.run(debug=True)
