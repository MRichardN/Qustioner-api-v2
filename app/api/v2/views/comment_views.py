from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, abort, make_response, jsonify
from marshmallow import ValidationError

from app.api.v2 import version2
from ..schemas.comments_schema import CommentSchema
from ..models.comment_models import CommentModel
from ..models.question_models import QuestionModel



@version2.route('/question/<int:question_id>/comments/', methods=['POST'])
@jwt_required
def post_comment(question_id):
    """ Post a question."""
    c_data = request.get_json()


    # No data provied
    if not c_data:
        abort(make_response(jsonify({'status': 400, 'message': 'No data sent'}), 400))

    else:
        try:
            data = CommentSchema().load(c_data)

            if not QuestionModel().exist('id', question_id):
                abort(make_response(jsonify({'status': 404, 'message': 'Question not found'}), 404))

            elif CommentModel().check_duplicate(question_id, data['body']):
                abort(make_response(jsonify({'status':409, 'message':'This comment has already been posted'}), 409))    

            else:
                data['user_id'] = get_jwt_identity()
                data['question_id'] = question_id
                comment = CommentModel().save(data)
                result = CommentSchema().dump(comment)
                return jsonify({'status': 201, 'message': 'Comment posted successfully', 'data':result}), 201
          
        # return errors alongside valid data
        except ValidationError as errors:
            #errors.messages
            valid_data = errors.valid_data
            abort(make_response(jsonify({'status': 400, 'message' : 'Invalid data.', 'errors': errors.messages, 'valid_data':valid_data}), 400)) 



# @version2.route('/question/<int:question_id>/comments/', methods=['POST'])
# @jwt_required
# def post_comment(question_id):
#     """ Post comment to a question."""

#     comment_data = request.get_json()

#     if not comment_data:
#         abort(make_response(jsonify({'status':400, 'message': 'No data provided'}), 400))

#     elif not QuestionModel().exist('id', question_id):
#         abort(make_response(jsonify({'status':404, 'message': 'Question not found'}), 404))

#     else:
#         try:
#             data = CommentSchema().load(comment_data)


#             data['user_id'] = get_jwt_identity()
#             data['question_id'] = question_id
#             res = CommentModel().save(data)
#             result = CommentSchema().dump(res)
#             return jsonify({'status':201, 'message':'Comment posted', 'data':result}), 201

#         except ValidationError as errors:
#             errors.messages
#             valid_data = errors.valid_data
#             abort(make_response(jsonify({'status': 400, 'error' : 'Invalid data',\
#             'errors': errors.messages, 'valid_data':valid_data}), 400))        


@version2.route('/question/<int:question_id>/comments/', methods=['GET'])
def get_comments(question_id):
    """ Fetch all comments."""
    if not QuestionModel().exist('id', question_id):
        abort(make_response(jsonify({'status': 404, 'message': 'Question not found'}), 404))
    
    else:
        comments = CommentModel().getAll(question_id)
        result = CommentSchema(many=True).dump(comments)
        return jsonify({'status':200, 'data': result}), 200
