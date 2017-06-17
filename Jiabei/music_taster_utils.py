# coding=utf-8

"""
Created by jayvee on 2017/6/18.
https://github.com/JayveeHe
"""
import requests


def get_most_familar_songs(song_name, top_k=10):
    try:
        get_url = 'http://api.jayveehe.com/musictaster/similar/song/%s' % song_name
        req = requests.get(get_url)
        return req.content
    except Exception, e:
        print 'error, details=%s' % e


if __name__ == '__main__':
    print get_most_familar_songs('可爱女人')
