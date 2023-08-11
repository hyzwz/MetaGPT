# 使用包含Python3.9和Nodejs20 slim版本的基础镜像
FROM nikolaik/python-nodejs:python3.9-nodejs20-slim

# 安装MetaGPT需要的Debian软件
RUN apt update &&\
    apt install -y git chromium fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 --no-install-recommends &&\
    apt clean

# 全局安装Mermaid CLI
ENV CHROME_BIN="/usr/bin/chromium" \
    AM_I_IN_A_DOCKER_CONTAINER="true"
RUN npm install -g @mermaid-js/mermaid-cli &&\
    npm cache clean --force

# 安装Python依赖并安装MetaGPT
COPY . /app/metagpt
RUN cd /app/metagpt &&\
    mkdir workspace &&\
    pip install -r requirements.txt &&\
    pip cache purge &&\
    python setup.py install

# 设置工作目录
WORKDIR /app/metagpt

# 使用tail命令运行一个无限循环
CMD ["sh", "-c", "tail -f /dev/null"]
