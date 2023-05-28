#!/bin/bash
CONTAINER_ALREADY_STARTED="CONTAINER_ALREADY_STARTED_PLACEHOLDER"

if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
  echo "-- First container startup --"
  # 此处插入你要执行的命令或者脚本文件
  echo "系统初始化中"
  python manage.py migrate
  touch $CONTAINER_ALREADY_STARTED
  echo "创建超级用户"
  DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME
  DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL
  DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD
  python manage.py createsuperuser --noinput
  echo "初始化完成"
else
  echo "-- Not first container startup --"
fi

echo "启动服务"
uvicorn auxiliary.asgi:application --reload
