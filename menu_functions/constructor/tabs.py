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


class ComplaintsTab(ConstructorTab):
    '''Вкладка с жалобами'''

    def __init__(self, note, margins):
        super().__init__(note, margins)

        default_content = 'Жалобы: активных не предъявляет. Явления '
        default_content += 'кровоточивости любых локализаций, дискомфорт '
        default_content += 'в правом подреберье отрицает.'

        # Поле ввода для жалоб
        self.complaints = self.text_space_create(self)

        # Ввод и форматирование текста жалоб
        self.text_add(self.complaints, default_content)


class AnamnesisTab(ConstructorTab):
    '''Вкладка с анамнезом'''

    def __init__(self, note, margins):
        super().__init__(note, margins)

        default_content = 'Анамнез заболевания: с анамнезом '
        default_content += 'ознакомлен, дополнений нет.'

        # Поле ввода для анамнеза
        self.anamnesis = self.text_space_create(self)

        # Ввод и форматирование текста жалоб
        self.text_add(self.anamnesis, default_content)

        # Кнопка для составления кастомного анамнеза
        ttk.Button(
            self, text='Составить анамнез...').grid(
                row=1, column=0, sticky=W, **self.margins
            )


class ExaminationTab(ConstructorTab):
    '''Вкладка с осмотром'''
    def __init__(self, note, margins):
        super().__init__(note, margins)

        default_content = (
            'Настоящее состояние: удовлетворительное.\n'
            'Кожные покровы, склеры и видимые слизистые: '
            'физиологической окраски, чистые.\n'
            'Антропометрические данные: вес 63 кг, рост 164 см.\n'
            'Дыхательная система: дыхание через нос свободное, ЧДД 17 в мин.'
            'Грудная клетка соответствует конституции, равномерно участвует '
            'в акте дыхания. Дыхание везикулярное. Хрипов аускультативно нет.\n'
            'Сердечно-сосудистая система: тоны сердца '
            'ясные, ритмичные. Шумов сердца нет.'
            'Верхушечный толчок нормальный. ЧСС – 74/мин. Пульс – 74/мин. '
            'Дефицита пульса нет. АД 120/80 мм. рт. ст.\n'
            'Пищеварительная система: язык влажный, чистый. Живот не вздут, '
            'симметричный, участвует в акте дыхания, мягкий, безболезненный '
            'при пальпации. Печень по краю реберной дуги, селезенка не '
            'пальпируется. Стул регулярный, оформленный, '
            'без патологических примесей.\n'
            'Мочевыделительная система: диурез со слов достаточный. '
            'Симптом Пастернацкого отрицательный с обеих сторон. '
            'Мочеиспускание не учащено, безболезненно, не затруднено. '
            'Отеков нет.\n'
        )
        

        


