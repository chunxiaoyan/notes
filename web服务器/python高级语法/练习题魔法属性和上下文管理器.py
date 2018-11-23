# 【代码题】
# 定义一个类字典对象(继承于dict类)，创建一个类字典对象，键“a”的值为1，键“b”的值为2.当访问键"a"的值得时候，屏幕打印100，注意这里不是修改字典。修改键“b”的值得时候，屏幕打印键“b”和修改后的值，最后打印修改之后的字典。
# 【代码题】
# 计算函数运行的时间，使用上下文管理器实现。
# def func(number):
# 	li = [1,2,4]
# 	if number < 4:
# 		return li[number-1]
# 	else:
# 		if number > 3:
# 			return func(number-1)+func(number-2)+func(number-3)


class Test1(dict):
    def __getitem__(self, item):
        print("get")

    def __setitem__(self, key, value):
        print("set")
        if key == "a":
            print(100)

    def __delitem__(self, key):
        print("del")

d = Test1()

d["a"]=1
d["b"]=2