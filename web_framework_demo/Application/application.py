import re
# import json


# Use sample_app to instead demo_app
"""
def sample_app(environ, start_response):
    # Simplest possible application object
    status = '200 OK'
    response_headers = [('Content-type', 'text/json')]
    start_response(status, response_headers)

    people = json.dumps({'name': 'aa', 'age': '16', 'job': 'teacher'})

    # python 2.x the result is string, but in python 3.x it must be bytes
    return [people.encode()]
"""

# Use class instead function
"""
class my_app:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        status = '200 OK'
        response_headers = [('Context-type', 'text/plain')]
        self.start_response(status, response_headers)
        yield b"Hello World! "
"""

# match URL
"""
class my_app:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        path = self.environ['PATH_INFO']

        if path == "/":
            return self.GET_index()
        elif path == "/hello":
            return self.GET_hello()
        else:
            return self.notfound()

    def GET_index(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield b"Welcome! "

    def GET_hello(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield b"Hello World! "

    def notfound(self):
        status = '404 Not Found'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield b"Not Found"
"""

# Use regex match URL
"""
class my_app:

    urls = (
        ("/", "index"),
        ("/hello/(.*)", "hello"),
    )

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']

        for pattern, name in self.urls:
            m = re.match("^" + pattern + "$", path)

            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()
                funcname = method.upper() + '_' + name
                
                if hasattr(self, funcname):
                    func = getattr(self, funcname)
                    return func(*args)
        return self.notfound()

    def GET_index(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield b"Welcome! "
    
    def GET_hello(self, name):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Hello {0}".format(name).encode()

    def notfound(self):
        status = '404 Not Found'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield b"Not Found"
""" 

# Distinct GET_* repeat code
"""
class my_app:

    urls = (
        ("/", "index"),
        ("/hello/(.*)", "hello"),
    )

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        self.status = '200 OK'
        self._headers = []

    def __iter__(self):
        result = self.delegate()
        self.start(self.status, self._headers)

        # Convert result(string or string list) to iterator object
        if isinstance(result, str):
            return iter([result])
        else:
            return iter(result)

    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']

        for pattern, name in self.urls:
            m = re.match("^" + pattern + "$", path)

            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()
                funcname = method.upper() + '_' + name
                if hasattr(self, funcname):
                    func = getattr(self, funcname)
                    return func(*args)

        return self.notfound()

    def header(self, name, value):
        self._headers.append((name, value))

    def GET_index(self):
        self.header('Content-type', 'text/plain')
        return "Welcome! ".encode()

    def GET_hello(self, name):
        self.header('Content-type', 'text/plain')
        return "Hello World! ".encode()

    def notfound(self):
        self.status = '404 Not Found'
        self.header('Content-type', 'text/plain')
        return "Not Found".encode()
"""

# release
class my_app:

    headers = []

    def __init__(self, urls = (), fvars = {}):
        self._urls = urls
        self._fvars = fvars

    def __call__(self, environ, start_response):
        self._status = '200 OK'         # default status OK
        del self.headers[:]             # clear prev headers

        result = self._delegate(environ)
        start_response(self._status, self.headers)

        # Convert result(string or string list) to iterator object
        if isinstance(result, str):
            return iter([result])
        else:
            return iter(result)

    def _delegate(self, environ):
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']

        for pattern, name in self._urls:
            m = re.match("^" + pattern + "$", path)

            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()
                funcname = method.upper()
                klass = self._fvars.get(name)
                if hasattr(klass, funcname):
                    func = getattr(klass, funcname)
                    return func(klass(), *args)

        return self._notfound()

    def _notfound(self):
        self._status = '404 Not Found'
        self.header('Content-type', 'text/plain')
        return b"Not Found"

    @classmethod
    def header(cls, name, value):
        cls.headers.append((name, value))