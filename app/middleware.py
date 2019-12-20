from . import app
from flask import g, request
import datetime
import time
from rfc3339 import rfc3339


@app.before_request
def startLog():
    g.start = time.time()

@app.after_request
def logRequest(response):
    if request.path == '/favicon.ico':
        return response
    if request.path == '/batch':
        return response

    now = time.time()
    duration = round(now - g.start, 2)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = rfc3339(dt, utc=True)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log = {
        'method': request.method,
        'path': request.path,
        'status': response.status_code,
        'duration': duration,
        'time': timestamp,
        'ip': ip,
        'host': host,
        'params': args
    }

    app.logger.info(log)

    return response

