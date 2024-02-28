from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/register/user')
def register_user():
    print("ユーザー登録API実行")
    return jsonify({'status':200, 'data':3})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333, debug=True)