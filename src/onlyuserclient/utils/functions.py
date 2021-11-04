'''工具函数
'''
import os
import datetime
import random
from onlyuserclient.settings import billing_settings
from onlyuserclient.settings import onlyuser_settings
from django.core.cache import caches, cache


def get_bill_cache():
    try:
        ch = caches[billing_settings.CACHE_ENGINE]
    except:
        ch = cache
    return ch
    
def get_onlyuser_cache():
    try:
        ch = caches[onlyuser_settings.CACHE_ENGINE]
    except:
        ch = cache
    return ch

def generate_cache_key(pfx, *args, **kwargs):
    keystr = ''
    for arg in args:
        keystr += '{}'.format(arg)
    for k, v in kwargs.items():
        keystr += '{}:{}'.format(k, v)
    return '{}:{}'.format(pfx, hash(keystr))


def generate_serial_number(prefix=''):
    '''生成序列号
    '''    
    g = globals()
    counter = g.get('_SERIAL_NUMBER_COUNTER', None)
    current = datetime.datetime.now()
    pfx = current.strftime('%Y%m%d%H%M%S')
    if counter is None:
        counter = {
            'pfx': pfx,
            'count': 0 
        }
        
    systype = os.name
    host = 'Unkwon hostname%d'%(random.randint(0, 99999999999))
    if systype == 'nt':
        host = os.getenv('computername')
    elif systype == 'posix':
        h = os.popen('echo $HOSTNAME')
        try:
            host = h.read()
        finally:
            h.close()
    if pfx == counter['pfx']:
        counter['count'] += 1
    else:
        counter['pfx'] = pfx
        counter['count'] = 0    
    g['_SERIAL_NUMBER_COUNTER'] = counter
    hostid = '%s%d'%(host, os.getpid())
    return '%s%s%04d%02d'%(prefix, pfx, abs(hash(hostid)>>56), counter['count'])

