# coding:utf-8
 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
import tensorflow as tf
from tensorflow import keras
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
               
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp']) # 设置允许的文件格式
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

KEYSPACE = "mykeyspacex"
# 数据库 keyspace 
 
# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
                return jsonify({"msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
 
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径

        f.save(upload_path)
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)  # 使用Opencv转换一下图片格式和名称, 用于网页显示
 
        img1 = cv2.imread(upload_path)            # 读入图片
        img_arr=np.array(img1,dtype=np.uint8)    # 将图片转为二维矩阵
        img = (np.expand_dims(img_arr, 0))       # 将图片矩阵转化为一维

        predictions_single = new_model.predict(img) 

        clothName = class_names[np.argmax(predictions_single[0])]
        htmlFile = open(os.path.join(basepath, 'templates', 'upload_ok.html'), "r").read().split('\n')  # 按行读入网页代码
        htmlFile[12] = "<h1>服装名：" + clothName + "</h1>"                                             # 输出模型结果
        fileto = open(os.path.join(basepath, 'templates', 'upload_ok.html'), "w")
        for line in htmlFile:
                print(line, file=fileto)
        fileto.close()

        image_read = open(upload_path, 'rb').read() #图片读取为二进制
        strCQL = "INSERT INTO mytable (QueryTime,QueryImage,QueryAnswer) VALUES (?,?,?)"
        pStatement = session.prepare(strCQL)
        session.execute(pStatement,[time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), image_read, clothName])

        return render_template('upload_ok.html',val1=time.time())
 
    return render_template('upload.html')
 
if __name__ == '__main__':
    cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
    session = cluster.connect()
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % KEYSPACE)
    session.set_keyspace(KEYSPACE)
    session.execute(""" CREATE TABLE IF NOT EXISTS mytable ( QueryTime text, QueryImage blob, QueryAnswer text, PRIMARY KEY(QueryTime)) """)
    # 设置当前使用这个keyspace
    session.execute('USE %s' % KEYSPACE)

    new_model = tf.keras.models.load_model('my_model.h5')
    app.run(host='0.0.0.0', port=5000, debug=True)

