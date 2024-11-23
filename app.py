from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return ''' Our first python app run by docker'''

@app.route('/health')
def health():
    return 'Server is up and running'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7999)
