## USER API ##############################################################################################

from flask import Blueprint, jsonify, request
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import json
from api.models import User, Device, db
from api.auth import admin_required

endpoint='/api/user'

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.before_request
def user_before():
    if not current_user.is_authenticated:
        return "Unauthorized", 401


@user_bp.route(endpoint, methods=['get'])
def users_get():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@user_bp.route(endpoint+'/<id>', methods=['get'])
def user_get(id):
    u = User.query.filter_by(id=id).first_or_404()
    return jsonify(u.to_dict())


@user_bp.route(endpoint, methods=['post'])
@admin_required
def user_post():
    #Get request parameters
    print("user_post()")
    try:
        data = request.json
        u = User(
            email=data['email'],
            name=data['name'],
            password=generate_password_hash(data['password'], method='sha256')
        )
        print("new user created")
        db.session.add(u)
        db.session.commit()
        print(u)
        return jsonify(u.to_dict())
    except Exception as e:
        return "Error: {}".format(e), 400


@user_bp.route(endpoint+'/<id>', methods=['delete'])
@admin_required
def user_delete(id=-1):

    u = User.query.filter_by(id=id).first_or_404()
    db.session.delete(u)
    db.session.commit()
    return jsonify(u.to_dict())
