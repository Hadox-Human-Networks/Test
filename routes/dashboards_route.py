from flask import Blueprint
from ..controllers import analytics_controller, data_controller, ml_controller
from flask_login import login_required

router = Blueprint('dashboards', __name__)


@router.route('/analytics/<category>')
@login_required
def analytics(category):
    return analytics_controller(category)

@router.route('/data/<category>')
@login_required
def data(category):
    return data_controller(category)

@router.route('/ml/<category>')
@login_required
def ml(category):
    return ml_controller(category)
