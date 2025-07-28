import requests
import sys
from tkinter.messagebox import showerror, showinfo
from pyperclip import copy

class UpdateApp:
    '''Класс для проверки обновлениий приложения'''
    def __init__(self):
        # Текущая версия
        self.current_version = 'v0.2.0'
        
        # Ссылка на страницу с релизами
        self.releases_url = 'https://api.github.com/repos/'
        self.releases_url += 'kuzark/DailyGen/releases/latest'
        
        # Получение последней версии и ссылки на релиз
        self.latest_version, self.latest_release_url = self._get_latest_version()

        # Проверка на совпадение версий
        self._check_update()

    
    def _get_latest_version(self):
        '''Получение последней версии'''
        try:
            # Попытка получения версии тега и ссылки на релиз
            response = requests.get(self.releases_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data['tag_name'], data['html_url']
        except requests.RequestException as err:
            # При возниконовении ошибки вывод окна с ошибкой
            err_msg = f'Ошибка! Код: {err}'
            showerror(title='Ошибка', message=err_msg)
            sys.exit()

    
    def _check_update(self):
        '''Сравнивает версии, если полученная версия новее, 
        предлагает скачать по ссылке'''
        if self.latest_version != self.current_version:
            
            # Копирование ссылки в буфер обмена
            copy(self.latest_release_url)

            # Вывод сообщения о новой версии
            msg = f'Скачайте новую версию по ссылке: {self.latest_release_url}'
            msg += '\nСсылка скопирована в буфер обмена'
            showinfo(title='Вышла новая версия', message=msg)
            
            # Выход из приложения
            sys.exit()

            


