from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .routes import index_router, dashboards_router, login_router
from .models.models import ModelUser
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
login_manager = LoginManager()
bootstrap = Bootstrap()
login_manager.login_view='auth.login'

def create_app():
    """Function to initialize Flask functions
    Also, the configuration can be changed with the method from_object
    Returns the created application instance
    """
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.register_blueprint(index_router)
    app.register_blueprint(dashboards_router, url_prefix='/dashboards')
    app.register_blueprint(login_router)

    bootstrap.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
 
    @login_manager.user_loader
    def load_user(id):
        return ModelUser.get_by_id(id)

    return app
