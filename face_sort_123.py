import face_recognition as fr
import sys
import os
import cv2
import face_recognition
import numpy as np
from time import sleep
import glob
def get_encoded_faces():
    """
    looks through the faces folder and encodes all
    the faces
    :return: dict of (name, image encoded)
    """
    encoded = {}
    for dirpath, dnames, fnames in os.walk("/media/patient/02/project_F/Korean-Models/testtttt"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("/media/patient/02/project_F/Korean-Models/testtttt/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding
    return encoded
def unknown_image_encoded(img):
    """
    encode a face given the file name
    """
    print(123)
    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]
    return encoding
def classify_face(im, path2):
    """
    will find all of the faces in a given image and label
    them if it knows what they are
    :param im: str of file path
    :return: list of face names
    """
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())
    img = cv2.imread(im, 1)
    try:
        face_locations = face_recognition.face_locations(img)
        unknown_face_encodings = face_recognition.face_encodings(img, face_locations)
        face_names = []
        for face_encoding in unknown_face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(faces_encoded, face_encoding)
            name = "Unknown"
            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            face_names.append(name)
        print(os.path.basename(str(im)))
        for faces in face_names:
            if faces != "Unknown":
                print(path2)
                if not os.path.exists(path2+'/'+im.split('/')[-2]):
                    print(path2+'/'+im.split('/')[-2])
                    os.mkdir(path2+'/'+im.split('/')[-2])

                cv2.imwrite(path2 + '/'+im.split('/')[-2]+'/'+im.split('/')[-1], img)
    except:
        print('No Face')
        pass
#for all the files in the directory
def main(path, path2):
    #for all the files in the directory
#     print(path)
    f = glob.glob(path+'/*')
    for i in f:
#         print(i)
        ff = glob.glob(i+'/*')
        for y in ff:
            print(y)
            classify_face(y, path2)
if __name__ == "__main__":
   main(sys.argv[1], sys.argv[2])
