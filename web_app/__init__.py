from flask import Flask

from web_app.routes.mta_routes import mta_routes
  
def create_app(): 
    app = Flask(__name__)
    app.register_blueprint(mta_routes)
    return app