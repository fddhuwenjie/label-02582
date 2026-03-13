#!/bin/bash
# TPshop自动安装脚本

set -e

echo "开始配置TPshop..."

# 等待MySQL就绪
until mysql -h mysql -u root -proot -e "SELECT 1" >/dev/null 2>&1; do
    echo "等待MySQL启动..."
    sleep 2
done

echo "MySQL已就绪"

# 创建数据库（如果不存在）
mysql -h mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS tpshop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 导入数据库
if [ -f /tmp/tpshop.sql ]; then
    echo "导入数据库..."
    mysql -h mysql -u root -proot tpshop < /tmp/tpshop.sql
fi

echo "TPshop配置完成!"
