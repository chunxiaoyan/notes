def set_func(func):
    print("-------开始进行装饰----------")

    def call_func(*args, **kwargs):
        print("验证-------------")
        print(*args)
        return func(*args, **kwargs)  #拆包
    return call_func


@set_func
def test1(num, *args, **kwargs):
    print("-------test1---------%d" % num)
    print("-------test1---------", *args)
    print("-------test1---------", **kwargs)
    return "ok"


ret = test1(100,200,3000)
print(ret)

