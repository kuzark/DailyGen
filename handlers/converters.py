'''Модуль с функциями для конвертации форматов данных'''

def str_to_float(results):
    '''Переводит строку в значение с плавающей точкой'''
    for j in range(len(results)):
        if results[j]:
            if ',' in results[j]:
                results[j] = results[j].replace(',', '.')
            results[j] = float(results[j])
    return results