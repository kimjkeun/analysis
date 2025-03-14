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
file_path = 'Result.csv'
df = pd.read_csv(file_path, encoding='utf-8')

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
            # 대학별 카운트
            university_counts = filtered_df['대학'].value_counts().to_dict()
            
            # 전형별 카운트
            admission_counts = filtered_df['전형\n분류'].value_counts().to_dict()
            
            # 계열별 카운트
            major_type_counts = filtered_df['계열'].value_counts().to_dict()
            
            # 모집단위 정보
            departments = filtered_df[['대학', '모집단위', '전형\n분류']].to_dict('records')
            
            results[label] = {
                'university_counts': university_counts,
                'admission_counts': admission_counts,
                'major_type_counts': major_type_counts,
                'departments': departments,
                'count': len(filtered_df)
            }
    
    return results

# 등급별 대학 분포 시각화
def plot_universities_by_grade(results):
    plt.figure(figsize=(15, 10))
    
    # 등급 범위별로 대학 수 계산
    grade_labels = []
    university_counts = []
    
    for label, data in results.items():
        grade_labels.append(label)
        university_counts.append(len(data['university_counts']))
    
    plt.bar(grade_labels, university_counts, color='skyblue')
    plt.title('등급별 지원 가능 대학 수', fontsize=16, fontweight='bold')
    plt.xlabel('등급 범위', fontsize=14)
    plt.ylabel('대학 수', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/universities_by_grade.png', dpi=300)
    plt.close()

# 등급별 전형 분포 시각화
def plot_admission_types_by_grade(results):
    admission_types = set()
    for data in results.values():
        admission_types.update(data['admission_counts'].keys())
    
    admission_types = list(admission_types)
    grade_labels = list(results.keys())
    
    data = np.zeros((len(admission_types), len(grade_labels)))
    
    for i, admission_type in enumerate(admission_types):
        for j, label in enumerate(grade_labels):
            if label in results and admission_type in results[label]['admission_counts']:
                data[i, j] = results[label]['admission_counts'][admission_type]
    
    plt.figure(figsize=(15, 10))
    bottom = np.zeros(len(grade_labels))
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(admission_types)))
    
    for i, admission_type in enumerate(admission_types):
        plt.bar(grade_labels, data[i], bottom=bottom, label=admission_type, color=colors[i])
        bottom += data[i]
    
    plt.title('등급별 전형 유형 분포', fontsize=16, fontweight='bold')
    plt.xlabel('등급 범위', fontsize=14)
    plt.ylabel('합격 사례 수', fontsize=14)
    plt.xticks(rotation=45)
    plt.legend(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/admission_types_by_grade.png', dpi=300)
    plt.close()

# 등급별 계열 분포 시각화
def plot_major_types_by_grade(results):
    major_types = set()
    for data in results.values():
        major_types.update(data['major_type_counts'].keys())
    
    major_types = list(major_types)
    grade_labels = list(results.keys())
    
    data = np.zeros((len(major_types), len(grade_labels)))
    
    for i, major_type in enumerate(major_types):
        for j, label in enumerate(grade_labels):
            if label in results and major_type in results[label]['major_type_counts']:
                data[i, j] = results[label]['major_type_counts'][major_type]
    
    plt.figure(figsize=(15, 10))
    bottom = np.zeros(len(grade_labels))
    
    colors = plt.cm.Paired(np.linspace(0, 1, len(major_types)))
    
    for i, major_type in enumerate(major_types):
        plt.bar(grade_labels, data[i], bottom=bottom, label=major_type, color=colors[i])
        bottom += data[i]
    
    plt.title('등급별 계열 분포', fontsize=16, fontweight='bold')
    plt.xlabel('등급 범위', fontsize=14)
    plt.ylabel('합격 사례 수', fontsize=14)
    plt.xticks(rotation=45)
    plt.legend(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/major_types_by_grade.png', dpi=300)
    plt.close()

# 등급별 상세 정보 텍스트 파일 생성
def generate_detailed_report(results):
    with open(f'{output_dir}/detailed_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("# 등급별 대학 입시 결과 상세 분석\n\n")
        
        for label, data in results.items():
            f.write(f"## {label} (총 {data['count']}개 사례)\n\n")
            
            # 대학별 분석
            f.write("### 대학별 합격 사례 수\n")
            for university, count in sorted(data['university_counts'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {university}: {count}개\n")
            f.write("\n")
            
            # 전형별 분석
            f.write("### 전형별 합격 사례 수\n")
            for admission_type, count in sorted(data['admission_counts'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {admission_type}: {count}개\n")
            f.write("\n")
            
            # 계열별 분석
            f.write("### 계열별 합격 사례 수\n")
            for major_type, count in sorted(data['major_type_counts'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {major_type}: {count}개\n")
            f.write("\n")
            
            # 모집단위 상세 정보
            f.write("### 모집단위 상세 정보\n")
            
            # 대학별로 그룹화
            university_departments = defaultdict(list)
            for dept in data['departments']:
                university_departments[dept['대학']].append((dept['모집단위'], dept['전형\n분류']))
            
            for university, departments in sorted(university_departments.items()):
                f.write(f"#### {university}\n")
                for dept, admission_type in sorted(departments):
                    f.write(f"- {dept} ({admission_type})\n")
                f.write("\n")
            
            f.write("\n" + "-"*50 + "\n\n")

# 등급별 요약 정보 생성
def generate_summary_report(results):
    with open(f'{output_dir}/summary_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("# 등급별 대학 입시 결과 요약\n\n")
        
        for label, data in results.items():
            f.write(f"## {label}\n\n")
            
            # 상위 대학 5개
            f.write("### 주요 대학\n")
            top_universities = sorted(data['university_counts'].items(), key=lambda x: x[1], reverse=True)[:5]
            for university, count in top_universities:
                f.write(f"- {university}: {count}개 사례\n")
            f.write("\n")
            
            # 주요 전형
            f.write("### 주요 전형\n")
            for admission_type, count in sorted(data['admission_counts'].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / data['count']) * 100
                f.write(f"- {admission_type}: {count}개 사례 ({percentage:.1f}%)\n")
            f.write("\n")
            
            # 주요 계열
            f.write("### 주요 계열\n")
            for major_type, count in sorted(data['major_type_counts'].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / data['count']) * 100
                f.write(f"- {major_type}: {count}개 사례 ({percentage:.1f}%)\n")
            f.write("\n")
            
            # 주요 모집단위 (상위 10개)
            f.write("### 주요 모집단위\n")
            department_counts = defaultdict(int)
            for dept in data['departments']:
                department_counts[dept['모집단위']] += 1
            
            top_departments = sorted(department_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            for dept, count in top_departments:
                f.write(f"- {dept}: {count}개 사례\n")
            f.write("\n")
            
            f.write("\n" + "-"*50 + "\n\n")

# 등급별 전형 유형 파이 차트 생성
def plot_admission_types_pie_charts(results):
    # 각 등급 범위별로 파이 차트 생성
    rows = (len(results) + 2) // 3  # 한 행에 3개씩 배치
    fig, axes = plt.subplots(rows, 3, figsize=(18, rows * 5))
    axes = axes.flatten()
    
    for i, (label, data) in enumerate(results.items()):
        if i < len(axes):
            admission_counts = data['admission_counts']
            if admission_counts:
                labels = list(admission_counts.keys())
                sizes = list(admission_counts.values())
                
                # 파이 차트 생성
                axes[i].pie(sizes, labels=None, autopct='%1.1f%%', 
                           shadow=False, startangle=90, 
                           colors=plt.cm.tab10(np.linspace(0, 1, len(sizes))))
                axes[i].set_title(f'{label} 전형 유형 분포', fontsize=14)
                
                # 범례 추가
                axes[i].legend(labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
    
    # 사용하지 않는 서브플롯 제거
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/admission_types_pie_charts.png', dpi=300)
    plt.close()

# 계열별 등급대 분석 함수 추가
def analyze_by_major_category():
    # 결과 저장할 딕셔너리
    categories = ['인문', '자연', '공통', '예체능']
    category_results = {category: {} for category in categories}
    
    for category in categories:
        # 해당 계열 데이터만 필터링
        category_df = df[df['계열'] == category]
        
        # 각 등급 범위별 분석
        for start, end, label in grade_ranges:
            # 해당 등급 범위 데이터 필터링
            grade_df = category_df[(category_df['전과목'] >= start) & (category_df['전과목'] < end)]
            
            if not grade_df.empty:
                # 대학별 합격 사례 수
                university_counts = grade_df['대학'].value_counts().to_dict()
                
                # 전형별 합격 사례 수
                admission_counts = grade_df['전형\n분류'].value_counts().to_dict()
                
                # 모집단위 정보
                department_info = {}
                for uni in grade_df['대학'].unique():
                    uni_df = grade_df[grade_df['대학'] == uni]
                    departments = []
                    for _, row in uni_df.iterrows():
                        departments.append(f"{row['모집단위']} ({row['전형\n분류']})")
                    department_info[uni] = departments
                
                # 결과 저장
                category_results[category][label] = {
                    'total': len(grade_df),
                    'university_counts': university_counts,
                    'admission_counts': admission_counts,
                    'department_info': department_info
                }
    
    return category_results

# 계열별 분석 보고서 생성
def generate_category_report(category_results):
    with open(f'{output_dir}/category_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("# 계열별 대학 입시 결과 분석\n\n")
        
        for category, results in category_results.items():
            f.write(f"## {category} 계열 분석\n\n")
            
            for label, data in results.items():
                f.write(f"### {label} (총 {data['total']}개 사례)\n\n")
                
                # 대학별 합격 사례 수
                f.write("#### 대학별 합격 사례 수\n")
                for uni, count in sorted(data['university_counts'].items(), key=lambda x: x[1], reverse=True):
                    f.write(f"- {uni}: {count}개\n")
                f.write("\n")
                
                # 전형별 합격 사례 수
                f.write("#### 전형별 합격 사례 수\n")
                for admission, count in sorted(data['admission_counts'].items(), key=lambda x: x[1], reverse=True):
                    f.write(f"- {admission}: {count}개\n")
                f.write("\n")
                
                # 모집단위 상세 정보
                f.write("#### 모집단위 상세 정보\n")
                for uni, departments in sorted(data['department_info'].items()):
                    f.write(f"##### {uni}\n")
                    for dept in departments:
                        f.write(f"- {dept}\n")
                    f.write("\n")
                
                f.write("\n--------------------------------------------------\n\n")

# 계열별 시각화 생성
def plot_category_analysis(category_results):
    categories = list(category_results.keys())
    
    # 등급대별 계열 분포 시각화
    grade_labels = []
    category_counts = {category: [] for category in categories}
    
    # 모든 등급대 수집
    all_grade_labels = set()
    for category_data in category_results.values():
        all_grade_labels.update(category_data.keys())
    
    # 정렬된 등급대 목록
    sorted_grade_labels = sorted(all_grade_labels, key=lambda x: float(x.split('-')[0].replace('등급', '').replace(' 이상', '')))
    
    # 데이터 준비
    for grade_label in sorted_grade_labels:
        grade_labels.append(grade_label)
        for category in categories:
            if grade_label in category_results[category]:
                category_counts[category].append(category_results[category][grade_label]['total'])
            else:
                category_counts[category].append(0)
    
    # 막대 그래프 생성
    fig, ax = plt.subplots(figsize=(15, 8))
    bar_width = 0.2
    index = np.arange(len(grade_labels))
    
    for i, category in enumerate(categories):
        ax.bar(index + i * bar_width, category_counts[category], bar_width, 
               label=category, color=plt.cm.tab10(i))
    
    ax.set_xlabel('등급 범위', fontsize=12)
    ax.set_ylabel('합격 사례 수', fontsize=12)
    ax.set_title('등급대별 계열 분포', fontsize=14)
    ax.set_xticks(index + bar_width * (len(categories) - 1) / 2)
    ax.set_xticklabels(grade_labels, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/category_distribution_by_grade.png', dpi=300)
    plt.close()
    
    # 각 계열별 전형 유형 분포 시각화
    for category in categories:
        # 전형 유형 데이터 수집
        admission_types = {}
        for grade_data in category_results[category].values():
            for admission_type, count in grade_data['admission_counts'].items():
                if admission_type in admission_types:
                    admission_types[admission_type] += count
                else:
                    admission_types[admission_type] = count
        
        if admission_types:  # 데이터가 있는 경우에만 시각화
            # 파이 차트 생성
            fig, ax = plt.subplots(figsize=(10, 8))
            labels = list(admission_types.keys())
            sizes = list(admission_types.values())
            
            ax.pie(sizes, labels=None, autopct='%1.1f%%', 
                   shadow=False, startangle=90, 
                   colors=plt.cm.tab10(np.linspace(0, 1, len(sizes))))
            ax.set_title(f'{category} 계열 전형 유형 분포', fontsize=14)
            
            # 범례 추가
            ax.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
            
            plt.tight_layout()
            plt.savefig(f'{output_dir}/{category}_admission_types.png', dpi=300)
            plt.close()

# 등급대별 통합 분석 보고서 생성 함수
def generate_integrated_report():
    # 결과 파일 경로
    output_file = f'{output_dir}/integrated_analysis.txt'
    
    # 등급별 분석 결과
    grade_results = analyze_by_grade_range()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 등급대별 통합 분석 보고서\n\n")
        f.write("이 보고서는 각 등급대별로 지원 가능한 학교, 전형, 계열, 모집단위(학과)를 통합적으로 정리한 자료입니다.\n\n")
        
        for start, end, label in grade_ranges:
            if label in grade_results:
                data = grade_results[label]
                
                f.write(f"## {label} (총 {data['count']}개 사례)\n\n")
                
                # 데이터 수집
                filtered_df = df[(df['전과목'] >= start) & (df['전과목'] < end)]
                
                # 표 헤더 작성
                f.write("| 대학 | 계열 | 모집단위 | 전형유형 |\n")
                f.write("|------|------|----------|----------|\n")
                
                # 정렬된 데이터 출력 (대학, 계열, 모집단위, 전형유형 순)
                sorted_rows = filtered_df.sort_values(['대학', '계열', '모집단위', '전형\n분류'])
                for _, row in sorted_rows.iterrows():
                    f.write(f"| {row['대학']} | {row['계열']} | {row['모집단위']} | {row['전형\n분류']} |\n")
                
                f.write("\n" + "-" * 50 + "\n\n")
    
    print(f"통합 분석 보고서가 생성되었습니다: {output_file}")
    return output_file

# 메인 함수 수정
def main():
    print("입시 결과 분석 중입니다...")
    
    # 결과 저장 디렉토리 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 등급별 분석
    results = analyze_by_grade_range()
    
    # 계열별 분석
    category_results = analyze_by_major_category()
    
    # 등급별 통합 분석 보고서 생성
    generate_integrated_report()
    
    # 상세 분석 보고서 생성
    generate_detailed_report(results)
    
    # 요약 분석 보고서 생성
    generate_summary_report(results)
    
    # 계열별 분석 보고서 생성
    generate_category_report(category_results)
    
    # 시각화
    plot_universities_by_grade(results)
    plot_admission_types_by_grade(results)
    plot_major_types_by_grade(results)
    plot_admission_types_pie_charts(results)
    plot_category_analysis(category_results)
    
    print(f"분석이 완료되었습니다. 결과는 {output_dir} 디렉토리에 저장되었습니다.")

if __name__ == "__main__":
    main()
