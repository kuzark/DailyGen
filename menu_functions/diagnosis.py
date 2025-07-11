from tkinter import Menu
from settings import Settings
from handlers.text_handler import TextHandler

class DiagnosisMenu(Menu):
    '''Добавляет диагноз с обоснованием'''
    def __init__(self, app):
        super().__init__()
        # Получение доступа к текстовому полю
        self.text = app.text
        # Инициализация настроек
        self.settings = Settings()
        # Инициализация обработчика текста
        self.text_handler = TextHandler(self.text)

        # Создание меню
        self.add_command(
            label='1-ое обоснование', 
            command=lambda: self.text_handler.text_add(
                content='\n' + self.settings.diagnosis_arguments[0] + '\n',
                tag='main'
            )
        )
        self.add_command(
            label='2-ое обоснование',
            command=self._add_second_argument
        )

    
    def _add_second_argument(self):
        '''Добавляет диагноз и второе обоснование диагноза'''
        # Добавление диагноза
        self.text_handler.text_add(
            content='\nДиагноз:\n',
            tag='subtitle'
        )
        
        # Добавление обоснования в текстовое поле
        self.text_handler.text_add(
            content='\n' + self.settings.diagnosis_arguments[1] + '\n',
            tag='main'
        )
        
        
    