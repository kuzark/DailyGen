from tkinter import SUNKEN, W
from tkinter import IntVar
from tkinter import ttk
from settings import Settings


class SelectForm(ttk.Frame):
    '''Форма выбора строк для выделения'''
    def __init__(self, app):
        super().__init__(app, relief=SUNKEN)
        settings = Settings()
        
        # Заголовок
        ttk.Label(
            self, text='Выделить:',
            font='TkDefaultFont 10 bold italic'
        ).grid(row=0, column=0, sticky=W, **settings.margins)

        # Словарь с настройками расположения
        f_sel_grid = {
            'column': 0,
            'padx': 10,
            'pady': 5,
            'sticky': W
        }

        # Список для хранения выбранных вариантов
        self.enabled_vars = []

        # Чек боксы выбора вариантов для выделения в тексте
        row = 1
        for paragraph_name in settings.paragraph_names.keys():
            self.enabled_vars.append(IntVar(value=0))
            ttk.Checkbutton(
                self, text=paragraph_name,
                variable=self.enabled_vars[-1]
            ).grid(row=row, **f_sel_grid)
            row += 1