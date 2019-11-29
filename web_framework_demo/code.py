from wsgiref.simple_server import make_server, demo_app
# from Application.application import sample_app as app
from Application.application import my_app


"""
if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 8086, app)
    sa = httpd.socket.getsockname()
    print('http://{0}:{1}'.format(sa[0], sa[1]))

    # Respond to requests until process is killed
    httpd.serve_forever()
"""



urls = (
    ("/", "index"),
    ("/hello/(.*)", "hello"),
)

wsgiapp = my_app(urls, globals())

class index:
    def GEt(self):
        my_app.header('Content-type', 'text/plain')
        return b"Welcome! "

class hello:
    def GET(self, name):
        my_app.header('Content-type', 'text/plain')
        return "Hello {0}!".format(name).encode()


if __name__ == '__main__':
    httpd = make_server('', 8086, wsgiapp)

    sa = httpd.socket.getsockname()
    print("http://{0}:{1}/".format(*sa))
    
    # Respond to requests until process is killed
    httpd.serve_forever()


