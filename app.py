from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask import request
import db.db_connect_postgresql as db

from psycopg2.sql import Identifier, Literal
from psycopg2.sql import SQL

import traceback
app = Flask(__name__)
#特定のオリジンだけを許可する

CORS(app)  # すべてのオリジンからのアクセスを許可
#cors = CORS(app, resources={r"/*":{"origin": ["http://localhost:5173","http://localhost:3000s"]}})

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

@app.route('/login/user', methods=["POST"])
def login():
    print("login関数")
    request_data = request.get_json()
    print("リクエスト", request_data)
    user_email = request_data["email"]
    user_password = request_data["password"]
    print("usr_email user_password", user_email, user_password)
    try:
        print("db接続")
        db_connect = db.DbConnectPostgres()
        sql = SQL("""SELECT salt 
        FROM "fridge_system".user_table
        WHERE mail={user_email};""").format(
            user_email = Literal(user_email)
        )
        result = db_connect.execute_query(sql=sql)
        print("result", result)
        if len(result) == 0:
            #メールアドレスが登録されていない
            db_connect.commit()
            return Response(status=300, response=jsonify({'content':"このメールアドレスは登録されていません。"}))
        elif len(result) == 1:
            #正常動作、ソルトを想定通り取得できたので、パスワード認証
            salt = result[0]["salt"]
            hash_value, _ = encode_password(user_password, salt)
            
        
            sql =SQL("""SELECT count(mail)
            FROM {schema}.{table} 
            WHERE mail={user_email} AND password={password};""").format(
                schema = Identifier("fridge_system"),
                table = Identifier("user_table"),
                user_email = Literal(user_email),
                password = Literal(hash_value.hexdigest())
            )
            result = db_connect.execute_query(sql=sql)
            num_login_user = result[0]["count"]
            print("num_login_user", num_login_user)
            print("ログインユーザー")
            if num_login_user == "1":
                print("1")
                return Response(status=200, response=jsonify({"num_login_user":num_login_user}))
            else:
                print("1じゃない")
                return Response(status=300, response=jsonify({"num_login_user":num_login_user, "content":"同じメールアドレスで複数登録されています"}))
        else:
            #想定外の動作
            return Response(status=300, response=jsonify({'content':"メースアドレスの照合が想定外の動作", "num_salt":len(salt)}))
    except Exception as e:
        print(traceback.format_exc())
        db_connect.rollback()
        print("ロールバックを実行しました。")
        return jsonify({'status':300, 'data':3})

    


def hash_password(password):
    import os
    import base64
    import hashlib
    #ソルトを生成
    # salt = os.urandom(32)
    # print("salt", salt)
    salt_decode = base64.b64encode(os.urandom(32)).decode('utf8')
    hash_value = encode_password(password, salt_decode)
    print("salt", salt_decode)
    return hash_value.hexdigest(), salt_decode

def encode_password(password,salt):
    import hashlib
    
    #パスワードにソルトを付与してハッシュ値生成
    hash_value = hashlib.sha256(password.encode() + salt.encode())
    print(hash_value)
    print("hash16", hash_value.hexdigest())#ハッシュオブジェクトからハッシュ値(16進数文字列)取得,sha256は16進数もじれt５うを生成する仕組み
    return hash_value, salt

def get_register_user_data(request_data):
    user_name = request_data["user"]["name"]
    user_email = request_data["user"]["email"]
    user_password = request_data["user"]["password"]
    user_password_confirm = request_data["user"]["password_confirm"]

    return user_name, user_email, user_password, user_password_confirm




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333, debug=True)