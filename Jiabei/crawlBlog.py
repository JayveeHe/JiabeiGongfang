# coding:utf8
from WeixinUtils import NewsItem

__author__ = 'Jayvee'
import urllib2
from bs4 import BeautifulSoup




def get_archives(maxcount=10):
    """
    获取个人博客的文章列表
    :rtype : object
    :return: postitem类型的list
    """
    baseurl = "http://jayveehe.github.io"
    req = urllib2.Request("http://jayveehe.github.io/archives/")
    html = urllib2.urlopen(req)
    text = html.read()
    soup = BeautifulSoup(text)
    # print soup.prettify()
    count = 1
    postlist = []
    # 添加博客文章列表的链接
    mainitem = NewsItem("http://jayveehe.github.io/archives/", "Jayvee's Blog文章列表",
                        "http://jayveestorage.qiniudn.com/blogtitle.jpg")
    postlist.append(mainitem)
    for article in soup.find_all("a", "archive-article-title"):
        item = NewsItem(baseurl + article["href"], article.text, "http://jayveehe.github.io/jayvee_avatar.jpg")
        # print count, ":", article
        # print article["href"]
        # print item.url
        # print item.title
        if count < maxcount:
            count += 1
            postlist.append(item)
        else:
            break
    # print postlist.__len__()
    return postlist


    # postlist = get_archives()
    # mainbody = WeixinUtils.make_news(postlist, 123, 321)
    # print mainbody