import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return 0
    if request.method == 'POST':        
        return 0

if __name__ == '__main__':
    app.run(debug=True)