#!/bin/bash
# Docker测试运行脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "========================================"
echo "自动化测试框架 Docker 运行脚本"
echo "========================================"

usage() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --demo              演示模式 (默认)"
    echo "  --test              运行测试 (需要配置商城地址)"
    echo "  --pytest            运行pytest测试"
    echo "  --ddt               运行DDT测试"
    echo "  --full              启动完整环境（TPshop + 测试）"
    echo "  --build             只构建镜像"
    echo "  --clean             清理Docker资源"
    echo "  --help              显示帮助信息"
    echo ""
    echo "环境变量:"
    echo "  TEST_URL            商城地址 (默认: http://localhost:8080)"
    echo "  TEST_USERNAME       测试用户名 (默认: 13800138000)"
    echo "  TEST_PASSWORD       测试密码 (默认: 123456)"
    echo "  VERIFY_CODE         验证码 (默认: 8888)"
    echo "  SHOP_TYPE           商城类型 (默认: tpshop)"
    echo ""
    echo "示例:"
    echo "  $0 --demo"
    echo "  TEST_URL=http://your-shop-url $0 --test"
    echo "  $0 --full"
    exit 1
}

build_image() {
    echo "构建 Docker 镜像..."
    cd "$PROJECT_ROOT"
    docker build -t test-framework:latest .
}

cleanup() {
    echo "清理 Docker 资源..."
    cd "$PROJECT_ROOT"
    docker compose down -v --remove-orphans
    docker rmi -f test-framework:latest 2>/dev/null || true
}

run_demo() {
    echo "运行演示模式..."
    docker run --rm test-framework:latest --demo
}

run_test() {
    echo "运行测试..."
    local test_url=${TEST_URL:-"http://localhost:8080"}
    local username=${TEST_USERNAME:-"13800138000"}
    local password=${TEST_PASSWORD:-"123456"}
    local verify_code=${VERIFY_CODE:-"8888"}
    local shop_type=${SHOP_TYPE:-"tpshop"}
    
    echo "商城地址: $test_url"
    echo "商城类型: $shop_type"
    
    docker run --rm \
        --network host \
        -e TEST_URL="$test_url" \
        -e TEST_USERNAME="$username" \
        -e TEST_PASSWORD="$password" \
        -e VERIFY_CODE="$verify_code" \
        -e SHOP_TYPE="$shop_type" \
        -e HEADLESS=true \
        -v "$PROJECT_ROOT/backend/reports:/app/reports" \
        test-framework:latest --test
}

run_pytest() {
    echo "运行 pytest 测试..."
    local test_url=${TEST_URL:-"http://localhost:8080"}
    
    docker run --rm \
        --network host \
        -e TEST_URL="$test_url" \
        -e HEADLESS=true \
        -v "$PROJECT_ROOT/backend/reports:/app/reports" \
        test-framework:latest -m pytest tests/test_login.py -v --html=reports/test_report.html
}

run_ddt() {
    echo "运行 DDT 测试..."
    local test_url=${TEST_URL:-"http://localhost:8080"}
    
    docker run --rm \
        --network host \
        -e TEST_URL="$test_url" \
        -e HEADLESS=true \
        -v "$PROJECT_ROOT/backend/reports:/app/reports" \
        test-framework:latest -m pytest tests/test_login_ddt.py -v
}

run_full_env() {
    echo "启动完整测试环境（TPshop + 测试框架）..."
    cd "$PROJECT_ROOT"
    
    echo "注意：完整环境需要手动部署TPshop源码到容器中"
    echo "请参考文档进行TPshop的安装配置"
    echo ""
    
    docker compose --profile with-tpshop up -d
    
    echo ""
    echo "服务启动中..."
    echo "TPshop: http://localhost:8080"
    echo "phpMyAdmin: http://localhost:8081"
    echo ""
    echo "等待MySQL启动..."
    sleep 10
    
    echo "请手动完成TPshop的安装:"
    echo "1. 访问 http://localhost:8080/install"
    echo "2. 数据库配置:"
    echo "   - 主机: mysql"
    echo "   - 数据库: tpshop"
    echo "   - 用户名: root"
    echo "   - 密码: root"
    echo ""
    echo "配置完成后，运行测试:"
    echo "TEST_URL=http://localhost:8080 $0 --test"
}

# 主逻辑
case "$1" in
    --help|-h)
        usage
        ;;
    --build)
        build_image
        ;;
    --clean)
        cleanup
        ;;
    --demo)
        build_image
        run_demo
        ;;
    --test)
        build_image
        run_test
        ;;
    --pytest)
        build_image
        run_pytest
        ;;
    --ddt)
        build_image
        run_ddt
        ;;
    --full)
        build_image
        run_full_env
        ;;
    *)
        build_image
        run_demo
        ;;
esac

echo ""
echo "操作完成!"
