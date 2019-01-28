from marshmallow import ValidationError
from flask import  request, jsonify, make_response, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2 import version2

from app.api.v2.models.question_models import QuestionModel
from app.api.v2.schemas.questions_schema import QuestionSchema
from app.api.v2.models.vote_model import VotesModel
from ..models.meetup_models import MeetupModel
#from ..models.vote_model import VotesModel


@version2.route('/question/', methods=["POST"])
@jwt_required
def post_question():
    """ Post a question."""
    q_data = request.get_json()


    # No data provied
    if not q_data:
        abort(make_response(jsonify({'status': 400, 'message': 'No data sent'}), 400))

    else:
        try:
            data = QuestionSchema().load(q_data)

            if not MeetupModel().exists('id', data['meetup_id']):
                abort(make_response(jsonify({'status': 404, 'message': 'Meetup not found'}), 404))

            else:
                data['user_id'] = get_jwt_identity()
                question = QuestionModel().save(data)
                result = QuestionSchema().dump(question)
                return jsonify({ 'status': 201, 'message': 'Question posted successfully', 'data':result}), 201
          
        # return errors alongside valid data
        except ValidationError as errors:
            #errors.messages
            valid_data = errors.valid_data
            abort(make_response(jsonify({'status': 400, 'message' : 'Invalid data.', 'errors': errors.messages, 'valid_data':valid_data}), 400)) 


@version2.route('/meetups/<int:meetup_id>/questions/', methods=['GET'])
def get_meetup_questions(meetup_id):
    """" Get all questions for a specific meetup."""

    if not MeetupModel().exists('id', meetup_id):
        abort(make_response(jsonify({'status':404, 'message': 'Meetup not found'}), 404))

    else:
        questions = QuestionModel().getAll(meetup_id)
        result = QuestionSchema(many=True).dump(questions)
        return jsonify({'status': 200, 'data': result}), 200


    
      
@version2.route('/question/<int:question_id>/downvote/', methods=["PATCH"])
@jwt_required
def downvote_question(question_id):
    """ Downvote a question."""
     
    current_user = get_jwt_identity()

    # check if question exists
    if not QuestionModel().exist('id', question_id):
        abort(make_response(jsonify({'status': 404, 'error': 'Question not found'}), 404))

    else:
        voted = VotesModel().checkVote(question_id, current_user)
        if voted:
            abort(make_response(jsonify({'status':403, 'message':'You have alaready voted for this question'}), 403))
        
        else:                  
            # Downvote the question
            question = QuestionModel().downvote(question_id)
            result = QuestionSchema().dump(question)
            VotesModel().addNewVote({
                'user_id': current_user,
                'question_id':question_id,
                'vote':'downvote'
            })
            return jsonify({'status': 200, 'message': 'Question down-voted', 'data': result}), 200

    

@version2.route('/question/<int:question_id>/upvote/', methods=["PATCH"])
@jwt_required
def upvote_question(question_id):
    """ upvote a question."""

    current_user = get_jwt_identity()

    # check if question exists
    if not QuestionModel().exist('id', question_id):
        abort(make_response(jsonify({'status': 404, 'error': 'Question not found'}), 404))

    else:
        voted = VotesModel().checkVote(question_id, current_user)
        if voted:
            abort(make_response(jsonify({'status':403, 'message':'You have already voted'}), 403))

        else:
            # Downvote the question
            question = QuestionModel().upvote(question_id)
            result = QuestionSchema().dump(question)
            VotesModel().addNewVote({
                'user_id':current_user,
                'question_id': question_id,
                'vote':'upvote'
            })
            return jsonify({'status': 200, 'message': 'Question up-voted', 'data': result}), 200
            


