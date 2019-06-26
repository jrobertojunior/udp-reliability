def print_received(msg, addr):
    if isinstance(msg, str):
        print("  <- {} from {}".format(msg, addr))
    else:
        print("  <- {} from {}".format(msg.decode("utf-8"), addr))


def print_sent(msg, addr):
    if isinstance(msg, str):
        print("  -> {} to {}".format(msg, addr))
    else:
        print("  -> {} to {}".format(msg.decode("utf-8"), addr))


def log(msg):
    print("-", msg)
