from flask import Blueprint, render_template, request, current_app
from sql_provider import SQLProvider
from access import login_required, external_required

blueprint_market = Blueprint('bp_market', __name__, template_folder='templates_market')


@blueprint_market.route('/')
@login_required
@external_required
def start_market():
    return render_template('basket_order_list.html')


@blueprint_market.route('/order')
def save_order():
    return 


@blueprint_market.route('/clear')
def clear_basket():
    return