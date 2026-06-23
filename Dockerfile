# 紫薇斗数排盘 - Docker 镜像
FROM python:3.11-slim AS base

WORKDIR /app

# 安装系统依赖（纯 Python 项目不需要）
# 复制依赖并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY . .

# 提供 entry point 脚本
RUN chmod +x main.py

# 默认命令：显示帮助
CMD ["python", "main.py", "--help"]

# -------------------------------
# 精简运行时镜像
FROM base AS runtime

ENTRYPOINT ["python", "main.py"]
