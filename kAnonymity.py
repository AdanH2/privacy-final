from flask import render_template
from flask.views import MethodView

class kAnonymity(MethodView):
    def get(self):
        return render_template('kAnonymity.html')