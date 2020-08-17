

## MNIST Flask Demo 

----

1. We use Keras with a TensorFlow backend to train a small network to recognize fashion image.
2. We then save the model structure and weights to a h5 file.
3. We use Flask to load the model and to predict the input fashion image.
4. We save all the input data and output data Casandra.
5. We use HTML to help display the whole process.
----


## How to run

1. Connect to Apache Cassandra database:

``` bash
docker run --name some-cassandra --network mnist-network -p 9042:9042 -d cassandra:latest
```

2. build the image:

``` bash
docker build -t fashion_mnist_project .
docker run -d --network mnist-network -p 5000:5000 fashion_mnist_project
```

*Note: We can also run locally. To do that, simply run the following commands:*

``` bash
sudo pip install -r requirements.txt
python3 upload_pictures.py
```

Then visit `http://0.0.0.0:5000/upload` to upload some fashion image.

There are some sample image in /app/testImage:

```
app/
testImage/
├── 0.jpg
├── 1.jpg
├── 2.jpg
├── 3.jpg
├── 4.jpg
├── 5.jpg
├── 6.jpg
├── 7.jpg
├── 8.jpg
├── 9.jpg
├── 10.jpg
├── 11.jpg
├── 12.jpg
├── 13.jpg
├── 14.jpg
├── 15.jpg
├── 16.jpg
├── 17.jpg
├── 18.jpg
├── 19.jpg
├── 20.jpg
├── 21.jpg
├── 22.jpg
├── 23.jpg
├── 24.jpg
├── 25.jpg
├── 26.jpg
├── 27.jpg
├── 28.jpg
└── 29.jpg
```


Then click upload buttom to upload fashion image to see the result.

3. Export query history

Run `python /app/cassandraInsert.py` to export all query records to directory `/app/`   with format like `Time_FashionName.jpg`.


