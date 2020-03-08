import socket

from flask import Flask, request, send_from_directory, render_template

from utils import search_titles, data

app = Flask(__name__)
app.data = data


@app.route('/search')
def search():
    query = request.args.get('query')
    result = search_titles(query)
    return render_template('index.html', result=result, data='')


@app.route('/get/<id>')
def get(id):
    print(id)
    data = app.data.get(id)
    return render_template('index.html', result=[], data=data)


@app.route('/')
def main():
    return send_from_directory('static', 'index.html')


@app.route('/check')
def check():
    return f'host: {socket.gethostname()} \nip: {socket.gethostbyname(socket.gethostname())}'


@app.route('/get/<path:path>')
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
