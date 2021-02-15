import pandas as pd
import re
# функция, которая чистит текст открытого исходного файла
def clean_schedule(line, file_path, count):
    # создание нового файла
    file = open(file_path, 'w', encoding = "UTF-8")
    line_clean = []
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

# Функция обнаружения параметров ключевого слова DATA в случае, если подается строка, а не список (пусть будет)
def parse_keyword_DATE_line_example(line):
    # создание списка из строки 
    parametrs = line.split(' ')
    
    if len(parametrs) > 3:
        if parametrs[0].isdigit() == True and parametrs[1].isalpha() == True and parametrs[2].isdigit() == True:
            line = parametrs[0] + ' ' + parametrs[1] + ' ' + parametrs[2]
            print(line)
            return line

# Функция обнаружения параметров ключевого слова DATA
def parse_keyword_DATE_line(line, count):
    
    identificator_dat = 0                               # вспомогательный параметр
    data_list = []
    
    for i in range(count):
        parametrs = line[i].split(' ')                  # разделение строки по пробелам
        
        #условия для нахождения дат
        if parametrs[0] == 'DATES': identificator_dat = 1 
        if parametrs[0] == '/': identificator_dat = 0
        if identificator_dat == 1 and parametrs[0] != 'DATES':
            data_list.append(parametrs[0] + ' ' + parametrs[1] + ' ' + parametrs[2]) # запись дат
            
    return pd.Series(data_list)

# Функция обнаружения параметров ключевого слова COMPDAT
def parse_keyword_COMPDAT_line(line, count):
    
    identificator_compdat = 0                            # вспомогательный параметр
    compdat_list = []
    
    for i in range(count):
        parametrs = line[i].split(' ')                   # разделение строки по пробелам
        
        #условия для нахождения параметров ключевого слова
        if parametrs[0] == 'COMPDAT': identificator_compdat = 1
        if parametrs[0] == '/': identificator_compdat = 0
        if identificator_compdat == 1 and parametrs[0] != 'COMPDAT':
            parametrs.remove('/')                        # удаление лишних символов
            parametrs.insert(1, float("nan"))            # добавление пустого параметра
            compdat_list.append(parametrs)               # запись параметров
            
    return pd.Series(compdat_list)

# Функция обнаружения параметров ключевого слова COMPDATl
def parse_keyword_COMPDATL_line(line, count):
    
    identificator_compdatl = 0                           # вспомогательный параметр
    compdatl_list = []
    
    for i in range(count):
        parametrs = line[i].split(' ')                   # разделение строки по пробелам
        
        #условия для нахождения параметров ключевого слова
        if parametrs[0] == 'COMPDATL': identificator_compdatl = 1
        if parametrs[0] == '/': identificator_compdatl = 0
        if identificator_compdatl == 1 and parametrs[0] != 'COMPDATL':
            parametrs.remove('/')                        # удаление лишних символов
            compdatl_list.append(parametrs)              # запись параметров
    return pd.Series(compdatl_list)

