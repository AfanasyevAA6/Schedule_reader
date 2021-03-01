from lib import schedule_lib as sl
import pandas as pd
import pytest

schedule_name = input('Введите имя shedule файла: ')  # ввод пути файла shedule секции
schedule_file = 'input' + '\\' + schedule_name
print(schedule_file)
count = 0

with open(schedule_file, "r", encoding="UTF-8") as file:
    line = file.readlines()  # считывание строк
count = len(line)

clean_schedule_name = 'handled_schedule.inc'
# создает новый путь очищенного файла
clean_schedule_file_path = "output" + '\\' + clean_schedule_name

if __name__ == "__main__":
    # список очищенных строк
    line_clean = []
    line_clean = sl.clean_schedule(line, clean_schedule_file_path, count)
    count_clean = len(line_clean)

    # список дат
    data_list = []
    data_list = sl.parse_keyword_DATE_line(line_clean, count_clean)
    print("DATES", "\n", data_list)

    # список COMPDAT
    compdat_list = []
    compdat_list = sl.parse_keyword_COMPDAT_line(line_clean, count_clean)
    print("COMPDAT", "\n", compdat_list)

    # список COMPDATL
    compdatl_list = []
    compdatl_list = sl.parse_keyword_COMPDATL_line(line_clean, count_clean)
    print("COMPDATL", "\n", compdatl_list)

    def data_list_test(self):
        output = pd.Series(['1 JUN 2018', '01 JUL 2018', '01 AUG 2018', '01 SEP 2018',
            '01 OCT 2018', '01 NOV 2018','01 DEC 2018'])
        assert sl.parse_keyword_COMPDAT_line(line_clean, count_clean) == output
