from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
#特定のオリジンだけを許可する
cors = CORS(app, resources={r"/*":{"origin": ["http://localhost:5173"]}})

@app.route('/register/user')
def register_user():
    print("ユーザー登録API実行")
    return jsonify({'status':200, 'data':3})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333, debug=True)