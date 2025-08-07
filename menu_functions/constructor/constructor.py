from tkinter import Toplevel, IntVar
from tkinter import SUNKEN, EW, W, S
from tkinter import ttk
from settings import Settings
from menu_functions.constructor.adders import Add
from menu_functions.constructor.tabs import (
    ComplaintsTab, AnamnesisTab, ExaminationTab, DiagnosisTab, RecomendationsTab
)
from handlers.text_handler import TextHandler


class ConstructorWindow(Toplevel):
    '''Окно для выбора составляющих документа'''
    def __init__(self, app):
        super().__init__()

        # Инициализация класса для добавления элементов
        self.add = Add(app)
        # Инициализация обработчика текста
        self.text_handler = TextHandler(app.text)
        # Экземпляр приложения
        self.app = app

        # Настройки окна
        self.title('Конструктор')
        self.geometry('705x650+607+215')
        self.resizable(False, False)

        # Отступы
        settings = Settings()
        self.margins = settings.margins

        # Словарь структурных элементов медицинских документов
        self.structure_elements = {
            'Заголовок': None,
            'Жалобы': ComplaintsTab,
            'Анамнез': AnamnesisTab,
            'Строка недели': None,
            'Осмотр': ExaminationTab,
            'Диагноз': DiagnosisTab,
            'Рекомендации': RecomendationsTab,
            'Дата и врач': None
        }

        # Список для хранения IntVar структурных элементов
        self.element_intvars = []

        # Создание области выбора структурных элементов
        choose_structure_frame = ttk.Frame(self, relief=SUNKEN)
        row = 0
        column = 0
        for element_name in self.structure_elements.keys():
            if row == 3: # Переход на следующий столбик
                row = 0
                column += 1
            
            # Создание переменных для хранения выбранных пользователем элементов
            self.element_intvars.append(IntVar(value=0))

            # Создание Чек-боксов
            ttk.Checkbutton(
                choose_structure_frame, 
                text=element_name, 
                width=31, 
                variable=self.element_intvars[-1]
            ).grid(row=row, column=column, sticky=W, **self.margins)
            row += 1

        choose_structure_frame.grid(row=0, sticky=EW, **self.margins)

        # Создание кнопки 'Сформировать'
        ttk.Button(
            self, text='Сформировать', command=self._create_note
        ).grid(row=1)

        # Создание ноутбука для вкладок
        self.note = ttk.Notebook(self)

    
    def _create_note(self):
        '''Создает ноутбук с вкладками характеристик элементов'''
        # Удаление ноутбука и создание заново
        self.note.destroy()
        self.note = ttk.Notebook(self)
        
        # Список для хранения выбранных структурных элементов
        self.chosen_elements = [] 

        # Добавление вкладок в ноутбук
        for i, (element_name, element_class) in enumerate(
            self.structure_elements.items()):
            
            # Проверка выбран ли структурный элемент пользователем
            if not self.element_intvars[i].get():
                continue

            if element_class:
                # Создание экземпляра вкладки
                element_tab = (
                    element_class(self.note, self.margins, self.app)
                    if element_name == 'Рекомендации'
                    else element_class(self.note, self.margins)
                )
                
                # Сохранение экземпляра в список
                self.chosen_elements.append(element_tab)
                
                # Добавление вкладки в ноутбук
                self.note.add(self.chosen_elements[-1], text=element_name)
            else:
                # Если нет вкладки для элемента добавляем имя элемента
                self.chosen_elements.append(element_name)

        # Размещение ноутбука
        if self.note.tabs():
            self.note.grid(row=2, sticky=EW, **self.margins)

        # Создание кнопки 'Добавить'
        ttk.Button(
            self, text='Добавить', command=self._add_elements
        ).grid(row=3, **self.margins)

    
    def _add_elements(self):
        '''Добавляет выбранные элементы медицинской документации'''
        for chosen_element in self.chosen_elements:
            # Добавление заголовка
            if chosen_element == 'Заголовок':
                self.add.add_title()
            
            # Добавление строки недели
            elif chosen_element == 'Строка недели':
                self.add.add_week()
            
            # Добавление строки подписи врача
            elif chosen_element == 'Дата и врач':
                self.add.add_doctor()
            
            # Добавление остальных элементов
            else:
                self.add.add_element(chosen_element.text)

        # Форматирование собранных элементов
        self.text_handler.paragraphs_selector()

        





    