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
    day_end = '04:59'

    new_rows = []
    for row in rdr:
        # desc escape 처리
        row[-1] = row[-1].replace('\n', '\\n').replace('"', "\'")
        # type 변환
        row[-2] = categories.get(row[-2], 'other')

        # 취침/기상 시각 ~ 변경
        # row[1] = 시작시각, row[2] = 종료시각
        if row[1] == '~':
            row[1] = day_start
        if row[2] == '~':
            row[2] = day_end

        # key:value 쌍 생성
        new_row = [f'{key}:"{value.strip()}"' for key, value in zip(h, row)]
        new_rows.append("  {" + ", ".join(new_row) + "}")

    # 전체를 const data 배열로 출력
    f2.write("const data = [\n")
    f2.write(",\n".join(new_rows))
    f2.write("\n];\n")
