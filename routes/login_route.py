from flask import Blueprint
from flask_login import login_required
from ..controllers import login_controller, logout_controller


router = Blueprint('auth', __name__)

@router.route('/login', methods=['GET', 'POST'])
def login():
    return login_controller()

@router.route('/logout')
@login_required
def logout():
    return logout_controller()


