from handlers.text_handler import TextHandler

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


    def add_title(self):
        '''Добавление заголовка дневника'''
        index = self.day_note_index
        content = self.day_tabs[index].day_dnevnic_type.get() + 2 * '\n'
        self.text_handler.text_add(content=content, tag='title')
    

    def add_element(self, element_tab_text):
        '''Добавление элемента в основное текстовое поле'''
        # Получение содержимого вкладки
        content = element_tab_text.get('1.0', 'end')

        # Добавление текста в текстовое поле
        self.text_handler.text_add(content=content, tag='main')

    
    def add_doctor(self):
        '''Добавление строки для подписи врача'''
        # Формирование строки подписи
        doc_sign = ' г. Врач-инфекционист:_____________________/'
        boss_sign = 'Зав. отд.:_____________________/Кайкова О.В./'
        content = '\n' + self.day_tabs[index].day_now_date.get() + doc_sign
        content += self.day_tabs[index].day_selected_doctor.get() + '/' + '\n'
        
        # Получение индекса текущей вкладки дня
        index = self.day_note_index
        
        # Добавление строки подписи заведующего при выборе
        boss_chosen = self.day_tabs[index].boss_doctor_chosen.get()
        if boss_chosen == 1:
            content += '\n' + boss_sign + '\n'

        # Добавление сформированной строки
        self.text_handler.text_add(content=content, tag='main')



