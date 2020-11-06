from functools import wraps
from employee_api import app
from employee_api.models import User
import jwt
from flask import request, jsonify

# Creating custom decorator to validate the API key
# that will be passed to all API routes that return DB info
def token_required(our_flask_function):
    # we are gathering parameters from returned function
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        # variable number of arguments and keyword arguments allowed
        token = None
        try:
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token'].split(' ')[1]
        except:
            if not token:
                return jsonify({'message', 'Token missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user_token = User.query.filter_by(id = data['public_id']).first()
            # my addition
            if current_user_token.token != token:
                return jsonify({'message': 'Token is invalid'}), 401
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return our_flask_function(current_user_token, *args, **kwargs)
    
    return decorated
            