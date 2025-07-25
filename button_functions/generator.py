import random
import re
from settings import Settings
from handlers.text_handler import TextHandler

class Generator:
    '''Класс для генерации дневника'''
    def __init__(self, app):
        # Список вкладок
        self.tabs = app.notebook.tab_frames
        # Индекс текущей вкладки
        self.note_index = app.notebook.index(app.notebook.select())
        # Экземпляр формы для выбора схемы лечения
        self.treatment_form = app.treatment_form
        # Текст из текстового поля
        self.dnevnic = app.text.get('1.0', 'end')
        # Проверка наличия гипертонической болезни
        self.gypertonic = app.enabled_gypertonic.get()
        # Инициализация настроек
        self.settings = Settings()
        # Инициализация обработчика текста
        text_handler = TextHandler(app.text)
        
        # Генерация дневника
        self._generate_title()
        self._generate_week_period()
        self._generate_week_number()
        self._generate_RR()
        self._generate_HR()
        self._generate_BP()
        self._generate_treatment()
        self._generate_signature()

        # Вставка сгенерированного дневника
        app.text.delete('1.0', 'end')
        app.text.insert('1.0', self.dnevnic)
        app.text.tag_add('main' ,'1.0', 'end')
        app.text.tag_add('title' ,'1.0', '2.0')

        # Форматирование дневника
        text_handler.empty_strings_cutter()
        text_handler.paragraphs_selector()

        
    def _generate_title(self):
        '''Генерация заголовка дневника'''
        # Список заголовков
        long_str = 'Совместный осмотр врача-инфекциониста '
        long_str += 'с заведующим отделения'
        titles = [
            'Ежедневный осмотр врача-инфекциониста',
            'Осмотр дежурного врача-инфекциониста',
            long_str
        ]
        
        # Генерация заголовка
        founded_title = False
        for title in titles:
            if self.dnevnic.find(title) != -1:
                idx = self.dnevnic.find(title)
                self.dnevnic = self.dnevnic.replace(
                    self.dnevnic[:idx + len(title)], 
                    self.tabs[self.note_index].day_dnevnic_type.get(), 1
                )
                founded_title = True
        if not founded_title:
            self.dnevnic = self.tabs[self.note_index].day_dnevnic_type.get() \
                + 2 * '\n' + self.dnevnic


    def _generate_week_period(self):
        '''Генерация периода недели'''
        periods = self.tabs[self.note_index].periods
        for period in periods:
            if self.dnevnic.find(period) != -1:
                idx = self.dnevnic.find(period)
                self.dnevnic = self.dnevnic.replace(
                    self.dnevnic[idx:idx + len(period)], 
                    self.tabs[self.note_index].day_week_period.get(), 1
                )
    

    def _generate_week_number(self):
        '''Генерация номера недели'''
        if self.dnevnic.find('недели') != -1:
            idx = self.dnevnic.find('недели')
            first_symbol_idx_count = 5
            if self.dnevnic[idx - 5] == ' ':
                first_symbol_idx_count -= 1
            self.dnevnic = self.dnevnic.replace(
                self.dnevnic[idx - first_symbol_idx_count:idx - 1], 
                str(self.tabs[self.note_index].day_week_num.get()) + '-й', 1
            )


    def _generate_RR(self):
        '''Генерация ЧДД'''
        rr = str(random.randint(16, 20))
        idx = self.dnevnic.find('в мин')
        self.dnevnic = self.dnevnic.replace(
            self.dnevnic[idx - 3:idx + 5], rr + ' в мин', 1
        )

    
    def _generate_HR(self):
        '''Генерация ЧСС'''
        pulse = str(random.randint(68, 90))
        idx = self.dnevnic.find('/мин')
        self.dnevnic = self.dnevnic.replace(
            self.dnevnic[idx - 2:idx + 1], pulse + '/', 2
        )

    
    def _generate_BP(self):
        '''Генерация АД'''
        if self.gypertonic == 0:
            # Генерация нормального давления
            pressure = f'{str(random.randrange(110, 125, 5))}/'
            pressure += f'{str(random.randrange(70, 85, 5))}'
        else:
            # Генерация повышенного давления
            pressure = f'{str(random.randrange(120, 145, 5))}/'
            pressure += f'{str(random.randrange(80, 95, 5))}'
        # Вставка сгенерированного давления в дневник
        idx = self.dnevnic.find('АД')
        self.dnevnic = self.dnevnic.replace(
            self.dnevnic[idx + 3:idx + 9], pressure, 1
        )


    def _generate_treatment(self):
        '''Генерация схемы лечения'''
        epclusa = self.settings.treatment['Эпклюза']['recomendation']
        pattern = self.settings.treatment['Эпклюза + РБВ']['recomend_pattern']
        ribavirin = self.settings.treatment['Эпклюза + РБВ']['recomendation']
        # Получение выбранного пользователем лечения
        chosen_treatment = self.treatment_form.treatment_var.get()
        
        # Запуск цикла перебора схем лечения
        fragment_have_founded = False
        for scheme, treatment in self.settings.treatment.items():
            # Если фрагмент найден, остановка цикла
            if fragment_have_founded == True:
                break
            # Поиск строки недели
            key = 'week'
            if self.dnevnic.find(treatment[key]) != -1:
                fragment_have_founded = True
                start_idx = self.dnevnic.find(treatment[key])
            
                # Замена строки недели
                self.dnevnic = self.dnevnic.replace(
                    self.dnevnic[start_idx:start_idx + len(treatment[key])],
                    self.settings.treatment[chosen_treatment][key], 1
                )

            # Пропускаем схему лечения 'Эпклюза + РБВ'
            if scheme == 'Эпклюза + РБВ':
                break

            # Поиск строки рекомендаций
            key = 'recomendation'
            if self.dnevnic.find(treatment[key]) != -1:
                fragment_have_founded = True
                # Вычисляем начало строки найденного фрагмента
                start_idx = self.dnevnic.find(treatment[key])
                
                # Если нашли Эпклюзу, проверяем наличие Рибавирина
                if treatment[key] == epclusa:
                    match = re.search(pattern, self.dnevnic)
                    if match:
                        # Если нашли Рибавирин, 
                        # вычисляем индекс окончания рекомендаций
                        end_idx = match.end()
                        
                        # Замена рекомендаций
                        self.dnevnic = self.dnevnic.replace(
                            self.dnevnic[start_idx:end_idx],
                            self.settings.treatment[chosen_treatment][key], 1
                        )

                # Замена рекомендаций
                # Если выбрана схема с Рибавирином
                if chosen_treatment == 'Эпклюза + РБВ':
                    # Расчет разовых доз Рибавирина
                    morning, evening = self.ribavirin_doses_calculate()
                    # Замена строки
                    self.dnevnic = self.dnevnic.replace(
                        self.dnevnic[start_idx:start_idx + len(treatment[key])],
                        ribavirin.format(morning=morning, evening=evening), 1
                    )
                
                # Если иная схема лечения
                else:
                    self.dnevnic = self.dnevnic.replace(
                        self.dnevnic[start_idx:start_idx + len(treatment[key])],
                        self.settings.treatment[chosen_treatment][key], 1
                    )


    def ribavirin_doses_calculate(self):
        '''Расчитывает утреннюю и вечернюю дозу Рибавирина'''
        capsuls = self.treatment_form.ribavirin_count.get()
        morning = capsuls // 2
        evening = morning + capsuls % 2
        return morning, evening


    def _generate_signature(self):
        '''Генерация строки для подписи врача'''
        # Замена даты
        if self.dnevnic.find('Врач-инфекционист') != -1:
            idx = self.dnevnic.find('Врач-инфекционист')
            self.dnevnic = self.dnevnic.replace(
                self.dnevnic[idx - 12:idx - 4], 
                self.tabs[self.note_index].day_now_date.get(), 1
            )

        # Замена ФИО врача
        if self.dnevnic.find('__/') != -1:
            idx = self.dnevnic.find('__/')
            self.dnevnic = self.dnevnic.replace(
                self.dnevnic[idx + 3:], 
                self.tabs[self.note_index].day_selected_doctor.get() + '/', 1
            )

        # Добавление пустых строк в конец
        self.dnevnic = self.dnevnic + 2 * '\n'
