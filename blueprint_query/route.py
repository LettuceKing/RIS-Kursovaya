from flask import Blueprint, request, render_template, current_app
from db_work import select
from sql_provider import SQLProvider
from access import login_required, group_required
import os


blueprint_query = Blueprint('bp_query', __name__, template_folder='templates_query')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/', methods=['GET', 'POST'])
@login_required
@group_required
def query():
    if request.method == 'GET':
        return render_template('product_form.html')
    else:
        product = request.form.get('blank_id')
        if product:
            _sql = provider.get('blank.sql', blank_id=product)
            result, schema = select(current_app.config['dbconfig'], _sql)
            if result:
                return render_template('result_set.html', schema=schema, result=result)
            else:
                return render_template('product_form.html', error='Результаты не найдены')
        else:
            return render_template('product_form.html', error='Повторите ввод')
