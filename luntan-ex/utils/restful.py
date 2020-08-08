"""json
{
    "code":200,
    "message":""，
    "data":{
        "name":"",
        "age":18
    },
    "flag":0
}
200成功
401 没有授权
400 参数有错误
500 服务器有问题
"""
from flask import jsonify


class HttpCode(object):
    success = 200
    unautherror = 401  # 没有授权
    paramserror = 400  # 参数错误
    servererror = 500  # 服务器的错误


def result(code, message, data, flag):
    return jsonify({'code': code, 'message': message, 'data': data, 'flag': flag, })


def success(flag=0, message='', data=None):
    return result(HttpCode.success, message=message, data=data, flag=flag, )


def unauth_error(message=''):
    return result(HttpCode.unautherror, message=message, data=None, flag=None)


def parms_error(message=''):
    return result(HttpCode.paramserror, message=message, data=None, flag=None)


def server_error(message=''):
    return result(HttpCode.servererror, message=message, data=None)
