def check(flag, order_type):
    f = flag[order_type]
    # signal = f["BB"]
    # signal = f["BB"] and f["MACD"]
    signal = f["BB"] and f["RSI"]
    
    return signal
