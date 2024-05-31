# 使用 python 官方基礎映像檔
FROM python:3.8

# 將工作目錄指定為 /app
WORKDIR /app

# 安裝 python 額外套件
RUN pip install requests psycopg2 pandas matplotlib

# 安裝 必要的字型
RUN apt-get update && apt-get install -y fonts-arphic-uming

# 將當前目錄的檔案複製到工作目錄中
COPY . .