# coding=utf-8
import music_utils

import WeixinUtils
import crawlBlog

__author__ = 'Jayvee'


def check_task(content_dict={}):
    """
    对用户提交的内容进行统一的识别，并给出相应的回复
    :param content_dict:
    :return:
    """
    func_dict = {"m": get_bloglist, "h": get_commandmenu, "s": get_music}
    text = content_dict["Content"]
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    if text[0] == "-" and len(text) > 1:
        # 进入功能模式
        func = func_dict.get(text[1])
        if func is not None:
            # print "function:", text[1]
            return func(content_dict)
        else:
            return get_error_resp(content_dict)
    else:
        return get_defaultresp(content_dict)


def get_bloglist(content_dict={}):
    """
    输入的指令为-m，则列出博客的文章列表
    :param content_dict:
    :return:
    """
    bloglist = crawlBlog.get_archives(5)
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    return WeixinUtils.make_news(bloglist, tousername, fromusername)


def get_defaultresp(content_dict={}):
    """
    返回指令列表
    :param content_dict:
    :return:
    """
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    reply = "感谢关注加贝工坊！\n可以使用 “-”前缀+字母 进行指令操作，例如：-h"
    return WeixinUtils.make_singletext(tousername, fromusername, reply)


def get_commandmenu(content_dict={}):
    """
    返回指令列表
    :param content_dict:
    :return:
    """
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    str_commandmenu = "-h：查看所有指令\n" \
                      "-m：查看作者最新博客\n" \
                      "-s <歌曲名>:搜索音乐"
    return WeixinUtils.make_singletext(tousername, fromusername, str_commandmenu)


def get_music(content_dict={}):
    """
    返回云音乐爬取结果
    :param content_dict:
    :return:
    """
    text = content_dict["Content"]
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    songname = text.split(" ")[1]
    songlist = music_utils.get_searchlist(songname, 5)
    return WeixinUtils.make_news(songlist, tousername, fromusername)


def get_error_resp(content_dict={}):
    """
    输入的指令以-开头，但是没有找到相应的指令关键字
    :param content_dict:
    :return:
    """
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    return WeixinUtils.make_singletext(tousername, fromusername, "指令有误,输入-h查看指令列表")

print check_task({"FromUserName": "123123", "ToUserName": "454564", "Content": "-s yellow"})