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
    

    def add_complaints(self, note):
        '''Добавление жалоб'''
        # Получение содержимого вкладки "Жалобы"
        complaint_tab = note.winfo_children()[0]
        content= complaint_tab.complaints.get('1.0', 'end')

        # Добавление текста в текстовое поле
        self.text_handler.text_add(content=content, tag='main')
