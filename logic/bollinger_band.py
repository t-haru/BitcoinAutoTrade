# ボリンジャーバンド（BB）
class Bollinger_band(object):
    def __init__(self, duration=20):
        self.duration = duration

    # BBの計算
    def calc_bollinger_band(self, df):
        sigma = 2

        # 平均と標準偏差の計算
        df["SMA"] = df["price"].rolling(window=self.duration).mean()
        df["std"] = df["price"].rolling(window=self.duration).std()

        df["-2σ"] = df["SMA"] - sigma*df["std"]
        df["+2σ"] = df["SMA"] + sigma*df["std"]

        return df

    # BBのチェック
    def check_bollinger_band(self, df, flag):
        # 売り
        if df["price"].iloc[-1] > df["+2σ"].iloc[-1]:
            flag["sell"]["BB"] = True
        else:
            flag["sell"]["BB"] = False
        # 買い
        if df["price"].iloc[-1] < df["-2σ"].iloc[-1]:
            flag["buy"]["BB"] = True
        else:
            flag["buy"]["BB"] = False
        
        return flag