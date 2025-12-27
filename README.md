# Personal Toolkits

個人常用工具集，整合多個自動化工具以提升日常效率。

## 📦 專案概覽

本專案包含以下工具：

### 1. 📊 Expense Tracker（帳本自動化工具）

一個自動化處理帳本的 Python 工具，支援多人分帳並整合 Google Sheets。

**主要功能：**

- CSV 數據解析與清理
- 月度支出分組統計
- 多成員支出追蹤與分攤
- 自動上傳至 Google Sheets
- 年度統計報表生成

**技術堆疊：**

- Python 3.13+
- pandas 2.3.3
- gspread 6.2.1

📖 [查看詳細說明](./expense-trakcer/README.md)

### 2. 📥 PDF Downloader（PDF 下載工具）

一個簡單的 Node.js 命令列工具，用於下載 PDF 檔案並顯示下載進度。

**主要功能：**

- 從 URL 下載 PDF 檔案
- 即時顯示下載進度條
- 自動儲存至 Downloads 目錄
- 支援大檔案下載

**技術堆疊：**

- Node.js
- axios
- progress

**使用方式：**

```bash
node pdf-downloader.js <PDF_URL>
```

## 🚀 快速開始

### Expense Tracker

```bash
cd expense-trakcer
uv sync
python main.py
```

### PDF Downloader

```bash
npm install axios progress
node pdf-downloader.js https://example.com/file.pdf
```

## 📁 專案結構

```
toolkits/
├── expense-trakcer/      # 帳本自動化工具（Python）
│   ├── main.py
│   ├── parser.py
│   ├── uploader.py
│   ├── config.py
│   ├── pyproject.toml
│   ├── README.md
│   ├── credential/       # Google API 憑證
│   ├── rawdata/          # 原始 CSV 數據
│   └── temp/             # 暫存檔案
│
├── pdf-downloader.js     # PDF 下載工具（Node.js）
├── README.md             # 本檔案
└── .gitignore
```

## 🛠️ 環境需求

- **Python**: 3.13+（用於 Expense Tracker）
- **Node.js**: 14+（用於 PDF Downloader）
- **套件管理工具**: uv（Python）、npm（Node.js）

## 📝 授權

本專案為個人工具集，僅供參考使用。

## 📮 聯絡方式

如有問題或建議，歡迎提出 issue。
