from tkinter.scrolledtext import ScrolledText
from settings import Settings

class TextSpace(ScrolledText):
    '''Текстовое поле со шрифтами'''
    def __init__(self, window):
        super().__init__(window,  wrap='word', undo=True)

        # Инициализация настроек
        self.settings = Settings()
    
        # Установка шрифтов
        self.tag_configure('main', font=self.settings.font_usual)
        self.tag_configure(
            'main_underlined',
            font=self.settings.font_usual_underlined
        )
        self.tag_configure('title', font='Times_New_Roman 12 bold')
        self.tag_configure('subtitle', font=self.settings.font_bold)
        self.tag_configure(
            'subtitle_underlined', 
            font=self.settings.font_bold_underlined
        )
        self.tag_configure(
            'italic', 
            font=self.settings.font_italic
        )
        self.tag_configure(
            'italic_underlined', 
            font=self.settings.font_italic_underlined
        )
        self.tag_configure('paragraph')