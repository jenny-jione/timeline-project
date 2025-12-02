import os
import shutil

# 경로 설정
download_folder = os.path.expanduser("~/Downloads")  # 다운로드 폴더
source_file = os.path.join(download_folder, "일간 회고 - csv.csv")
target_folder = "."
target_file = os.path.join(target_folder, "timeblock.csv")


# 기존 timeblock.csv 있으면 삭제
if os.path.exists(target_file):
    os.remove(target_file)

# csv를 . 폴더로 이동하면서 이름 변경
shutil.move(source_file, target_file)

print("작업 완료!")
