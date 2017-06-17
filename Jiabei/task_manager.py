# coding=utf-8
import json
import os
import re
import sys

abs_path = os.path.dirname(os.path.abspath(__file__))
abs_father_path = os.path.dirname(abs_path)
PROJECT_PATH = abs_father_path
print 'Used file: %s\nProject path=%s' % (__file__, PROJECT_PATH)
sys.path.append(PROJECT_PATH)
sys.path.append(abs_path)

import music_utils
import WeixinUtils
import crawlBlog
from Jiabei.music_taster_utils import get_most_familar_songs

__author__ = 'Jayvee'

reload(sys)
sys.setdefaultencoding('utf8')


def check_task(content_dict={}):
    """
    对用户提交的内容进行统一的识别，并给出相应的回复
    :param content_dict:
    :return:
    """
    func_dict = {u'博客': get_bloglist, u'帮助': get_commandmenu,
                 u'听歌': get_music, u'song': get_music, u's': get_music, u't': get_similar_songs,
                 u'风格': get_similar_songs}
    text = content_dict["Content"]
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    if text[0] == "/" and len(text) > 1:
        # 进入功能模式，首先获取命令
        commd = re.compile(r'/[^ ]*').match(text).group()
        commd = commd[1:]
        commd_content = re.compile(r'/[^ ]* ').sub("", text)
        # print commd
        # print commd_content
        func = func_dict.get(commd)
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
    reply = "你好，可以使用 “/”前缀+短语 进行指令操作，例如：/帮助"
    return WeixinUtils.make_singletext(tousername, fromusername, reply)


def get_commandmenu(content_dict={}):
    """
    返回指令列表
    :param content_dict:
    :return:
    """
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    str_commandmenu = "/帮助：查看所有指令\n" \
                      "/博客：查看作者最新博客\n" \
                      "/听歌 <歌曲名>或/s <歌曲名>：搜索音乐，例如：/s 我为祖国献石油\n" \
                      "/风格 <歌曲名>或/t <歌曲名>:查看最相似的歌曲。"
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
    songname = re.compile(r'/[^ ]* ').sub("", text)
    if len(songname) > 0 and songname != "/听歌":
        songlist = music_utils.get_searchlist(songname, 5)
        if songlist != None:
            return WeixinUtils.make_news(songlist, tousername, fromusername)
        else:
            return WeixinUtils.make_singletext(tousername, fromusername, "未找到相应的歌曲！")
    else:
        return WeixinUtils.make_singletext(tousername, fromusername, "请输入歌曲名！")


def get_similar_songs(content_dict={}):
    """
    返回musictaster结果
    :param content_dict:
    :return:
    """
    text = content_dict["Content"]
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    songname = re.compile(r'/[^ ]* ').sub("", text)
    if len(songname) > 0 and songname != "/t":
        str_similar_list = get_most_familar_songs(song_name=songname)
        slist_obj = json.loads(str_similar_list)
        if slist_obj['code'] == 200:
            resp_text = '【歌名】\t【相似度】'
            for song_item in slist_obj['result']:
                resp_text += '\n%s\t%s' % (song_item['name'], round(song_item['similarity'], 5))
            return WeixinUtils.make_singletext(tousername, fromusername, resp_text)
        else:
            return WeixinUtils.make_singletext(tousername, fromusername, "未找到相应的歌曲！\n%s" % slist_obj['error_msg'])
    else:
        return WeixinUtils.make_singletext(tousername, fromusername, "请输入歌曲名！")


def get_error_resp(content_dict={}):
    """
    输入的指令以-开头，但是没有找到相应的指令关键字
    :param content_dict:
    :return:
    """
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    return WeixinUtils.make_singletext(tousername, fromusername, "指令有误,输入 /帮助 查看指令列表")


    # print check_task({"FromUserName": "123123", "ToUserName": "454564", "Content": "/帮助 查看"})
