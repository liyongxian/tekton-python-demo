# -*- coding: utf-8 -*-
__version__ = '1.0.0'
__doc__ = '''
    handler oss-putobject event 
'''

import os
import json
import time
import logging
import requests
import traceback
from functools import wraps
from enum import Enum, unique

import redis
import pika
import oss2

"""
Define Hyper Parameters Here
"""
# Http config
INTERNAL_SCHEME = 'http'
HTTP_TIMEOUT = 10
# default retry times
SUPPLIER = 'ali'
REGION_DICT = {'cn-hangzhou': 'hz', 'cn-shanghai': 'sh', 'cn-beijing': 'bj', 'cn-shenzhen': 'sz'}

# log level must be one of : [TRACE, DEBUG, INFO, WARN, ERROR]
__log_level = 'INFO'
__http_timeout = 10
__internal_scheme = INTERNAL_SCHEME
__redis_host, __redis_port, __redis_auth, __redis_timeout = '', 6379, '', 10

__redis_service, __http_sender = None, None
__oss_helper = None

logging.basicConfig(level=__log_level)

class Logger(object):
    def __init__(self, prefix=''):
        self.__prefix = prefix
        self.logger = logging.getLogger()

    @property
    def prefix(self):
        return self.__prefix

    @prefix.setter
    def prefix(self, s):
        self.__prefix = s

    def debug(self, msg):
        self.logger.debug(self.prefix + " | " + msg)

    def info(self, msg):
        self.logger.info(self.prefix + " | " + msg)

    def warning(self, msg):
        self.logger.warning(self.prefix + " | " + msg)

    def error(self, msg):
        self.logger.error(self.prefix + " | " + msg)


logging.getLogger('pika').setLevel(logging.WARNING)
logger = Logger()

# services
class HttpSender(object):
    def __init__(self, internal_scheme: str, timeout: int):
        self.internal_scheme = internal_scheme
        self.timeout = timeout

    def send_post(self, host: str, path: str, body: dict, params: dict = None):
        res = requests.post(url=host + path, json=body, timeout=self.timeout, params=params)

class RedisService(object):
    def __init__(self, host: str, port: int = 5672, password: str = '', timeout: int = 10):
        self.__host = host
        self.__port = port
        self.__password = password
        self.__timeout = timeout
        self.__client = redis.StrictRedis(
            host=host, port=port, password=password, socket_connect_timeout=timeout, socket_timeout=timeout)

    def operate_redis(self, key: str):
        self.__client.get(key)

class OssHelper(object):

    def get_metadata_from_oss(self, credentials, endpoint, bucket_name, obj_name):
        """
        get all metadata of a object from aliyun-oss
        """
        return dict()


class UploadHandler(object):
    def __init__(
            self, redis_service: RedisService, http_sender: HttpSender):
        self.redis_service = redis_service
        self.http_sender = http_sender

    def handle_upload_event(self, evt, metadata):
        self.redis_service.operate_redis("key")
        self.http_sender.send_post("host", "path", dict(), dict())
        

def read_environ():
    """
    get environment parameter
    """
    global __log_level,  __internal_scheme, \
        __redis_host, __redis_port, __redis_auth, __redis_timeout
    __internal_scheme = 'https' if os.environ.get('INTERNAL_SCHEME') is not None and os.environ.get(
        'INTERNAL_SCHEME').lower() == 'https' else 'http'
    # redis
    __redis_host, __redis_auth = \
        os.environ.get('REDIS_HOST'), os.environ.get('REDIS_AUTH')
    if 'REDIS_PORT' in os.environ.keys() and os.environ.get('REDIS_PORT').isdigit():
        __redis_port = int(os.environ.get('REDIS_PORT'))
    if 'REDIS_TIMEOUT' in os.environ.keys() and os.environ.get('REDIS_TIMEOUT').isdigit():
        __redis_timeout = int(os.environ.get('REDIS_TIMEOUT'))

# if you open the initializer feature, please implement the initializer function, as below
def initializer(context):
    global __redis_service, __http_sender, __oss_helper, logger
    logger = Logger('initialize')
    read_environ()
    oss2.set_stream_logger(level=logging.WARNING)
    __redis_service = RedisService(__redis_host, __redis_port, __redis_auth, __redis_timeout)
    __http_sender = HttpSender(__internal_scheme, __http_timeout, __host_msg2mq, __path_checkfile2mq)
    __oss_helper = OssHelper()

def main(evt: dict, creds):
    #global __oss_helper
    #oss_obj_key = evt['oss']['object']['key']
    #logger.prefix = oss_obj_key
    #region = evt['region']
    #bucket_name = evt['oss']['bucket']['name']
    #inner_endpoint = 'http://oss-{}-internal.aliyuncs.com'.format(region)
    #if __oss_helper is None:
    #    __oss_helper = OssHelper()
    #metadata = __oss_helper.get_metadata_from_oss(creds, inner_endpoint, bucket_name, oss_obj_key)
    #upload_handler = UploadHandler(__redis_service, __http_sender)
    #return upload_handler.handle_upload_event(evt, metadata)
    print(event)
    print(creds)
    return "hello world!"

def handler(event, context):
    global logger
    logger = Logger('handler')
    creds = context.credentials
    try:
        evt = json.loads(event)
        main(evt['events'][0], creds)
    except BaseException as e:
        logger.error('handler catch exception from main: {}'.format(traceback.format_exc()))
    return 'end'
