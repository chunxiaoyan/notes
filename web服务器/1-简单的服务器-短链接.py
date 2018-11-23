
import socket
import re
import gevent
from gevent import monkey
monkey.patch_all()


def service_client(new_socket):
    """为这个客户端返回数据 """
    # 1 接受浏览器发送过来的请求，即http
    # GET / HTTP/1.1
    request = new_socket.recv(1024)    
    #print(request)
    request_lines = request.splitlines()
    print(request_lines)
    print(request_lines[0])
    # 2. 返回http格式的数据 给浏览
    # 准备数据 header

    try:
        file_name = re.match("[^/]+(/[^ ]*)", request_lines[0].decode("utf-8")).group(1)
        print("file_name %s " % file_name)
        if file_name == "/":
            file_name = "index.html"
    except:
        print("exeception")

    # 准备数据 body
    # response += "<h1>hahhahhahhaha</h1>"
    try:

        f = open(file_name,"rb")

    except:
        response = "HTTP/1.1 404 not found \r\n"
        response += "\r\n"
        response_body = "----sorry, file not found----".encode("utf-8")

    else:
        response = "HTTP/1.1 200 Ok\r\n"
        response += "\r\n"
        response_body = f.read()
        f.close()
    finally:
        new_socket.send(response.encode("utf-8"))
        new_socket.send(response_body)
        # 关闭套接字
        new_socket.close()


def main():
    """用来完成整体控制 """
    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    tcp_server_socket.bind(("", 7890))

    tcp_server_socket.listen(128)

    while True:
        new_socket, client_addr = tcp_server_socket.accept()
    
        gevent.spawn(service_client, new_socket)

    tcp_server_socket.close()


if __name__ == "__main__":
    main()
