from combojsonapi.event import EventPlugin
from combojsonapi.permission import PermissionPlugin
from combojsonapi.spec import ApiSpecPlugin
from flask import Flask

from blog import commands
from blog.extensions import db, login_manager, migrate, csrf, admin, api
from blog.models import User


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['FLASK_DEBUG'] = 0
    app.config['FLASK_ENV'] = 'development'
    app.config['DATABASE_URL'] = 'sqlite:///blognew.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blognew.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '-u%644akr4bplr*b6397=yj6^4-76#_#=2qpmwlpkh#-0zb1i_'
    app.config['API_URL'] = 'http://0.0.0.0:10000'

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)
    admin.init_app(app)
    api.plugins = [
        EventPlugin(),
        PermissionPlugin(),
        ApiSpecPlugin(
            app=app,
            tags={
                'Tag': 'Tag API',
                'User': 'User API',
                'Author': 'Author API',
                'Article': 'Article API',
            }
        ),
    ]
    api.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    from blog.auth.views import auth
    from blog.user.views import user
    from blog.author.views import author
    from blog.articles.views import article
    from blog.api.views import api_blueprint
    from blog import admin

    app.register_blueprint(user)
    app.register_blueprint(auth)
    app.register_blueprint(author)
    app.register_blueprint(article)
    app.register_blueprint(api_blueprint)

    admin.register_views()


def register_commands(app: Flask):
    app.cli.add_command(commands.init_db)
    app.cli.add_command(commands.create_user)
    app.cli.add_command(commands.create_tags)
