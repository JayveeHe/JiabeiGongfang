# encoding:utf8
import json
import requests
from Jiabei import WeixinUtils, task_manager

__author__ = 'Jayvee'

from flask import Flask, request, make_response
import hashlib

app = Flask(__name__)


@app.route('/jiabei', methods=['GET', 'POST'])
def jiabei():
    if request.method == 'GET':
        if len(request.args) > 3:
            temparr = []
            token = "jiabeigongfang"
            signature = request.args["signature"]
            timestamp = request.args["timestamp"]
            nonce = request.args["nonce"]
            echostr = request.args["echostr"]
            temparr.append(token)
            temparr.append(timestamp)
            temparr.append(nonce)
            temparr.sort()
            newstr = "".join(temparr)
            sha1str = hashlib.sha1(newstr)
            temp = sha1str.hexdigest()
            if signature == temp:
                return echostr
            else:
                return "认证失败，不是微信服务器的请求！"
        else:
            return "你请求的方法是：" + request.method
    else:  # POST
        xmldict = WeixinUtils.recv_msg(request.data)
        if xmldict["MsgType"] == "event":
            if xmldict["Event"] == "subscribe":
                reply = WeixinUtils.make_singletext(xmldict["FromUserName"], xmldict["ToUserName"],
                                                    "欢迎关注加贝工坊，希望能与你交流更多有趣的想法！\n输入/帮助 查看相关操作指令。祝愉快！")
            else:
                reply = ""
        else:
            reply = task_manager.check_task(xmldict)
        response = make_response(reply)
        response.content_type = 'application/xml'
        return response


@app.route('/login/', methods=['GET'])
def login_and_have_fun():
    code = request.args.get('code')
    state = request.args.get('state')
    acess_token = ''
    get_acesstoken_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx158f7ee3772b322a&secret=4808311ba12d1dd2c6eea47711583cb2&code=%s&grant_type=authorization_code' % code
    result = requests.get(get_acesstoken_url).content
    print result
    rjson = json.loads(result)
    openid = rjson['openid']
    print openid
    return 'code=%s, state=%s, openid=%s' % (code, state, openid)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=909, debug=True)
