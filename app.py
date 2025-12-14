from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the ML model
with open('rf_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    inputs = [
        float(request.form['flow_duration']),
        int(request.form['total_fwd_packets']),
        int(request.form['total_backward_packets']),
        float(request.form['total_length_fwd']),
        float(request.form['fwd_packet_max']),
        float(request.form['idle_mean'])
    ]
    
    # Make prediction
    prediction = model.predict([inputs])
    output = "MALICIOUS" if prediction[0] == 1 else "BENIGN"
    
    # Render results
    return render_template('result.html', prediction=output)

if __name__ == '__main__':
    app.run(debug=True)
