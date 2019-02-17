# Third party import
import datetime
from flask import jsonify, request, abort, make_response
from marshmallow import ValidationError

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                get_jwt_identity, jwt_refresh_token_required, get_raw_jwt, JWTManager)

# local import
from app.api.v2 import version2
from ..models.user_models import UserModel
from ..models.token_model import RevokedTokenModel
from ..schemas.user_schemas import UserSchema



@version2.route('/auth/register/', methods=['POST'])
def register_user():
    """ Register user endpoint."""
    reg_data = request.get_json()
    print('######## reg data: /auth/register/  #######', reg_data)

    
    # Empty entry
    if not reg_data:
        abort(make_response(jsonify({'status': 400, 'message': 'No data provided'}), 400))

    else:                
        try:            
            # Check if request is valid
            data = UserSchema().load(reg_data)
            print('############## data: UserSchema:#######', data)
        
            # Check if username exists
            if UserModel().exists('username', data['username']):
                abort(make_response(jsonify({'status': 409, 'message' : 'Username already exists'}), 409))
            
            # Check if email exists    
            elif UserModel().exists('email', data['email']):
                abort(make_response(jsonify({'status': 409, 'message' : 'Email already exists'}), 409))

            else:
                # Save new user 
                new_user = UserModel().save(data)
                print('#############new_user############',new_user)
                result = UserSchema(exclude=['password']).dump(new_user)
                # Generate access and refresh tokens
                access_token = create_access_token(identity=new_user['id'])
                refresh_token = create_refresh_token(identity=new_user['id'])
                return jsonify({
                    'status': 201, 
                    'message' : 'New user created', 
                    'data': result, 
                    'access_token' : access_token, 
                    'refresh_token' : refresh_token
                    }), 201
            #display errors and valid data entered          
        except ValidationError as error:
            error.messages
            valid_data = error.valid_data
            abort(make_response(jsonify({'status': 400, 'message' : 'Invalid data', 'errors': error.messages, 'valid_data':valid_data}), 400))    

@version2.route('/auth/login/', methods=['POST'])
def login():
    """ Login a registered user"""
    login_data = request.get_json()

    # Check for empty entries
    if not login_data:
        abort(make_response(jsonify({'status': 400, 'message': 'No data provided'}), 400))

    else:
        try:
            # Check if credentials have been passed
            data = UserSchema().load(login_data, partial=True)
            
            try:
                username = data['username']
                password = data['password']

                if not UserModel().exists('username', username):
                    abort(make_response(jsonify({'status': 404, 'message' : 'User not found'}), 404))

                else:
                    user = UserModel().where('username', username)

                    # Check if password match
                    if not UserModel().checkpwdhash(user['password'], password):
                        abort(make_response(jsonify({'status': 422, 'message' : 'Invalid password'}), 422))

                    else:
                        # Generate user tokens 
                        expires = datetime.timedelta(days=10)
                        access_token = create_access_token(identity=user['id'], expires_delta=expires)
                        refresh_token = create_refresh_token(identity=True)
                        return jsonify({
                            'status': 200, 
                            'message': 'User logged in successfully',
                            'access_token': access_token,
                            'refresh_token': refresh_token,
                            'user_id': user['id']
                            }), 200

            except:
                abort(make_response(jsonify({'status': 400, 'message': 'Invalid credentials'}), 400))

        except ValidationError as error:
            #errors = error.messages
            abort(make_response(jsonify({'status': 400, 'message' : 'Invalid data', 'errors': error}), 400))        
    

@version2.route('/refresh_token/', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
    """ Refresh user token."""
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'status': 200, 'message': 'Token refreshed successfully', 'access_token': access_token, 'current_user':current_user })


@version2.route('/auth/logout/', methods=['POST'])
@jwt_required
def logout():
    """ Logout user """
    jti = get_raw_jwt()['jti']
    RevokedTokenModel().save(jti)
    return jsonify({'status': 200, 'message': 'Logged out successfully'}), 200

@version2.route('/profile/<int:user_id>/', methods=['GET'])
def get_user_profile(user_id):
    """ Get user profile."""
      
    if not UserModel().exists('id', user_id):
        abort(make_response(jsonify({'status': 404, 'message': 'User not found'}), 404))

    else:
        user = UserModel().getOne(user_id)
        result = UserSchema().dump(user) 
        return jsonify({
            'status': 200,
            'data': result
             })   



    










