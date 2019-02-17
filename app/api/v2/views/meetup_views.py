# third party import
from flask import jsonify, request, abort, make_response
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

# local import
from app.api.v2 import version2
from ..schemas.meetups_schema import MeetupSchema
from ..models.meetup_models import MeetupModel
from ..models.user_models import UserModel
from ..schemas.rsvp_schema import RsvpSchema
from ..models.rsvp_model import RsvpModel
from ..schemas.user_schemas import UserSchema






@version2.route('/meetups/upcoming/', methods=['GET'])
def get_all_meetups():
    """ View all meetups."""
    meetups = MeetupModel().getAll()
    result = MeetupSchema(many=True).dump(meetups)
    return jsonify({'status': 200, 'data': result}), 200

    

@version2.route('/meetup/', methods=['POST'])
@jwt_required
def post_meetups():
    """ Post a meetup."""

    current_user = get_jwt_identity()
    
    if not UserModel().isAdmin(current_user):
        abort(make_response(jsonify({'status': 401, 'message': 'You are not authorized'}), 401))
    
    else:
        meetup_data = request.get_json()

        # No data provided
        if not meetup_data:
            abort(make_response(jsonify({'status': 400, 'message': 'No data provided'}), 400))
       
        else:
            try:
                # Check if request is valid
                data = MeetupSchema().load(meetup_data)
                duplicate, message = MeetupModel().check_if_duplicate(data)

                if duplicate:
                    abort(make_response(jsonify({'status':403, 'message':message}), 403))

                else:
                    new_meetup = MeetupModel().save(data)
                    print('## new-meetup in meetup view::', new_meetup)
                    result = MeetupSchema().dump(new_meetup) 
                    print('## result in meetup view::', result)
                    return jsonify({'status': 201, 'message': 'Meetup created', 'data': result}), 201   
        
            # display errors alongside valid data entered
            except ValidationError as errors:
                errors.messages
                valid_data = errors.valid_data
                abort(make_response(jsonify({'status': 400, 'message' : 'Invalid data', 'errors': errors.messages, 'valid_data':valid_data}), 400))    

    
 
@version2.route('/meetups/<int:meetup_id>/', methods=['GET'])
def get_a_specific_meetup(meetup_id):
    """ Get a specific question."""

    #check if meetup exists
    if not MeetupModel().exists('id', meetup_id):
        abort(make_response(jsonify({'status': 404, 'error': 'Meetup does not exist'}), 404))
    
        
    else:
        # Get a specific meetup
        meetup = MeetupModel().getOne(meetup_id)
        attendees = RsvpModel().usersAttending(meetup_id)
        meetup['usersAttending'] = attendees
        result = MeetupSchema().dump(meetup)
        return jsonify({'status':200, 'data': result}), 200


@version2.route('/meetups/<int:meetup_id>/<string:rsvps>/', methods=['POST'])
@jwt_required
def rspvs_meetup(meetup_id, rsvps):
    """ rsvp meetup."""

    response = ('yes', 'Yes', 'YES', 'no', 'No', 'NO', 'maybe', 'Maybe', 'MAYBE')

    current_user = get_jwt_identity()
        
    # Check if meetup exists
    if not MeetupModel().exists('id', meetup_id):
        abort(make_response(jsonify({'status': 404, 'message': 'Meetup does not exist'}), 404))

    # Check if rsvp is valid
    elif rsvps not in response:
        abort(make_response(jsonify({'status': 400, 'message': 'Invalid rsvp'}), 400))

    elif RsvpModel().exists(meetup_id, current_user):
        abort(make_response(jsonify({'status': 403, 'message': 'Already responded'}), 403))

    else:
        data = {'meetup_id':meetup_id, 'user_id': current_user, 'response':rsvps}
        resp = RsvpModel().save(data)
        result = RsvpSchema().dump(resp) 
        return jsonify({'status': 200, 'message':'Responded successfully', 'data': result}), 200
    
@version2.route('/meetup/<int:meetup_id>/', methods=['DELETE'])
@jwt_required
def delete_meetup(meetup_id):
    """ delete meetup """

    current_user = get_jwt_identity()

    if not UserModel().isAdmin(current_user):
        abort(make_response(jsonify({'status':401, 'message': 'Unauthorized'}), 401))
            
    else:
        if not MeetupModel().exists('id', meetup_id):
            abort(make_response(jsonify({'status':404, 'message': 'Meetup not found'}), 404))

        else:
            MeetupModel().delete(meetup_id)
            return jsonify({'status':200, 'message':'Meetup Deleted'}), 200   

           
@version2.route('/meetups/<int:meetup_id>/attendees/', methods=['GET'])
def get_attendees(meetup_id):
    """ Get meetup attendees."""

    if not MeetupModel().exists('id', meetup_id):
        abort(make_response(jsonify({'status': 404, 'message':'Meetup not found'}), 404))

    else:
        users = MeetupModel().usersAttending(meetup_id)
        result = UserSchema(many=True).dump(users)
        return jsonify({'status': 200, 'users': result, 'attendees': len(users)}), 200
    

@version2.route('/meetups/<int:meetup_id>/tags/', methods=['PATCH'])
@jwt_required
def update_meetup_tags(meetup_id):
    """ update meetup tags."""

    current_user = get_jwt_identity()

    if not UserModel().isAdmin(current_user):
        abort(make_response(jsonify({'status':401, 'message': 'Unauthorized'}), 401))
        
    else:
        meetup_data = request.get_json()

        if not MeetupModel().exists('id', meetup_id):
            abort(make_response(jsonify({'status':404, 'message': 'Meetup not found'}), 404))
            
        elif not meetup_data:
            abort(make_response(jsonify({'status': 400, 'message': 'No data provided'}), 400))
            
        elif 'tags' not in meetup_data:
            abort(make_response(jsonify({'status': 400, 'message': 'No meetup tags provided'}), 400))
            
        elif not len(meetup_data['tags']) > 0:
            abort(make_response(jsonify({'status': 400, 'message': 'Enter atleast one meetup tag'}), 400))
            
        else:
            meetup = MeetupModel().meetupTags(meetup_id, meetup_data['tags'])
            result = MeetupSchema().dump(meetup)
            return jsonify({
                'status': 200,
                'message':'Tags updated',
                'data':result
            })
            
    

        