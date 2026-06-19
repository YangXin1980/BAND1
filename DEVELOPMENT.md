# BAND Browser Manager - 开发指南

## 项目概述

本项目是一个基于 Python 的企业级多账号管理系统，用于 BAND 应用的自动化和批量管理。

## 技术栈

| 组件 | 技术 | 版本 | 用途 |
|------|------|------|------|
| UI框架 | PyQt5 | 5.15+ | 跨平台图形界面 |
| 浏览器自动化 | Selenium | 4.15+ | Chrome 自动化和登录 |
| 加密库 | cryptography | 41.0+ | AES-256 加密存储 |
| 日志 | logging | 3.10+ | 系统日志记录 |

## 项目结构详解

### 配置模块 (config/)
```python
config/
├── __init__.py
└── settings.py          # 配置管理
    ├── Settings        # 配置类
    │   ├── get()      # 获取配置
    │   ├── set()      # 设置配置
    │   └── save()     # 保存配置
    └── settings        # 全局实例
```

### 核心模块 (core/)
```python
core/
├── __init__.py
├── encryption.py        # 加密
│   └── Encryption      # AES-256 加密类
│       ├── encrypt()   # 加密数据
│       └── decrypt()   # 解密数据
├── account_storage.py   # 账号存储
│   └── AccountStorage  # 账号管理类
│       ├── add_account()        # 添加账号
│       ├── get_all_accounts()   # 获取所有账号
│       ├── delete_account()     # 删除账号
│       ├── export_accounts()    # 导出账号
│       └── import_accounts()    # 导入账号
├── chrome_automation.py # Chrome 自动化
│   └── ChromeAutomation # Selenium 包装类
│       ├── create_driver()      # 创建驱动
│       ├── login()              # 自动登录
│       └── navigate_to()        # 页面导航
├─�� browser_manager.py   # 浏览器管理
│   └── BrowserManager  # 多浏览器管理类
│       ├── launch_browser_for_account()  # 单个启动
│       ├── launch_multiple_browsers()    # 批量启动
│       ├── close_browser()               # 关闭浏览器
│       └── arrange_windows()            # 排列窗口
└── window_manager.py    # 窗口管理
    └── WindowManager   # 窗口控制类
        ├── get_screen_info()            # 屏幕信息
        ├── calculate_window_positions() # 计算位置
        └── move_window()                # 移动窗口
```

### UI 模块 (ui/)
```python
ui/
├── __init__.py
├── main_window.py       # 主窗口
│   └── MainWindow       # 主应用窗口
├── account_manager.py   # 账号管理UI
│   ├── AccountManagerWidget   # 账号管理界面
│   └── AddAccountDialog       # 添加账号对话框
├── browser_launcher.py  # 浏览器启动UI
│   └── BrowserLauncherWidget  # 浏览器启动界面
└── styles.qss          # 样式表
```

### 工具模块 (utils/)
```python
utils/
├── __init__.py
├── logger.py            # 日志系统
│   └── Logger          # 日志类
│       ├── info()      # 信息日志
│       ├── error()     # 错误日志
│       └── debug()     # 调试日志
└── helpers.py           # 工具函数
    ├── get_data_dir()           # 数据目录
    ├── get_machine_id()         # 机器ID
    ├── find_chrome_executable() # 查找Chrome
    └── load/save_json()         # JSON操作
```

## 开发工作流

### 1. 环境设置

```bash
# 克隆仓库
git clone https://github.com/YangXin1980/BAND1.git
cd BAND1
git checkout browser-manager-system

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 安装开发依赖
pip install -r requirements.txt
pip install pytest pytest-cov black flake8  # 开发工具
```

### 2. 编码规范

#### PEP 8 风格指南
```python
# ✅ 好的例子
def add_account(email: str, password: str) -> tuple:
    """Add new BAND account.
    
    Args:
        email: BAND account email
        password: Account password
    
    Returns:
        (success, message) tuple
    """
    pass

# ❌ 不好的例子
def addaccount(e,p):
    pass
```

#### 文档字符串
```python
class MyClass:
    """Brief description.
    
    Detailed description if needed.
    
    Attributes:
        attr1: Description
        attr2: Description
    """
    
    def my_method(self):
        """Method description.
        
        Returns:
            Description
        """
        pass
```

### 3. 测试

```bash
# 运行所有测试
pytest

# 运行指定测试
pytest tests/test_encryption.py

# 生成覆盖率报告
pytest --cov=core --cov=ui
```

### 4. 代码质量

```bash
# 代码格式化
black .

# 代码检查
flake8 .

# 类型检查
mypy .
```

## 扩展指南

### 添加新的账号字段

1. 修改 `core/account_storage.py`
```python
def add_account(self, email, password, name=None, **kwargs):
    account = {
        'id': len(self.accounts) + 1,
        'email': email,
        'password': encryption.encrypt(password),
        'name': name,
        'custom_field': kwargs.get('custom_field', ''),  # 新字段
        # ...
    }
```

2. 修改 `ui/account_manager.py`
```python
class AddAccountDialog(QDialog):
    def init_ui(self):
        # 添加新输入字段
        self.custom_input = QLineEdit()
        # ...
```

### 添加新的自动化功能

1. 继承 `ChromeAutomation`
```python
class CustomAutomation(ChromeAutomation):
    def my_custom_action(self):
        """Custom automation action."""
        # Your code here
        pass
```

2. 在 `browser_manager.py` 中使用
```python
def launch_browser_for_account(self, account_id, ...):
    chrome_auto = CustomAutomation()
    # ...
```

### 添加新的界面

1. 创建新的 QWidget 类
```python
class NewFeatureWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        # UI 代码
        pass
```

2. 添加到主窗口的标签页
```python
class MainWindow(QMainWindow):
    def init_ui(self):
        self.new_widget = NewFeatureWidget()
        self.tabs.addTab(self.new_widget, "🎯 New Feature")
```

## 调试技巧

### 启用调试模式
```python
# main.py
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    main()
```

### 查看日志
```bash
# 实时查看日志
tail -f logs/20260619.log  # macOS/Linux
Get-Content -Wait logs\20260619.log  # Windows
```

### 使用调试器
```python
import pdb

# 在代码中添加断点
pdb.set_trace()

# 或使用 VS Code 调试
# 创建 .vscode/launch.json
```

## 性能优化

### 优化加密性能
```python
# 缓存加密实例
encryption = Encryption()  # 全局使n例

# 批量加密
encrypted_passwords = [encryption.encrypt(pwd) for pwd in passwords]
```

### 优化浏览器启动
```python
# 并行启动多个浏览器
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(launch_browser, acc) for acc in accounts]
```

## 部署

### 构建 Windows EXE
```bash
python build.py
```

### 构建 macOS DMG
```bash
# 使用 py2app
pip install py2app
py2app
```

### 构建 Linux AppImage
```bash
# 使用 AppImage
pip install appimage-builder
appimage-builder --skip-tests
```

## 常见陷阱

### 1. 密码加密密钥
❌ **错误**: 硬编码密钥
```python
key = "my-secret-key"  # 不安全
```

✅ **正确**: 使用机器ID
```python
key = get_machine_id()  # 从 helpers.py
```

### 2. 资源文件引用
❌ **错误**: 相对路径
```python
with open("styles.qss") as f:  # 可能失败
```

✅ **正确**: 使用 __file__
```python
style_file = os.path.join(os.path.dirname(__file__), 'styles.qss')
```

### 3. 线程管理
❌ **错误**: 在 UI 线程中进行长操作
```python
def launch_browser(self):
    # 会冻结 UI
    browser_manager.launch_multiple_browsers(accounts)
```

✅ **正确**: 使用工作线程
```python
from PyQt5.QtCore import QThread

class LaunchThread(QThread):
    def run(self):
        browser_manager.launch_multiple_browsers(accounts)
```

## 贡献指南

### Pull Request 流程

1. Fork 项目
2. 创建功能分支: `git checkout -b feature/amazing-feature`
3. 提交更改: `git commit -m 'Add amazing feature'`
4. 推送分支: `git push origin feature/amazing-feature`
5. 开启 Pull Request

### 提交信息规范
```
[type] Brief description (50 chars)

Detailed explanation (wrap at 72 chars)

- 具体改动 1
- 具体改动 2

Fixes #123
```

类型: feat, fix, docs, style, refactor, perf, test

---

**祝您开发愉快！** 🚀
