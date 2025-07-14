from tkinter import IntVar, StringVar, Menu
from tkinter import SUNKEN, W
from tkinter import ttk
from datetime import datetime
from settings import Settings

class TabsMenu(Menu):
    '''Меню 'Вкладки' задает количество вкладок с характеристиками дня'''
    def __init__(self, app):
        super().__init__()
        # Определение переменной для хранения количества вкладок 
        settings = Settings()
        day_count = IntVar(value=settings.start_num_tabs)

        # Создание меню 'Вкладки'
        for i in range(settings.max_tabs):
            if i == 0:
                title = f'{i + 1} день'
            elif 1 <= i <= 3:
                title = f'{i + 1} дня'
            else:
                title = f'{i + 1} дней'

            self.add_radiobutton(
                label=title,
                variable=day_count,
                value=i + 1,
                command=lambda: app.notebook.tabs_create(day_count.get())
            )
    

class NoteBook(ttk.Notebook):
    '''Ноутбук с вкладками с характеристиками дня'''
    def __init__(self, app):
        super().__init__(app)
        # Определение списка для хранения экземпляров вкладок
        self.tab_frames = []
        # Инициализация настроек программы
        self.settings = Settings()
        # Создание вкладок при запуске программы
        self.tabs_create(self.settings.start_num_tabs)

    
    def tabs_create(self, tabs_num):
        '''Создание вкладок с характеристиками дня'''
        # Определение необходимости добавить или удалить вкладки
        selected_tabs_num = tabs_num
        current_tabs_num = self.index('end')
        if current_tabs_num < selected_tabs_num:
            tabs_num = selected_tabs_num - current_tabs_num
        elif current_tabs_num > selected_tabs_num:
            while current_tabs_num != selected_tabs_num:
                self.forget(current_tabs_num - 1)
                current_tabs_num -= 1
            return
        else:
            return 
        
        # Создание вкладок
        for _ in range(tabs_num):
            self.tab_frames.append(TabFrame(self, self.settings))

            # Добавление и именование вкладки
            last_tab = self.index('end')
            self.add(self.tab_frames[-1], text=f'День {last_tab + 1}')
    

    def daily_dnevnic_btn_clicked(self):
        '''Функция, меняющая интерфейс формы при выборе ежедневного осмотра'''
        tab_selected = self.index(self.select())
        tab_frame = self.tab_frames[tab_selected]
        tab_frame.day_doctors_box.config(values=self.settings.doctors)
        tab_frame.day_selected_doctor.set('')
        tab_frame.day_doctor_label['text'] = 'Врач:'


    def duty_dnevnic_btn_clicked(self):
        '''Функция, меняющая интерфейс формы при выборе дежурного осмотра'''
        tab_selected = self.index(self.select())
        tab_frame = self.tab_frames[tab_selected]
        tab_frame.day_doctors_box.config(values=self.settings.duty_doctors)
        tab_frame.day_selected_doctor.set('')
        tab_frame.day_doctor_label['text'] = 'Дежурный врач:'


class TabFrame(ttk.Frame):
    '''Вкладка с характеристиками дня'''

    def __init__(self, notebook, settings):
        super().__init__(notebook, relief=SUNKEN)
        
        # Словарь расположения элементов
        notes_elem_grid = {
            'padx': 10,
            'pady': 5,
            'sticky': W
        }
        
        # Интерфейс выбора типа дневника
        self.day_dnevnic_type = StringVar(
            value='Ежедневный осмотр врача-инфекциониста'
        )
        
        ttk.Radiobutton(
            self,
            text='Ежедневный осмотр врача-инфекциониста',
            value='Ежедневный осмотр врача-инфекциониста',
            variable=self.day_dnevnic_type,
            command=lambda: notebook.daily_dnevnic_btn_clicked()
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            **notes_elem_grid
        )
        
        ttk.Radiobutton(
            self,
            text='Осмотр дежурного врача-инфекциониста',
            value='Осмотр дежурного врача-инфекциониста',
            variable=self.day_dnevnic_type,
            command=lambda: notebook.duty_dnevnic_btn_clicked()
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            **notes_elem_grid
        )

        long_str = 'Совместный осмотр врача-инфекциониста '
        long_str += 'с заведующим отделения'
        ttk.Radiobutton(
            self,
            text='Совместный осмотр с заведующим',
            value=long_str,
            variable=self.day_dnevnic_type,
            command=lambda: notebook.daily_dnevnic_btn_clicked()
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            **notes_elem_grid
        )
        
        ttk.Radiobutton(
            self,
            text='Без заголовка',
            value='',
            variable=self.day_dnevnic_type,
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            **notes_elem_grid
        )

        # Интерфейс выбора периода недели
        ttk.Label(self, text='Период недели:', width=22).grid(
            row=4, column=0, **notes_elem_grid
        )

        self.periods = ['Начало', 'Продолжение', 'Завершение']
        self.day_week_period = StringVar(value='Начало')
        ttk.Combobox(
            self,
            values=self.periods,
            state='readonly',
            textvariable=self.day_week_period,
            width=15
        ).grid(row=4, column=1, **notes_elem_grid)

        # Интерфейс выбора номера недели
        ttk.Label(self, text='Номер недели:').grid(
            row=5, column=0, **notes_elem_grid
        )

        self.day_week_num = IntVar(value=1)
        ttk.Spinbox(
            self,
            from_=1.0,
            to=12.0,
            textvariable=self.day_week_num,
            width=3,
            state='readonly'
        ).grid(row=5, column=1, **notes_elem_grid)
        
        # Интерфейс выбора врача
        self.day_doctor_label = ttk.Label(self, text='Врач:')
        self.day_doctor_label.grid(
            row=6,
            column=0,
            **notes_elem_grid
        )

        self.day_selected_doctor = StringVar()
        self.day_doctors_box = ttk.Combobox(
            self,
            values=settings.doctors,
            width=15,
            textvariable=self.day_selected_doctor
        )
        self.day_doctors_box.grid(
            row=6,
            column=1,
            **notes_elem_grid
        )

        # Интерфейс выбора даты
        ttk.Label(self, text='Дата:').grid(
            row=7, column=0, **notes_elem_grid
        )

        now = datetime.today()
        self.day_now_date = StringVar()
        self.day_now_date.set(now.strftime('%d.%m.%y'))
        self.day_date = ttk.Entry(
            self,
            textvariable=self.day_now_date,
            width=18
        )
        self.day_date.grid(
            row=7,
            column=1,
            **notes_elem_grid
        )



    
    
