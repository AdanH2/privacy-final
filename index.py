from flask import render_template, session
from flask.views import MethodView

class Index(MethodView):
    def get(self):
        if 'dev' not in session:
            session['dev'] = False
        return render_template('index.html')