from tkinter import Menu, Toplevel, StringVar, IntVar
from tkinter import SUNKEN, W, END
from tkinter.messagebox import showerror
from tkinter import ttk
from datetime import datetime, timedelta
from math import floor

from settings import Settings
import handlers.validators as valid
import handlers.converters as convert
from handlers.text_handler import TextHandler

class AnalysisMenu(Menu):
    '''Меню для добавления анализов'''
    def __init__(self, app):
        super().__init__()
        # Доступ к экземпляру поля с характеристиками дня
        self.notebook = app.notebook
        # Доступ к текстовому полю
        self.text = app.text
        # Инициализация обработчика текста
        self.text_handler = TextHandler(self.text)
        
        # Переменные хранящие выбор анализов пользователем
        self.analysis_chosen = {
            'КАК': IntVar(value=1),
            'БАК': IntVar(value=1),
            'ОАМ': IntVar(value=1),
            'Коагулограмма': IntVar(value=0),
        }

        # Создание меню
        for analysis_name, variable in self.analysis_chosen.items():
            self.add_checkbutton(label=analysis_name, variable=variable)
        self.add_separator()
        self.add_command(
            label='Добавить', command=lambda: AnalysisWindow(self, app)
        )
        self.add_command(label='Назначить', command=self._add_analysis_plan)
        self.add_command(label='В работе', command=self._add_analysis_in_work)

    
    def _add_analysis_plan(self):
        '''Добавляет назначение анализов на завтра'''
        
        # Индекс текущей вкладки
        note_index = self.notebook.index(self.notebook.select())
        
        # Список вкладок с параметрами дня
        day_tabs = self.notebook.tab_frames
        
        # Расчет следующего дня от указанного во вкладке
        note_day = datetime.strptime(day_tabs[note_index].day_now_date.get(), \
            '%d.%m.%y')
        next_day = note_day + timedelta(1)

        # Формирование строки плана анализов
        content = '- ' + self._analysis_listing() 
        content += f' на {next_day.strftime('%d.%m.%y')} г.\n'

        # Вставка и форматирование текста
        self.text_handler.text_add(content, tag='main')


    def _add_analysis_in_work(self):
        '''Добавляет указание, что анализы в работе'''
        content = self._analysis_listing() + ' в работе.'
        self.text_handler.text_add(content, tag='main')


    def _analysis_listing(self):
        '''Формирует список анализов'''
        analysis_list = []
        for analysis in self.analysis_chosen.keys():
            if self.analysis_chosen[analysis].get() == 1:
                analysis_list.append(analysis)
                if 'Коагулограмма' in analysis_list:
                    analysis_list[-1] = analysis_list[-1].lower()
        return ', '.join(analysis_list)


class AnalysisWindow(Toplevel):
    '''Окно для внесения результатов анализов'''
    def __init__(self, analysis_menu, app):
        super().__init__()
        # Доступ к переменной с выбранными пользователем анализами
        a_chosen = analysis_menu.analysis_chosen
        # Словарь для хранения экземпляров вкладок
        self.tabs = {}

        # Настройки окна
        self.title('Анализы')
        self.geometry('258x510+831+285')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self._dismiss)
        self.grab_set()

        # Отступы
        margins = {'padx': 5, 'pady': 5}

        # Создание области выбора пола
        gender_fr = ttk.Frame(self, relief=SUNKEN)
        
        ttk.Label(gender_fr, text='Выберите пол пациента.', width=39).grid(
            row=0, sticky=W, **margins
        )
        
        # Переменная для хранения выбранного пола
        self.gender = StringVar(value='male')

        ttk.Radiobutton(
            gender_fr, text='мужской', value='male', variable=self.gender
        ).grid(row=1, sticky=W, **margins)

        ttk.Radiobutton(
            gender_fr, text='женский', value='female', variable=self.gender
        ).grid(row=2,sticky=W, **margins)
        
        gender_fr.grid(row=0, **margins)

        # Создание области вкладок
        note = ttk.Notebook(self)
        note.grid(row=1)

        # Добавление вкладок в область
        for note_name in a_chosen.keys():
            self.tabs[note_name] = AnalysisTab(note, note_name, margins)
            self.tabs[note_name].grid()
            note.add(self.tabs[note_name], text=note_name)

        # Скрывание всех вкладок
        for note_num in range(4):
            note.hide(note_num)

        # Доступ пользователя к вкладкам выбранных анализов
        note_num = 3
        for value in reversed(list(a_chosen.values())):
            if value.get() == 1:
                note.select(note_num)
            note_num -= 1

        # Кнопка оценки анализов
        ttk.Button(
            self, 
            text='Сформировать', 
            command=lambda: AnalysisHandler(self, app, a_chosen)
            ).grid(row=2, **margins)


    def _dismiss(self):
        '''Отключение пользовательского захвата при закрытии окна'''
        self.grab_release()
        self.destroy()


class AnalysisTab(ttk.Frame):
    '''Вкладка для ввода результатов анализа'''
    def __init__(self, note, note_name, margins):
        super().__init__(note)

        # Инициализация настроек
        settings = Settings()

        # Список для хранения полей ввода
        self.entries = []

        # Создание вкладки
        row = 0
        for key, value in settings.paraclinics[note_name].items():
            
            ttk.Label(self, text=key, width=20).grid(
                row=row, column=0, sticky=W, **margins
            )

            self.entries.append(ttk.Entry(self, width=6))
            self.entries[-1].grid(row=row, column=1)

            if note_name == 'ОАМ' and value:
                value = value[1]
            
            ttk.Label(self, text=value).grid(
                row=row, column=2, sticky=W, **margins
            )

            row += 1


class AnalysisHandler:
    def __init__(self, a_window, app, a_chosen):
        # Доступ к списку вкладок с анализами
        self.tabs = a_window.tabs
        # Доступ к выбранному полу пациента
        self.gender = a_window.gender
        # Инициализация настроек
        self.settings = Settings()
        # Список вкладок с параметрами дня
        day_tabs = app.notebook.tab_frames
        # Индекс текущей вкладки
        note_index = app.notebook.index(app.notebook.select())
        # Доступ к текстовому полю
        self.text = app.text
        # Инициализация обработчика текста
        self.text_handler = TextHandler(self.text)
        # Расчет предыдущего дня от указанного во вкладке
        note_day = datetime.strptime(day_tabs[note_index].day_now_date.get(), \
            '%d.%m.%y')
        previous_day = note_day - timedelta(1)
        # Переменная с результатами анализов
        self.content = ''
        # Переменная с заключением по результатам анализов
        self.conclusion = []
        # Переменная для выявления ошибок при вводе результатов
        tabs_err = 0

        # Перебор вкладок с анализами
        for analysis in self.settings.paraclinics.keys():
            # Определение выбрана ли вкладка пользователем
            if a_chosen[analysis].get() == 0:
                continue
            
            # Считывание и валидация данных с вкладки
            results, err = self._tab_read(analysis)

            # При наличии ошибок переход на след вкладку
            if err > 0:
                tabs_err += 1
                continue

            # Формирование заголовка строки анализа    
            self.content += f'\n- {analysis} от '
            self.content += f'{previous_day.strftime('%d.%m.%y')} г: '

            # Формирование строки с результатами анализа
            self._content_writer(analysis, results)
            
            # Формирование заключения по анализу
            self._conclusion_writer(analysis, results)
            
        if not self.conclusion:
            self.conclusion.append(
                'все показатели в пределах референсных значений'
            )
        self.conclusion = ', '.join(self.conclusion) + '.'

        # Вывод сообщения о наличии ошибок
        if tabs_err > 0:
            err_text = 'Вводимые значения должны быть в виде десятичной '
            err_text += 'дроби, разделенной точкой или запятой!'
            showerror(title='Ошибка', message=err_text)
            return
        
        # Добавление результатов и заключения в текстовое поле
        self._add_results_analysis()


    def _tab_read(self, analysis):
        '''Считывание и валидация данных с вкладки'''
        results = []
        err = 0
        for result_entry in self.tabs[analysis].entries:
            result = result_entry.get()

            # Валидация и отметка ошибок при наличии
            if valid.validate_float(result) or valid.validate_nulls(result):
                result_entry.delete(0, END)
                result_entry.insert(0, 'ERROR')
                err += 1
                continue

            # Добавление данных, если они прошли валидацию
            results.append(result)
        return results, err


    def _content_writer(self, analysis, results):
        '''Формирование строки с результатами анализа'''
        i = 0
        for key, value in self.settings.paraclinics[analysis].items():
            if analysis == 'ОАМ':
                if key != 'уд. вес':
                    if results[i]:
                        self.content += f'{key} - {results[i]} {value[1]}, '
                    else:
                        self.content += f'{key} - {results[i]} {value[0]}, '
                else:
                    if results[i]:
                        self.content += f'{key} - {results[i]}{value}, '
            else:
                if results[i]:
                    self.content += f'{key} - {results[i]} {value}, '
            i += 1
        self.content = self.content[:-2]


    def _conclusion_writer(self, analysis, results):
        '''Формирование заключения по анализу'''
        if analysis == 'КАК':
            results = convert.str_to_float(results)

            if results[0]:
                if 90 <= results[0] < 110:
                    self.conclusion.append('анемия легкой степени тяжести')
                elif 70 <= results[0] < 90:
                    self.conclusion.append('анемия средней степени тяжести')
                elif results[0] < 70:
                    self.conclusion.append('анемия тяжелой степени')

            if results[1]:
                if results[1] < 3.87:
                    self.conclusion.append('эритропения')
                elif results[1] > 5.68:
                    self.conclusion.append('эритроцитоз')

            if results[2]:
                if results[2] < 150:
                    self.conclusion.append('тромбоцитопения')
                elif results[2] > 366.8:
                    self.conclusion.append('тромбоцитоз')

            if results[3]:
                if results[3] < 3.71:
                    self.conclusion.append('лейкопения')
                elif results[3] > 10.67:
                    self.conclusion.append('лейкоцитоз')

            if results[4]:
                if results[4] > 71.65:
                    self.conclusion.append('относительный нейтрофилез')
                elif results[4] < 40.62:
                    self.conclusion.append('относительная нейтропения')

            if results[5]:
                if results[5] > 46.71:
                    self.conclusion.append('относительный лимфоцитоз')
                elif results[5] < 18.94:
                    self.conclusion.append('относительная лимфопения')

            if results[6]:
                if results[6] > 12.81:
                    self.conclusion.append('моноцитоз')

            if results[7]: 
                if results[7] > 6.73:
                    self.conclusion.append('эозинофилия')

            if self.gender.get() == 'male':
                if results[8]:
                    if results[8] > 10:
                        self.conclusion.append('ускоренное СОЭ')
            elif self.gender.get() == 'female':
                if results[8]:
                    if results[8] > 15:
                        self.conclusion.append('ускоренное СОЭ')

        if analysis == 'БАК':
            results = convert.str_to_float(results)

            if results[0]:
                if results[0] < 66:
                    self.conclusion.append('гипопротеинемия')

            if results[1]:
                if results[1] < 35:
                    self.conclusion.append('гипоальбуминемия')

            if results[2]:
                if results[2] > 21:
                    conclusion_bil = 'гипербилирубинемия'

                    if results[3]:
                        if results[3] > 5.1:
                            conclusion_bil += ' преимущественно за '
                            conclusion_bil += 'счет прямого билирубина'

                    self.conclusion.append(conclusion_bil)

            if results[4]:
                if results[4] > 41:
                    min_norm = floor(results[4] / 41)
                    max_norm = min_norm + 1
                    conclusion_ALT = f'АлАТ от {min_norm} '
                    conclusion_ALT += f'до {max_norm} норм'
                    self.conclusion.append(conclusion_ALT)

            if results[5]:
                if results[5] > 37:
                    self.conclusion.append('АсАТ выше нормы')

            if self.gender.get() == 'male':
                if results[6]:
                    if results[6] > 128:
                        self.conclusion.append('ЩФ выше нормы')
            elif self.gender.get() == 'female':
                if results[6]:
                    if results[6] > 98:
                        self.conclusion.append('ЩФ выше нормы')

            if self.gender.get() == 'male':
                if results[7]:
                    if results[7] > 49:
                        self.conclusion.append('ГГТП выше нормы')
            elif self.gender.get() == 'female':
                if results[7]:
                    if results[7] > 32:
                        self.conclusion.append('ГГТП выше нормы')

            if results[8]:
                if results[8] > 5.9:
                    self.conclusion.append('гипергликемия')

            azotemia = False
            if results[9]:
                if results[9] > 8.3:
                    azotemia = True
            if self.gender.get() == 'male':
                if results[10]:
                    if results[10] > 115:
                        azotemia = True
            elif self.gender.get() == 'female':
                if results[10]:
                    if results[10] > 97:
                        azotemia = True
            if azotemia:    
                self.conclusion.append('гиперазотемия')

            if results[11]:
                if results[11] > 5.2:
                    self.conclusion.append('гиперхолестеринемия')

        if analysis == 'ОАМ':
            params = [
                'лейкоцитурия',
                'протеинурия',
                'кетонурия',
                'гематурия',
                'уробилиногенурия',
                'глюкозурия',
            ]

            for j in range(len(params)):
                if results[j + 1]:
                    self.conclusion.append(params[j])


    def _add_results_analysis(self):
        '''Добавление вывода по анализам в текстовое поле'''

        # Ввод и форматирование заголовка вывода результатов анализов
        self.text_handler.text_add(
            content='\n' + 'При обследовании:',  
            tag='main_underlined'
        )
        
        # Ввод и форматирование результатов анализов
        self.text_handler.text_add(
            content=self.content,
            tag='main'
        )

        # Ввод и форматирование заголовка заключения по результатам анализов
        self.text_handler.text_add(
            content=2 * '\n' + 'Анализ анализов:' + '\n',
            tag='main_underlined'
        )
        
        # Ввод и форматирование заключения по результатам анализов
        self.text_handler.text_add(
            content=self.conclusion, 
            tag='main'
        )


        