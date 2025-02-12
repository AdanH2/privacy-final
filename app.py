from flask import Flask, request, url_for, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kAnonymization')
def kAnonymity():
    return render_template('kAnonymity.html')

@app.route('/masking')
def masking():
    return render_template('masking.html')

@app.route('/pseudonymization')
def pseudonymization():
    return render_template('pseudonymization.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)