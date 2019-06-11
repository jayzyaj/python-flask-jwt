from flask_restplus import Resource, reqparse
from models.bank_account import BankAccountModel
from flask_jwt_extended import jwt_required
from run import api

parser = reqparse.RequestParser()
parser.add_argument('bank_account', help = 'This field cannot be blank', required = True)
parser.add_argument('bank_account_name', help = 'This field cannot be blank', required = True)
parser.add_argument('bank_account_number', help = 'This field cannot be blank', required = True)

class BankRegistration(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        
        new_bank_account = BankAccountModel(
            bank_account = data['bank_account'],
            bank_account_name = data['bank_account_name'],
            bank_account_number = data['bank_account_number']
        )
        
        try:
            new_bank_account.save_to_db()
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'User {} was created'.format(data['email']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }, 201
        except:
            return {'message': 'Something went wrong'}, 500