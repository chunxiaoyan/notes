import socket
import re
import sys
import gevent
from gevent import monkey
monkey.patch_all()


class WSGI_Server():
    def __init__(self, port, app):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("", port))
        self.server_socket.listen(128)
        self.application = app

    def run(self):
        while True:
            new_client_socket, addr = self.server_socket.accept()
            # self.server_client(new_client_socket)
            gevent.spawn(self.server_client, new_client_socket)

    def server_client(self, new_client_socket):

        request = new_client_socket.recv(1024)
        request = request.decode("utf-8")
        # 若没有返回，就关闭这次服务
        print(request)
        if not request:
            new_client_socket.close()
            return

        # 分成行
        request_lines= request.splitlines()
        print(request_lines)

        # 获取请求的路径 如果是/ 就改为index.html
        ret = re.match(r"([^/]*)([^ ]+)", request_lines[0])

        if ret:
            print("正则提取数据 %s" % ret.group(1))
            print("正则提取数据 %s" % ret.group(2))
            if ret.group(2) == "/":
                file_name = "/index.html"
            else:
                file_name = ret.group(2)

        # 如果请求的不是 html结尾
        if not file_name.endswith(".html"):
            # print("404 not found")
            response_body = "404 not found"
            response_header = "HTTP/1.1 404 not found\r\n"
            response_header += "Content-Type: text/html; charset=utf-8\r\n"
            response_header += "Content-Length: %d\r\n" % (len(response_body))
            new_client_socket.send((response_header+response_body).encode("utf-8"))
            new_client_socket.close()

        # 如果不是
        else:
            env = dict()
            env["PATH"] = file_name
            response_body = self.application(env, self.set_response_headers)

            response_header = "HTTP/1.1 %s\r\n" % self.status

            for temp in self.headers:
                response_header += "%s:%s\r\n" % (temp[0], temp[1])

            response_header += "\r\n"

            new_client_socket.send((response_header+response_body).encode("utf-8"))
            new_client_socket.close()

    def set_response_headers(self, status, headers):
        self.status = status
        self.headers = [("server", "mini_web")]
        self.headers += headers


G_DYNAMIC_ROOT_PATH = "./dynamic"


def main():
    # 1. 获取配置文件里的端口 和 web 框架 sys.argv
    # python3 web_server.py 7890  mini_frame:application
    if not len(sys.argv) == 3:
        print("输入的参数不是3个 请按照一下方式运行：python3 web_server.py 7890 mini_frame:application")
        return
    else:
        try:
            port = int(sys.argv[1])
            print(port)

            frame_app_name = sys.argv[2]
            print(frame_app_name)
        except Exception as  ret:
            print("输入端口错误")
            return
        ret = re.match(r"([^:]+):(.*)", frame_app_name)

        try:
            frame_name = ret.group(1)
            app_name = ret.group(2)
        except Exception as ret:
            print(ret)
            print("正则，请按照以下方式运行：python3 web_server.py 7890 mini_frame:application")
            return ret

        # 2. 打开配置文件 获取文件路径
        config_dict = eval(open("web_server.conf").read())

        # 3. 加入 dyanmic 路径， application 模块导入  __import__ , getattr()

        sys.path.append(config_dict['dynamic_path'])

        frame = __import__(frame_name)
        app = getattr(frame, app_name)

        # 4. 启动服务器
        session_server = WSGI_Server(port, app)
        session_server.run()


if __name__ == '__main__':
    main()
