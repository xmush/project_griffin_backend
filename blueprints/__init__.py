
from flask_cors import CORS, cross_origin
import json
import config
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_script import Manager
from functools import wraps

app = Flask(__name__)
jwt = JWTManager(app)
app.config['APP_DEBUG'] = True
CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True, intercept_exceptions=False)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['user_type'] != "admin":
            return {'user_type': 'FORBIDDEN', 'message': 'Admin only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


flask_env = os.environ.get('FLASK_ENV', 'Production')
if flask_env == "Production":
    app.config.from_object(config.ProductionConfig)
elif flask_env == "Testing":
    app.config.from_object(config.TestingConfig)
else:
    app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



@app.before_request
def before_request():
    if request.method != 'OPTIONS':  # <-- required
        pass
    else:
        return {}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': '*', 'Access-Control-Allow-Headers': '*'}


@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.warning("REQUEST_LOG\t%s",
                           json.dumps({
                               'method': request.method,
                               'code': response.status,
                               'uri': request.full_path,
                               'request': requestData,
                               'response': json.loads(response.data.decode('utf-8'))
                           })
                           )
    else:
        app.logger.error("REQUEST_LOG\t%s",
                         json.dumps({
                             'method': request.method,
                             'code': response.status,
                             'uri': request.full_path,
                             'request': requestData,
                             'response': json.loads(response.data.decode('utf-8'))
                         }))
    return response

from blueprints.auth import bp_auth
from blueprints.user.resources import bp_user
from blueprints.product_type.resources import bp_product_type
from blueprints.publisher.resources import bp_publisher
from blueprints.payment_method.resources import bp_payment_method
from blueprints.ads_spot.resources import bp_ads_spot
from blueprints.ads_image.resources import bp_ads_image

app.register_blueprint(bp_auth, url_prefix='/signin')
app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_product_type, url_prefix='/ads_type')
app.register_blueprint(bp_publisher, url_prefix='/publisher')
app.register_blueprint(bp_payment_method, url_prefix='/payment_method')
app.register_blueprint(bp_ads_spot, url_prefix='/ads_spot')
app.register_blueprint(bp_ads_image, url_prefix='/ads_image')

db.create_all()
