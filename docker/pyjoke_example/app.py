import pyjokes
from flask import Flask

app = Flask(__name__)

@app.route('/')
def respose():
    r = str(pyjokes.get_jokes('es'))
    return r

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)