#!/usr/bin/bash
echo "versão: "
read v
docker build -t glossario:$v ../.
docker tag ramonufsc/glossario:$v ramonufsc/glossario:latest
docker push ramonufsc/glossario:$v
docker push ramonufsc/glossario:latest