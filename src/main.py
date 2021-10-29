from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello EEE3095S! <br/> This is our webserver <br/> Done by: LXXHSI007 and VBNREE001'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
