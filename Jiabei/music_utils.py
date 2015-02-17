# coding:utf8
import json
import urllib
import urllib2
from WeixinUtils import NewsItem

__author__ = 'Jayvee'


# class MusicUtils:
# @staticmethod
def get_searchlist(name, limit):
    data = {"s": name, "type": "1", "limit": limit}
    value = urllib.urlencode(data)
    req = urllib2.Request("http://music.163.com/api/search/get/web")
    req.add_header("Referer", "http://music.163.com/")
    html = urllib2.urlopen(req, value).read()
    jsonobj = json.loads(html)
    list = []
    for obj in jsonobj["result"]["songs"]:
        name = obj["name"]
        artistname = obj["artists"][0]["name"]
        albumname = obj["album"]["name"]
        songid = obj["id"]
        details = json.loads(get_songdetails(songid))
        songurl = "http://music.163.com/m/song/%s" % songid
        ltemp = [""]
        ltemp.append(name)
        ltemp.append("\n")
        ltemp.append(artistname)
        ltemp.append("-")
        ltemp.append(albumname)
        songtitle = "".join(ltemp)
        picurl = details["songs"][0]["album"]["picUrl"]
        list.append(NewsItem(songurl, songtitle, picurl))
    return list


# @staticmethod
def get_songdetails(songid):
    url = 'http://music.163.com/api/song/detail/?id=%s&ids=%%5B%s%%5D&csrf_token=Method=GET' % (songid, songid)
    req = urllib2.Request(url)
    req.add_header("Referer", "http://music.163.com/")
    resp = urllib2.urlopen(req)
    return resp.read()


    # ilist = MusicUtils.get_searchlist("半兽人", 5)
    # for ii in ilist:
    # print ii.title
    # print ii.url
    #     print ii.picurl