from flask import Flask, jsonify, redirect, request, current_app
import boto3
from flask_cors import CORS

from functools import wraps
import json

app = Flask(__name__)
CORS(app)

s3_bucket_url = 'https://s3.eu-central-1.amazonaws.com/ora-col/'
s3_bucket_name = 'ora-col'
data_relative_url = '/data/data.json'
data = {"r": "R"}
s3_object = 'new_data.json'


def support_jsonp(f):
    """Require user authorization"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            resp = f(*args, **kwargs)
            resp.set_data('{}({})'.format(
                str(callback),
                resp.get_data(as_text=True)
            ))
            resp.mimetype = 'application/javascript'
            return resp
        else:
            return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@support_jsonp
def hello_world():
    print('update_questions')
    print(request)
    print('-------')
    print(request.args.get('questions_arr'))
    print('-------')

    # client = boto3.client('s3')
    # questions_arr = request.args.get('questions_arr')
    # if questions_arr:
    #     questions_data = json.loads(questions_arr)
    #     print('questions_data')
    #     print(questions_data)
    #     response = client.put_object(
    #         ACL='public-read-write',
    #         Bucket=s3_bucket_name,
    #         Body=json.dumps(questions_data),
    #         Key=s3_object
    #     )

    #     print('asdf')
    #     print(response)
    #     return jsonify(response)

    # else:

    print('start...')
    client = boto3.client('s3')
    obj = client.get_object(Bucket=s3_bucket_name, Key=s3_object)
    questions_data = obj['Body'].read().decode('utf-8')
    # [{"question": "what?", "tag": 'blue'}, {"question": "who?", "tag": 'red'}]
    questions_data = json.loads(questions_data)
    # print(type(questions_data))
    print('got object')
    print(questions_data)
    # questions_data['r'] = questions_data['r'] + 'l'

    print('connected')
    return jsonify(questions_data)


@app.route('/update_questions', methods=['POST'])
@support_jsonp
def update_questions_method():
    print('update_questions')
    print(request)

    client = boto3.client('s3')
    print(request.get_json())
    questions_data = request.get_json()
    print(questions_data)
    questions_data = (json.dumps(questions_data['questions_arr']))
    # questions_data = json.loads(questions_arr)

    print('-------1')
    # print(request.get_json())
    print('-------')
    # print(request.args.get('questions_arr'))
    print(questions_data)
    print('-------')
    # obj = [{"question": "what?", "tag": "blue"},
    #        {"question": "who?", "tag": "red"}]
    response = client.put_object(
        ACL='public-read-write',
        Bucket=s3_bucket_name,
        Body=questions_data,
        Key=s3_object
    )

    print(response)
    return jsonify(response)

# @app.route('/update_questions', methods=['GET'])
# @support_jsonp
# def update_questions_method():
#     print('update_questions')
#     print(request)
#     print('-------')
#     print(request.args.get('questions_arr'))
#     print('-------')

#     client = boto3.client('s3')
#     questions_data = json.loads(request.args.get('questions_arr'))
#     print('questions_data')
#     print(questions_data)
#     response = client.put_object(
#         ACL='public-read-write',
#         Bucket=s3_bucket_name,
#         Body=json.dumps(questions_data),
#         Key=s3_object
#     )

#     print('asdf')
#     print(response)
#     return jsonify(response)


if __name__ == '__main__':
    app.run()
