# coding:utf-8
 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify

from werkzeug.utils import secure_filename

import os
import cv2
import time

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np

import matplotlib.pyplot as plt

from PIL import Image 

from datetime import timedelta
from skimage import io

new_model = tf.keras.models.load_model('my_model.h5')

fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

#for i in range(30):
#	img = Image.fromarray(test_images[i]) # 将array转化成图片
#	img.save("%d.jpg" % i)

# fileimage = open("testimage/1.jpg", "r")
basepath = os.path.dirname(__file__)
upload_path = os.path.join(basepath, 'testImage', '0.jpg')
img1 = io.imread(upload_path)
img_arr=np.array(img1,dtype=np.uint8) 


img = (np.expand_dims(img_arr, 0)) # 将图片矩阵转化为一维

predictions_single = new_model.predict(img) 

print(class_names[np.argmax(predictions_single[0])])
