from flask import Flask, jsonify, request
from flask_cors import CORS
from flask import request
import db.db_connect_postgresql as db
app = Flask(__name__)
#特定のオリジンだけを許可する
cors = CORS(app, resources={r"/*":{"origin": ["http://localhost:5173"]}})

@app.route('/register/user', methods=["POST"])
def register_user():
    print("ユーザー登録API実行")
    requeat_data = request.get_json()
    print("リクエスト", requeat_data)
    hash_password("yusei9981")

    print("db接続")
    db_connect = db.DbConnectPostgres()
    
    return jsonify({'status':200, 'data':3})


def hash_password(password):
    import os
    import base64
    import hashlib
    
    salt = os.urandom(32)
    print("salt", salt)
    salt_encode = base64.b64encode(salt)

    hash_value = hashlib.sha256(password.encode() + salt_encode)
    print(hash_value)
    print("hash16", hash_value.hexdigest())#ハッシュオブジェクトからハッシュ値(16進数文字列)取得,sha256は16進数もじれt５うを生成する仕組み

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333, debug=True)