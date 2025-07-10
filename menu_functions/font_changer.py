from tkinter import Menu, IntVar, TclError
from tkinter.messagebox import showerror

class FontMenu(Menu):
    '''Меню со шрифтами'''
    def __init__(self, text):
        super().__init__()
        # Получение доступа к текстовому полю
        self.text = text

        # Создание меню
        self.add_command(
            label='Жирный', command=self._selected_bold
        )
        self.add_command(
            label='Курсив', command=self._selected_italic
        )
        self.add_command(
            label='Обычный', command=self._selected_usual
        )
        self.add_separator()

        self.underlined = IntVar(value=0)
        self.add_checkbutton(label='Подчеркнутый', variable=self.underlined)


    def _selected_bold(self):
        '''Устанавливает шрифт жирный и при выборе подчеркнутый'''
        pos, end = self._text_selection()
        if self.underlined.get() == 0:
            self.text.tag_add('subtitle', pos, end)
        else:
            self.text.tag_add('subtitle_underlined', pos, end)


    def _selected_italic(self):
        '''Устанавливает шрифт курсив и при выборе подчеркнутый'''
        pos, end = self._text_selection()
        if self.underlined.get() == 0:
            self.text.tag_add('italic', pos, end)
        else:
            self.text.tag_add('italic_underlined', pos, end)


    def _selected_usual(self):
        '''Устанавливает шрифт обычный и при выборе подчеркнутый'''
        pos, end = self._text_selection()
        if self.underlined.get() == 0:
            self.text.tag_add('main', pos, end)
        else:
            self.text.tag_add('main_underlined', pos, end)
    

    def _text_selection(self):
        '''Функция для получения выделенного текста'''
        try:
            self.text.selection_get()
        except TclError:
            showerror(title='Ошибка', message='Сначала выделите текст')
        else:
            text_copy = self.text.selection_get()
            pos = self.text.index('sel.first')
            end = self.text.index('sel.last')
            self.text.replace(pos, end, text_copy)
            return pos, end