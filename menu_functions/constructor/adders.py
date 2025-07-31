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
    

    def add_complaints(self, complaints_tab):
        '''Добавление жалоб'''
        # Получение содержимого вкладки "Жалобы"
        content = complaints_tab.complaints.get('1.0', 'end')

        # Добавление текста в текстовое поле
        self.text_handler.text_add(content=content, tag='main')

    
    def add_anamnesis(self, anamnesis_tab):
        '''Добавление анамнеза'''
        # Получение содержимого вкладки "Анамнез"
        content = anamnesis_tab.anamnesis.get('1.0', 'end')

        # Добавление текста в текстовое поле
        self.text_handler.text_add(content=content, tag='main')
