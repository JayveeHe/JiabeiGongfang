# encoding:utf8
import WeixinUtils

__author__ = 'Jayvee'

from flask import Flask, request, make_response
import hashlib

import task_manager

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
        if xmldict["MsgType"] == "Event":
            reply = WeixinUtils.make_singletext(xmldict["FromUserName"], xmldict["ToUserName"],
                                                "欢迎关注加贝工坊，输入/帮助 查看相关操作指令。祝愉快！")
        else:
            reply = task_manager.check_task(xmldict)
        response = make_response(reply)
        response.content_type = 'application/xml'
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=909, debug=True)
