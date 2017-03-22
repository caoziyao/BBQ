# coding: utf-8

import socket
import _thread
from util import log
from models.request import Request
from route.todo import route_todo

port = 8081
host = ''  # '' 代表接收任意 ip


class Server():
    """
    服务端
    """

    def __init__(self, host='', port=5000):
        try:
            addr = (host, port)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(addr)
            self.socket.listen(5)
        except Exception as e:
            log('error', e)
            self.socket.close()

    def accept(self):
        return self.socket.accept()

    def close(self):
        self.socket.close()


def response_for_path(path, request):
    """根据 path 回应客户端"""
    r = {}
    r.update(route_todo)
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    response = r.get(path, 404)
    return response(request)


def parsed_headers(headers):
    """ 解析 headers """
    query = {}
    for h in headers:
        k, v = h.split(': ', 1)
        query[k] = v
    return query


def parsed_request(r):
    """第一步解析整个请求
    返回 method header body
    """
    request = Request()
    request.method = r.split()[0]
    request.url = r.split()[1]
    request.protocol = r.split()[2]
    headers = r.split('\r\n\r\n', 1)[0].split('\r\n')[1:]
    request.body = r.split('\r\n\r\n', 1)[1]
    request.headers = parsed_headers(headers)

    return request


def process_request(connection):
    """ 接收处理数据线程"""
    r = connection.recv(1024)
    r = r.decode('utf-8')
    # 因为 chrome 会发送空请求导致 split 得到空 list
    # 所以这里判断一下防止程序崩溃
    if len(r.split()) < 2:
        connection.close()
        return

    request = parsed_request(r)
    response = response_for_path(request.url, request)
    connection.sendall(response.encode('utf-8'))

    connection.close()


def run(host='', port=3000, debug=False):
    """
    启动服务器
    """
    s = Server(host, port)
    while True:
        # 接收一个连接
        connection, addr = s.accept()
        # 开一个新的线程来处理请求, 第二个参数是传给新函数的参数列表, 必须是 tuple
        # tuple 如果只有一个值 必须带逗号
        _thread.start_new_thread(process_request, (connection,))


if __name__ == '__main__':
    config = dict(
        host='',
        port=3000,
        debug=True,
    )
    run(**config)

"""
GET / HTTP/1.1
Host: 127.0.0.1:8080
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding: gzip, deflate, sdch, br
Accept-Language: zh-CN,zh;q=0.8

"""
