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

        # Кнопки выбора схемы лечения
        row = 1
        for treatment in settings.treatment.keys():
            ttk.Radiobutton(
                self, text=treatment, 
                value=treatment, 
                variable=self.treatment_var,
                command=self._activate_ribavirin
            ).grid(row=row, **elem_grid)
            row += 1
        
        # Интерфейс активации и выбора количества капсул Рибавирина
        self.enabled_ribavirin = IntVar()
        self.check_rib = ttk.Checkbutton(
            self, 
            text='Рибавирин (капсулы):', 
            width=22,
            variable=self.enabled_ribavirin,
            state='disabled',
            command=self._activate_spin_caps
            )
        self.check_rib.grid(
            row=row, column=0, **elem_grid
        )
        self.spin_rib = ttk.Spinbox(
            self,
            from_=1.0,
            to=7.0,
            textvariable=self.ribavirin_count,
            width=3,
            state='disabled'
        )
        self.spin_rib.grid(row=row, column=1, **elem_grid)

    
    def _activate_ribavirin(self):
        '''Активация и деактивация Рибавирина'''
        if self.treatment_var.get() == 'Эпклюза':
            self.check_rib.config(state='normal')
        else:
            self.check_rib.config(state='disabled')
            self.enabled_ribavirin.set(value=0)
            self._activate_spin_caps()

    
    def _activate_spin_caps(self):
        '''Активация спинбокса для выбора количества капсул Рибавирина'''
        if self.enabled_ribavirin.get():
            self.spin_rib.config(state='readonly')
        else:
            self.spin_rib.config(state='disabled')

