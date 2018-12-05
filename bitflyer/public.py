import requests
import simplejson as json
from urllib.parse import urlencode, quote_plus
"""
document: https://lightning.bitflyer.jp/docs
"""

base_url = "https://api.bitflyer.com/v1/"
api_urls = { 'getticker'     : '/getticker',
             'getexecutions' : '/getexecutions',
             'getboard'      : '/getboard',
             'gethealth'     : '/gethealth'
             }

class Public(object):
    def __init__(self):
        pass


    def public_api(self,url, **kwargs):
        ''' template function of public api'''
        params = ''
        if kwargs:
            params = '?%s' % urlencode(kwargs, quote_via=quote_plus)

        requrl = base_url + api_urls.get(url) + params

        try :
            url in api_urls
            return json.loads(requests.get(requrl).text)
        except Exception as e:
            print('ERROR request %s: %s' % (requrl, e))

    def getticker(self, product_code=None):
        '''Ticker を取得'''
        if product_code:
            return self.public_api('getticker', product_code=product_code)
        else:
            return self.public_api('getticker')

    def getboard(self):
        ''' 板情報を取得 '''
        return self.public_api('getboard')

    def getexecutions(self):
        ''' 約定の一覧を取得 '''
        return self.public_api('getexecutions')

    def gethealth(self):
        '''get exchange health'''
        return self.public_api('gethealth')
