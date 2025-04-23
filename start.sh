#!/bin/bash

# 设置Python路径
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 清理已存在的进程
echo "清理已存在的进程..."
pkill -f "uvicorn"
sudo kill -9 $(sudo lsof -t -i:8000) 2>/dev/null || true

# 等待端口释放
sleep 2

# 启动后端服务
echo "启动后端服务..."
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 启动前端服务
echo "启动前端服务..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# 等待用户按下 Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait 