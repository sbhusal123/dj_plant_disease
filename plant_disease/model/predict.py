from sklearn.preprocessing import LabelBinarizer
from keras.preprocessing.image import img_to_array
from keras.models import load_model


import numpy as np
import pickle
import cv2
import os
import tensorflow as tf



default_image_size = tuple((256, 256))

label_pkl_path = os.path.join(os.path.dirname(__file__), './model_files/label_list.pkl')
h5_model_path = os.path.join(os.path.dirname(__file__), './model_files/mymodel.h5')

def convert_image_to_array(image_dir):
    try:
        image = cv2.imread(image_dir)
        if image is not None :
            image = cv2.resize(image, default_image_size)
            return img_to_array(image)
        else :
            return np.array([])
    except Exception as e:
        print(f"Error : {e}")
        return None

def get_pickle_label_binarizer(path_to_pickle_file):
    """Takes a path of pickle file containing label list and returns LabelBinarizer"""

    # Load pickle file
    open_file = open(path_to_pickle_file, "rb")
    label_list = pickle.load(open_file)
    open_file.close()

    # fit the dataset labels
    label_binarizer = LabelBinarizer()
    label_binarizer.fit_transform(label_list)
    return label_binarizer



def predict_disease(image_path):
    # load model
    model = load_model(h5_model_path)

    # normalize image
    image_array = convert_image_to_array(image_path)
    np_image = np.array(image_array, dtype=np.float16) / 225.0
    np_image = np.expand_dims(np_image,0)

    label_binarizer = get_pickle_label_binarizer(label_pkl_path)

    # Predict 
    result = model.predict_classes(np_image)

    # return label
    return label_binarizer.classes_[result][0]
