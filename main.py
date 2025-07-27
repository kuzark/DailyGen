from tkinter import Tk, IntVar
from tkinter import FALSE, EW, SUNKEN, W, NS
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import askyesnocancel
from pathlib import Path

# Мои модули
from settings import Settings
from forms.day_params_form import NoteBook
from forms.treatment_form import TreatmentForm
from menus import MainMenu, ContextMenu
from button_functions.generator import Generator
from button_functions.html_conventer import HTMLConventer


class DnevnicApp(Tk):
    '''Основное окно приложения'''

    def __init__(self):
        '''Инициализирует приложение'''
        super().__init__()

        # Настройки основного окна
        self.title('Генератор дневников')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.exit)
        self.option_add("*tearOff", FALSE)
        
        # Инициализация настроек и данных программы
        self.settings = Settings()

        # Создание виджетов
        self.create_widgets()

        # Установка главного меню
        self.config(menu=MainMenu(self))

        # Установка контекстного меню
        self.context_menu = ContextMenu(self)

            
    def exit(self):
        '''Действия при закрытии главного окна'''
        result_file = Path('result.html')
        content = 'Вы уверены, что хотите закрыть программу? '
        content += 'Несохраненные данные будут утеряны.'
        answer = askyesnocancel(
            title='Подтверждение', 
            message=content,
            icon='warning'
        )
        if answer:
            # Удаление файла при закрытии главного окна
            if result_file.exists():
                result_file.unlink()
            # Закрытие окна
            self.destroy()

    
    def create_widgets(self):
        '''Создание интерфейса'''
        # Форма с вкладками для выбора заголовка, даты, врача, дня и недели
        self.notebook = NoteBook(self)
        self.notebook.grid(
            row=0, column=0, padx=10, pady=5, sticky=EW, columnspan=2
        )

        # Форма наличия гипертонической болезни
        frame_gypertonic = ttk.Frame(relief=SUNKEN)
        self.enabled_gypertonic = IntVar(value=0)
        ttk.Checkbutton(
            frame_gypertonic, 
            text='Гипертоническая болезнь', 
            variable=self.enabled_gypertonic
        ).grid(row=0, column=0, sticky=W, **self.settings.margins)
        frame_gypertonic.grid(
            row=1, 
            column=0, 
            columnspan=2, 
            sticky=EW, 
            **self.settings.margins
        )

        # Область для работы с текстом
        self.text = ScrolledText(self, width=110, wrap='word', undo=True)
        self.text.grid(
            row=0, column=2, rowspan=5, columnspan=3, pady=6, sticky=NS
        )
        
        # Установка шрифтов
        self.text.tag_configure('main', font=self.settings.font_usual)
        self.text.tag_configure(
            'main_underlined', 
            font=self.settings.font_usual_underlined
        )
        self.text.tag_configure('title', font='Times_New_Roman 12 bold')
        self.text.tag_configure('subtitle', font=self.settings.font_bold)
        self.text.tag_configure(
            'subtitle_underlined', 
            font=self.settings.font_bold_underlined
        )
        self.text.tag_configure(
            'italic', 
            font=self.settings.font_italic
        )
        self.text.tag_configure(
            'italic_underlined', 
            font=self.settings.font_italic_underlined
        )
        self.text.tag_configure('paragraph')
        
        # Установка событий нажатия клавиш
        self.text.bind(
            '<Control-KeyPress>', 
            lambda event: self.context_menu.ctrl_C_V(event)
        )
        self.text.bind(
            '<Button-3>', 
            lambda event: self.context_menu.post(event.x_root, event.y_root)
        )

        # Форма выбора схемы лечения
        self.treatment_form = TreatmentForm(self)
        self.treatment_form.grid(
            row=2, column=0, columnspan=2, padx=10, pady=5, sticky=EW
        )

        # Установка пустого фрейма
        ttk.Frame(height=175).grid(row=3)

        # Кнопки главной панели
        ttk.Button(
            text="Сгенерировать",
            command=lambda: Generator(self)
        ).grid(row=4, column=0, padx=10, pady=10)

        ttk.Button(
            text='Сохранить',
            command=lambda: HTMLConventer(self.text)
        ).grid(row=4, column=1, padx=10, pady=10)

        
# Запуск цикла событий приложения
if __name__ == '__main__':
    app = DnevnicApp()
    app.mainloop()
