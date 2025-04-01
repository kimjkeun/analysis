import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import os

# 한글 폰트 설정
import matplotlib.font_manager as fm
import platform

# 운영체제별 기본 한글 폰트 설정
system = platform.system()
if system == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif system == 'Darwin':  # macOS
    plt.rc('font', family='AppleGothic')
else:  # Linux
    plt.rc('font', family='NanumGothic')
    
# 마이너스 기호 깨짐 방지
plt.rc('axes', unicode_minus=False)

# 결과 파일 읽기
file_path = '입시결과.xlsx'
df = pd.read_excel(file_path)

# 등급 구간 정의
grade_ranges = [
    (1.0, 1.5, "1.0-1.5등급"),
    (1.5, 2.0, "1.5-2.0등급"),
    (2.0, 2.5, "2.0-2.5등급"),
    (2.5, 3.0, "2.5-3.0등급"),
    (3.0, 3.5, "3.0-3.5등급"),
    (3.5, 4.0, "3.5-4.0등급"),
    (4.0, 4.5, "4.0-4.5등급"),
    (4.5, 5.0, "4.5-5.0등급"),
    (5.0, 5.5, "5.0-5.5등급"),
    (5.5, 6.0, "5.5-6.0등급"),
    (6.0, 9.0, "6.0등급 이상")
]

# 결과 저장 디렉토리 생성
output_dir = 'analysis_results'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 등급별 분석 함수
def analyze_by_grade_range():
    results = {}
    
    for start, end, label in grade_ranges:
        # 해당 등급 범위에 속하는 데이터 필터링
        filtered_df = df[(df['전과목'] >= start) & (df['전과목'] < end)]
        
        if not filtered_df.empty:
            # 모집단위 정보
            departments = filtered_df[['대학', '모집단위', '년도']].to_dict('records')
            
            results[label] = {
                'departments': departments,
                'count': len(filtered_df)
            }
    
    return results

# 등급별 상세 정보 텍스트 파일 생성
def generate_detailed_report(results):
    with open(f'{output_dir}/detailed_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("# 등급별 대학 입시 결과 상세 분석\n\n")
        
        for label, data in results.items():
            f.write(f"## {label} (총 {data['count']}개 사례)\n\n")
            
            # 모집단위 상세 정보
            f.write("### 모집단위 상세 정보\n")
            
            # 대학별로 모집단위 정보 정리
            university_departments = defaultdict(list)
            for dept in data['departments']:
                university_departments[dept['대학']].append(f"{dept['모집단위']}")
            
            for university, departments in sorted(university_departments.items()):
                f.write(f"#### {university}\n")
                for dept in departments:
                    f.write(f"- {dept}\n")
                f.write("\n")

# 등급별 요약 정보 생성
def generate_summary_report(results):
    with open(f'{output_dir}/summary_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("# 등급별 대학 입시 결과 요약\n\n")
        
        for label, data in results.items():
            f.write(f"## {label}\n\n")
            
            # 합격 사례 수
            f.write(f"- 합격 사례 수: {data['count']}개\n")
            f.write("\n")

# 메인 함수
def main():
    print("입시 결과 분석 중입니다...")
    
    # 결과 디렉토리 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 등급별 분석
    results = analyze_by_grade_range()
    
    # 상세 분석 보고서 생성
    generate_detailed_report(results)
    
    # 요약 보고서 생성
    generate_summary_report(results)
    
    print(f"분석이 완료되었습니다. 결과는 {output_dir} 디렉토리에 저장되었습니다.")

if __name__ == "__main__":
    main()
