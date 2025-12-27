"""
主程式：串接 CSV 解析與 Google Sheets 上傳流程
"""
from parser import FinanceDataParser
from uploader import GoogleSheetsUploader


def main():
    """執行完整的家庭帳本自動化流程"""
    
    print("=" * 50)
    print("家庭帳本自動化處理系統")
    print("=" * 50)
    
    # 步驟 1: 解析 CSV 數據
    print("\n[步驟 1] 開始解析 CSV 數據...")
    parser = FinanceDataParser()
    parser.load_and_process()
    print(f"✓ 數據解析完成，共 {len(parser.df)} 筆記錄")
    print(f"✓ 識別成員: {', '.join(parser.get_members())}")
    
    # 步驟 2: 準備上傳器
    print("\n[步驟 2] 準備連接 Google Sheets...")
    uploader = GoogleSheetsUploader()
    uploader.authenticate()
    
    # 步驟 3: 按月上傳數據
    print("\n[步驟 3] 開始上傳月度數據...")
    monthly_data = parser.get_data_by_month()
    
    for month, month_df in monthly_data.items():
        tab_name = f"Data_{month}"
        print(f"\n處理 {month} 的數據 ({len(month_df)} 筆)...")
        uploader.upload_monthly_data(tab_name, month_df, parser.get_members())
    
    # # 步驟 4: 生成並上傳年度統計報表
    print("\n[步驟 4] 生成年度統計報表...")
    annual_report = parser.generate_annual_report()
    print(f"✓ 年度報表生成完成")
    
    print("\n上傳年度統計報表到 Google Sheets...")
    uploader.upload_annual_report(annual_report, tab_name="Annual_Expense_Report")
    
    print("\n" + "=" * 50)
    print("✓ 所有處理完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
