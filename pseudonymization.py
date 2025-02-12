from flask import render_template
from flask.views import MethodView

class pseudonymization(MethodView):
    def get(self):
        return render_template('pseudonymization.html')