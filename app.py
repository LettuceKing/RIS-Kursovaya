from flask import Flask, render_template, json, session
from blueprint_query.route import blueprint_query
from blueprint_auth.route import blueprint_auth
from blueprint_market.route import blueprint_market
from blueprint_report.route import blueprint_report
from access import login_required

app = Flask(__name__)
app.secret_key = '1fdcb2db5cef073da8672be0a0c151af6f01bb1b'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_market, url_prefix='/market')
app.register_blueprint(blueprint_report, url_prefix='/report')

with open('configs/db_config.json', 'r') as file:
    db_config = json.load(file)
app.config['dbconfig'] = db_config

with open('configs/access_config.json', 'r') as file:
    access_config = json.load(file)
app.config['access_config'] = access_config


@app.route('/')
def start_func():
    if 'user_id' in session:
        return render_template('start_page_auth.html')
    else:
        return render_template('start_page_no_auth.html')


@app.route('/menu')
@login_required
def menu_choice():
    group = session.get('user_group')
    if group == 'admin':
        return render_template('menu/internal_user_admin.html')
    elif group == 'marketer':
        return render_template('menu/internal_user_marketer.html')
    return render_template('menu/external_user.html')


@app.route('/exit')
def exit_func():
    session.clear()
    return render_template('exit_request.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
