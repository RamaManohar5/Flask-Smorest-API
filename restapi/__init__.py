# restapi/__init__.py
import logging
import os

# basic flask app
from flask import Flask, jsonify
# flask rest api
from flask_smorest import Api

# restapi blueprints
from restapi.resources.item import blp as ItemBluePrint
from restapi.resources.store import blp as StoreBluePrint
from restapi.resources.tag import blp as TagBluePrint
from restapi.resources.user import blp as UserBluePrint


# databases
from restapi.db import db
import restapi.models as models

# authentication
from flask_jwt_extended import JWTManager
import secrets

# block lists
from restapi.blocklists.blocklist import BLOCKLIST

# database migration
from flask_migrate import Migrate

# Configure logging
'''
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.FileHandler("restapi/logs/app.log"),
                              logging.StreamHandler()])
'''

def create_app(db_url=None):
    app = Flask(__name__)
    from restapi.main_views import sample_page
    app.register_blueprint(sample_page)
    #from restapi.stores.store_views import stores_page
    #app.register_blueprint(stores_page))
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URI","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    api = Api(app)
    # secret key generator # secrets.SystemRandom().getrandbits(128)
    app.config["JWT_SECRET_KEY"] = "140094610085460819041977930860792918628"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "description" : "the token has been revoked",
                "error" : "token revoked"
            }),
            401,
        )

 
    @jwt.additional_claims_loader
    def additional_claims_to_jwt(identity):
        # look in to the database and see whether the user is admin.
        if identity == 1:
            return {"is_admin" : True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_call_back(jwt_header, jwt_payload):
        return (
            jsonify({"message" :" the token has exipred.", "error" : "token expired"}), 
            401,
        )
    
    @jwt.invalid_token_loader
    def invalid_token_call_back(error):
        return (
            jsonify({"message" :" signature verification failed", "error" : "invalid token"}), 
            401,
        )
    
    @jwt.unauthorized_loader
    def missing_token_call_back(error):
        return (
            jsonify({"description" :" request doesn't contain an access token ", "error" : "authorization required"}), 
            401,
        )

    api.register_blueprint(ItemBluePrint)
    api.register_blueprint(StoreBluePrint)
    api.register_blueprint(TagBluePrint)
    api.register_blueprint(UserBluePrint)

    return app