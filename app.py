from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session, jsonify
from flask_session import Session
import neural_style_ai as nst_ai
import GFPGAN.inference_gfpgan as gfp_gan
import os
import base64, io
import qrcode
import hashlib
import urllib.parse

"""
Template from: https://github.com/alfanme/dts-deployment-ann
"""
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = './static/images/'
# model = load_model('Mask Classification Model_1.npy')
app.secret_key = "f!#&^rty(*wjf(ijf)!#(*!t(h*!%(*&@)"
Session(app)

@app.route('/')
def index():
    # Using md5 hash since it is the fastest hashing algorithm
    # Convert the IP Address string to bytes before hashing
    dir = './static/images/results'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    session["uid"] = hashlib.md5(bytes(ip, 'utf-8')).hexdigest()
    print(session.get("uid"))
    print(ip)
    return render_template('index.html')

@app.route('/process_trans_type', methods=["POST", "GET"])
def process_user_transformation_choice():
    transform_type = request.form['transform-type']
    return redirect(url_for(transform_type))

@app.route('/enchancement')
def enchancement():
    return render_template("upload_for_gfpgan.html")

@app.route('/neural')
def neural():
    all_styles = os.listdir('./static/images/examples')
    all_style_paths = []  # Had to make this because flask cannot format string in html properly
    for i in range(len(all_styles)):
        all_style_paths.append(url_for('static', filename=f"images/examples/{all_styles[i]}"))
        all_styles[i] = all_styles[i].split('.')[0]

    return render_template("neural_styles.html", all_style_paths=all_style_paths, all_styles=all_styles)

@app.route('/render_style', methods=["POST", "GET"])
def show_rendered_image():
    if request.method == 'GET':
        chosen_style = request.args['neural-style']
        computing_device = request.args['computing-device']
        chosen_style.replace('examples', 'styles')  # Change path from example dir to styles dir
        return render_template('upload_photo.html', chosen_style_path=chosen_style, computing_device=computing_device)

    if request.method == 'POST':
        imagestr = request.form['webcam']
        imagestr = imagestr.split('data:image/jpeg;base64,')[1]
        with open("./static/images/webcam.jpg","wb") as f:
            f.write(base64.b64decode(imagestr))

        chosen_style = request.form['neural-style']
        computing_device = request.form['computing-device']
        session['style'] = chosen_style
        session['device'] = computing_device
        return redirect(url_for('render_process'))

@app.route('/render_result')
def render_result():
    before_img = "./static/images/webcam.jpg"
    result_path = url_for('static', filename='images/results/220_neural.jpg')
    qr_path = url_for('static', filename='images/results/qr_results.png')
    #Creating an instance of qrcode
    qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4)
    qr.add_data(request.url_root + result_path)
    print(request.url_root)
    print(request.url_root + result_path)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('./static/images/results/qr_results.png')
    
    return render_template("neural_results.html", after_image=result_path, before_img=before_img, qr_path=qr_path)

@app.route('/render_process')
def render_process():
    chosen_style = session['style']
    computing_device = session['device']
    return render_template("neural_process.html", chosen_style_path=chosen_style, computing_device=computing_device)

@app.route('/get_neural_images')
def get_neural_images():
    all_results = os.listdir('./static/images/results')
    # all_results = sorted(all_results, key=int)
    all_results = sorted(all_results, key=len)
    all_results_path = []  # Had to make this because flask cannot format string in html properly
    for i in range(len(all_results)):
        all_results_path.append(url_for('static', filename=f"images/results/{all_results[i]}"))

    response = {"data" : all_results_path}
    response = jsonify(response)
    return response

@app.route('/queue_ai', methods=["POST"])
def queue_ai():    
    chosen_style = request.form['neural-style']
    computing_device = request.form['computing-device']
    nst_ai.render_all_image(urllib.parse.unquote(chosen_style), "./static/images/webcam.jpg", computing_device)
    # result_path = url_for('static', filename='images/results/999_neural.jpg') 
    return "Done"

@app.route('/upload_gfpgan', methods=["POST"])
def upload_gfpgan():
    if request.method == 'POST':
        imagestr = request.form['webcam']
        imagestr = imagestr.split('data:image/jpeg;base64,')[1]
        with open("./static/images/webcam.jpg","wb") as f:
            f.write(base64.b64decode(imagestr))

    return redirect(url_for('gfpgan_results'))

@app.route('/gfpgan_results')
def gfpgan_results():
    gfp_gan.main()
    before_img = "./static/images/webcam.jpg"
    restored_img = "./static/images/results/webcam.jpg"
    qr_path = url_for('static', filename='images/results/qr_gan_results.png')
    #Creating an instance of qrcode
    qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4)
    qr.add_data(request.url_root + restored_img)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('./static/images/results/qr_gan_results.png')
    return render_template("gfpgan_results.html",before_img=before_img, restored_img=restored_img, qr_path=qr_path)
if __name__ == '__main__':
    app.run(debug=True)
