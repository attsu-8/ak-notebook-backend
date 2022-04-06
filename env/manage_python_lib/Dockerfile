########################################################
### pythonのライブラリを管理するための環境
### update_lockfile.shを起動してlockファイルを更新する             
########################################################

FROM python:3.9
#️以降のコマンドを実行するユーザーを指定
USER root


########################################################
### パッケージのインストール              
########################################################
#パッケージリストの更新
RUN apt-get update

# 日本語ロケールの設定
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get -y install vim less
RUN apt-get -y install default-mysql-client


########################################################
### pythonライブラリのインストール              
########################################################
WORKDIR /root/src
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
