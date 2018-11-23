
import socket
import re


def service_client(new_socket, request):
    """为这个客户端返回数据 """
    # 1 接受浏览器发送过来的请求，即http
    # GET / HTTP/1.1
    # request = new_socket.recv(1024)
    # print(request)
    request_lines = request.splitlines()
    print(request_lines)
    print(request_lines[0])
    # 2. 返回http格式的数据 给浏览
    # 准备数据 header

    try:
        file_name = re.match("[^/]+(/[^ ]*)", request_lines[0]).group(1)
        print("file_name %s " % file_name)
        if file_name == "/":
            file_name = "index.html"
    except:
        print("exeception")

    # 准备数据 body
    # response += "<h1>hahhahhahhaha</h1>"
    try:

        f = open(file_name, "rb")

    except:
        response_header = "HTTP/1.1 404 not found \r\n"
        response_header += "\r\n"
        response_body = "----sorry, file not found----".encode("utf-8")

    else:

        response_body = f.read()
        response_header = "HTTP/1.1 200 Ok\r\n"
        response_header += "Content-Length:%d\r\n" % len(response_body)  # 告诉服务器内容有多长，收完所有的再关闭套接字
        response_header += "\r\n"
        f.close()
    finally:
        new_socket.send(response_header.encode("utf-8") + response_body)
        # 关闭套接字



def main():
    """用来完成整体控制 """
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    tcp_server_socket.bind(("", 7890))

    tcp_server_socket.listen(128)

    tcp_server_socket.setblocking(False)  # 解阻塞

    client_socket_list = list()
    while True:
        try:
            # 收到客户端链接
            new_socket, client_addr = tcp_server_socket.accept()
        except Exception as ret:
            pass
        else:
            new_socket.setblocking(False) # 客户端解阻塞
            client_socket_list.append(new_socket)

        for client_socket in client_socket_list:
            try:
                recv_data = client_socket.recv(1024).decode("utf-8")
                # 等待数据
            except Exception as ret:
                # 如果没有服务器的反应
                pass

            else:
                # 如果有反应。那么看数据是不是空，是空说明客户端关闭了套接字
                # 如果不是空则为这个客户端服务
                if recv_data:
                    # 如果收到数据
                    service_client(client_socket, recv_data)
                else:
                    client_socket.close()
                    client_socket_list.remove(client_socket)


    tcp_server_socket.close()


if __name__ == "__main__":
    main()