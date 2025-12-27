"""
設定檔：集中管理所有配置參數
"""

# Google Sheets 相關設定
GOOGLE_SHEET_NAME = "帳本_2024_測試"
CREDENTIALS_JSON = "credential/finance-project-482013-2012ba8a6a8b.json"

# CSV 檔案路徑
CSV_FILE_PATH = "rawdata/Daily_2024年.csv"

# 日期格式
DATE_FORMAT = '%Y/%m/%d'
MONTH_FORMAT = '%Y-%m'

# 中間檔案輸出設定
ENABLE_INTERMEDIATE_OUTPUT = True  # 是否產生中間檔案
ENABLE_ANNUAL_REPORT_OUTPUT = True  # 是否產生年度統計報表中間檔
OUTPUT_DIR = "temp"  # 輸出目錄
OUTPUT_FILENAME_PROCESSED = "processed_data.csv"  # 處理後的完整數據
OUTPUT_FILENAME_MONTHLY = "monthly_{month}.csv"  # 按月分組的數據
OUTPUT_FILENAME_ANNUAL_REPORT = "annual_report_{year}.csv"  # 年度統計報表
