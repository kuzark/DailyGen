from tkinter import Menu
from pathlib import Path
from handlers.text_handler import TextHandler

class DiagnosisMenu(Menu):
    '''Добавляет диагноз с обоснованием'''
    def __init__(self, app):
        super().__init__()
        # Получение доступа к текстовому полю
        self.text = app.text
        # Получение доступа к форме для выделения
        self.select_form = app.select_form
        # Инициализация обработчика текста
        self.text_handler = TextHandler(self.text)
        # Построчное считывание файла с обоснованиями
        file = Path('resourses/arguments.txt')
        self.arguments = file.read_text(encoding='utf-8').splitlines()

        # Создание меню
        self.add_command(
            label='1-ое обоснование', 
            command=lambda: self.text_handler.text_add(
                content='\n' + self.arguments[0] + '\n',
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
            content='\n' + self.arguments[1] + '\n',
            tag='main'
        )
        
        
    