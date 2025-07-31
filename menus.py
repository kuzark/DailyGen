from pyperclip import paste, copy
from tkinter import Menu, TclError
from tkinter.messagebox import showerror, askyesnocancel
from ctypes import windll
from menu_functions.font_changer import FontMenu
from forms.day_params_form import TabsMenu
from menu_functions.analysis import AnalysisMenu
from menu_functions.constructor.constructor import ConstructorWindow


class MainMenu(Menu):
    '''Главное меню'''
    def __init__(self, app):
        super().__init__()
        self.app = app
        
        self.add_separator()
        self.add_cascade(label='Назад', command=self._undo)
        self.add_separator()
        self.add_cascade(command=self._clear_all, label='Очистить все')
        self.add_separator()
        self.add_cascade(label='Шрифт', menu=FontMenu(app.text))
        self.add_separator()
        self.add_cascade(label='Вкладки', menu=TabsMenu(app))
        self.add_separator()
        self.add_cascade(label='Анализы', menu=AnalysisMenu(app))
        self.add_separator()
        self.add_cascade(
            label='Конструктор', 
            command= lambda: ConstructorWindow(app)
        )
        self.add_separator()
        self.add_cascade(label='Шаблоны')


    def _clear_all(self):
        '''Очищает текстовое поле полностью'''
        # Запрос подтверждения действия
        content = 'Вы уверены, что хотите полностью очистить тескстовое поле? '
        content += 'Несохраненные данные будут утеряны.'
        answer = askyesnocancel(
            title='Подтверждение', 
            message=content,
            icon='warning')
        if answer:
            # Полная очистка текстового поля
            self.app.text.delete('1.0', 'end')


    def _undo(self):
        '''Функция отмены изменений'''
        try:
            self.app.text.edit_undo()
        except TclError:
            showerror(title='Ошибка', message='Нет действий для отмены')
        else:
            self.app.text.edit_undo()

    
class ContextMenu(Menu):
    '''Контекстное меню'''
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.add_cascade(label='Вырезать', command=self._cut_result)
        self.add_cascade(label='Копировать', command=self._copy_result)
        self.add_cascade(label='Вставить', command=self._paste_text)
        self.add_cascade(label='Удалить', command=self._delete_result)
    

    def ctrl_C_V(self, event):
        '''Обеспечение работы Ctrl+C и Ctrl+V'''
        u = windll.LoadLibrary("user32.dll")
        pf = getattr(u, "GetKeyboardLayout")
        if hex(pf(0)) == '0x4190419':
            if event.keycode == 86 and event.state == 12:
                self._paste_text()
            if event.keycode == 67 and event.state == 12:
                self._copy_result()

    
    def _cut_result(self):
        '''Функция вырезания'''
        try:
            self.app.text.selection_get()
        except TclError:
            showerror(title='Ошибка', message='Сначала выделите текст')
        else:
            copy(self.app.text.selection_get())
            self.app.text.delete('sel.first', 'sel.last')

    
    def _copy_result(self):
        '''Функция копирования'''
        try:
            self.app.text.selection_get()
        except TclError:
            showerror(title='Ошибка', message='Сначала выделите текст')
        else:
            copy(self.app.text.selection_get())

    
    def _paste_text(self):
        '''Функция вставки'''
        if paste() == '':
            showerror(title='Ошибка', message='Буфер обмена пуст')
        else:
            if not self.app.text.tag_ranges('sel'):
                self.app.text.insert('insert', paste())
            else:
                self.app.text.replace('sel.first', 'sel.last', paste())


    def _delete_result(self):
        '''Функция удаления'''
        try:
            self.app.text.selection_get()
        except TclError:
            showerror(title='Ошибка', message='Сначала выделите текст')
        else:
            self.app.text.delete('sel.first', 'sel.last')