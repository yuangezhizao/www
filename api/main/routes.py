from flask import Response, jsonify

from . import app


@app.before_request
def before_request():
    g.start_time = time.time()
    if 'profile' in request.args:
        g.profiler = Profiler()
        g.profiler.start()


@app.after_request
def after_request(response):
    if ('Content-Length' in response.headers):
        response.headers.add('LAB-Uncompressed-Content-Length', response.headers['Content-Length'])
    start_to_stop_time = time.time() - g.start_time
    response.headers.add('LAB-Response-Time', start_to_stop_time)
    if not hasattr(g, 'profile'):
        return response
    g.profiler.stop()
    output_html = g.profiler.output_html()
    return make_response(output_html)


@app.route('/')
def index():
    return 'index'


@app.route('/ip')
def get_my_ip():
    return jsonify({
        'IP': request.remote_addr,
        'X-Client-IP': request.headers.get('X-Client-IP', None),
        'X-Remote-IP': request.headers.get('X-Remote-IP', None),
        'X-Remote-Addr': request.headers.get('X-Remote-Addr', None),
        'X-Originating-IP': request.headers.get('X-Originating-IP', None),
        'X-Forwarded-For': request.headers.get('X-Forwarded-For', None),
    })
