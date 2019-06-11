from flask import Flask
from flask_restplus import Api, Namespace
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/cash_advance_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return users.RevokedTokenModel.is_jti_blacklisted(jti)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}
api = Api(app, security='Bearer Auth', authorizations=authorizations)

name_space = Namespace('main', description='Main APIs')
app.run(host='0.0.0.0')

from models import users, bank_account
from routes import users as user_route