def print_received(msg, addr):
    if isinstance(msg, str):
        print("  <- {} from {}".format(msg, addr))
    elif isinstance(msg, list):
        print("  <- {} from {}".format(str(msg), addr))
    else:
        try:
            print("  <- {} from {}".format(msg.decode("utf-8"), addr))
        except UnicodeDecodeError:
            print(" <- {} from {}".format(msg, addr))


def print_sent(msg, addr):
    if isinstance(msg, str):
        print("  -> {} to {}".format(msg, addr))
    else:
        try:
            print("  -> {} to {}".format(msg.decode("utf-8"), addr))
        except UnicodeDecodeError:
            print("  -> {} to {}".format(msg, addr))


def log(msg):
    print("-", msg)
