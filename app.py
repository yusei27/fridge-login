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

    #リクエストデータからユーザ登録に必要な情報を取得    
    user_name, user_email, user_password, user_password_confirm = get_register_user_data(requeat_data)
    if user_password == user_password_confirm:
        hashed_password, salt = hash_password(user_password)
        
        sql = f"""
            INSERT INTO "fridge_system".user_table
            (name_user, mail, password, salt)
                VALUES (%s, %s, %s, %s);    
        """
        try:
            print("db接続")
            db_connect = db.DbConnectPostgres()
            db_connect.execute_non_query(sql=sql, bind_var=(user_name, user_email, hashed_password, salt))
            db_connect.commit()
        except Exception as e:
            print(e)
            db_connect.rollback()
            print("ロールバックを実行しました。")
            return jsonify({'status':300, 'data':3})
	

    else:
        print("パスワードと確認用パスワードが異なります")
        return jsonify({'status':300, 'data':3})
    return jsonify({'status':200, 'data':3})


def hash_password(password):
    import os
    import base64
    import hashlib
    #ソルトを生成
    salt = os.urandom(32)
    print("salt", salt)
    salt_encode = base64.b64encode(salt)
    #パスワードにソルトを付与してハッシュ値生成
    hash_value = hashlib.sha256(password.encode() + salt_encode)
    print(hash_value)
    print("hash16", hash_value.hexdigest())#ハッシュオブジェクトからハッシュ値(16進数文字列)取得,sha256は16進数もじれt５うを生成する仕組み
    return hash_value.hexdigest(), salt_encode

def get_register_user_data(request_data):
    user_name = request_data["user"]["name"]
    user_email = request_data["user"]["email"]
    user_password = request_data["user"]["password"]
    user_password_confirm = request_data["user"]["password_confirm"]

    return user_name, user_email, user_password, user_password_confirm

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333, debug=True)