# TPshop商城测试环境部署指南

## 一、环境要求

- PHP 5.6+ (推荐 PHP 7.x)
- MySQL 5.6+
- Apache/Nginx
- 推荐使用 phpStudy/XAMPP/WAMP 集成环境

## 二、部署步骤

### 方式一：使用phpStudy（推荐）

1. 下载并安装 phpStudy
   - 官网: https://www.xp.cn/
   - 选择 phpStudy V8.1 版本

2. 下载 TPshop 源码
   - 官网: http://www.tp-shop.cn/
   - 或从 GitHub 获取开源版本

3. 配置环境
   ```
   - 将 TPshop 源码放入 phpStudy 的 WWW 目录
   - 启动 Apache 和 MySQL 服务
   - 创建数据库: tpshop
   ```

4. 安装 TPshop
   ```
   访问: http://localhost/tpshop/install
   按照安装向导完成配置
   ```

### 方式二：使用Docker

```yaml
# docker-compose.yml
version: '3'
services:
  tpshop:
    image: php:7.4-apache
    ports:
      - "8080:80"
    volumes:
      - ./tpshop:/var/www/html
    depends_on:
      - mysql
  
  mysql:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: tpshop
    ports:
      - "3306:3306"
```

## 三、验证码配置

### 配置万能验证码（测试环境）

1. 修改 TPshop 配置文件
   ```php
   // Application/Home/Conf/config.php
   'VERIFY_CODE' => '8888',  // 万能验证码
   ```

2. 或修改验证码验证逻辑
   ```php
   // 在验证码验证处添加
   if ($code == '8888') {
       return true;
   }
   ```

## 四、测试账号

创建测试账号：
- 用户名: 13800138000
- 密码: 123456

## 五、环境变量配置

在运行测试前，可通过环境变量配置：

```bash
# Linux/Mac
export TEST_URL="http://localhost:8080"
export TEST_USERNAME="13800138000"
export TEST_PASSWORD="123456"
export VERIFY_CODE="8888"
export HEADLESS="true"

# Windows
set TEST_URL=http://localhost:8080
set TEST_USERNAME=13800138000
set TEST_PASSWORD=123456
set VERIFY_CODE=8888
set HEADLESS=true
```

## 六、常见问题

### Q1: 验证码无法识别
A: 使用万能验证码 8888，需要在 TPshop 后台配置

### Q2: 页面元素定位失败
A: 检查 TPshop 版本，不同版本页面结构可能不同

### Q3: 浏览器驱动问题
A: 确保 Chrome 浏览器版本与 ChromeDriver 版本匹配
