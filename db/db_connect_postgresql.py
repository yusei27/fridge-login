import psycopg2
import psycopg2.extras
import configparser
import os
import errno

class DbConnectPostgres:
    """
    Postgresqlにアクセスするための汎用クラス
    以下のサイトを参考に作成
    https://tech.nkhn37.net/python-psycopg2-postgresql-dbaccess/
    """
    def __init__(self) -> None:
        """コンストラクタ
        :return: None
        """
        # コンフィグファイルからデータを取得
        # config_db = configparser.ConfigParser()
        # config_ini_path = "./config/dbconfig.ini"

        # # 指定したiniファイルが存在しない場合、エラー発生
        # if not os.path.exists(config_ini_path):
        #     raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
        # config_db.read(config_ini_path)
        # print(config_db)
        # 接続情報の取得
        host = os.environ.get("DB_HOST")
        port = os.environ.get("DB_PORT")
        dbname = os.environ.get("DB_NAME")
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")
        print(host, port, dbname, user, password)
        # コネクションを確立する
        self.con = psycopg2.connect(
            host=host, port=port, dbname=dbname, user=user, password=password
        )
        self.con.set_client_encoding("utf-8")
        # カーソルを作成する
        self.cursor = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    def execute_non_query(self, sql: str, bind_var: tuple = None) -> None:
        """CREATE/INSERT/UPDATE/DELETEのSQL実行メソッド
        :param sql: 実行SQL
        :param bind_var: バインド変数
        :return: None
        """
        # SQLの実行
        if bind_var is None:
            self.cursor.execute(sql)
        else:
            # バインド変数がある場合は指定して実行
            self.cursor.execute(sql, bind_var)
    def execute_query(self, sql: str, bind_var: tuple = None, count: int = 0) -> list:
        """SELECTのSQL実行メソッド
        :param sql: 実行SQL
        :param bind_var: バインド変数
        :param count: データ取得件数
        :return: 結果リスト
        """
        # SQLの実行
        if bind_var is None:
            print(sql)
            self.cursor.execute(sql)
        else:
            # バインド変数がある場合は指定して実行
            print("bind_varあり", sql)
            self.cursor.execute(sql, bind_var)
        result = []
        if count == 0:
            rows = self.cursor.fetchall()
            for row in rows:
                result.append(dict(row))
        else:
            # 件数指定がある場合はその件数分を取得する
            rows = self.cursor.fetchmany(count)
            for row in rows:
                result.append(dict(row))
        return result
    def commit(self) -> None:
        """コミット
        :return: None
        """
        self.con.commit()
    def rollback(self) -> None:
        """ロールバック
        :return: None
        """
        self.con.rollback()
    def __del__(self) -> None:
        """デストラクタ
        :return: None
        """
        self.cursor.close()
        self.con.close()