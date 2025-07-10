'''Модуль с функциями для валидации данных'''

def validate_float(s):
        '''Валидация вводимых значений на соответствие 
        числам с плавающей точкой'''
        flag = False
        invalid_symbols = '\\qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъ'
        invalid_symbols += 'фывапролджэячсмитьбю~`!@#$%^&*()_-=+"№;:?|/ '
        for i in range(len(invalid_symbols)):
            if invalid_symbols[i] in s.lower():
                flag = True
        if (
            s.count('.') > 1 
            or s.startswith('.') 
            or s.endswith('.')
            or s.count(',') > 1
            or s.startswith(',') 
            or s.endswith(',')
        ):
            flag = True
        if '.' in s and ',' in s or s == '0':
            flag = True
        return flag


def validate_nulls(s):
    '''Функция проверки на наличие нуля'''
    null_vars = ['0', '0.0', '0,0']
    return s in null_vars