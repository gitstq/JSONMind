<div align="center">

# 🧠 JSONMind

**Lightweight JSON Data Intelligence Processing & Visualization Engine**

**轻量级JSON数据智能处理与可视化引擎**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey.svg)](https://github.com/gitstq/JSONMind)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen.svg)]()
[![Code Size](https://img.shields.io/badge/Code%20Size-<50KB-orange.svg)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🎉 Introduction

**JSONMind** is a powerful yet lightweight CLI tool designed for developers who work with JSON data daily. It provides a comprehensive suite of features for JSON validation, transformation, querying, and visualization — all with **zero dependencies** and a single Python file.

### Why JSONMind?

- 🚀 **Zero Dependencies**: Uses only Python standard library
- 📦 **Single File**: Just one `.py` file, easy to integrate anywhere
- ⚡ **Lightning Fast**: Optimized for performance with large JSON files
- 🎯 **Developer-Friendly**: Intuitive CLI with helpful error messages
- 🌐 **Cross-Platform**: Works on Windows, macOS, and Linux

---

## ✨ Core Features

| Feature | Description | Command |
|---------|-------------|---------|
| ✅ **Validation** | Validate JSON syntax with detailed error reporting | `jsonmind validate file.json` |
| 📊 **Statistics** | Comprehensive analysis of JSON structure | `jsonmind stats file.json` |
| 🔍 **Query** | JSONPath-like query support | `jsonmind query file.json '$.users[*].name'` |
| 🔄 **Flatten** | Convert nested JSON to flat structure | `jsonmind flatten file.json` |
| 🌳 **Tree View** | ASCII tree visualization | `jsonmind tree file.json` |
| 📄 **CSV Export** | Convert JSON arrays to CSV | `jsonmind csv file.json -o out.csv` |
| 🌐 **HTML Export** | Generate HTML tables from JSON | `jsonmind html file.json -o out.html` |
| 📋 **XML Export** | Convert JSON to XML format | `jsonmind xml file.json -o out.xml` |
| 🔍 **Diff** | Compare two JSON files | `jsonmind diff file1.json file2.json` |
| 🎨 **Format** | Pretty print with customizable indentation | `jsonmind format file.json` |

---

## 🚀 Quick Start

### Installation

#### Option 1: Direct Download
```bash
# Download the single file
curl -O https://raw.githubusercontent.com/gitstq/JSONMind/main/jsonmind.py

# Make it executable
chmod +x jsonmind.py

# Run directly
python3 jsonmind.py --help
```

#### Option 2: Clone Repository
```bash
git clone https://github.com/gitstq/JSONMind.git
cd JSONMind
python3 jsonmind.py --help
```

#### Option 3: Install via pip (coming soon)
```bash
pip install jsonmind
```

### Requirements
- **Python 3.7** or higher
- **Zero external dependencies**

---

## 📖 Usage Guide

### 1. Validate JSON
```bash
# Basic validation
python3 jsonmind.py validate data.json

# Verbose mode with statistics
python3 jsonmind.py validate data.json -v
```

### 2. Get Statistics
```bash
python3 jsonmind.py stats data.json

# JSON output format
python3 jsonmind.py stats data.json -f json
```

**Sample Output:**
```
📊 JSON Statistics
==================================================
📦 Total Size: 1,251 bytes
🔑 Total Keys: 54
📁 Objects: 14
📋 Arrays: 6
📝 Strings: 37
🔢 Numbers: 15
📏 Max Depth: 4
```

### 3. Query JSON Data
```bash
# Query specific path
python3 jsonmind.py query data.json '$.users[0].name'

# Wildcard query
python3 jsonmind.py query data.json '$.users[*].email'

# Recursive search
python3 jsonmind.py query data.json '$..price'
```

### 4. Visualize as Tree
```bash
python3 jsonmind.py tree data.json

# Limit depth
python3 jsonmind.py tree data.json -d 3
```

**Sample Output:**
```
└── company
│   ├── TechCorp International (str)
└── employees
│   ├── [0]
│   │   ├── id
│   │   │   ├── 1 (int)
│   │   ├── name
│   │   │   ├── Alice Johnson (str)
```

### 5. Convert Formats
```bash
# JSON to CSV
python3 jsonmind.py csv data.json -o output.csv

# JSON to HTML table
python3 jsonmind.py html data.json -o output.html -t "My Data"

# JSON to XML
python3 jsonmind.py xml data.json -o output.xml
```

### 6. Compare JSON Files
```bash
python3 jsonmind.py diff file1.json file2.json

# JSON output format
python3 jsonmind.py diff file1.json file2.json -f json
```

---

## 💡 Design Philosophy

JSONMind was built with the following principles:

1. **Simplicity**: No complex configuration, just works out of the box
2. **Performance**: Handles large JSON files efficiently
3. **Portability**: Single file, no dependencies, runs anywhere
4. **Extensibility**: Clean architecture for easy feature additions

---

## 📦 Packaging & Distribution

### Create Standalone Executable

#### Using PyInstaller
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile jsonmind.py

# Executable will be in dist/jsonmind
```

#### Using Nuitka (better performance)
```bash
# Install Nuitka
pip install nuitka

# Compile to binary
python -m nuitka --standalone --onefile jsonmind.py
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone the repo
git clone https://github.com/gitstq/JSONMind.git
cd JSONMind

# Run tests
python3 test_jsonmind.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🎉 项目介绍

**JSONMind** 是一款强大而轻量级的CLI工具，专为日常处理JSON数据的开发者设计。它提供了一套完整的功能，用于JSON验证、转换、查询和可视化 —— **零依赖**，仅需单个Python文件。

### 为什么选择JSONMind？

- 🚀 **零依赖**: 仅使用Python标准库
- 📦 **单文件**: 只有一个`.py`文件，易于集成到任何地方
- ⚡ **极速**: 针对大型JSON文件进行了性能优化
- 🎯 **开发者友好**: 直观的CLI界面，提供有用的错误提示
- 🌐 **跨平台**: 支持Windows、macOS和Linux

---

## ✨ 核心特性

| 特性 | 描述 | 命令 |
|---------|-------------|---------|
| ✅ **验证** | 验证JSON语法并提供详细错误报告 | `jsonmind validate file.json` |
| 📊 **统计** | 全面分析JSON结构 | `jsonmind stats file.json` |
| 🔍 **查询** | 支持JSONPath风格查询 | `jsonmind query file.json '$.users[*].name'` |
| 🔄 **扁平化** | 将嵌套JSON转换为扁平结构 | `jsonmind flatten file.json` |
| 🌳 **树形视图** | ASCII树形可视化 | `jsonmind tree file.json` |
| 📄 **CSV导出** | 将JSON数组转换为CSV | `jsonmind csv file.json -o out.csv` |
| 🌐 **HTML导出** | 从JSON生成HTML表格 | `jsonmind html file.json -o out.html` |
| 📋 **XML导出** | 将JSON转换为XML格式 | `jsonmind xml file.json -o out.xml` |
| 🔍 **差异对比** | 比较两个JSON文件 | `jsonmind diff file1.json file2.json` |
| 🎨 **格式化** | 美化打印，支持自定义缩进 | `jsonmind format file.json` |

---

## 🚀 快速开始

### 安装

#### 方式1: 直接下载
```bash
# 下载单文件
curl -O https://raw.githubusercontent.com/gitstq/JSONMind/main/jsonmind.py

# 添加执行权限
chmod +x jsonmind.py

# 直接运行
python3 jsonmind.py --help
```

#### 方式2: 克隆仓库
```bash
git clone https://github.com/gitstq/JSONMind.git
cd JSONMind
python3 jsonmind.py --help
```

#### 方式3: 通过pip安装（即将推出）
```bash
pip install jsonmind
```

### 环境要求
- **Python 3.7** 或更高版本
- **零外部依赖**

---

## 📖 使用指南

### 1. 验证JSON
```bash
# 基础验证
python3 jsonmind.py validate data.json

# 详细模式（含统计信息）
python3 jsonmind.py validate data.json -v
```

### 2. 获取统计信息
```bash
python3 jsonmind.py stats data.json

# JSON格式输出
python3 jsonmind.py stats data.json -f json
```

**示例输出：**
```
📊 JSON统计信息
==================================================
📦 总大小: 1,251 字节
🔑 总键数: 54
📁 对象数: 14
📋 数组数: 6
📝 字符串: 37
🔢 数字: 15
📏 最大深度: 4
```

### 3. 查询JSON数据
```bash
# 查询特定路径
python3 jsonmind.py query data.json '$.users[0].name'

# 通配符查询
python3 jsonmind.py query data.json '$.users[*].email'

# 递归搜索
python3 jsonmind.py query data.json '$..price'
```

### 4. 树形可视化
```bash
python3 jsonmind.py tree data.json

# 限制深度
python3 jsonmind.py tree data.json -d 3
```

### 5. 格式转换
```bash
# JSON转CSV
python3 jsonmind.py csv data.json -o output.csv

# JSON转HTML表格
python3 jsonmind.py html data.json -o output.html -t "我的数据"

# JSON转XML
python3 jsonmind.py xml data.json -o output.xml
```

### 6. 比较JSON文件
```bash
python3 jsonmind.py diff file1.json file2.json

# JSON格式输出
python3 jsonmind.py diff file1.json file2.json -f json
```

---

## 💡 设计理念

JSONMind遵循以下设计原则：

1. **简洁性**: 无需复杂配置，开箱即用
2. **性能**: 高效处理大型JSON文件
3. **可移植性**: 单文件，无依赖，随处运行
4. **可扩展性**: 清晰的架构，便于添加新功能

---

## 📦 打包与分发

### 创建独立可执行文件

#### 使用PyInstaller
```bash
# 安装PyInstaller
pip install pyinstaller

# 创建可执行文件
pyinstaller --onefile jsonmind.py

# 可执行文件位于 dist/jsonmind
```

---

## 🤝 贡献指南

我们欢迎贡献！请查看我们的[贡献指南](CONTRIBUTING.md)了解详情。

### 开发环境设置
```bash
# 克隆仓库
git clone https://github.com/gitstq/JSONMind.git
cd JSONMind

# 运行测试
python3 test_jsonmind.py
```

---

## 📄 开源协议

本项目采用MIT协议开源 - 详见[LICENSE](LICENSE)文件。

---

<a name="繁體中文"></a>
## 🎉 專案介紹

**JSONMind** 是一款強大且輕量級的CLI工具，專為日常處理JSON資料的開發者設計。它提供了一套完整的功能，用於JSON驗證、轉換、查詢和視覺化 —— **零依賴**，僅需單個Python檔案。

### 為什麼選擇JSONMind？

- 🚀 **零依賴**: 僅使用Python標準庫
- 📦 **單檔案**: 只有一個`.py`檔案，易於整合到任何地方
- ⚡ **極速**: 針對大型JSON檔案進行效能最佳化
- 🎯 **開發者友善**: 直觀的CLI介面，提供有用的錯誤提示
- 🌐 **跨平台**: 支援Windows、macOS和Linux

---

## ✨ 核心特性

| 特性 | 描述 | 指令 |
|---------|-------------|---------|
| ✅ **驗證** | 驗證JSON語法並提供詳細錯誤報告 | `jsonmind validate file.json` |
| 📊 **統計** | 全面分析JSON結構 | `jsonmind stats file.json` |
| 🔍 **查詢** | 支援JSONPath風格查詢 | `jsonmind query file.json '$.users[*].name'` |
| 🔄 **扁平化** | 將巢狀JSON轉換為扁平結構 | `jsonmind flatten file.json` |
| 🌳 **樹形檢視** | ASCII樹形視覺化 | `jsonmind tree file.json` |
| 📄 **CSV匯出** | 將JSON陣列轉換為CSV | `jsonmind csv file.json -o out.csv` |
| 🌐 **HTML匯出** | 從JSON生成HTML表格 | `jsonmind html file.json -o out.html` |
| 📋 **XML匯出** | 將JSON轉換為XML格式 | `jsonmind xml file.json -o out.xml` |
| 🔍 **差異比對** | 比較兩個JSON檔案 | `jsonmind diff file1.json file2.json` |
| 🎨 **格式化** | 美化列印，支援自訂縮排 | `jsonmind format file.json` |

---

## 🚀 快速開始

### 安裝

#### 方式1: 直接下載
```bash
# 下載單檔案
curl -O https://raw.githubusercontent.com/gitstq/JSONMind/main/jsonmind.py

# 新增執行權限
chmod +x jsonmind.py

# 直接執行
python3 jsonmind.py --help
```

#### 方式2: 克隆倉庫
```bash
git clone https://github.com/gitstq/JSONMind.git
cd JSONMind
python3 jsonmind.py --help
```

#### 方式3: 透過pip安裝（即將推出）
```bash
pip install jsonmind
```

### 環境要求
- **Python 3.7** 或更高版本
- **零外部依賴**

---

## 📖 使用指南

### 1. 驗證JSON
```bash
# 基礎驗證
python3 jsonmind.py validate data.json

# 詳細模式（含統計資訊）
python3 jsonmind.py validate data.json -v
```

### 2. 取得統計資訊
```bash
python3 jsonmind.py stats data.json

# JSON格式輸出
python3 jsonmind.py stats data.json -f json
```

**範例輸出：**
```
📊 JSON統計資訊
==================================================
📦 總大小: 1,251 位元組
🔑 總鍵數: 54
📁 物件數: 14
📋 陣列數: 6
📝 字串: 37
🔢 數字: 15
📏 最大深度: 4
```

### 3. 查詢JSON資料
```bash
# 查詢特定路徑
python3 jsonmind.py query data.json '$.users[0].name'

# 萬用字元查詢
python3 jsonmind.py query data.json '$.users[*].email'

# 遞迴搜尋
python3 jsonmind.py query data.json '$..price'
```

### 4. 樹形視覺化
```bash
python3 jsonmind.py tree data.json

# 限制深度
python3 jsonmind.py tree data.json -d 3
```

### 5. 格式轉換
```bash
# JSON轉CSV
python3 jsonmind.py csv data.json -o output.csv

# JSON轉HTML表格
python3 jsonmind.py html data.json -o output.html -t "我的資料"

# JSON轉XML
python3 jsonmind.py xml data.json -o output.xml
```

### 6. 比較JSON檔案
```bash
python3 jsonmind.py diff file1.json file2.json

# JSON格式輸出
python3 jsonmind.py diff file1.json file2.json -f json
```

---

## 💡 設計理念

JSONMind遵循以下設計原則：

1. **簡潔性**: 無需複雜配置，開箱即用
2. **效能**: 高效處理大型JSON檔案
3. **可攜性**: 單檔案，無依賴，隨處執行
4. **可擴充性**: 清晰的架構，便於新增新功能

---

## 📦 打包與分發

### 建立獨立可執行檔

#### 使用PyInstaller
```bash
# 安裝PyInstaller
pip install pyinstaller

# 建立可執行檔
pyinstaller --onefile jsonmind.py

# 可執行檔位於 dist/jsonmind
```

---

## 🤝 貢獻指南

我們歡迎貢獻！請查看我們的[貢獻指南](CONTRIBUTING.md)了解詳情。

### 開發環境設定
```bash
# 克隆倉庫
git clone https://github.com/gitstq/JSONMind.git
cd JSONMind

# 執行測試
python3 test_jsonmind.py
```

---

## 📄 開源協議

本專案採用MIT協議開源 - 詳見[LICENSE](LICENSE)檔案。

---

<div align="center">

**Made with ❤️ by the JSONMind Team**

⭐ Star us on GitHub if you find this project helpful!

</div>
