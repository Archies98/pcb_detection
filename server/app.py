import os
from flask import Flask, flash, request, redirect, url_for, make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS
from PIL import Image
import torch
from werkzeug.exceptions import BadRequest
import cv2
import io
from io import BytesIO

app = Flask(__name__)
CORS(app)


@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_prediction(img_bytes):
    print('before')
    img = Image.open(io.BytesIO(img_bytes))
    # inference
    model = torch.hub.load('ultralytics/yolov5', 'custom',
                           path='models_train/best.pt', force_reload=True)
    results = model(img, size=640)
    print('after')
    print(results)
    return results


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        app.logger.info("In post")
        # check if the post request has the file part
        if 'file' not in request.files:
            app.logger.info("No file part")
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            app.logger.info('No selected file')
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # print(os.path.join())
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            response = predict(file.filename)
            print(response)
            # image = Image.open(io.BytesIO(response.im_arr))
            # image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'result.jpg'))
            print(type(response))
            return response
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


def extract_img(request):
    # checking if image uploaded is valid
    if 'file' not in request.files:
        raise BadRequest("Missing file parameter!")

    file = request.files['file']

    if file.filename == '':
        raise BadRequest("Given file is invalid")

    return file


def predict(file):
    print('*****')
    file = os.path.join('uploads/', file)
    print(file)
    img = Image.open(file)
    # Create a buffer to hold the bytes
    buf = BytesIO()

    # Save the image as jpeg to the buffer
    img.save(buf, 'jpeg')

    # Rewind the buffer's file pointer
    buf.seek(0)

    # Read the bytes from the buffer
    image_bytes = buf.read()

    # Close the buffer
    buf.close()

    # choice of the model
    # results = get_prediction(img_bytes,dictOfModels[request.form.get("model_choice")])
    results = get_prediction(image_bytes)
    # print(f'User selected model : {request.form.get("model_choice")}')

    # updates results.imgs with boxes and labels
    results.render()

    # encoding the resulting image and return it
    for img in results.ims:
        RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_arr = cv2.imencode('.jpg', RGB_img)[1]
        response = make_response(im_arr.tobytes())
        response.headers['Content-Type'] = 'image/jpeg'
    # RGB_img = cv2.cvtColor(results, cv2.COLOR_BGR2RGB)
    # im_arr = cv2.imencode('.jpg', RGB_img)[1]
    # response = make_response(im_arr.tobytes())
    # response.headers['Content-Type'] = 'image/jpeg'
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
