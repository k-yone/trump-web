def app(environ, start_response):
    data = "hello\n"
    start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(data)))])
    return iter([data])
