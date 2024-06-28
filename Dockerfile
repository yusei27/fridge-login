#元となるDockerイメージの指定
FROM python:3.12.1
#作成者
LABEL maintainer "yusei-hashimoto"

WORKDIR /fridge-login

#デフォルトでDebianが入る、下記のコマンドで余計なものを削除してコンテナサイズを落とす
# 「&&（複数コマンドが書ける）」と「 \（改行して書ける）」
# https://dev.classmethod.jp/articles/apt-get-magic-spell-in-docker/
# RUN apt-get update && apt-get install -y \
#     xxx \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

#pipenvをインストール
RUN pip install --upgrade pip && \
    pip install pipenv
    


COPY ./ /fridge-login/

RUN pipenv install

#API起動
#CMD ["pipenv", "run", "python", "app.py"]
CMD ["pipenv", "run", "gunicorn", "--config", "./wsgi/gunicorn.py"]
#[各種コマンド]
# docker build . -t example3:latest 

# docker image ls

# docker run -it imageid

# docker ps 現在起動中のコンテナの一覧が出力されます。

#docker exec -i -t コンテナID /bin/bash  指定したコンテナのコマンドプロンプトに接続 psコマンドでIDを見る

#docker run -it -v $(pwd) イメージID  カレントディレクトリをマウントしてコンテナを起動

#docker logs コンテナID コンテナのログを出力

#docker stop コンテナID コンテナを停止