from handlers.text_handler import TextHandler
from handlers import validators as valid
from settings import Settings

class Add:
    '''Содержит функции для добавления элементов медицинской документации'''
    def __init__(self, app):
        # Получение доступа к текстовому полю
        self.text = app.text
        # Список вкладок c характеристиками дня
        self.day_tabs = app.notebook.tab_frames
        # Индекс текущей вкладки с характеристиками дня
        self.day_note_index = app.notebook.index(app.notebook.select())
        # Инициализация обработчика текста
        self.text_handler = TextHandler(self.text)
        # Выбранная схема лечения
        self.treatment_chosen = app.treatment_form.treatment_var.get()
        # Инициализация настроек
        self.settings = Settings()


    def add_title(self):
        '''Добавление заголовка дневника'''
        index = self.day_note_index
        content = self.day_tabs[index].day_dnevnic_type.get() + 2 * '\n'
        self.text_handler.text_add(content=content, tag='title')

    
    def add_week(self):
        '''Добавление строки недели'''
        # Добавление характеристик недели с активной вкладки дня
        index = self.day_note_index
        content = f'{self.day_tabs[index].day_week_period.get()} '
        content += f'{self.day_tabs[index].day_week_num.get()}-й недели '
        
        # Добавление выбранной схемы лечения
        treatment = self.settings.treatment[self.treatment_chosen]['week']
        content += treatment

        # Добавление продолжения строки недели
        content += 'Терапию переносит удовлетворительно. '
        content += 'Возникновения НЯ не отмечает. '

        # Добавление текста в текстовое поле
        self.text_handler.text_add(content=content, tag='main')


    def add_element(self, element_tab_text):
        '''Добавление элемента в основное текстовое поле'''
        # Получение содержимого вкладки
        content = element_tab_text.get('1.0', 'end')

        # Добавление текста в текстовое поле
        self.text_handler.text_add(content=content, tag='main')

    
    def add_doctor(self):
        '''Добавление строки для подписи врача'''
        # Получение индекса текущей вкладки дня
        index = self.day_note_index

        # Получение и валидация даты
        date = self.day_tabs[index].day_now_date.get()
        if not valid.validate_date(date):
            return
        
        # Формирование строки подписи
        doc_sign = ' г. Врач-инфекционист:_____________________/'
        boss_sign = 'Зав. отд.:_____________________/Кайкова О.В./'
        content = '\n' + date + doc_sign
        content += self.day_tabs[index].day_selected_doctor.get() + '/' + '\n'
        
        # Добавление строки подписи заведующего при выборе
        boss_chosen = self.day_tabs[index].boss_doctor_chosen.get()
        if boss_chosen == 1:
            content += '\n' + boss_sign + '\n'

        # Добавление сформированной строки
        self.text_handler.text_add(content=content, tag='main')




