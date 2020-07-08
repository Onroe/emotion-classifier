from flask import Flask,jsonify,request,json
from flask_cors import CORS
import uuid
import os




app=Flask(__name__)
CORS(app)

#Record Emotion from Webcam picture
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

#load json file with emotions
@app.route('/emotionjson/', methods=['GET', 'POST'])
def emotion_json():
    path = "D:/Python/Flask/FlaskChat/api/model/emotion/model.json"
    Json = "model.json"
    file_path = os.path.join(path, Json)
    if os.path.exists(path):
       data = "" 
       try:
          with open(path) as file:
              data = json.load(file)
       except: 
              data = "could not read file"
       return jsonify(data)    

#load json file with gender
@app.route('/genderjson/', methods=['GET', 'POST'])
def gender_json():
    path = "D:/Python/Flask/FlaskChat/api/model/gender"
    Json = "model.json"
    file_path = os.path.join(path, Json)
    if os.path.exists(path):
       data = "" 
       try:
          with open(file_path) as file:
              data = json.load(file)
       except: 
              data = "could not read file"
       return jsonify(data)           
 