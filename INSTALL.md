# BAND Browser Manager - 安装指南

## 系统要求

| 项目 | 要求 | 说明 |
|------|------|------|
| 操作系统 | Windows 10+, macOS 10.14+, Linux | 跨平台支持 |
| Python | 3.7 或更高 | 建议使用 3.9+ |
| Chrome | 最新版本 | 自动检测安装位置 |
| 内存 | 4GB+ | 运行多个浏览器实例需要更多 |
| 磁盘空间 | 500MB | 仅用于应用和数据 |

## 安装步骤

### 方式 1：使用自动设置脚本（推荐）

#### Windows
```batch
# 1. 打开命令提示符（Win + R，输入 cmd）
# 2. 导航到项目目录
cd path\to\BAND1

# 3. 运行设置脚本
python setup.py

# 4. 运行应用
python main.py
```

#### macOS 和 Linux
```bash
# 1. 打开终端
# 2. 导航到项目目录
cd path/to/BAND1

# 3. 运行设置脚本
python3 setup.py

# 4. 运行应用
python3 main.py
```

### 方式 2：手动安装

#### 1. 克隆或下载项目
```bash
git clone https://github.com/YangXin1980/BAND1.git
cd BAND1
git checkout browser-manager-system
```

#### 2. 创建虚拟环境（可选但推荐）

**Windows**:
```batch
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 运行应用
```bash
python main.py
```

### 方式 3：使用独立 EXE（仅 Windows）

#### 构建 EXE
```bash
python build.py
```

#### 运行 EXE
完成后，在 `dist/` 文件夹中找到 `BAND-Browser-Manager.exe`

## 验证安装

### 检查 Python 版本
```bash
python --version  # Windows
python3 --version # macOS/Linux
```

### 检查依赖安装
```bash
pip list | grep -E "PyQt5|selenium|cryptography"
```

### 检查 Chrome 安装
```bash
# Windows: 应该在以下位置之一
# C:\Program Files\Google\Chrome\Application\chrome.exe
# C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
# C:\Users\Username\AppData\Local\Google\Chrome\Application\chrome.exe

# macOS:
# /Applications/Google Chrome.app/Contents/MacOS/Google Chrome

# Linux:
# /usr/bin/google-chrome
```

## 常见问题

### Q1: "Python 不是内部或外部命令"

**A**: Python 没有添加到 PATH 环境变量

**解决方案**:
1. 重新安装 Python，勾选 "Add Python to PATH"
2. 或使用完整路径：`C:\Python39\python.exe main.py`

### Q2: "ModuleNotFoundError: No module named 'PyQt5'"

**A**: 依赖未正确安装

**解决方案**:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Q3: "Chrome not found. Please install Google Chrome."

**A**: Chrome 未安装或位置不标准

**解决方案**:
1. 从 https://www.google.com/chrome/ 安装 Chrome
2. 重启应用

### Q4: "Permission denied" 错误

**A**: 文件权限问题

**解决方案**:
```bash
# Linux/macOS
chmod +x main.py setup.py build.py
```

### Q5: "Address already in use"

**A**: 端口被占用

**解决方案**:
1. 关闭所有 Chrome 实例
2. 等待 30 秒后重试
3. 重启应用

## 升级应用

### 更新代码
```bash
git pull origin browser-manager-system
```

### 更新依赖
```bash
pip install -r requirements.txt --upgrade
```

## 卸载应用

### 删除虚拟环境
```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

### 删除用户数据

**Windows**: 删除 `%LOCALAPPDATA%\BAND-Manager\`
**macOS**: 删除 `~/.band-manager/`
**Linux**: 删除 `~/.band-manager/`

## 获取帮助

### 查看日志
日志文件位于应用数据目录的 `logs/` 文件夹中

### 获取详细信息
在命令行运行时会显示详细的错误信息

### 报告问题
在 GitHub Issues 中提交 bug 报告，包括：
- 操作系统版本
- Python 版本
- 错误信息
- 日志文件内容

## 优化性能

### 减少内存使用
```json
{
  "chrome_instances": 2  // 减少同时打开的浏览器数
}
```

### 加快启动速度
1. 关闭自动翻译功能
2. 减少启动的账号数量
3. 禁用浏览器扩展

## 隐私和安全

### 数据安全
- ✅ 所有密码都经过 AES-256 加密
- ✅ 密钥存储在本机，不会上传
- ✅ 离线工作，无需网络连接（除了登录 BAND）

### 数据备份
```bash
# 导出所有账号（加密）
# 在应用中点击 "Export" 按钮
```

---

**安装完成后，即可开始使用 BAND Browser Manager！** 🎉
