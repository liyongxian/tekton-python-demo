import os

from flask import Flask, request
import index
import time
import logging

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_world():
    app.logger.info("helloworld start-------------------------")
    app.logger.info(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    target = os.environ.get('TARGET', 'World')
    header=request.headers
    data=request.stream.read()
    #print("print info start-------------------------")
    #app.logger.info(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    #print(header)
    #print(data)
    #app.logger.info(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    #print("print info end-------------------------")
    #print("logger info start-------------------------")
    #app.logger.info(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    app.logger.info(header)
    app.logger.info(data)
    index.handler(data, header)
    app.logger.info(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    app.logger.info("logger info end-------------------------")
    return 'Hello {}!\n'.format(target)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
