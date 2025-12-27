# 帳本自動化工具 (Expense Tracker)

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![pandas](https://img.shields.io/badge/pandas-2.3.3-green.svg)](https://pandas.pydata.org/)
[![gspread](https://img.shields.io/badge/gspread-6.2.1-orange.svg)](https://gspread.readthedocs.io/)
[![License](https://img.shields.io/badge/license-Personal-lightgrey.svg)]()

一個自動化處理帳本的 Python 工具，可以解析 CSV 格式的支出記錄，且支援多人分帳帳本，並自動上傳至 Google Sheets 進行管理與統計。

## 功能特色

- 📊 **CSV 數據解析**：自動讀取和清理帳本 CSV 檔案
- 📅 **月度分組**：按月份自動整理支出記錄
- 👥 **多成員支援**：支援多位成員的支出追蹤與分攤
- ☁️ **Google Sheets 整合**：自動上傳數據到 Google Sheets
- 📈 **年度統計報表**：自動生成年度支出統計與分析

## 專案結構

```
finance/
├── main.py              # 主程式入口
├── parser.py            # CSV 解析模組
├── uploader.py          # Google Sheets 上傳模組
├── config.py            # 配置文件
├── pyproject.toml       # Python 專案配置
├── credential/          # Google API 憑證存放目錄
├── rawdata/             # 原始 CSV 數據目錄
└── temp/                # 中間處理檔案輸出目錄
```

## 安裝與設定

### 1. 環境需求

- Python 3.13+
- uv 套件管理工具

### 2. 安裝相依套件

```bash
# 或使用 uv (推薦)
uv sync
```

### 3. Google Sheets API 設定

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用 Google Sheets API 和 Google Drive API
4. 建立服務帳號並下載 JSON 憑證檔
5. 將憑證檔放入 `credential/` 目錄
6. 在 `config.py` 中更新 `CREDENTIALS_JSON` 路徑

### 4. 配置設定

編輯 `config.py` 檔案：

```python
# Google Sheets 名稱
GOOGLE_SHEET_NAME = "你的帳本名稱"

# CSV 檔案路徑
CSV_FILE_PATH = "rawdata/Daily_2024年.csv"

# 憑證檔案路徑
CREDENTIALS_JSON = "credential/your-credentials.json"
```

## 使用方式

### 基本使用

```bash
python main.py
```

### 執行流程

程式會自動執行以下步驟：

1. 📖 讀取並解析 CSV 數據
2. 🔍 識別成員
3. 📊 按月份分組數據
4. ☁️ 上傳月度數據到 Google Sheets
5. 📈 生成並上傳年度統計報表

### CSV 格式要求

CSV 檔案應包含以下欄位：

- `日期`：格式如 "2024 年 1 月 1 日"
- `金額`：支出金額
- `匯率`：（選填）外幣匯率
- `成員名稱(類別)`：各成員的支出欄位，如 "小明(食)"

## 輸出說明

### Google Sheets 分頁

- `Data_YYYY-MM`：各月份的明細數據
- `Annual_Expense_Report`：年度統計報表

### 本地暫存檔（可選）

如果在 `config.py` 中啟用 `ENABLE_INTERMEDIATE_OUTPUT`：

- `temp/processed_data.csv`：處理後的完整數據
- `temp/monthly_YYYY-MM.csv`：各月份數據
- `temp/annual_report_YYYY.csv`：年度統計報表

## 配置選項

在 `config.py` 中可調整：

```python
# 啟用/停用中間檔案輸出
ENABLE_INTERMEDIATE_OUTPUT = True

# 啟用/停用年度報表輸出
ENABLE_ANNUAL_REPORT_OUTPUT = True

# 輸出目錄
OUTPUT_DIR = "temp"
```

## 注意事項

- 確保 Google Sheets 已與服務帳號共享編輯權限
- CSV 檔案需使用 UTF-8 編碼
- 日期格式需符合設定檔中的 `DATE_FORMAT`
- 首次執行前請確認 `credential/` 和 `rawdata/` 目錄存在

## 授權

本專案為個人工具，僅供參考使用。
