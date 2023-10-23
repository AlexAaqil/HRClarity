from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from hrms.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'user.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from hrms.main.routes import main
    from hrms.organization.routes import organization
    from hrms.employee.routes import employee
    from hrms.hrm.routes import admin
    from hrms.announcements.routes import announcements
    from hrms.leaves.routes import leaves
    from hrms.users.routes import user
    app.register_blueprint(main)
    app.register_blueprint(organization)
    app.register_blueprint(employee)
    app.register_blueprint(admin)
    app.register_blueprint(announcements)
    app.register_blueprint(leaves)
    app.register_blueprint(user)

    from hrms.models import User
    create_database(app)

    return app



def create_database(app):
    with app.app_context():
        db.create_all()
