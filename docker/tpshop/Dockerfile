# TPshop商城Docker镜像
FROM php:7.4-apache

# 安装必要的PHP扩展
RUN docker-php-ext-install mysqli pdo_mysql gd \
    && docker-php-ext-enable mysqli pdo_mysql gd

# 安装其他依赖
RUN apt-get update && apt-get install -y \
    unzip \
    wget \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# 重新配置GD扩展以支持JPEG和Freetype
RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) gd

# 启用Apache mod_rewrite
RUN a2enmod rewrite

# 下载TPshop源码（使用开源版本）
RUN wget -O /tmp/tpshop.zip "https://github.com/hnzyzwh/tpshop/archive/refs/heads/master.zip" \
    && unzip /tmp/tpshop.zip -d /tmp/ \
    && mv /tmp/tpshop-master/* /var/www/html/ \
    && rm -rf /tmp/tpshop.zip /tmp/tpshop-master

# 设置文件权限
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html \
    && chmod -R 777 /var/www/html/runtime \
    && chmod -R 777 /var/www/html/public/upload \
    && chmod -R 777 /var/www/html/vendor

# 复制配置文件
COPY config.php /var/www/html/application/config.php
COPY database.php /var/www/html/application/database.php

# 设置工作目录
WORKDIR /var/www/html

# 暴露端口
EXPOSE 80
