import pandas as pd
import re
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

def identification_kyeword(parametrs, keyword, identificator):

    # условия для нахождения ключевого слова
    if parametrs[0] == keyword: 
        identificator = 1
    if parametrs[0] == '/': 
        identificator = 0

    return identificator

# Функция обнаружения параметров ключевого слова DATA
def parse_keyword_DATE_line(parametrs):
    date = parametrs[0] + ' ' + parametrs[1] + ' ' + parametrs[2]
    return date # запись дат

# Функция обнаружения параметров ключевого слова COMPDAT
def parse_keyword_COMPDAT_line(parametrs):

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
def parse_keyword_COMPDATL_line(parametrs):

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

def finder_date(parametrs, keyword, identificator, date):
    if identification_kyeword(parametrs, keyword, identificator) == 1 and parametrs[0] != keyword:
        return parse_keyword_DATE_line(parametrs)
    else: return date

def finder_key_word(parametrs, keyword, identificator):
    if identification_kyeword(parametrs, keyword, identificator) == 1 and parametrs[0] != keyword:
        if keyword == 'COMPDAT':
            return parse_keyword_COMPDAT_line(parametrs)
        if keyword == 'COMPDATL':
            return parse_keyword_COMPDATL_line(parametrs)
    return []

# условие для присваивания значений параметров привязанных к датам
def for_date_with_parametrs(data, data_list, compdat_list, compdatl_list, result):        
    if data_list != [] and (compdat_list != [] or compdatl_list != []):
        result = [data] + compdat_list + compdatl_list
    return result

# условие для присваивания значений на последнюю дату, в случае если на эту дату не были заданы параметры ранее
def for_last_date_without_parametrs(i, count, data, final_result, data_list, result):    
    if data_list != []:
        if i == count - 1 and final_result[len(final_result) - 1][0] != data_list:
            result = [data] + [np.nan]
    return result

# условие для присваивания значений параметров, непривязанных к датам
def for_parametrs_without_date(data_list, compdat_list, compdatl_list, result):        
    if data_list == [] and (compdat_list != [] or compdatl_list != []):
        result = [np.nan] + compdat_list + compdatl_list
    return result

# условие для присваивания на тот случай, если на определенную дату нет значений параметров
def for_date_without_parametrs(data_list, final_result):
    if len(data_list) > 1:
        if data_list[len(data_list)-2] != final_result[len(final_result) - 1][0]:
            if ([data_list[len(data_list)-2], np.nan] in final_result) == False:
                final_result.append([data_list[len(data_list)-2], np.nan])
    return final_result

# условие для дополнения списка найденной информацией
def sum_for_date_with_parametrs(result, final_result):
    if result!= [] and (result in final_result) == False :
        final_result.append(result)
    return final_result