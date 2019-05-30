from run import api
from controllers import users

api.add_resource(users.UserRegistration, '/registration')
api.add_resource(users.UserLogin, '/login')
api.add_resource(users.UserLogoutAccess, '/logout/access')
api.add_resource(users.UserLogoutRefresh, '/logout/refresh')
api.add_resource(users.TokenRefresh, '/token/refresh')
api.add_resource(users.AllUsers, '/users')
api.add_resource(users.SecretResource, '/secret')