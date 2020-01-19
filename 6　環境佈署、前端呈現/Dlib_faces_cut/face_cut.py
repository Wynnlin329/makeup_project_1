from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import numpy as np
import imutils
import dlib
import cv2

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("C:/Users/Big data/Desktop/db104_2_project/Dlib_faces_cut/data/dlib/shape_predictor_68_face_landmarks.dat")
fa = FaceAligner(predictor, desiredFaceWidth=361)

face_filename = 1


def detect_face_landmarks(filename):
    try:
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 1)

        for face in faces:
            (x, y, w, h) = rect_to_bb(face)
            # faceOrig = imutils.resize(img[y: y + h, x: x + w], width=200)
            faceAligned = fa.align(img, gray, face)
            global face_filename
            # cv2.imwrite('data/images/faces_result/faceOrig_{0}.png'.format(face_filename), faceOrig)
            cv2.imwrite('C:/Users/Big data/Desktop/db104_2_project/static/456.jpg'.format(face_filename), faceAligned)
            face_filename += 1
    except Exception as f:
        print(f)



# filename = "data/images/faces_for_test/IU.jpg"
filename = "C:/Users/Big data/Desktop/db104_2_project/static/123.jpg"
detect_face_landmarks(filename)