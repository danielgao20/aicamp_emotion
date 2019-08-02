from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import render_template
import os
from ai import get_yolo_net, yolo_forward, yolo_save_img
import cv2
import numpy as np
import time

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024


# here = os.getcwd()
# names_path = os.path.join(here, 'hotdog', 'hotdog1.names')
# # load the COCO class labels our YOLO model was trained on
# LABELS = open(names_path).read().strip().split("\n")
# np.random.seed(42)
# COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
#     dtype="uint8")

# weights_path = os.path.join(here, 'hotdog', 'hotdog1-yolov3-tiny_last.weights')
# cfg_path = os.path.join(here, 'hotdog', 'hotdog1-yolov3-tiny.cfg')
# net = get_yolo_net(cfg_path, weights_path)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))


    return render_template('home.html')


from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    # here = os.getcwd()
    # image_path = os.path.join(here, app.config['UPLOAD_FOLDER'], filename)
    # image = cv2.imread(image_path)
    # (class_ids, labels, boxes, confidences) = yolo_forward(net, LABELS, image, confidence_level=0.5, threshold=0.3)
    
    # if len(class_ids) > 0:
    #     found = True
    #     new_filename = 'yolo_' + filename
    #     file_path = os.path.join(here, app.config['UPLOAD_FOLDER'], new_filename)
    #     yolo_save_img(image, class_ids, boxes, labels, confidences, COLORS, file_path=file_path)
    #     return send_from_directory(app.config['UPLOAD_FOLDER'], new_filename)
    # else:
    #     found = False
    #     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

