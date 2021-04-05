from lib import schedule_lib as sl
import numpy as np

schedule_name = r'test_schedule.inc'  # ввод имени файла shedule секции
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

    # вспомогательные параметры
    identificator_dat = 0
    identificator_compdat = 0
    identificator_compdatl = 0
    for i in range(count):

        result = []
        parametrs = line_clean[i].split(' ')

        # -----------------определение наличия ключевого слова---------------------

        identificator_dat = sl.identification_kyeword(parametrs, 'DATES', identificator_dat)
        identificator_compdat = sl.identification_kyeword(parametrs, 'COMPDAT', identificator_compdat)
        identificator_compdatl = sl.identification_kyeword(parametrs, 'COMPDATL', identificator_compdatl)

        #------------------------нахождение дат--------------------------------------

        data = sl.finder_date(parametrs, 'DATES', identificator_dat, data)
        if data not in data_list and data!='': data_list.append(data)

        #-----------------нахождение параметров кл. слова COMPDAT--------------------

        compdat_list = sl.finder_key_word(parametrs, 'COMPDAT', identificator_compdat)

        #-----------------нахождение параметров кл. слова COMPDATL-------------------

        compdatl_list = sl.finder_key_word(parametrs, 'COMPDATL', identificator_compdatl)

        #---------------условия для формирования результата------------------------
       
        result = sl.for_date_with_parametrs(data, data_list, compdat_list, compdatl_list, result)
        
        result = sl.for_last_date_without_parametrs(i, count, data, final_result, data_list, result)
        
        result = sl.for_parametrs_without_date(data_list, compdat_list, compdatl_list, result)
       
        final_result = sl.for_date_without_parametrs(data_list, final_result)
        
        final_result = sl.sum_for_date_with_parametrs(result, final_result)

    #---------------------------------------------------------------------------------------------------------------
    
    outfile = open(r'output\\result.txt', 'w')
    for i in range(len(final_result)):
        for j in range(len(final_result[i])):
            if final_result[i][j]!=np.nan:final_result[i][j] = str(final_result[i][j])
            outfile.write(final_result[i][j] + '\t')
        outfile.write('\n')
        print(final_result[i])
    outfile.close()
