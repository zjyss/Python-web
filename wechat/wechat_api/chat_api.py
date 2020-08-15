import time

from flask import jsonify, request, abort
import hashlib
import xmltodict

from . import api

# 微信公众平台设置
wechat_token = 'wechatzhang'


@api.route('/test/')
def test():
    return jsonify({'code': '200'})


@api.route('/chat', methods=['GET', 'POST'])
def chat():
    '''
    设置自动回复
    :return:
    '''
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    # 随机数
    nonce = request.args.get('nonce')
    # 转列表按字典序排序
    target = [wechat_token, timestamp, nonce]
    target.sort()
    temp_str = ''.join(target)
    hash_str = hashlib.sha1(temp_str.encode('utf-8')).hexdigest()
    if not hash_str == signature:
        abort(403)
    else:
        if request.method == 'GET':
            # 微信服务器发来的字符串，验证成功后要返回给微信服务器
            echostr = request.args.get('echostr')
            if not echostr:
                abort(400)
            return echostr
        # 返回字符串
        if request.method == 'POST':
            resp_dict = {}
            xml_data = request.data
            if not xml_data:
                abort(401)
            xml_dict = xmltodict.parse(xml_data)
            xml_dict = xml_dict.get('xml')
            msg_type = xml_dict.get('MsgType')
            if msg_type == 'text':
                resp_dict = {
                    "xml": {
                        "ToUserName": xml_dict.get('FromUserName'),
                        "FromUserName": xml_dict.get('ToUserName'),
                        "CreateTime": int(time.time()),
                        "MsgType": "text",
                        "Content": xml_dict.get('Content')
                    }
                }
            elif msg_type == 'image':
                resp_dict = {
                    "xml": {
                        "ToUserName": xml_dict.get('FromUserName'),
                        "FromUserName": xml_dict.get('ToUserName'),
                        "CreateTime": int(time.time()),
                        "MsgType": "image",
                        "PicUrl": xml_dict.get('PicUrl'),
                        "MediaId": xml_dict.get('MediaId'),
                    }
                }
            resp_xml_dict = xmltodict.unparse(resp_dict)
            print(resp_xml_dict)
            return resp_xml_dict
