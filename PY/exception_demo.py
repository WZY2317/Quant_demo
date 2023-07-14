def demo1():
    a = 1
    b = a+1
    return b


def demo2():
    symbol_exchange_map = {
        "IF2020", "CFFEX",
        "rb2101", "SHFE"
    }

    exchange = symbol_exchange_map["rb2101"]
    return exchange


def add(a, b):
    return a+b


def test():
    i = 1
    for n in [1, 2, 3, True, "hhh"]:
        try:
            m = add(i, n)
            print(m)
        except TypeError:
            print("add error:data:", i)
        finally:
            print("run add end")


def mian():
    print("start run")
    test()
    print("end")
