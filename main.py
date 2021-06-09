# ライブラリのインポート
import configparser
import datetime
import time

import pandas as pd

from coincheck import Coincheck
from flag import check
from logic.bollinger_band import Bollinger_band
from logic.macd import MACD
from logic.rsi import RSI
from notify import send_message_to_line

# 設定ファイルの読み込み
conf = configparser.ConfigParser()
conf.read("config.ini")

ACCESS_KEY = conf["coincheck"]["access_key"]
SECRET_KEY = conf["coincheck"]["secret_key"]

coincheck = Coincheck(access_key=ACCESS_KEY, secret_key=SECRET_KEY)

print("**************************************************")
print("自動取引開始")
send_message_to_line("自動取引開始")

# 空のデータフレームを作成
df = pd.DataFrame()

# フラグ
flag = {
    "buy": {
        "BB": False,
        "MACD": False,
        "RSI": False
    },
    "sell": {
        "BB": False,
        "MACD": False,
        "RSI": False
    }
}

# 変数の設定
INTERVAL = 59
AMOUNT = 0.008
DURATION = 20

# 期間の設定
bb_duration = 20        # ボリンジャーバンドの期間

short_duration = 9      # 短期移動平均の期間
long_duration = 26      # 長期移動平均の期間
signal_duration = 9     # シグナルの計算に用いるMACDの期間

rsi_duration = 14

# ループの準備
cnt = 1

bb = Bollinger_band(bb_duration)
macd = MACD(short_duration, long_duration, signal_duration)
rsi = RSI(rsi_duration)

while True:
    time.sleep(INTERVAL)
    print("**************************************************")

    position = coincheck.position
    if not position.get("jpy"):
        print("日本円がありません")
        send_message_to_line("日本円がありません")
        raise

    # ビットコインの最新価格を取得する
    df = df.append({"price": coincheck.last}, ignore_index=True)

    # データの収集
    if len(df) < DURATION:
        # LOG出力
        dt_now = datetime.datetime.now()
        print("Loop:" + str(cnt) + "  -  " + dt_now.strftime("%m/%d %H:%M:%S"))
        print(df)
        cnt += 1
        continue
    if cnt == DURATION:
        print("========== 取引開始 ==========")
        send_message_to_line("取引開始")

    # 計算ロジック
    df = bb.calc_bollinger_band(df)
    df = rsi.calc_rsi(df)
    # df = macd.calc_macd(df)

    # 判定ロジック
    flag = bb.check_bollinger_band(df, flag)
    flag = rsi.check_rsi(df, flag)
    # flag = macd.check_macd(df, flag)

    # 売買
    # 売り（SELL）
    if "btc" in position.keys():
        if check(flag, order_type="sell") and coincheck.ask_rate < df["price"].iloc[-1]:
        # if check(flag, order_type="sell"):
            params = {
                "pair": "btc_jpy",
                "order_type": "market_sell",
                "amount": position["btc"]
            }
            r = coincheck.order(params)

            print("########## SELL ##########")
            send_message_to_line(r)
            send_message_to_line("レート：" + str(coincheck.bid_rate))
    # 買い
    else:
        if check(flag, order_type="buy"):
            params = {
                "pair": "btc_jpy",
                "order_type": "buy",
                "amount": AMOUNT
            }
            market_buy_amount = coincheck.rate(params)

            params = {
                "pair": "btc_jpy",
                "order_type": "market_buy",
                "market_buy_amount": market_buy_amount["price"]
            }
            r = coincheck.order(params)

            print("########## BUY ##########")
            send_message_to_line(r)
            send_message_to_line("レート：" + str(coincheck.ask_rate))

    # LOG出力
    dt_now = datetime.datetime.now()
    print("Loop:" + str(cnt) + "  -  " + dt_now.strftime("%m/%d %H:%M:%S"))
    print(df.iloc[-2:])
    cnt += 1

    # 先頭行の削除
    df = df.drop(df.index[0])
