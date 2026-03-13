#!/bin/bash
# TPshop 自动化测试 Docker 启动脚本
# 使用方式:
#   ./docker-run.sh [命令]
# 命令列表:
#   build    - 构建 Docker 镜像
#   start    - 启动 TPshop Web 服务
#   test     - 运行自动化测试
#   demo     - 运行演示模式
#   stop     - 停止所有服务
#   clean    - 清理 Docker 资源
#   logs     - 查看日志
#   help     - 显示帮助信息

set -e

PROJECT_NAME="tpshop-test"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

info() {
    echo -e "${GREEN}[INFO] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARN] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

show_help() {
    echo "TPshop 自动化测试 Docker 启动脚本"
    echo ""
    echo "使用方式: $0 [命令]"
    echo ""
    echo "命令列表:"
    echo "  build    - 构建 Docker 镜像"
    echo "  start    - 启动 TPshop Web 服务"
    echo "  test     - 运行自动化测试（需要 Web 服务已启动）"
    echo "  demo     - 运行演示模式（展示框架结构）"
    echo "  all      - 一键启动 Web 服务并运行测试"
    echo "  stop     - 停止所有服务"
    echo "  clean    - 清理 Docker 资源（镜像和容器）"
    echo "  logs     - 查看测试日志"
    echo "  help     - 显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 build      # 构建镜像"
    echo "  $0 start      # 启动 Web 服务"
    echo "  $0 test       # 运行测试"
    echo "  $0 all        # 启动服务并运行测试"
    echo "  $0 stop       # 停止服务"
}

build_image() {
    info "构建 Docker 镜像..."
    docker build -t ${PROJECT_NAME}:latest .
    info "镜像构建完成: ${PROJECT_NAME}:latest"
}

start_web() {
    info "启动 TPshop Web 服务..."
    docker compose up -d tpshop-web
    info "等待 Web 服务启动..."
    sleep 10
    info "TPshop Web 服务已启动，访问地址: http://localhost:8080"
}

run_test() {
    info "运行自动化测试..."
    # 确保报告目录存在
    mkdir -p backend/reports/screenshots
    docker compose run --rm tpshop-test
    info "测试完成，报告已生成在 backend/reports 目录下"
}

run_demo() {
    info "运行演示模式..."
    docker compose run --rm tpshop-demo
}

run_all() {
    info "一键启动 TPshop 服务并运行测试..."
    # 构建镜像
    build_image
    # 启动所有服务并运行测试
    mkdir -p backend/reports/screenshots
    docker compose up --abort-on-container-exit
    info "测试完成，报告已生成在 backend/reports 目录下"
}

stop_services() {
    info "停止所有服务..."
    docker compose down --remove-orphans
    info "服务已停止"
}

clean_resources() {
    warn "清理 Docker 资源..."
    docker compose down --rmi all --volumes --remove-orphans
    docker rmi -f ${PROJECT_NAME}:latest 2>/dev/null || true
    info "资源清理完成"
}

show_logs() {
    info "查看测试日志..."
    docker compose logs -f tpshop-test
}

# 主逻辑
case "${1:-help}" in
    build)
        build_image
        ;;
    start)
        start_web
        ;;
    test)
        run_test
        ;;
    demo)
        run_demo
        ;;
    all)
        run_all
        ;;
    stop)
        stop_services
        ;;
    clean)
        clean_resources
        ;;
    logs)
        show_logs
        ;;
    help)
        show_help
        ;;
    *)
        error "未知命令: $1"
        show_help
        exit 1
        ;;
esac
