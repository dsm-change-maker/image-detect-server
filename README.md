# image-detect-server with darknet

A simple server that returns whether or not there are people in the image.

```
# install darknet
$ git clone https://github.com/pjreddie/darknet
$ cd darknet
$ make
$ wget https://pjreddie.com/media/files/yolov3.weights

# run the darkent for test
$ ./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg
...
dog: 99%
truck: 93%
bicycle: 99%

# install this server
$ git clone https://github.com/dsm-change-maker/image-detect-server.git
$ cd image-detect-server

# run this server
# python3 app.py [darknet dir path] [host] [port]
$ python3 app.py ../darknet 127.0.0.1 5000

# test request
$ curl -F 'file=@./test.jpg' 127.0.0.1:5000/upload
{"is_there_anyone":true}
```
