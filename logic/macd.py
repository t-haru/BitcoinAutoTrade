import pandas as pd

# MACD
class MACD(object):
    def __init__(self, short_duration=9, long_duration=26, signal_duration=9):
        self.short_duration = short_duration
        self.long_duration = long_duration
        self.signal_duration = signal_duration

    # MACDの計算
    def calc_macd(self, df: pd.DataFrame):
        df["short_SMA"] = df["price"].rolling(window=self.short_duration).mean()
        df["long_SMA"] = df["price"].rolling(window=self.long_duration).mean()

        df["short_EMA"] = df["short_SMA"]*(1-1/(self.short_duration+1))+df["price"]/(self.short_duration+1)
        df["long_EMA"] = df["long_SMA"]*(1-1/(self.long_duration+1))+df["price"]/(self.long_duration+1)
        
        df["MACD"] = df["short_EMA"] - df["long_EMA"]
        df["signal"] = df["MACD"].rolling(window=self.signal_duration).mean()
        
        df["MACD-signal"] = df["MACD"] - df["signal"]

        return df

    # MACDのチェック
    def check_macd(self, df: pd.DataFrame, flag):
        if df.iloc[-2]["MACD-signal"] < 0 and df.iloc[-1]["MACD-signal"] > 0:
            flag["buy"]["MACD"] = True
        else:
            flag["buy"]["MACD"] = False

        if df.iloc[-2]["MACD-signal"] > 0 and df.iloc[-1]["MACD-signal"] < 0:
            flag["sell"]["MACD"] = True
        else:
            flag["sell"]["MACD"] = False
        
        return flag