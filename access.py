from flask import session, render_template, current_app, request, redirect, url_for
from functools import wraps


def login_required(func):
    # позволяет определять задекорированную функцию как исходную(передана как аргумент), вместо декорирующей wrapper()
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect(url_for('bp_auth.start_auth'))
    return wrapper


# проверка на доступ к позициям меню для внутренних
def group_validation(config: dict) -> bool:
    endpoint_func = request.endpoint
    endpoint_app = request.endpoint.split('.')[0]
    if 'user_group' in session:
        user_group = session['user_group']
        if user_group in config and endpoint_app in config[user_group]:
            return True
        if user_group in config and endpoint_func in config[user_group]:
            return True
    return False


# декоратор для доступа внутренних пользователей к функционалу
def group_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if group_validation(config):
            return f(*args, **kwargs)
        return render_template('menu/exceptions/internal_user.html')
    return wrapper


# проверка на доступ к позициям меню для внешних
def external_validation(config):
    endpoint_app = request.endpoint.split('.')[0]
    user_id = session.get('user_id')
    user_group = session.get('user_group')
    if user_id and user_group is None:
        if endpoint_app in config['external']:
            return True
    return False


# декоратор для доступа внешних пользователей к функционалу
def external_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if external_validation(config):
            return f(*args, **kwargs)
        return render_template('menu/exceptions/external_user.html')
    return wrapper
