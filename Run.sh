#!/bin/bash -e
# 
docker build -t cargastock .
full_path=$(realpath $0)
SCRIPTPATH=$(dirname $full_path)
echo {$SCRIPTPATH/script-log/}
docker run -it --rm --name microservicio -v $SCRIPTPATH/script-log/:/usr/src/app/log/ cargastock 