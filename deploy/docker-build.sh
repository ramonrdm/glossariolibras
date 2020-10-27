#!/bin/bash
docker login
echo "versão: "
read v
docker build -t glossario:$v .
docker tag 	glossario:$v ramonufsc/glossario:$v
docker tag 	glossario:$v ramonufsc/glossario:latest
docker push ramonufsc/glossario:$v
docker push ramonufsc/glossario:latest