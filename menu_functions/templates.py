from tkinter import Menu
from menu_functions.constructor.constructor import ConstructorWindow

class TemplatesMenu(Menu):
    '''Меню с шаблонами'''
    def __init__(self, app):
        super().__init__()

        # Экземпляр приложения
        self.app = app

        # Создание меню
        self.add_command(
            label='Направление на ДС', 
            command=self._referral_to_DH
        )
        self.add_command(
            label='Прием на ДС', 
            command=self._admission_to_DH
        )
        self.add_command(
            label='Осмотр с заведующим', 
            command=self._inspection_with_the_supervisor
        )
        self.add_command(
            label='Ежедневный осмотр',
            command=self._daily_inspection
        )
        self.add_command(
            label='Осмотр деж. врача',
            command=self._duty_inspection
        )

    
    def _referral_to_DH(self):
        '''Сборка направления на ДС'''
        # Индексы для активации чек-боксов в конструкторе
        activate_indices = [1, 2, 4, 5, 6, 7]
        # Создание конструктора
        self._create_constructor(activate_indices)


    def _admission_to_DH(self):
        '''Сборка первичного приема на ДС'''
        # Получение текущей вкладки
        current_tab = self._get_current_day_tab()
        # Активация необходимого заголовка
        current_tab.day_dnevnic_type.set('Прием врача-инфекциониста первичный')
        # Индексы для активации чек-боксов в конструкторе
        activate_indices = [0, 1, 2, 4, 5, 6, 7]
        # Создание конструктора
        self._create_constructor(activate_indices)


    def _inspection_with_the_supervisor(self):
        '''Сборка осмотра с заведующим'''
        # Получение текущей вкладки
        current_tab = self._get_current_day_tab()
        # Активация необходимого заголовка
        current_tab.day_dnevnic_type.set(current_tab.supervisor_title)
        # Активация чек-бокса с заведующим
        current_tab.boss_doctor_chosen.set(1)
        # Индексы для активации чек-боксов в конструкторе
        activate_indices = [0, 1, 2, 4, 5, 6, 7]
        # Создание конструктора
        self._create_constructor(activate_indices)


    def _daily_inspection(self):
        '''Сборка ежедневного осмотра'''
        # Получение текущей вкладки
        current_tab = self._get_current_day_tab()
        # Активация необходимого заголовка
        current_tab.day_dnevnic_type.set(
            'Ежедневный осмотр врача-инфекциониста'
        )
        # Индексы для активации чек-боксов в конструкторе
        activate_indices = [0, 1, 3, 4, 6, 7]
        # Создание конструктора
        self._create_constructor(activate_indices)
    

    def _duty_inspection(self):
        '''Сборка осмотра дежурного врача'''
        # Получение текущей вкладки
        current_tab = self._get_current_day_tab()
        # Активация необходимого заголовка
        current_tab.day_dnevnic_type.set('Осмотр дежурного врача-инфекциониста')
        # Индексы для активации чек-боксов в конструкторе
        activate_indices = [0, 1, 3, 4, 6, 7]
        # Создание конструктора
        self._create_constructor(activate_indices)


    def _create_constructor(self, activate_indices):
        '''Открытие конструктора с активацией чек-боксов'''
        constructor = ConstructorWindow(self.app)
        for i in range(len(constructor.element_intvars)):
            if i in activate_indices:
                constructor.element_intvars[i].set(1)

    
    def _get_current_day_tab(self):
        '''Получение текущей вкладки с характеристиками дня'''
        # Список вкладок c характеристиками дня
        self.day_tabs = self.app.notebook.tab_frames
        # Индекс текущей вкладки с характеристиками дня
        self.day_note_index = self.app.notebook.index(
            self.app.notebook.select()
        )
        # Возврат текущей вкладки
        return self.day_tabs[self.day_note_index]