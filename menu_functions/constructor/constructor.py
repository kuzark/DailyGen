from tkinter import Toplevel, IntVar
from tkinter import SUNKEN, EW, W
from tkinter import ttk
from settings import Settings
from menu_functions.constructor.adders import Add
from menu_functions.constructor.tabs import (
    ComplaintsTab, AnamnesisTab, ExaminationTab
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

        # Настройки окна
        self.title('Конструктор')
        self.geometry('705x580+831+285')
        self.resizable(False, False)

        # Отступы
        settings = Settings()
        self.margins = settings.margins

        # Список структурных элементов медицинских документов
        structure_elements = [
            'Заголовок',
            'Жалобы',
            'Анамнез',
            'Осмотр',
            'Диагноз',
            'Дата и врач'
        ]

        # Список для хранения выбранных пользователем элементов
        self.chosen_elements = []

        # Создание области выбора структурных элементов
        choose_structure_frame = ttk.Frame(self, relief=SUNKEN)
        row = 0
        column = 0
        for element in structure_elements:
            if row == 3: # Переход на следующую строку
                row = 0
                column = 1
            
            # Создание переменных для хранения выбранных пользователем элементов
            self.chosen_elements.append(IntVar(value=0))

            # Создание Чек-боксов
            ttk.Checkbutton(
                choose_structure_frame, 
                text=element, 
                width=50, 
                variable=self.chosen_elements[-1]
            ).grid(row=row, column=column, sticky=W, **self.margins)
            row += 1

        choose_structure_frame.grid(row=0, sticky=EW, **self.margins)

        # Создание кнопки 'Сформировать'
        ttk.Button(
            self, text='Сформировать', command=self._create_note
        ).grid(row=1)

    
    def _create_note(self):
        '''Создает ноутбук с вкладками характеристик элементов'''
        self.note = ttk.Notebook(self)
        # Добавление вкладки 'Жалобы'
        if self.chosen_elements[1].get() == 1:
            # Переменная для хранения вкладки с жалобами
            self.complaints_tab = ComplaintsTab(self.note, self.margins)
            # Добавление вкладки в ноутбук
            self.note.add(self.complaints_tab, text='Жалобы')

        # Добавление вкладки 'Анамнез'
        if self.chosen_elements[2].get() == 1:
            # Переменная для хранения вкладки с анамнезом
            self.anamnesis_tab = AnamnesisTab(self.note, self.margins)
            # Добавление вкладки в ноутбук
            self.note.add(self.anamnesis_tab, text='Анамнез')

        self.note.grid(row=2, sticky=EW, **self.margins)

        # Добавление вкладки 'Осмотр'
        if self.chosen_elements[3].get() == 1:
            # Переменная для хранения вкладки с осмотром
            self.examination_tab = ExaminationTab(self.note, self.margins)
            # Добавление вкладки в ноутбук
            self.note.add(self.examination_tab, text='Осмотр')

        self.note.grid(row=2, sticky=EW, **self.margins)

        # Создание кнопки 'Добавить'
        ttk.Button(
            self, text='Добавить', command=self._add_elements
        ).grid(row=3)

    
    def _add_elements(self):
        '''Добавляет выбранные элементы медицинской документации'''
        # Добавление заголовка
        if self.chosen_elements[0].get() == 1:
            self.add.add_title()
        
        # Добавление жалоб
        if self.chosen_elements[1].get() == 1:
            self.add.add_element(self.complaints_tab.complaints)

        # Добавление анамнеза
        if self.chosen_elements[2].get() == 1:
            self.add.add_element(self.anamnesis_tab.anamnesis)

        # Добавление осмотра
        if self.chosen_elements[3].get() == 1:
            self.add.add_element(self.examination_tab.examination)
        
        # Форматирование собранных элементов
        self.text_handler.paragraphs_selector()

        





    