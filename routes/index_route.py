from flask import Blueprint
from ..controllers import index_controller
from flask_login import login_required

router = Blueprint('index', __name__)

@router.route('/', methods=['GET', 'POST'])
def index():
    return index_controller()
