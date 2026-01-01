"""
Google Sheets 上傳模組：負責將處理後的數據上傳到 Google Sheets
"""
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from config import CREDENTIALS_JSON, GOOGLE_SHEET_NAME


class GoogleSheetsUploader:
    """處理 Google Sheets 的數據上傳與格式化"""
    
    def __init__(self, credentials_file=CREDENTIALS_JSON, sheet_name=GOOGLE_SHEET_NAME):
        self.credentials_file = credentials_file
        self.sheet_name = sheet_name
        self.client = None
        self.sheet = None
    
    def authenticate(self):
        """
        認證並連接到 Google Sheets
        
        注意：需要解除註解並提供正確的憑證檔案
        """
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_file, scope
        )
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(self.sheet_name)
        
        print(f"認證 Google Sheets: {self.sheet_name}")
        print("(目前為 Placeholder，需要啟用認證代碼)")
    
    def upload_monthly_data(self, tab_name, month_df, members):
        """
        上傳月度數據到指定分頁，只上傳原始明細數據
        
        Args:
            tab_name (str): 分頁名稱
            month_df (pd.DataFrame): 月度數據
            members (list): 成員列表
        """
        print(f"準備上傳數據到分頁: {tab_name}")
        
        # 準備寫入內容
        content = self._build_content(month_df)
        
        # 儲存 content 供格式化使用
        self._current_content = content
        
        # 寫入 Google Sheet
        self._write_to_sheet(tab_name, content)
    
    def _build_content(self, month_df):
        """
        構建要上傳的內容結構，只包含原始數據
        
        Args:
            month_df (pd.DataFrame): 月度明細數據
            
        Returns:
            list: 二維列表格式的內容
        """
        # 移除 Month 欄位
        detail_df = month_df.drop(columns=['Month']).copy()
        
        # 格式化金額，添加幣別符號
        currency_symbols = {
            'TWD': 'NT$',
            'JPY': '¥',
            'USD': '$',
            'EUR': '€',
            'CNY': '¥'
        }
        
        # 格式化金額欄位（已經是 TWD，統一顯示 NT$）
        if '金額' in detail_df.columns:
            detail_df['金額'] = detail_df['金額'].apply(
                lambda x: f"NT${int(x):,}" if pd.notna(x) and x != 0 else ""
            )
        
        # Header
        content = [detail_df.columns.tolist()]
        
        # 轉換所有數值為 Python 原生類型
        for row in detail_df.values:
            converted_row = []
            for val in row:
                if pd.isna(val):
                    converted_row.append("")
                elif isinstance(val, (pd.Int64Dtype, int)):
                    converted_row.append(int(val))
                elif hasattr(val, 'item'):  # numpy/pandas 數值類型
                    converted_row.append(val.item())
                else:
                    converted_row.append(val)
            content.append(converted_row)
        
        return content
    
    def _write_to_sheet(self, tab_name, content):
        """
        將內容寫入 Google Sheet
        
        Args:
            tab_name (str): 分頁名稱
            content (list): 要寫入的內容
        """
        if self.sheet is None:
            print(f"  [模擬] 寫入分頁 '{tab_name}'，共 {len(content)} 行數據")
            return
        
        # 實際寫入邏輯 (解除認證後啟用)
        try:
            worksheet = self.sheet.worksheet(tab_name)
        except:
            worksheet = self.sheet.add_worksheet(title=tab_name, rows="1000", cols="20")
        
        worksheet.clear()
        worksheet.update('A1', content)
        
        # 格式優化 (選用)：將第一欄標題加粗
        # worksheet.format("A1:B1", {"textFormat": {"bold": True}})
        
        print(f"  成功上傳到分頁: {tab_name}")
    
    
    def upload_annual_report(self, report_df, tab_name="Annual_Report"):
        """
        上傳年度統計報表到 Google Sheets
        
        Args:
            report_df (pd.DataFrame): 年度統計報表（已包含 header）
            tab_name (str): 分頁名稱，預設為 "Annual_Report"
        """
        print(f"準備上傳年度統計報表到分頁: {tab_name}")
        
        # 建立內容（DataFrame 的值已經包含 header，不需要額外添加 columns）
        content = []
        
        # 轉換所有數值為 Python 原生類型
        for row in report_df.values:
            converted_row = []
            for val in row:
                if pd.isna(val):
                    converted_row.append("")
                elif isinstance(val, (pd.Int64Dtype, int)):
                    converted_row.append(int(val))
                elif hasattr(val, 'item'):  # numpy/pandas 數值類型
                    converted_row.append(val.item())
                else:
                    converted_row.append(val)
            content.append(converted_row)
        
        # 儲存 content 供格式化使用
        self._current_content = content
        
        # 寫入 Google Sheet
        self._write_to_sheet(tab_name, content)
    
    