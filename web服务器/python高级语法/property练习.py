
# 定义一个test类，初始化name 私有属性,通过property去访问修改和删除name属性。


class Test:
    def __init__(self):
        self.__name = None

    @property
    def name(self):
        # 这个就是get方法
        return self.__name

    @name.setter
    def name(self,name_str):
        if isinstance(name_str,str):
            self.__name = name_str
        else:
            print("the name is not a string")

    @name.deleter
    def name(self):
        del self.__name
        print("delete name ")


obj = Test()

print(obj.name)
obj.name = "xiaoming"
print(obj.name)
del obj.name
obj.name = "xiaozhang"
print(obj.name)






