import requests
import time
import hmac
import hashlib
import simplejson as json
import re
import os,sys
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(current_dir,'.'))
from bitflyer.utils import make_nonce
from urllib.parse import urlencode, quote_plus

"""
document: https://lightning.bitflyer.jp/docs?lang=ja
"""


class Private(object):

    def __init__(self,
                 access_key=None,
                 secret_key=None):
        self.access_key     = access_key
        self.secret_key     = secret_key
        self.url           = 'https://api.bitflyer.com'
        self.timestamp      = make_nonce()

    def base_get(self,path=None,**kwargs):
        '''
        API base function
        '''
        params = ''
        if kwargs:
            params = '?%s' % urlencode(kwargs, quote_via=quote_plus)

        timestamp = self.timestamp
        uri = self.url + path + params
        method = 'GET'
        text = timestamp + method + path + params
        sign = hmac.new(self.secret_key.encode('utf-8'), text.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {
                    'ACCESS-KEY': self.access_key,
                    'ACCESS-TIMESTAMP':  timestamp,
                    'ACCESS-SIGN':  sign
                    }



        r = requests.get(uri,
                         headers = headers)
        if r.text:
            result = { 'status_code': r.status_code, 'response': json.loads(r.text) }
        else:
            result = { 'status_code': r.status_code }
        return result

    def base_post(self,path=None,**kwargs):
        '''
        base post function
        '''
        timestamp = self.timestamp
        body = str(kwargs)
        method = 'POST'
        uri = self.url + path
        text = timestamp + method + path + body
        sign = hmac.new(self.secret_key.encode('utf-8'), text.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {
                    'ACCESS-KEY': self.access_key,
                    'ACCESS-TIMESTAMP':  timestamp,
                    'ACCESS-SIGN':  sign,
                    'Content-Type': 'application/json'
                    }
        r = requests.post(uri,
                         headers = headers,
                         data    = body
                         )
        if r.text:
            result = { 'status_code': r.status_code, 'response': json.loads(r.text) }
        else:
            result = { 'status_code': r.status_code }
        return result


    def getbalance(self,**kwargs):
        '''
        Show user balance

        parameters
            None
        '''
        return self.base_get(path = '/v1/me/getbalance', **kwargs)

    def getcollateral(self,**kwargs):
        '''
        Show user information

        parameters
            None

        '''
        return self.base_get(path = '/v1/me/getcollateral', **kwargs)

    def sendchildorder(self,**kwargs):
        '''
        send child order

        parameters
            product_code     : str: (required) 'BTC_JPY' or 'FX_BTC_JPY'
            child_order_type : str
            side             : str
            price            : int
            size             : float
        see for more detail:
        https://lightning.bitflyer.jp/docs?lang=ja#新規注文を出す
        '''
        return self.base_post(path='/v1/me/sendchildorder',**kwargs)

    def sendparentorder(self,**kwargs):
        ...

    def cancelchildorder(self,**kwargs):
        '''
        send cancel child order

        parameters
            product_code     :str: (required) 'BTC_JPY' or 'FX_BTC_JPY'
            child_order_id   :str: Order ID to be canceled.
            child_order_acceptance_id :str: Acceptance ID to be caneld.

        see for more detail:
        https://lightning.bitflyer.jp/docs?lang=ja#注文をキャンセルする
        '''
        return self.base_post(path='/v1/me/cancelchildorder',**kwargs)

    def cancelparentorder(self,**kwargs):
        ...

    def cancelallchildorders(self,**kwargs):
        '''
        send cancel all child order

        parameters
            product_code     :str: (required) 'BTC_JPY' or 'FX_BTC_JPY'
        see for more detail:
        https://lightning.bitflyer.jp/docs?lang=ja#すべての注文をキャンセルする
        '''
        return self.base_post(path='/v1/me/cancelallchildorders',**kwargs)


    def getchildorders(self,**kwargs):
        '''
        Get child orders

        parameters
            None

        '''
        return self.base_get(path='/v1/me/getchildorders',**kwargs)

    def getparentorders(self,**kwargs):
        '''
        Get child orders

        parameters
            None

        '''
        return self.base_get(path='/v1/me/getparentorders',**kwargs)

    def getparentorder(self,**kwargs):
        '''
        Get child orders

        parameters
            None

        '''
        return self.base_get(path='/v1/me/getparentorder',**kwargs)

    def getexecutions(self,**kwargs):
        '''
        Get child orders

        parameters
            None

        '''
        return self.base_get(path='/v1/me/getexecutions',**kwargs)

    def getpositions(self,**kwargs):
        '''
        Get positions

        parameters
            None

        '''
        return self.base_get(path='/v1/me/getpositions',**kwargs)

    def getpermissions(self,**kwargs):
        '''
        Get permissiions

        parameters
            None

        '''
        return self.base_get(path='/v1/me/getpermissions',**kwargs)

    def gettradingcommission(self,product_code='BTC_JPY', **kwargs):
        '''
        Get traddingcommission

        parameters
            None

        '''
        return self.base_get(
            path='/v1/me/gettradingcommission',
            product_code=product_code,
            **kwargs
        )


    def getbalancehistory(self, currency_code='JPY', count=100, before=0, after=0, **kwargs):
        '''
        Get balance history

        parameters
            None

        '''
        return self.base_get(
            path='/v1/me/getbalancehistory',
            currency_code=currency_code, count=count, before=before, after=after,
            **kwargs
        )


    def getcollateralhistory(self,count=100, before=0, after=0, **kwargs):
        '''
        Get collateral  history

        parameters
            None

        '''
        return self.base_get(
            path='/v1/me/getcollateralhistory',
            count=count, before=before, after=after,
            **kwargs
        )

    def getcoinins(self,count=100, before=0, after=0, **kwargs):
        '''
        Get coin ins

        parameters
            None

        '''
        return self.base_get(
            path='/v1/me/getcoinins',
            count=count, before=before, after=after,
            **kwargs
        )


    def getcoinouts(self, count=100, before=0, after=0, **kwargs):
        '''
        Get coin outs

        parameters
            None

        '''
        return self.base_get(
            path='/v1/me/getcoinouts',
            count=count, before=before, after=after,
            **kwargs
        )



    def getwithdrawals(self, count=100, before=0, after=0, message_id=None, **kwargs):
        '''
        Get withdrawals

        parameters
            None

        '''
        return self.base_get(
            path='/v1/me/getwithdrawals',
            count=count, before=before, after=after, message_id=message_id,
            **kwargs
        )

