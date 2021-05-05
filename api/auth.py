## AUTHENTICATION #######################################################################################

from flask import Blueprint, render_template, redirect, request, url_for, flash, jsonify, current_app
from flask_login import login_required, login_user, logout_user, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import User, db
from functools import wraps
import json

endpoint = '/api/auth'

auth_bp = Blueprint('auth', __name__, template_folder='templates')

login_manager = LoginManager()
login_manager.session_protection = "strong"

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        u = User.query.filter_by(id = current_user.id).first()
        print("admin_required: u.name={} priv?={}".format(u.name, u.admin))
        if u.admin != None and not u.admin:
            return "Unauthorized", 404
        return f(*args, **kwargs)
    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route(endpoint, methods=['get'])
@login_required
def auth_get():
    return jsonify(current_user.to_dict())


@auth_bp.route(endpoint, methods=['post'])
def auth_post():
    try:
        data = json.loads(request.data.decode())

        remember = True if "remember" in data and data["remember"] else False
        user = User.query.filter_by(email = data["email"]).first()

        if not user or not check_password_hash(user.password, data["password"]):
            return "Login incorrect", 401
        else:
            login_user(user, remember=remember)
            return jsonify(user.to_dict())

    except Exception as e:
        print("auth_post(): Exception: {}".format(e))
        return "bad request {}".format(e), 400

@auth_bp.route(endpoint, methods=['delete'])
def auth_delete():
    logout_user()
    return jsonify({})


# @auth_bp.route('/signup', methods=['get'])
# def signup_get():
#     return render_template('signup.html')


# @auth_bp.route('/signup', methods=['post'])
# def signup_post():
#     email = request.form.get('email')
#     name = request.form.get('name')
#     password = request.form.get('password')
#     user = User.query.filter_by(email=email).first() # does the email already exist in database?
#     if user:
#         flash('That email address is already in use')
#         return redirect('/signup')
#     new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
#     db.session.add(new_user)
#     db.session.commit()

#     return redirect('/signup')


#@auth_bp.route('/login', methods=['get'])
#def login():
#    return render_template("login.html")


#@auth_bp.route('/login', methods=['post'])
#def login_post():
#    email = request.form.get('email')
#    password = request.form.get('password')
#    remember = True if request.form.get('remember') else False
#
#    user = User.query.filter_by(email=email).first()
#    if not user or not check_password_hash(user.password, password):
#        flash('Please check login credentials and try again')
#        return redirect(url_for('auth_bp.login'))
#
#    login_user(user, remember=remember)
#    return redirect('/')


#@auth_bp.route('/logout')
#@login_required
#def logout():
#    logout_user()
#    return redirect(url_for('main.index'))
