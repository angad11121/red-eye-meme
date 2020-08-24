from flask import Flask, request, render_template, url_for, redirect
from PIL import Image
import numpy as np
import os
import cv2
from gaze_tracking import GazeTracking
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
DIRNAME = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(DIRNAME,"source_img")

# Flask instantiation
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
count = 0

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def imagecov(photoname, relative_eye_size=1.5):
    global count
    '''
    Keep the image in the folder source_image and 
    put in the name of image in photoname
    '''
    photoname = photoname
    sourcename = DIRNAME + '/source_img/' + photoname
    finalname =  DIRNAME + '/static/' + str(count)+".jpg"
    '''
    You can change the relative eye size to optimize the image further
    '''
    # relative_eye_size = 1.5

    gaze = GazeTracking()
    frame = cv2.imread(sourcename)

    # cv2.imshow("Demo1", frame)

    gaze.refresh(frame)
    frame = gaze.annotated_frame()

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    try:
        distance = (left_pupil[0] - right_pupil[0]) * (left_pupil[0] - right_pupil[0]) + (left_pupil[1] - right_pupil[1]) * (left_pupil[1] - right_pupil[1])
    except:
        return False
    distance = np.sqrt(distance)
    print(distance)
    face_image = Image.open(sourcename)
    eye_image = Image.open(DIRNAME + '/source_img/redeye.png')

    eye_image = eye_image.resize((int(distance*2*relative_eye_size),int(distance*relative_eye_size)))
    eye_image = eye_image.rotate(15)

    Image.Image.paste(face_image, eye_image,(left_pupil[0] - int(distance*relative_eye_size),left_pupil[1]-int(distance*relative_eye_size/2)), eye_image) 
    Image.Image.paste(face_image, eye_image,(right_pupil[0] - int(distance*relative_eye_size),right_pupil[1]-int(distance*relative_eye_size/2)), eye_image) 
    count+=1
    # face_image.show()
    face_image.save(finalname)
    # eye_image.show()
    return True

links = {}

# Driver code
@app.route("/failed")
def failure():
    return 'Program failed to find any eyes :('
@app.route("/", methods=['GET','POST'])
def index(): 
    global count
    if request.method=="POST": 
        file = request.files['file']
        if file: 
            filename=secure_filename(file.filename)
            # print("hello "+os.path.join(app.config['UPLOAD_FOLDER'], filename))

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("hello "+ filename)
            if(imagecov(filename)):
                return redirect("static/"+str(count-1)+".jpg")
            else: 
                return redirect(url_for('failure'))
    return render_template('index.html')

if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=8000, debug=True) 
