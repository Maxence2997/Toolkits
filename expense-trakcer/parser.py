"""
CSV 解析模組：負責讀取和處理家庭帳本 CSV 數據
"""
import pandas as pd
import re
import os
from pathlib import Path
from config import (
    CSV_FILE_PATH, DATE_FORMAT, MONTH_FORMAT,
    ENABLE_INTERMEDIATE_OUTPUT, ENABLE_ANNUAL_REPORT_OUTPUT, OUTPUT_DIR,
    OUTPUT_FILENAME_PROCESSED, OUTPUT_FILENAME_MONTHLY, OUTPUT_FILENAME_ANNUAL_REPORT
)


class FinanceDataParser:
    """處理家庭帳本 CSV 檔案的解析與數據清理"""
    
    def __init__(self, file_path=CSV_FILE_PATH, save_intermediate=ENABLE_INTERMEDIATE_OUTPUT):
        self.file_path = file_path
        self.df = None
        self.members = []
        self.save_intermediate = save_intermediate
        self.save_annual_report = ENABLE_ANNUAL_REPORT_OUTPUT
        self.output_dir = OUTPUT_DIR
    
    def load_and_process(self):
        """
        載入並處理 CSV 數據
        
        Returns:
            pd.DataFrame: 處理後的數據框
        """
        df = pd.read_csv(self.file_path)
        df = df.dropna(how='all')
        
        # 處理日期與提取月份
        df['日期'] = df['日期'].apply(
            lambda x: str(x).replace('年', '/').replace('月', '/').replace('日', '') 
            if pd.notna(x) else ""
        )
        df['Month'] = pd.to_datetime(df['日期'], format=DATE_FORMAT).dt.strftime(MONTH_FORMAT)
        
        # 識別成員
        person_cols = [c for c in df.columns if '(' in c and ')' in c]
        self.members = sorted(list(set([re.sub(r'\s*\(.*\)', '', c) for c in person_cols])))
        
        # 數值預處理
        for col in ['金額', '匯率'] + person_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace(',', ''), 
                    errors='coerce'
                ).fillna(0)
        
        # 判斷交易類型：收入或支出
        df['交易類型'] = df['類別'].apply(lambda x: '收入' if str(x) == '收入' else '支出')
        
        # 成員欄位保持原始金額（不轉換成 TWD）
        for m in self.members:
            related = [c for c in person_cols if c.startswith(m)]
            df[m] = df[related].max(axis=1).astype(int)
        
        # 金額欄位換算成 TWD
        df['金額'] = (df['金額'] * df['匯率']).round().astype(int)
        
        keep_cols = ['日期', 'Month', '交易類型', '類別', '名稱', '金額', '幣別'] + self.members
        self.df = df[keep_cols]
        
        # 若啟用中間檔案輸出，儲存處理後的數據
        if self.save_intermediate:
            self.save_processed_data()
        
        return self.df
    
    def get_data_by_month(self):
        """
        按月份分組數據
        
        Returns:
            dict: {月份: DataFrame} 的字典
        """
        if self.df is None:
            self.load_and_process()
        
        return {month: month_df for month, month_df in self.df.groupby('Month')}
    
    def get_members(self):
        """
        獲取所有成員列表
        
        Returns:
            list: 成員名稱列表
        """
        if not self.members and self.df is None:
            self.load_and_process()
        return self.members
    
    def save_processed_data(self):
        """
        儲存處理後的完整數據到 CSV 檔案
        """
        if self.df is None:
            print("警告：尚未處理數據，無法儲存")
            return
        
        # 建立輸出目錄
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        # 儲存完整數據（移除千分位格式化）
        output_path = os.path.join(self.output_dir, OUTPUT_FILENAME_PROCESSED)
        self.df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"✓ 已儲存處理後的數據: {output_path} ({len(self.df)} 筆)")
    
    def save_monthly_data(self):
        """
        儲存按月分組的數據到個別 CSV 檔案
        """
        if self.df is None:
            self.load_and_process()
        
        # 建立輸出目錄
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        monthly_data = self.get_data_by_month()
        for month, month_df in monthly_data.items():
            filename = OUTPUT_FILENAME_MONTHLY.format(month=month)
            output_path = os.path.join(self.output_dir, filename)
            month_df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"✓ 已儲存 {month} 的數據: {output_path} ({len(month_df)} 筆)")
    
    def generate_annual_report(self, year=None):
        """
        生成年度收支統計報表（支出 + 收入）
        
        Args:
            year (str, optional): 年份，例如 '2024'。若不指定則從數據中自動提取
        
        Returns:
            pd.DataFrame: 年度統計報表
        """
        if self.df is None:
            self.load_and_process()
        
        # 提取年份
        if year is None:
            year = self.df['Month'].str[:4].unique()[0]
        
        # 分別取支出和收入數據
        expense_df = self.df[self.df['交易類型'] == '支出'].copy()
        income_df = self.df[self.df['交易類型'] == '收入'].copy()
        
        # 提取月份數字 (1-12)
        expense_df['月份數字'] = pd.to_datetime(expense_df['Month']).dt.month
        income_df['月份數字'] = pd.to_datetime(income_df['Month']).dt.month
        
        # 取得所有支出類別（排序，過濾掉 NaN）
        expense_categories = sorted([c for c in expense_df['類別'].unique() if pd.notna(c)])
        
        # 月份名稱
        months = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 
                  'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']
        
        # === 建立支出報表（類別為行，月份為列）===
        expense_rows = []
        
        # 第一行：Header
        header = ['類別/月份'] + months + ['年度總計']
        expense_rows.append(header)
        
        # 每個類別一行
        for category in expense_categories:
            row = [category]
            monthly_amounts = []
            for month_num in range(1, 13):
                amount = expense_df[
                    (expense_df['月份數字'] == month_num) & 
                    (expense_df['類別'] == category)
                ]['金額'].sum()
                monthly_amounts.append(int(amount))
            
            # 年度總計
            yearly_total = sum(monthly_amounts)
            row.extend(monthly_amounts)
            row.append(yearly_total)
            expense_rows.append(row)
        
        # 支出總計行
        total_row = ['總支出']
        for month_num in range(1, 13):
            total = expense_df[expense_df['月份數字'] == month_num]['金額'].sum()
            total_row.append(int(total))
        # 整年度支出總計
        grand_total = int(expense_df['金額'].sum())
        total_row.append(grand_total)
        expense_rows.append(total_row)
        
        # === 建立收入報表（使用名稱而非類別）===
        income_rows = []
        
        # 空行分隔
        income_rows.append([''] * len(header))
        income_rows.append([''] * len(header))
        
        # Header
        income_rows.append(header)
        
        # 取得所有收入名稱（排序，過濾掉 NaN）
        income_names = sorted([n for n in income_df['名稱'].unique() if pd.notna(n)])
        
        # 每個名稱一行
        for name in income_names:
            row = [name]
            monthly_amounts = []
            for month_num in range(1, 13):
                amount = income_df[
                    (income_df['月份數字'] == month_num) & 
                    (income_df['名稱'] == name)
                ]['金額'].sum()
                monthly_amounts.append(int(amount))
            
            # 年度總計
            yearly_total = sum(monthly_amounts)
            row.extend(monthly_amounts)
            row.append(yearly_total)
            income_rows.append(row)
        
        # 收入總計行
        total_row = ['總收入']
        for month_num in range(1, 13):
            total = income_df[income_df['月份數字'] == month_num]['金額'].sum()
            total_row.append(int(total))
        # 整年度收入總計
        grand_total = int(income_df['金額'].sum())
        total_row.append(grand_total)
        income_rows.append(total_row)
        
        # === 建立月度收支簡表（用於圖表，月份為行）===
        summary_rows = []
        
        # 空行分隔
        summary_rows.append([''] * len(header))
        summary_rows.append([''] * len(header))
        
        # Header
        summary_header = ['Month', '支出', '收入']
        summary_rows.append(summary_header)
        
        # 計算每月的支出和收入
        for month_num, month_name in enumerate(months, start=1):
            expense_total = int(expense_df[expense_df['月份數字'] == month_num]['金額'].sum())
            income_total = int(income_df[income_df['月份數字'] == month_num]['金額'].sum())
            summary_rows.append([month_name, expense_total, income_total])
        
        # 年度總計行
        year_expense_total = int(expense_df['金額'].sum())
        year_income_total = int(income_df['金額'].sum())
        summary_rows.append(['年度總計', year_expense_total, year_income_total])
        
        # === 合併支出、收入和簡表 ===
        all_rows = expense_rows + income_rows + summary_rows
        
        # 建立 DataFrame（不使用第一行作為 header）
        report_df = pd.DataFrame(all_rows)
        
        # 若啟用，儲存中間檔案
        if self.save_annual_report:
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)
            filename = OUTPUT_FILENAME_ANNUAL_REPORT.format(year=year)
            output_path = os.path.join(self.output_dir, filename)
            report_df.to_csv(output_path, index=False, header=False, encoding='utf-8-sig')
            print(f"✓ 已儲存年度統計報表: {output_path}")
        
        return report_df
