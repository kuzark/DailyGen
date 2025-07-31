from tkinter import ttk
from tkinter import SUNKEN, W
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
        self.complaints.grid(row=0, columnspan=2, **self.margins)

        # Ввод и форматирование текста жалоб
        text_handler = TextHandler(self.complaints)
        text_handler.text_add(default_content, 'main')
        text_handler.paragraphs_selector()


class AnamnesisTab(ConstructorTab):
    '''Вкладка с анамнезом'''

    def __init__(self, note, margins):
        super().__init__(note, margins)

        default_content = 'Анамнез заболевания: с анамнезом '
        default_content += 'ознакомлен, дополнений нет.'

        # Поле ввода для анамнеза
        self.anamnesis = TextSpace(self)
        self.anamnesis.config(**self.text_size)
        self.anamnesis.grid(row=0, columnspan=2, **self.margins)

        # Ввод и форматирование текста жалоб
        text_handler = TextHandler(self.anamnesis)
        text_handler.text_add(default_content, 'main')
        text_handler.paragraphs_selector()

        # Кнопка для составления кастомного анамнеза
        ttk.Button(
            self, text='Составить анамнез...').grid(
                row=1, column=0, sticky=W, **self.margins
            )
        
        


