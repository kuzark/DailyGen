from tkinter import ttk, StringVar, IntVar, Text
from tkinter import SUNKEN, W, E
from datetime import datetime
from forms.text_space import TextSpace
from handlers.text_handler import TextHandler
from settings import Settings
from button_functions.generator import Generator


class ConstructorTab(ttk.Frame):
    '''Класс для построения вкладок для конструктора'''
    def __init__(self, note, margins):
        super().__init__(note, relief=SUNKEN)
        self.note = note
        self.margins = margins

        # Инициализация настроек
        self.settings = Settings()

        # Настройки текстового поля
        self.text_size = {
            'width': 80,
            'height': 20,
        }

    
    def text_space_create(self, tab_frame):
        '''Создание текстового поля'''
        text_space = TextSpace(tab_frame)
        text_space.config(**self.text_size)
        text_space.grid(row=0, columnspan=2, **self.margins)
        return text_space

    
    def text_add(self, text_space, content):
        '''Ввод и форматирование текста'''
        text_handler = TextHandler(text_space)
        text_handler.text_add(content, 'main')
        text_handler.paragraphs_selector()
    

    def add_custom_button(self, button_name):
        '''Добавление кнопки для создания кастомного элемента'''
        ttk.Button(
            self, text=button_name).grid(
                row=1, column=0, sticky=W, **self.margins
            )


class ComplaintsTab(ConstructorTab):
    '''Вкладка с жалобами'''

    def __init__(self, note, margins):
        super().__init__(note, margins)

        default_content = 'Жалобы: активных не предъявляет. Явления '
        default_content += 'кровоточивости любых локализаций, дискомфорт '
        default_content += 'в правом подреберье отрицает.'

        # Поле ввода для жалоб
        self.text = self.text_space_create(self)
        self.text.config(height=3)

        # Ввод и форматирование текста жалоб
        self.text_add(self.text, default_content)


class AnamnesisTab(ConstructorTab):
    '''Вкладка с анамнезом'''

    def __init__(self, note, margins):
        super().__init__(note, margins)

        default_content = 'Анамнез заболевания: с анамнезом '
        default_content += 'ознакомлен, дополнений нет.'

        # Поле ввода для анамнеза
        self.text = self.text_space_create(self)

        # Ввод и форматирование текста анамнеза
        self.text_add(self.text, default_content)

        # Кнопка для составления кастомного анамнеза
        self.add_custom_button('Составить анамнез...')


class ExaminationTab(ConstructorTab):
    '''Вкладка с осмотром'''
    def __init__(self, note, margins):
        super().__init__(note, margins)

        # Текст объективного осмотра
        default_content = self.settings.examination
        
        # Поле ввода для осмотра
        self.text = self.text_space_create(self)

        # Ввод и форматирование текста осмотра
        self.text_add(self.text, default_content)

        # Кнопка для составления кастомного осмотра
        self.add_custom_button('Составить осмотр...')


class RecomendationsTab(ConstructorTab):
    '''Вкладка с рекомендациями'''
    def __init__(self, note, margins, app):
        super().__init__(note, margins)

        # Выбранная схема лечения
        self.treatment_chosen = app.treatment_form.treatment_var.get()
        
        # Поле ввода для рекомендаций
        self.text = self.text_space_create(self)
        self.text.config(height=13)

        # Список типов рекомендаций
        self.recomendations_types = [
            'Рекомендации для дневника',
            'Рекомендации при приеме пациента на ДС',
            'Рекомендации при направлении на ДС'
        ]

        # Переменная для хранения выбранного типа рекомендаций
        self.recomendations_type_chosen = StringVar(
            value=self.recomendations_types[0]
        )

        # Интерфейс выбора рекомендаций
        # Кнопки выбора типа рекомендаций
        row = 1
        for recomendations_type in self.recomendations_types:
            ttk.Radiobutton(
                self,
                text=recomendations_type,
                value=recomendations_type,
                variable=self.recomendations_type_chosen,
                command=lambda: self._content_create(app)
            ).grid(
                row=row, sticky=W, columnspan=2, **self.margins
            )
            row += 2
        
        # Интерфейс с характеристиками рекомендаций при приеме на ДС
        ttk.Label(self, text='Дата ВК:').grid(
            row=4, column=0, sticky=W, **self.margins
        )

        # Дата врачебной коммиссии
        now = datetime.today()
        self.date_med_commission = StringVar(value=now.strftime('%d.%m.%y'))
        ttk.Entry(self, textvariable=self.date_med_commission, width=7).grid(
            row=4, column=0, **self.margins
        )

        # Чек-бокс на наличие цирроза
        self.cirrhosis = IntVar(value=0)
        ttk.Checkbutton(self, text='Цирроз', variable=self.cirrhosis).grid(
            row=4, column=1, sticky=W, **self.margins
        )

        # Поле для ввода совместимых препаратов
        ttk.Label(self, text=(
            'Совместимые препараты (если отсутствуют, оставьте поле пустым):'
        )).grid(
            row=6, sticky=W, **self.margins
        )
        self.medicines = Text(self, width=83, height=3)
        self.medicines.grid(row=7, columnspan=2, **self.margins)

        # Ввод и форматирование текста рекомендаций
        self._content_create(app)
        

    def _content_create(self, app):
        '''Создание и ввод строки рекомендаций'''
        # Получение выбранной схемы лечения
        scheme = self.settings.treatment[self.treatment_chosen]['week']
        course = self.settings.treatment[self.treatment_chosen]['course']
        key = 'recomendation'
        treatment = self.settings.treatment[self.treatment_chosen][key]
        if self.treatment_chosen == 'Эпклюза + РБВ':
            morning, evening = Generator(app).ribavirin_doses_calculate()
            treatment = treatment.format(morning=morning, evening=evening)
        
        # Очистка текстового поля
        self.text.delete('1.0', 'end')

        # Выбранный пользователем тип рекомендаций
        recomendations_type = self.recomendations_type_chosen.get()
        
        # Формирование рекомендаций для дневника
        if recomendations_type == self.recomendations_types[0]:
            content = '\nЛечение продолжить согласно листу назначений:\n'
            content += treatment

        # Формирование рекомендаций при приеме пациента на ДС
        elif recomendations_type == self.recomendations_types[1]:
            date = self.date_med_commission.get()
            recomendations = self.settings.recomendations_admission
            
            content = '\nРекомендации:\n'
            content += recomendations['begin'].format(
                date=date, scheme=scheme[:-2], course=course
            )
            if self.cirrhosis.get() == 1:
                content += recomendations['coagulogram']
            content += recomendations['end'].format(
                treatment=treatment
            )

        # Формирование рекомендаций при направлении на ДС
        else:
            recomendations = self.settings.recomendations_ambulance
            medicines = self.medicines.get('1.0', 'end-1c')
            content = '\nНазначения:\n'
            
            if medicines:
                content += recomendations['begin']
                content += recomendations['medicines'].format(
                    medicines=medicines
                )
                content += recomendations['end'].format(
                    treatment=scheme, weeks=course
                )
            else:
                content += recomendations['begin']
                content += recomendations['end'].format(
                    treatment=scheme, weeks=course
                )

        # Ввод и форматирование текста рекомендаций
        self.text_add(self.text, content)


class DiagnosisTab(ConstructorTab):
    '''Вкладка с диагнозом'''
    def __init__(self, note, margins):
        super().__init__(note, margins)
        
        default_content = 'Диагноз:' + 2 * '\n'

        # Поле ввода для диагноза
        self.text = self.text_space_create(self)
        self.text.config(height=9)

        # Ввод и форматирование текста диагноза
        self.text_add(self.text, default_content)

        # Кнопка для составления кастомного диагноза
        self.add_custom_button('Составить диагноз...')

        ttk.Label(self, text='Добавить:').grid(
            row=1, column=0, sticky=E, **self.margins
        )
        
        # Кнопка для добавления 1-го обоснования
        ttk.Button(
            self, 
            text='1-ое обоснование',
            command=lambda: self.text_add(
                self.text, self.settings.diagnosis_arguments[0]
            )
        ).grid(
            row=1, column=1, sticky=W, **self.margins
        )
        
        # Кнопка для добавления 2-го обоснования
        ttk.Button(
            self, 
            text='2-ое обоснование',
            command=lambda: self.text_add(
                self.text, self.settings.diagnosis_arguments[1]
            )
        ).grid(
            row=1, column=1, sticky=E, **self.margins
        )


