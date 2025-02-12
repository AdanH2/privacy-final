from flask import render_template
from flask.views import MethodView

class masking(MethodView):
    def get(self):
        return render_template('masking.html')