from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.after_request
def set_cors_headers(response):
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    print(response.headers)
    return response

@app.route('/test', methods=['GET'])
def hello_world():
    data = {"message": "Hello Poland"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)