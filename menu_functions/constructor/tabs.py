from tkinter import ttk
from tkinter import SUNKEN
from forms.text_space import TextSpace
from handlers.text_handler import TextHandler


class ConstructorTab(ttk.Frame):
    '''Класс для построения вкладок для конструктора'''
    def __init__(self, note, margins):
        super().__init__(note, relief=SUNKEN)
        self.note = note
        self.margins = margins

        # Настройки текстового поля
        self.text_size = {
            'width': 80,
            'height': 3,
        }


class ComplaintsTab(ConstructorTab):
    '''Вкладка с жалобами'''

    def __init__(self, note, margins):
        super().__init__(note, margins)

        default_content = 'Жалобы: активных не предъявляет. Явления '
        default_content += 'кровоточивости любых локализаций, дискомфорт '
        default_content += 'в правом подреберье отрицает.'

        # Поле ввода для жалоб
        self.complaints = TextSpace(self)
        self.complaints.config(**self.text_size)
        self.complaints.grid(row=0, column=1, **self.margins)

        # Ввод и форматирование текста жалоб
        text_handler = TextHandler(self.complaints)
        text_handler.text_add(default_content, 'main')
        text_handler.paragraphs_selector()

        
        


