## USER API ##############################################################################################

from flask import Blueprint, jsonify
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from models import User, Device

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.before_request
def user_before():
    if not current_user.is_authenticated:
        return "Unauthorized", 401


@user_bp.route('/api/user', methods=['get'])
def users_get():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@user_bp.route('/api/user/<id>')
def user_get(id):
    u = User.query.filter_by(id=id).first_or_404()
    return jsonify(u.to_dict())


@user_bp.route('/api/user/<id>', methods=['delete'])
def user_delete(id=-1):
    u = User.query.filter_by(id=id).first_or_404()
    db.session.delete(u)
    db.session.commit()
    return jsonify(u.to_dict())
