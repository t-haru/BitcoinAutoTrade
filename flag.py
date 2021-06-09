def check(flag, order_type):
    # signal = flag[order_type]["BB"]
    # signal = flag[order_type]["BB"] and flag[order_type]["MACD"]

    signal = flag[order_type]["BB"] and flag[order_type]["RSI"]
    # signal = flag[order_type]["MACD"]

    return signal
