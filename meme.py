from PIL import Image
import numpy as np
import os
import cv2
from gaze_tracking import GazeTracking

'''
Keep the image in the folder source_image and 
put in the name of image in photoname
'''
photoname = 'harss.png'
sourcename = 'source_img/' + photoname
finalname = 'final_img/' + photoname
'''
You can change the relative eye size to optimize the image further
'''
relative_eye_size = 1.5



gaze = GazeTracking()
frame = cv2.imread(sourcename)

# cv2.imshow("Demo1", frame)

gaze.refresh(frame)
frame = gaze.annotated_frame()

left_pupil = gaze.pupil_left_coords()
right_pupil = gaze.pupil_right_coords()

distance = (left_pupil[0] - right_pupil[0]) * (left_pupil[0] - right_pupil[0]) + (left_pupil[1] - right_pupil[1]) * (left_pupil[1] - right_pupil[1])
distance = np.sqrt(distance)
print(distance)
face_image = Image.open(sourcename)
eye_image = Image.open('source_img/redeye.png')

eye_image = eye_image.resize((int(distance*2*relative_eye_size),int(distance*relative_eye_size)))
eye_image = eye_image.rotate(15)

Image.Image.paste(face_image, eye_image,(left_pupil[0] - int(distance*relative_eye_size),left_pupil[1]-int(distance*relative_eye_size/2)), eye_image) 
Image.Image.paste(face_image, eye_image,(right_pupil[0] - int(distance*relative_eye_size),right_pupil[1]-int(distance*relative_eye_size/2)), eye_image) 
face_image.show()
face_image.save(finalname)
# eye_image.show()



