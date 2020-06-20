import time

from flask import Flask, jsonify, g, request, Response

app = Flask(__name__)


@app.before_request
def before_request():
    g.start_time = time.time()


@app.after_request
def after_request(response):
    if ('Content-Length' in response.headers):
        response.headers.add('LAB-Uncompressed-Content-Length', response.headers['Content-Length'])
    start_to_stop_time = time.time() - g.start_time
    response.headers.add('LAB-Response-Time', start_to_stop_time)


@app.route('/api/ip')
def get_my_ip():
    return jsonify({
        'IP': request.remote_addr,
        'X-Client-IP': request.headers.get('X-Client-IP', None),
        'X-Remote-IP': request.headers.get('X-Remote-IP', None),
        'X-Remote-Addr': request.headers.get('X-Remote-Addr', None),
        'X-Originating-IP': request.headers.get('X-Originating-IP', None),
        'X-Forwarded-For': request.headers.get('X-Forwarded-For', None),
    })


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return Response("<h1>Flask</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")
