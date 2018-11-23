
import time


G_DICT_PATH = {}


def route(url):
    def set_func(func):
        G_DICT_PATH[url] = func

        def call_func(*args,**kwargs):
            func(*args, **kwargs)
        return call_func
    return set_func


@route("/index.html")
def index():
    with open("./templates/index.html") as f:
        content = f.read()
        content = content.replace("这里添加时间", time.asctime(time.localtime(time.time())))
        return content


def application(env, set_headers):
    file_name = env["PATH"]
    print(G_DICT_PATH)
    try:
        if file_name not in G_DICT_PATH:
            # 如果这个请求的html文件不存在 就返回404
            set_headers("404 not found", [("Content-type", "text/html;charset=utf8")])
            return "404 not found"
        else:
            # 如果存在 返回相应的func()
            set_headers("200 OK", [("Content-type", "text/html;charset=utf8")])
            func = G_DICT_PATH[file_name]
            print(func)
        return func()

    except Exception as ret:
        return "出现异常 %s" % str(ret)
