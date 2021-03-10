import pandas as pd
import re
import test
import numpy as np

# функция, которая чистит текст открытого исходного файла
def clean_schedule(line, file_path):
    # создание нового файла
    file = open(file_path, 'w', encoding = "UTF-8")
    line_clean = []
    count = len(line)

    for i in range(count):
        # удаление лишних пробелов между параметрами
        line[i] = re.sub(r'\s+', ' ', line[i])

        # удаление коментарий
        position_comment = line[i].find("-")          # определение начала комментария
        if position_comment != -1: 
            line[i] = line[i][:position_comment]      # удаление комментария из строки    
        
        if len(line[i]) > 1:    
            if line[i][0] == ' ': 
                line[i] = line[i].replace(' ', '', 1) # удаление пробела в начале, если он есть
        
            if line[i][len(line[i])-1] == ' ': 
                line[i] = line[i][:len(line[i])-1]     # удаленеие пробела в конце, если он есть
                
        # запись в файл
        if line[i].isspace() == False and position_comment != 0:
            file.write(line[i] + '\n')                 # запись без лишних переносов
            line_clean.append(str(line[i]))            # создает список без лишних переносов
    
    file.close()
    return line_clean

# Функция обнаружения параметров ключевого слова DATA
def parse_keyword_DATE_line(line):

    parametrs = line.split(' ')                  # разделение строки по пробелам
    data_list = parametrs[0] + ' ' + parametrs[1] + ' ' + parametrs[2] # запись дат
            
    return data_list

# Функция обнаружения параметров ключевого слова COMPDAT
def parse_keyword_COMPDAT_line(line):

    parametrs = line.split(' ')  # разделение строки по пробелам
    parametrs.remove('/')  # удаление лишних символов
    parametrs.insert(1, np.nan)  # добавление пустого параметра
    length = len(parametrs)
    p = 0
    for k in range(length):
        if type(parametrs[k]) == str:
            length_word = len(parametrs[k])
            if parametrs[k][length_word - 1] == '*':
                p = k
                chislo = int(parametrs[k][:(length_word - 1)])
                parametrs.pop(p)
                length -= 1
                for j in range(chislo):
                    parametrs.insert(p, "DEFAULT")
                    length += 1

    compdat_list = parametrs  # запись параметров

    return compdat_list

# Функция обнаружения параметров ключевого слова COMPDATL
def parse_keyword_COMPDATL_line(line):

    parametrs = line.split(' ')  # разделение строки по пробелам
    parametrs.remove('/')  # удаление лишних символов
    length = len(parametrs)
    p = 0
    for k in range(length):
        if type(parametrs[k]) == str:
            length_word = len(parametrs[k])
            if parametrs[k][length_word - 1] == '*':
                p = k
                chislo = int(parametrs[k][:(length_word - 1)])
                parametrs.pop(p)
                length -= 1
                for j in range(chislo):
                    parametrs.insert(p, "DEFAULT")
                    length += 1

    compdatl_list = parametrs  # запись параметров

    return compdatl_list
