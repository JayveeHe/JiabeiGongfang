# coding: utf-8

from wsgiref import simple_server

import leancloud

from app import app
from cloud import engine
from config import token_config


# APP_ID = os.environ.get('LC_APP_ID', 'pelj09whtpy6ipcob33o4zw4jl6850et2be2f1g331lcn7vr')  # your app id
# MASTER_KEY = os.environ.get('LC_APP_MASTER_KEY', '')  # your app master key

leancloud.init(token_config.LEANCLOUD_APP_ID, token_config.LEANCLOUD_APP_KEY)

application = engine

if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    app.debug = True
    server = simple_server.make_server('localhost', token_config.APP_PORT, application)
    server.serve_forever()
