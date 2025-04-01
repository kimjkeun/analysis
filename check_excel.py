import pandas as pd
import sys

# 출력 인코딩 설정
sys.stdout.reconfigure(encoding='utf-8')

try:
    # Excel 파일 읽기
    df = pd.read_excel('입시결과.xlsx')
    
    # 컬럼 정보 출력
    print("=== 컬럼 정보 ===")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")
    
    # 데이터 샘플 출력
    print("\n=== 데이터 샘플 (5행) ===")
    for i in range(min(5, len(df))):
        print(f"\n--- 행 {i} ---")
        for col in df.columns:
            print(f"{col}: {df.iloc[i][col]}")
    
    # CSV로 저장
    df.to_csv('excel_data.csv', index=False, encoding='utf-8-sig')
    print("\nCSV 파일로 변환 완료: excel_data.csv")
    
except Exception as e:
    print(f"오류 발생: {e}")
