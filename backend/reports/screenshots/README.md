# 测试截图目录

此目录用于存放测试运行时自动生成的截图。

## 截图命名规则

- `{case_id}_before_login.png` - 登录前页面截图
- `{case_id}_after_login.png` - 登录后页面截图
- `{case_id}_error.png` - 错误情况截图

## 生成截图

运行测试时会自动生成截图：

```bash
pytest tests/test_login.py -v --html=reports/test_report.html
```

**注意**：需要配置真实的商城测试环境才能生成截图。
