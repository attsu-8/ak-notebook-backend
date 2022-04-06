#!/bin/sh

######################################################################
#コンテナ環境のpythonライブラリをlobkファイルへ出力して親階層へMOVEする
######################################################################

WORK_DIR=$(pwd)
IMAGE_NAME="manage_python_lib:latest"
CONTAINER_NAME="manage_python_lib_env"
EXPORT_FILE="requirements.lock"

function log_info () {
    echo
    echo +++++++++++++++++++++++++++++++++++++++++++++
    echo "# $1"
    echo +++++++++++++++++++++++++++++++++++++++++++++
}

log_info "rebuild dokcer image."
docker build -t ${IMAGE_NAME} .

log_info "run docker container."
docker run --name ${CONTAINER_NAME} \
           -v "${WORK_DIR}":/root/src \
           -it -d ${IMAGE_NAME} 

log_info "update pip,wheel,setuptools."
docker exec -it ${CONTAINER_NAME} pip install --upgrade pip wheel setuptools

log_info "freeze pip into $EXPORT_FILE"
docker exec -it ${CONTAINER_NAME} pip freeze > ${EXPORT_FILE}
echo "EXPORT $EXPORT_FILE --> $WORK_DIR/$EXPORT_FILE"  

log_info "remove container."
docker rm -f ${CONTAINER_NAME}

log_info "move requirements.lock"
mv ${EXPORT_FILE} ../
echo MOVE $EXPORT_FILE
