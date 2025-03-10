from flask import Flask, request, url_for, render_template, redirect, session, jsonify
from index import Index
from kAnonymity import kAnonymity
from dp import DP
from pseudonymization import pseudonymization
from flask_session import Session
import ast
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
# Configure server-side session storage
app.config['SESSION_TYPE'] = 'filesystem'  # You can also use 'redis', 'memcached', etc.
app.config['SESSION_FILE_DIR'] = './flask_session/'  # Directory to store session files
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
# Initialize the session
Session(app)


app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=['GET'])

app.add_url_rule('/kAnonymity',
                 view_func=kAnonymity.as_view('kAnonymity'),
                 methods=['GET', 'POST'])

app.add_url_rule('/dp',
                 view_func=DP.as_view('dp'),
                 methods=['GET', 'POST'])

app.add_url_rule('/pseudonymization',
                 view_func=pseudonymization.as_view('pseudonymization'),
                 methods=['GET'])

@app.route('/toggle_dev_mode', methods=['POST'])
def toggle_dev_mode():
    # print('toggle_dev_mode')
    # print(request.json)
    session['dev'] = request.json.get('dev')
    return jsonify(success=True)

@app.route('/calc', methods=['GET'])
def get():
    return render_template('dp.html')

@app.route('/calc', methods=['POST'])
def calc():
    method = request.form.get('method')
    column = request.form.get('column')
    epsilon = float(request.form.get('epsilon'))
    lower_bound = request.form.get('lower')
    upper_bound = request.form.get('upper')
    if request.form.get('data1'):
        data = request.form.get('data1')
        data = ast.literal_eval(data)

        if method == 'sum':
            non_private_sum = DP().sum_data(data, column)
            if lower_bound == '' or upper_bound == '':
                private_sum = DP().sum_dp(data, column, epsilon=epsilon)
            else:
                private_sum = DP().sum_dp(data, column, epsilon=epsilon, lower_bound=float(lower_bound), upper_bound=float(upper_bound))

            non_private_sum = f"{non_private_sum:,}"
            private_sum = round(private_sum, 2)
            private_sum = f"{private_sum:,}"
            return render_template('dp.html', method=method, column=column, realSum=non_private_sum, privateSum=private_sum, data1=data)
        elif method == 'mean':
            non_private_mean = DP().mean(data, column)
            if lower_bound == '' or upper_bound == '':
                private_mean = DP().mean_dp(data, column, epsilon=epsilon)
            else:
                private_mean = DP().mean_dp(data, column, epsilon=epsilon, lower_bound=float(lower_bound), upper_bound=float(upper_bound))

            non_private_mean = round(non_private_mean, 2)
            non_private_mean = f"{non_private_mean:,}"
            private_mean = round(private_mean, 2)
            private_mean = f"{private_mean:,}"
            return render_template('dp.html', method=method, column=column, realMean=non_private_mean, privateMean=private_mean, data1=data)
        elif method == 'count':
            non_private_count = DP().count(data)
            private_count = DP().count_dp(data, column, epsilon=epsilon)

            non_private_count = f"{non_private_count:,}"
            private_count = f"{private_count:,}"
            return render_template('dp.html', method=method, column=column, realCount=non_private_count, privateCount=private_count, data1=data)
    elif request.form.get('data2'):
        data = request.form.get('data2')
        data = ast.literal_eval(data)

        if method == 'sum':
            non_private_sum = DP().sum_data(data, column)
            if lower_bound == '' or upper_bound == '':
                private_sum = DP().sum_dp(data, column, epsilon=epsilon)
            else:
                private_sum = DP().sum_dp(data, column, epsilon=epsilon, lower_bound=float(lower_bound), upper_bound=float(upper_bound))

            non_private_sum = f"{non_private_sum:,}"
            private_sum = round(private_sum, 2)
            private_sum = f"{private_sum:,}"
            return render_template('dp.html', method=method, column=column, realSum=non_private_sum, privateSum=private_sum, data2=data)
        elif method == 'mean':
            non_private_mean = DP().mean(data, column)
            if lower_bound == '' or upper_bound == '':
                private_mean = DP().mean_dp(data, column, epsilon=epsilon)
            else:
                private_mean = DP().mean_dp(data, column, epsilon=epsilon, lower_bound=float(lower_bound), upper_bound=float(upper_bound))

            non_private_mean = round(non_private_mean, 2)
            non_private_mean = f"{non_private_mean:,}"
            private_mean = round(private_mean, 2)
            private_mean = f"{private_mean:,}"
            return render_template('dp.html', method=method, column=column, realMean=non_private_mean, privateMean=private_mean, data2=data)
        elif method == 'count':
            non_private_count = DP().count(data)
            private_count = DP().count_dp(data, column, epsilon=epsilon)

            non_private_count = f"{non_private_count:,}"
            private_count = f"{private_count:,}"
            return render_template('dp.html', method=method, column=column, realCount=non_private_count, privateCount=private_count, data2=data)
    return render_template('dp.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear the session data
    return redirect(url_for('index'))  # Redirect to the landing page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)