# csv 데이터를 const data = [...] 형식으로 변환해 txt에 저장하는 코드 (2025.09.04)

import csv

with open('timeblock.csv', 'r', encoding='utf-8') as f,\
    open('timeblock_array.txt', 'w', encoding='utf-8') as f2:
    rdr = csv.reader(f)
    next(rdr)

    h = ['date', 'start', 'end', 'type', 'desc']

    categories = {
        '일상':'daily', 
        '일정':'schedule',
        '집중':'focus', 
        '생산':'productive', 
        '마음':'mind',
        '낭비':'waste',
        '수면':'sleep'
    }

    day_start = '05:00'
    day_end = '05:00'

    new_rows = []

    prev_date = None
    max_hour = 0  # 날짜별 누적 최대값 기준

    for row in rdr:
        # desc escape 처리
        row[-1] = row[-1].replace('\n', '\\n').replace('"', "\'")

        # type 변환
        row[-2] = categories.get(row[-2], 'other')

        # '~' 처리
        if row[1] == '~':
            row[1] = day_start
        if row[2] == '~':
            row[2] = day_end
        
        # 날짜 변경 시 max_hour 초기화
        date = row[0]
        if date != prev_date:
            max_hour = 0
            prev_date = date

        # 시각을 시간 단위 float로 변환
        sh, sm = map(int, row[1].split(":"))
        eh, em = map(int, row[2].split(":"))
        start_num = sh + sm/60
        end_num = eh + em/60


        # 누적 최대값 기준으로 24 더할지 판단
        if start_num < max_hour:
            start_num += 24
        if end_num < max_hour:
            end_num += 24
        

        # max_hour 갱신
        max_hour = max(max_hour, end_num)

        # 다시 HH:MM 문자열로 변환
        row[1] = f"{int(start_num):02d}:{int((start_num-int(start_num))*60):02d}"
        row[2] = f"{int(end_num):02d}:{int((end_num-int(end_num))*60):02d}"

        # key:value 쌍 생성
        new_row = [f'{key}:"{value.strip()}"' for key, value in zip(h, row)]
        new_rows.append("  {" + ", ".join(new_row) + "}")

    # 전체를 const data 배열로 출력
    f2.write("const data = [\n")
    f2.write(",\n".join(new_rows))
    f2.write("\n];\n")
