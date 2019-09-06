# auth.py
#####################################
# from https://github.com/PrettyPrinted/flask_auth_scotch #
#####################################

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from ..models import User
from .. import db

auth = Blueprint('auth', __name__)

@auth.route('/log_admin', methods=['POST'])
def log_admin():
    password = request.form.get('password')
    #remember = True if request.form.get('remember') else False
    admin_user = User.query.first()
    if not admin_user : 
        flash('No admin user in database', 'warning')
        # app.logger.error('logging failed : No admin user in database')        
        return redirect(url_for('charts.now'))
    if not check_password_hash(admin_user.password, password): 
        flash('Wrong password', 'warning')
        # app.logger.info('logging failed : Wrong password')        
        return redirect(url_for('charts.now'))
        
    # if the above check passes, then we know the user has the right credentials
    #login_user(admin_user, remember=remember)
    login_user(admin_user)
    return redirect(url_for('admin.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('charts.now'))
