# BAND Browser Manager System

一个专业的 Python 多账号管理系统，专为 BAND 应用设计，具有 Chrome 自动化、账号加密存储和批量操作功能。

## ✨ 核心功能

### 📱 账号管理
- 🔐 **AES-256 加密存储** - 所有密码都经过军用级加密
- 📥 **导入/导出** - 轻松备份和恢复账号信息
- 📝 **快速编辑** - 快速修改账号信息
- 🗑️ **批量删除** - 管理多个账号

### 🌐 Chrome 自动化
- 🔓 **自动登录** - 使用保存的凭据自动登录 BAND
- 🖥️ **多实例支持** - 同时打开多个浏览器窗口
- 👤 **隔离配置文件** - 每个账号独立的浏览器配置
- 🌍 **保留翻译功能** - 保留 Google Chrome 翻译特性

### ⚙️ 高级功能
- 📊 **实时监控** - 监控所有浏览器实例状态
- 🎯 **自动排列窗口** - 智能排列浏览器窗口布局
- ⚡ **批量操作** - 一键启动多个账号
- 📋 **任务调度** - 支持定时启动
- 📝 **完整日志** - 详细的操作日志记录

## 🚀 快速开始

### 系统要求
- **操作系统**: Windows 10+, macOS 10.14+, 或 Linux
- **Python**: 3.7+
- **Chrome**: 最新版本（必需）
- **内存**: 至少 4GB
- **磁盘**: 至少 500MB

### 安装步骤

#### 1. 克隆仓库
```bash
git clone https://github.com/YangXin1980/BAND1.git
cd BAND1
git checkout browser-manager-system
```

#### 2. 安装依赖
```bash
# 使用 setup.py 自动设置
python setup.py

# 或手动安装
pip install -r requirements.txt
```

#### 3. 运行应用
```bash
python main.py
```

### 首次使用

#### 添加账号
1. 打开应用
2. 点击「📋 Account Manager」标签页
3. 点击「➕ Add Account」按钮
4. 输入 BAND 邮箱和密码
5. 点击「Save Account」

#### 启动浏览器
1. 切换到「🚀 Browser Launcher」标签页
2. 在「Select Accounts」中选择要打开的账号
3. 配置选项：
   - **Number of Instances**: 最多同时打开几个浏览器
   - **Auto-arrange windows**: 是否自动排列窗口
4. 点击「▶️ Launch Selected」或「▶️ Launch All」
5. 浏览器将自动打开并登录选定的账号

## 📁 项目结构

```
BAND-Browser-Manager/
├── main.py                      # 应用入口
├── setup.py                     # 初始化脚本
├── build.py                     # 打包脚本
├── requirements.txt             # Python 依赖
│
├── config/
│   ├── __init__.py
│   └── settings.py              # 配置管理
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py           # 主窗口
│   ├── account_manager.py       # 账号管理UI
│   ├── browser_launcher.py      # 浏览器启动UI
│   └── styles.qss               # 样式表
│
├── core/
│   ├── __init__.py
│   ├── encryption.py            # AES-256 加密
│   ├── account_storage.py       # 账号数据库
│   ├── browser_manager.py       # 浏览器管理
│   ├── chrome_automation.py     # Selenium 自动化
│   └── window_manager.py        # 窗口管理
│
├── utils/
│   ├── __init__.py
│   ├── logger.py                # 日志系统
│   └── helpers.py               # 工具函数
│
└── data/                        # 数据目录
    ├── logs/                    # 日志文件
    ├── chrome_profiles/         # Chrome 配置文件
    └── config.json              # 应用配置
```

## 🔐 安全性

### 加密保护
- ✅ 所有密码使用 **AES-256** 加密
- ✅ 加密密钥由本机 ID 派生（无法跨机器使用）
- ✅ 导出文件始终保持加密状态
- ✅ 没有明文密码存储

### 数据位置
数据存储在本机的应用数据目录：

**Windows**: `%LOCALAPPDATA%\BAND-Manager\`
**macOS**: `~/.band-manager/`
**Linux**: `~/.band-manager/`

## 🎯 使用场景

### 多账号管理
- 同时管理多个 BAND 账号
- 快速切换不同账号
- 独立的浏览器配置和 Cookie

### 批量操作
- 一键启动所有账号
- 批量导入/导出账号信息
- 统一管理账号列表

### 自动化工作流
- 自动登录所有账号
- 定时启动特定账号
- 完整的操作日志记录

## 🔧 高级配置

### 配置文件位置
应用配置保存在：`%LOCALAPPDATA%\BAND-Manager\config.json`

### 可配置项目
```json
{
  "chrome_instances": 2,           // 最多同时打开的浏览器数
  "auto_arrange_windows": true,    // 是否自动排列窗口
  "enable_translation": true,      // 是否启用翻译
  "auto_login": false,             // 是否自动登录
  "default_timeout": 30,           // 加载超时时间（秒）
  "window_width": 1200,            // 窗口宽度
  "window_height": 700             // 窗口高度
}
```

## 📦 打包成 EXE

### 构建独立可执行文件
```bash
python build.py
```

构建完成后，可执行文件位于：`dist/BAND-Browser-Manager.exe`

## 🐛 故障排查

### Chrome 未找到
```
ERROR: Chrome not found. Please install Google Chrome.
```
**解决方案**: 从 https://www.google.com/chrome/ 安装 Google Chrome

### 自动登录失败
```
WARNING: Auto-login failed, manual login required
```
**解决方案**:
1. 检查账号信息是否正确
2. BAND 可能需要验证（二次认证等）
3. 手动登录后，浏览器会记住会话

### 端口被占用
```
ERROR: Failed to create WebDriver
```
**解决方案**:
1. 关闭其他 Chrome 实例
2. 检查是否有其他程序占用端口
3. 重启应用

### 数据库锁定
```
ERROR: Failed to save accounts
```
**解决方案**:
1. 确保应用正常关闭
2. 检查是否有其他进程占用数据库文件
3. 删除 `config/accounts.db` 并重新启动

## 📚 开发文档

### 日志查看
日志文件位于：`logs/YYYYMMDD.log`

### 扩展功能
可以通过继承以下类来添加新功能：
- `core.encryption.Encryption` - 自定义加密
- `core.chrome_automation.ChromeAutomation` - 自定义自动化
- `core.browser_manager.BrowserManager` - 自定义浏览器管理

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 📞 支持

### 报告问题
- 在 GitHub Issues 中报告 bug
- 提供详细的错误信息和日志
- 说明操作系统和 Python 版本

### 功能请求
- 在 GitHub Discussions 中提出建议
- 详细描述需要的功能
- 解释为什么需要这个功能

## 🎉 致谢

感谢以下项目的贡献：
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro)
- [Selenium](https://www.selenium.dev/)
- [cryptography](https://cryptography.io/)

## 📈 路线图

### 已完成 ✅
- [x] 基础账号管理
- [x] Chrome 自动化登录
- [x] 账号加密存储
- [x] 批量操作
- [x] 窗口自动排列
- [x] 导入/导出功能
- [x] PyQt5 UI 界面

### 计划中 🚧
- [ ] 定时启动任务
- [ ] 邮件通知
- [ ] 云同步备份
- [ ] 更多浏览器支持（Firefox、Edge）
- [ ] 网页版管理界面
- [ ] 移动端配套应用

---

**祝您使用愉快！** 🎊
