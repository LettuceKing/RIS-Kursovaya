from flask import Blueprint, render_template, request, current_app, redirect
from db_work import call_proc
from access import login_required, group_required

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates_report')

report_list = [
    {'rep_name': 'Отчет о месячной выручке', 'rep_id': '1'},
    {'rep_name': 'Отчет о продажах', 'rep_id': '2'}
]  # todo в JSON

report_url = {
    '1': {'create_rep': 'bp_report.create_rep1', 'view_rep': 'bp_report.view_rep1'},
    '2': {'create_rep': 'bp_report.create_rep2', 'view_rep': 'bp_report.view_rep2'}
}  # todo в JSON


@blueprint_report.route('/', methods=['GET', 'POST'])
@login_required
@group_required
def start_report():
    if request.method == 'GET':
        return render_template('menu_report.html', report_list=report_list)
    else:
        rep_id = request.form.get('rep_id')
        print('rep_id = ', rep_id)
        if request.form.get('create_rep'):
            url_rep = report_url[rep_id]['create_rep']
        else:
            url_rep = report_url[rep_id]['view_rep']
        print('url_rep = ', url_rep)
        return redirect(url_for(url_rep))


@blueprint_report.route('/create_rep1')
@login_required
@group_required
def create_rep1():
    rep_month = 9
    rep_year = 2022  # todo ввод из формы
    res = call_proc(current_app.config['db_config'], 'product_report', rep_month, rep_year)
    print('res = ', res)
    return render_template('report_created.html')  # todo html


@blueprint_report.route('/view_rep1')
@login_required
@group_required
def view_rep1():
    return 'I am view report 1'
