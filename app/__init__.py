
import psycopg2
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv
load_dotenv()

from instance.config import app_config
from app.api.v2.database.db_config import DbConnection

from app.api.v2.views.user_views import version2 as v2Users
from app.api.v2.views.question_views import version2 as v2Questions
from app.api.v2.views.meetup_views import version2 as v2Meetups
from app.api.v2.views.comment_views import version2 as v2Comments

from app.api.v2.models.token_model import RevokedTokenModel




def create_app(config_name):
    """Initialize  app."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # Register version2 Blueprints
    app.register_blueprint(v2Users)
    app.register_blueprint(v2Questions)
    app.register_blueprint(v2Meetups)
    app.register_blueprint(v2Comments)

    jwt = JWTManager(app)

   #db
    try:
        conn = DbConnection()
        print('###At app/__init__.py; conn::', conn)

        conn.db_conn(config_name)
        print('### config name::', config_name)

        conn.createTables()
        print('###At app/__init__.py; create tables::', conn.createTables())

        conn.seed() 
        print('###At app/__init__.py; seed::', conn.seed())
        
    except (Exception, psycopg2.Error) as error:
        print('Error creating db connection', error)  

    @app.route('/', methods=['GET'])
    @app.route('/index', methods=['GET'])
    def landing_page():
        """ Landing page endpoint."""
        return jsonify({
            'status': 200,
            'message': 'Welcome to Questioner'
            }), 200

    #############################
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'status': 404,
            'message': 'Url not found. Check your url and try again'
            }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'status': 500,
            'message': 'Internal server Error. Your request could not be processed'
            }), 500

    @jwt.token_in_blacklist_loader
    def check_blacklisted(token):
        jti = token['jti']
        return RevokedTokenModel().blacklistedTokens(jti)

    @jwt.expired_token_loader
    def expired_token():
        return jsonify({
            'status': 401,
            'message': 'Token has expired'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return jsonify({
            'status': 401,
            'message': reason
        }), 401

    @jwt.revoked_token_loader
    def revoked_token():
        return jsonify({
            'status': 401,
            'message': 'Token has been revoked'
        }), 401

    @jwt.unauthorized_loader
    def unauthorized(reason):
        return jsonify({
            'status': 401,
            'message': reason
        }), 401
    return app
