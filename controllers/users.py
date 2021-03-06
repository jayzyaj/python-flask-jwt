from flask_restplus import Resource, reqparse
from models.users import UserModel, RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from run import api

parser = reqparse.RequestParser()
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        
        if UserModel.find_by_email(data['email']):
            return {'message': 'User {} already exists'.format(data['email'])}, 422
        
        new_user = UserModel(
            email = data['email'],
            password = UserModel.generate_hash(data['password'])
        )
        
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'User {} was created'.format(data['email']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }, 201
        except:
            return {'message': 'Something went wrong'}, 500

@api.doc(params={'email': 'An email of the user', 'password': 'Password of the user'})
class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_email(data['email'])

        if not current_user:
            return {'message': 'Email {} doesn\'t exist'.format(data['email'])}, 422
        
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'Logged in as {}'.format(current_user.email),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': current_user,
                }, 200
        else:
            return {'message': 'Invalid credentials'}, 422

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
      
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
      
      
class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()
    
    def delete(self):
        return UserModel.delete_all()
      
      
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }