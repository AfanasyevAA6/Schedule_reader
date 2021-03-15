from lib import schedule_lib as sl
import numpy as np

schedule_name = input('Введите имя shedule файла (name.inc): ')  # ввод имени файла shedule секции
schedule_file = 'input' + '\\' + schedule_name

with open(schedule_file, "r", encoding="UTF-8") as file:
    line = file.readlines()  # считывание строк

clean_schedule_name = 'handled_schedule.inc'
# создает новый путь очищенного файла
clean_schedule_file_path = "output" + '\\' + clean_schedule_name

if __name__ == "__main__":

    # список очищенных строк
    line_clean = []
    line_clean = sl.clean_schedule(line, clean_schedule_file_path)
    count = len(line_clean)

    #------------------------------------------------------------------------------------------------------------------

    data_list = []
    data = ''
    compdat_list = []
    compdatl_list = []
    result = []
    final_result = []
    # TODO: всё работает, но код ниже тяжело читать из-за обилия вложенных идущих друг за другом циклов
    
    # вспомогательные параметры
    identificator_dat = 0
    identificator_compdat = 0
    identificator_compdatl = 0
    # TODO: сюда же - понятно, что мы проходим файл по строкам, но это понятно, пока код небольшой
    for i in range(count):

        compdat_list = []
        compdatl_list = []
        result = []
        # TODO: лучше разбить код на небольшие функции так, чтобы такого количества поясняющих комментариев не понадобилось
        # можно разбить код на отдельные функции даже по линиям #-------------
        
        #TODO: для кода без функций тяжелее писать тесты - формально твой код их не проходит, хотя результат возвращает верный. Но мне нужно лезть сравнивать результат руками
        
        # нахождение дат
        parametrs = line_clean[i].split(' ')

        # условия для нахождения дат
        if parametrs[0] == 'DATES': identificator_dat = 1
        if parametrs[0] == '/': identificator_dat = 0

        # список дат
        if identificator_dat == 1 and parametrs[0] != 'DATES':
            data = sl.parse_keyword_DATE_line(line_clean[i])
            data_list.append(data)
            #print(data_list)
        #---------------------------------------------------------------------------------------------------------------

        # нахождение COMPDAT

        # условия для нахождения дат
        if parametrs[0] == 'COMPDAT': identificator_compdat = 1
        if parametrs[0] == '/': identificator_compdat = 0

        # список COMPDAT
        if identificator_compdat == 1 and parametrs[0] != 'COMPDAT':
            compdat_list = sl.parse_keyword_COMPDAT_line(line_clean[i])
            #print(compdat_list)
        #---------------------------------------------------------------------------------------------------------------

        # нахождение COMPDATL

        # условия для нахождения дат
        if parametrs[0] == 'COMPDATL': identificator_compdatl = 1
        if parametrs[0] == '/': identificator_compdatl = 0

        # список COMPDATL
        if identificator_compdatl == 1 and parametrs[0] != 'COMPDATL':
            compdatl_list = sl.parse_keyword_COMPDATL_line(line_clean[i])
            #print(compdatl_list)

    #------------------------------------------------------------------------------------------------------------------

        # условие для присваивания значений параметров, непривязанных к датам
        if data_list == [] and (compdat_list != [] or compdatl_list != []):
            result = [np.nan] + compdat_list + compdatl_list
        # условие для присваивания значений на последнюю дату, в случае если на эту дату не были заданы параметры ранее
        if data_list != []:
            if line_clean[i+1].split(' ')[0] == 'END' and final_result[len(final_result) - 1][0] != data_list:
                result = [data] + [np.nan]
        # условие для присваивания значений параметров привязанных к датам
        if data_list != [] and (compdat_list != [] or compdatl_list != []):
            result = [data] + compdat_list + compdatl_list
        # условие для присваивания на тот случай, если на определенную дату нет значений параметров
        if len(data_list) > 1:
            if data_list[len(data_list)-2] != final_result[len(final_result) - 1][0]:
                if ([data_list[len(data_list)-2], np.nan] in final_result) == False:
                    final_result.append([data_list[len(data_list)-2], np.nan])
        # условие для дополнения списка найденной информацией
        if result!= [] and (result in final_result) == False :
            final_result.append(result)
        # условие для работы условия для последней даты
        if i == count - 2: break

    for i in range(len(final_result)):
        print(final_result[i])
