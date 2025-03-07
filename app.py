from flask import Flask, request, url_for, render_template
from index import Index
from kAnonymity import kAnonymity
from masking import masking
from pseudonymization import pseudonymization

app = Flask(__name__)

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=['GET'])

app.add_url_rule('/kAnonymity',
                 view_func=kAnonymity.as_view('kAnonymity'),
                 methods=['GET','POST'])

app.add_url_rule('/masking',
                 view_func=masking.as_view('masking'),
                 methods=['GET'])

app.add_url_rule('/pseudonymization',
                 view_func=pseudonymization.as_view('pseudonymization'),
                 methods=['GET'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)