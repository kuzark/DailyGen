from tkinter import SUNKEN, W
from tkinter import IntVar, StringVar
from tkinter import ttk
from settings import Settings


class TreatmentForm(ttk.Frame):
    '''Форма выбора схемы лечения'''
    def __init__(self, app):
        super().__init__(app, relief=SUNKEN)
        settings = Settings()
        
        # Словарь с настройками расположения элементов
        elem_grid = {
            'column': 0,
            'padx': 10,
            'pady': 5,
            'sticky': W
        }

        # Переменная для хранения выбранной схемы лечения
        self.treatment_var = StringVar(value='Мавирет')

        # Переменная для хранения выбранного количества капсул Рибавирина
        self.ribavirin_count = IntVar(value=5)

        # Заголовок
        ttk.Label(
            self, text='Схема лечения:',
            font='TkDefaultFont 10 bold italic'
        ).grid(row=0, column=0, sticky=W, **settings.margins)

        # Чек боксы выбора вариантов для выделения в тексте
        row = 1
        for paragraph_name in settings.paragraph_names.keys():
            ttk.Checkbutton(
                self, text=paragraph_name,
            ).grid(row=row, **elem_grid)
            row += 1