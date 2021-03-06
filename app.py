from flask import Flask, render_template, request, send_from_directory, session
import os
from data_prep import *

"""
Template from: https://github.com/alfanme/dts-deployment-ann
"""

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads/'
model = load_model('Mask Classification Model_1.npy')
app.secret_key = "f!#&^rty(*wjf(ijf)!#(*!t(h*!%(*&@)"
class_dict = {0: 'No Mask', 1: 'With Mask'}
def predict_label(img_path):
    loaded_img = load_img(img_path, target_size=(64, 64))
    img_array = img_to_array(loaded_img)
    predicted_bit = predict_image(img_array,model).astype('int')
    return class_dict[int(predicted_bit)]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.files:
            #So previously uploaded files are not   

            image = request.files['image']
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(img_path)
            prediction = predict_label(img_path)
            session['image'] = image.filename
            return render_template('index.html', uploaded_image=image.filename, prediction=prediction)

    return render_template('index.html')

@app.route('/display/<filename>')
def send_uploaded_image(filename=''):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)