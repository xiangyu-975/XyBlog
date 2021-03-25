from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_(!zgr+82bhdhy_)07p6s+v%q4(l!^-(ab@&dvh5z$37a32xh1'
# "l9(!^=2prtj_9)&=h6%-hmk!6&ind*@53+1716cwf8oz81@0t7"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
HAYSTACK_CONNECTIONS['default']['URL'] = 'http://192.168.73.131:9200/'
