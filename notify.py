import configparser

import requests

from coincheck import Coincheck

def edit_message(d, order_type):
    coincheck = Coincheck()
    if order_type == "sell":
        del d["rate"], d["pair"], d["created_at"], d["market_buy_amount"], d["stop_loss_rate"]
        d["bid_rate"] = coincheck.bid_rate
    if order_type == "buy":
        del d["amount"], d["rate"], d["pair"], d["created_at"], d["stop_loss_rate"]
        d["ask_rate"] = coincheck.ask_rate
    return d

def pprint(message):
    s = ""
    if isinstance(message, dict):
        for k, v in message.items():
            s += f"{k}: {v}\n"
        message = s
    return "\n" + message.rstrip("\r\n")

def send_message_to_line(message):
    url = "https://notify-api.line.me/api/notify"

    # 設定ファイルの読み込み
    conf = configparser.ConfigParser()
    conf.read("config.ini")
    ACCESS_TOKEN = conf["line"]["access_token"]

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    data = {"message": pprint(message)}
    
    r = requests.post(url=url, headers=headers, data=data)
