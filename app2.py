import numpy as np
from flask import Flask, jsonify, request, render_template
import pickle
import json

app = Flask(__name__)
model = pickle.load(open('PreFinal.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    if("text" == "M"):
        text = 1
    else:
        text =0
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 12)

    return render_template('index1.html', prediction_text='The Patient is {}'.format(output))
    #return json.dumps({prediction:format(output)})

if __name__ == "__main__":
    app.run(debug=True)
