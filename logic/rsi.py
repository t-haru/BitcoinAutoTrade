import pandas as pd

# RSI
class RSI(object):
    def __init__(self, duration=14):
        self.duration = duration
    
    # RSIの計算
    def calc_rsi(self, df):
        df["price_diff"] = df["price"].diff()

        df["up"] = df["price_diff"]
        df["down"] = df["price_diff"]
        df.loc[df["up"] <= 0, "up"] = 0
        df.loc[df["down"] > 0, "down"] = 0

        df["up_sum"] = df["up"].rolling(self.duration).sum().abs()
        df["down_sum"] = df["down"].rolling(self.duration).sum().abs()

        df["RSI"] = df["up_sum"] / (df["up_sum"] + df["down_sum"])

        return df
    
    # RSIのチェック
    def check_rsi(self, df, flag):
        if df["RSI"].iloc[-1] > 0.7:
            flag["sell"]["RSI"] = True
        else:
            flag["sell"]["RSI"] = False

        if df["RSI"].iloc[-1] < 0.3:
            flag["buy"]["RSI"] = True
        else:
            flag["buy"]["RSI"] = False
        
        return flag