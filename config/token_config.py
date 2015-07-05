import json

__author__ = 'Jayvee'
import os

filedir = os.path.dirname(__file__)
token_config = json.loads(open(r'%s/config.json' % filedir, 'r').read())
# print token_config
LOGENTRIES_TOKEN = token_config['LOGENTRIES_TOKEN']
LOG_TAG = token_config['LOG_TAG']
# ROLLBAR_TOKEN = ""
APP_ENV = token_config['APP_ENV']
LEANCLOUD_APP_ID = token_config['LEANCLOUD_APP_ID']
LEANCLOUD_APP_KEY = token_config['LEANCLOUD_APP_KEY']
LEANCLOUD_APP_MASTER_KEY = token_config['LEANCLOUD_APP_MASTER_KEY']
APP_PORT = token_config['APP_PORT']
# init shell
# sh_output = open('%s/avoscloud_setup.sh' % filedir, 'w')
# shell_str = 'avoscloud add senz.analyzer.user.staticinfo.degree.dev %s\navoscloud deploy' % LEANCLOUD_APP_ID
# # print shell_str
# sh_output.write(shell_str)