import pandas as pd

shedule_file = input('Введите путь shedule файла: ') # ввод пути файла shedule секции
count = 0

with open(shedule_file, "r", encoding = "UTF-8") as file:
    for lines in file: count += 1 # определение кол-ва строк
          
with open(shedule_file, "r", encoding="UTF-8") as file: 
    line = file.readlines() # считывание строк

for i in range(count):
    print(line[i])C:\Users\afana\OneDrive\Документы\test_schedule.inc