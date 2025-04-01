import pandas as pd

# Excel 파일 읽기
try:
    df = pd.read_excel('입시결과.xlsx')
    print("엑셀 파일 읽기 성공")
    print(f"컬럼 목록: {df.columns.tolist()}")
    print(f"데이터 샘플:\n{df.head()}")
    
    # CSV 파일로 저장
    df.to_csv('excel_converted.csv', index=False, encoding='utf-8')
    print("CSV 파일로 변환 완료: excel_converted.csv")
except Exception as e:
    print(f"오류 발생: {e}")
