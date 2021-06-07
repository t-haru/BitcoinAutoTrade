def check(flag, order_type):
    f = flag[order_type]
    signal = f["BB"] and f["MACD"]
    
    return signal
