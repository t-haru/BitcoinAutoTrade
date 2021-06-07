# ライブラリのインポート
import hmac
import hashlib
import json
import time

import requests

class Coincheck(object):
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.url = "https://coincheck.com"

    def _request(self, endpoint, params=None, method="GET"):
        time.sleep(1)
        # 認証
        nonce = str(int(time.time()))

        body = json.dumps(params) if params else ""

        message = nonce + endpoint + body

        signature = hmac.new(self.secret_key.encode(),
                            message.encode(),
                            hashlib.sha256).hexdigest()

        headers = {
            "ACCESS-KEY": self.access_key,
            "ACCESS-NONCE": nonce,
            "ACCESS-SIGNATURE": signature,
            "Content-Type": "application/json"
        }

        try:
            if method == "GET":
                r = requests.get(endpoint, headers=headers, params=params)
            else:
                r = requests.post(endpoint, headers=headers, data=body)
        except Exception as e:
            print(e)
            raise

        return r.json()

    # 各種最新情報を取得
    def ticker(self):
        endpoint = self.url + "/api/ticker"
        return self._request(endpoint=endpoint)

    # 最後の取引の価格
    @property
    def last(self):
        return self.ticker()["last"]

    # 最新の取引履歴を取得
    def trades(self, params):
        endpoint = self.url + "/api/trades"
        return self._request(endpoint=endpoint, params=params)

    # 板情報を取得
    def order_books(self, params=None):
        endpoint = self.url + "/api/order_books"
        return self._request(endpoint=endpoint, params=params)

    # 残高を確認
    def balance(self):
        endpoint = self.url + "/api/accounts/balance"
        return self._request(endpoint=endpoint)
    
    # 残高
    @property
    def position(self):
        balance = self.balance()
        return {k: v for k, v in balance.items()
                if isinstance(v, str) and float(v)}

    # 新規注文
    def order(self, params):
        endpoint = self.url + "/api/exchange/orders"
        return self._request(endpoint=endpoint, params=params, method="POST")

    # 自分の最近の取引履歴を参照
    def transaction(self):
        endpoint = self.url + "/api/exchange/orders/transactions"
        return self._request(endpoint=endpoint)

    # 約定価格
    @property
    def ask_rate(self):
        transaction = self.transaction()
        ask_transaction = [d for d in transaction["transactions"] if d["side"] == "buy"]
        return float(ask_transaction[0]["rate"])
    
    @property
    def bid_rate(self):
        transaction = self.transaction()
        bid_transaction = [d for d in transaction["transactions"] if d["side"] == "sell"]
        return float(bid_transaction[0]["rate"])

    # 取引所の注文を元にレートを算出
    def rate(self, params):
        endpoint = self.url + "/api/exchange/orders/rate"
        return self._request(endpoint=endpoint, params=params)