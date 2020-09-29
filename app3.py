import numpy as np
from flask import Flask, jsonify, request, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('classifier.pkl', 'rb'))

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

    if(output == 1):
        return render_template('index1.html', prediction_text='The Patient is Corona Positive')
    else:
        return render_template('index1.html', prediction_text='The Patient is Corona Negative')


if __name__ == "__main__":
    app.run(debug=True)
