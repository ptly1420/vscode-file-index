#!/bin/bash

# 定义变量
NGINX_VERSION="1.18.0"
MOD_HTTP_UPSTREAM_HASH_VERSION="1.2.2"
MOD_STREAM_UPSTREAM_HASH_VERSION="1.9.0"
NGINX_SOURCE="nginx-${NGINX_VERSION}.tar.gz"
MOD_HTTP_UPSTREAM_HASH_SOURCE="ngx_http_upstream_hash-${MOD_HTTP_UPSTREAM_HASH_VERSION}.tar.gz"
MOD_STREAM_UPSTREAM_HASH_SOURCE="ngx_stream_upstream_hash-${MOD_STREAM_UPSTREAM_HASH_VERSION}.tar.gz"
DOWNLOAD_PATH="/usr/local/src"
INSTALL_PATH="/usr/local/nginx"

# 安装依赖
sudo yum install -y gcc pcre-devel zlib-devel openssl-devel readline-devel

# 下载 Nginx 源码
wget http://nginx.org/download/${NGINX_SOURCE} -P ${DOWNLOAD_PATH}
tar -zxvf ${DOWNLOAD_PATH}/${NGINX_SOURCE} -C ${DOWNLOAD_PATH}

# 下载并安装 HTTP 四层反向代理模块
wget https://github.com/yaoweibin/ngx_http_upstream_hash_module/archive/v${MOD_HTTP_UPSTREAM_HASH_VERSION}.tar.gz -O ${DOWNLOAD_PATH}/${MOD_HTTP_UPSTREAM_HASH_SOURCE}
tar -zxvf ${DOWNLOAD_PATH}/${MOD_HTTP_UPSTREAM_HASH_SOURCE} -C ${DOWNLOAD_PATH}
cp -rf ${DOWNLOAD_PATH}/ngx_http_upstream_hash-${MOD_HTTP_UPSTREAM_HASH_VERSION}/ngx_http_upstream_hash ${DOWNLOAD_PATH}/${NGINX_SOURCE}/src/http/modules/

# 下载并安装 Stream 四层反向代理模块
wget https://github.com/yaoweibin/nginx_upstream_hash_module/archive/v${MOD_STREAM_UPSTREAM_HASH_VERSION}.tar.gz -O ${DOWNLOAD_PATH}/${MOD_STREAM_UPSTREAM_HASH_SOURCE}
tar -zxvf ${DOWNLOAD_PATH}/${MOD_STREAM_UPSTREAM_HASH_SOURCE} -C ${DOWNLOAD_PATH}
cp -rf ${DOWNLOAD_PATH}/nginx_upstream_hash-${MOD_STREAM_UPSTREAM_HASH_VERSION}/ngx_stream_upstream_hash ${DOWNLOAD_PATH}/${NGINX_SOURCE}/src/stream/modules/

# 配置并编译安装 Nginx
cd ${DOWNLOAD_PATH}/${NGINX_SOURCE}
./configure --prefix=${INSTALL_PATH} --with-http_ssl_module --with-stream --add-module=../ngx_http_upstream_hash-${MOD_HTTP_UPSTREAM_HASH_VERSION} --add-module=../nginx_upstream_hash-${MOD_STREAM_UPSTREAM_HASH_VERSION}
make && sudo make install

# 创建系统服务并设置开机启动
sudo ln -sf ${INSTALL_PATH}/sbin/nginx /usr/sbin/nginx
sudo tee /etc/systemd/system/nginx.service <<EOF
[Unit]
Description=The nginx HTTP and reverse proxy server
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/var/run/nginx.pid
ExecStartPre=/usr/sbin/nginx -t
ExecStart=/usr/sbin/nginx
ExecReload=/bin/kill -s HUP \$MAINPID
ExecStop=/bin/kill -s QUIT \$MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# 启动 Nginx
sudo systemctl daemon-reload
sudo systemctl start nginx
sudo systemctl enable nginx

echo "Nginx with HTTP and Stream Upstream Hash modules installed successfully!"