from flask import Flask,jsonify,request
from flask_cors import CORS
import uuid



app=Flask(__name__)
CORS(app)


@app.route('/server/', methods=['GET', 'POST'])
def record():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        EMOTIONS.append({
            'id': uuid.uuid4().hex,
            'emotion': post_data.get('emotion')
        })
        response_object['emotion'] = 'emotion  recorded!'
    else:
        response_object['emotions'] = EMOTIONS
    return jsonify(response_object)

EMOTIONS =  [{
              } 
                  
            ]