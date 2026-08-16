from flask import Flask

from web_app.routes.mta_routes import mta_routes
from web_app.routes.board_routes import board_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(mta_routes)
    app.register_blueprint(board_routes)
    return app