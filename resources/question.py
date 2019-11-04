from flask_restful import Resource, reqparse
from bson import json_util
from bson.objectid import ObjectId
from db import mongo
import traceback

class QuestionCreator(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('question',
                        type=str,
                        required=True,
                        help="Questions field cannot be left blank!"
                        )
    parser.add_argument('A',
                        type=str,
                        required=True,
                        help="A field cannot be left blank!"
                        )
    parser.add_argument('B',
                        type=str,
                        required=True,
                        help="B field cannot be left blank!"
                        )
    parser.add_argument('C',
                        type=str,
                        required=True,
                        help="C field cannot be left blank!"
                        )
    parser.add_argument('D',
                        type=str,
                        required=True,
                        help="D field cannot be left blank!"
                        )
    parser.add_argument('answer',
                        type=str,
                        required=True,
                        help="answer field cannot be left blank!"
                        )

    def post(self):
        data = QuestionCreator.parser.parse_args()

        try:
            # try **data later
            question_id = mongo.db.questions.insert_one({
                "question": data['question'],
                "A": data['A'],
                "B": data['B'],
                "C": data['C'],
                "D": data['D'],
                "answer": data['answer']
            }).inserted_id
            question_created = mongo.db.questions.find_one(
                {"_id": question_id})
        except:
            return {'message': 'An error occured inserting the Question'}, 500

        return json_util._json_convert(question_created), 201


class Question(Resource):
    # TODO: Implement get and delete for question
    pass


class QuestionList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('questions',
                        type=dict,
                        required=True,
                        action='append',
                        help="Questions field cannot be left blank!"
                        )

    def get(self):
        try:
            questions = mongo.db.questions.find()
        except:
            return {'message': 'An error occured trying to look up these Questions'}, 500

        return json_util._json_convert(questions), 200

    def post(self):
        data = QuestionList.parser.parse_args()
        
        try:
            questions_created = []
            for question in data['questions']:
                question_id = mongo.db.questions.insert_one({
                    "question": question['question'],
                    "A": question['A'],
                    "B": question['B'],
                    "C": question['C'],
                    "D": question['D'],
                    "answer": question['answer']
                }).inserted_id
                question_created = mongo.db.questions.find_one(
                    {"_id": question_id})
                questions_created.append(mongo.db.questions.find_one({"_id": question_id}))
        except:
            return {'message': 'An error occured creating the Questions'}, 500

        return json_util._json_convert({"questions":questions_created}), 201
