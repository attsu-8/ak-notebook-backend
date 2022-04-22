########################################################
### builder stage             
########################################################
FROM python:3.9-buster as builder

USER root

WORKDIR /root/src

COPY ./env/requirements.lock ./

RUN pip install -r requirements.lock


########################################################
### production stage             
########################################################
FROM python:3.9-slim-buster as production

USER root

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
# 端末の種類を指定
ENV TERM xterm
# .pycを生成しない
ENV PYTHONDONTWRITEBYTECODE 1
#標準出力・エラーのストリームのバッファリングを行わない
ENV PYTHONUNBUFFERED 1

WORKDIR /root/src

#ECSのタスクをセキュリティの観点でreadonlyにしているが、
# migrationsファイルの出力は行いたいためボリュームを確保
VOLUME /root/src/api/migrations

# pythonライブラリの取得
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

RUN apt update && \
    apt -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 && \
    apt install -y libpq5 libxml2 && \
    apt -y install vim less && \
    apt -y install default-mysql-client && \
    apt clean && \
    apt -y install make  && \
    rm -rf /var/lib/apt/lists/*

COPY ./app ./

EXPOSE 8000

CMD sh runserver.sh