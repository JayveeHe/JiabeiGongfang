# coding=utf-8
__author__ = 'Jayvee'
import time
import xml.etree.ElementTree as ET
import sys
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')


class NewsItem:
    def __init__(self, url, title, picurl=""):
        self.url = url
        self.title = title
        self.picurl = picurl


def recv_msg(oriData):
    """
    获取从微信服务器post而来的消息
    :param oriData: post的data
    :return:返回一个包含发送者、接收者、消息内容的字典
    """
    xmldata = ET.fromstring(oriData)
    # 获取发送方的ID
    fromusername = xmldata.find("FromUserName").text
    # 接收方的ID
    tousername = xmldata.find("ToUserName").text
    # 消息的类别
    msgtype = xmldata.find("MsgType").text
    if msgtype == "event":
        event = xmldata.find("Event").text
        xmldict = {"FromUserName": fromusername, "ToUserName": tousername, "MsgType": msgtype, "Event": event}
    else:
        # 消息的内容
        content = xmldata.find("Content").text
        xmldict = {"FromUserName": fromusername, "ToUserName": tousername, "MsgType": msgtype, "Content": content}
    return xmldict


def make_singletext(tousername="", fromusername="", text=""):
    """
    编制回复信息
    :param content_dict:
    :return:
    """
    # toname = content_dict["FromUserName"]
    # fromname = content_dict["ToUserName"]
    # content = content_dict["Content"]
    # content = "对啊，%s，然后呢" % (text)
    reply = """
    <xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        <FuncFlag>0</FuncFlag>
    </xml>"""
    resp_str = reply % (tousername, fromusername, int(time.time()), text)
    return resp_str


def make_news(newslist, touser, fromuser):
    """
    根据NewsItem的列表等创建多图文消息
    :param newslist:
    :param touser:
    :param fromuser:
    :return:
    """
    mainbody = '''
        <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[news]]></MsgType>
            <ArticleCount>%s</ArticleCount>
            <Articles>
                %s
            </Articles>
        </xml>'''

    post_count = min(10, len(newslist))
    itemslist = []
    for index in range(post_count):
        item = newslist[index]
        items_body = '''
        <item>
            <Title><![CDATA[%s]]></Title>
            <Description><![CDATA[description]]></Description>
            <PicUrl><![CDATA[%s]]></PicUrl>
            <Url><![CDATA[%s]]></Url>
        </item>'''
        items_body = items_body % (item.title, item.picurl, item.url)
        itemslist.append(items_body)
    mainbody = mainbody % (touser, fromuser, str(time.time()), str(post_count), "".join(itemslist))
    # soup = BeautifulSoup(mainbody)
    # return soup.prettify()
    return mainbody
