from webbrowser import open_new_tab

class HTMLConventer:
    '''Класс для преобразования формата текста в код HTML'''
    def __init__(self, text):
        # Переменная для хранения сгенерированного кода HTML
        self.html_code = ''

        # Словарь тегов виджета и html
        self.tag_to_html = {
            ('tagon', 'title'): '<b><h3>',
            ('tagoff', 'title'): '</b></h3>',
            ('tagon', 'subtitle'): '<b>',
            ('tagoff', 'subtitle'): '</b>',
            ('tagon', 'italic'): '<i>',
            ('tagoff', 'italic'): '</i>',
            ('tagon', 'main_underlined'): '<u>',
            ('tagoff', 'main_underlined'): '</u>',
            ('tagon', 'subtitle_underlined'): '<b><u>',
            ('tagoff', 'subtitle_underlined'): '</u></b>',
            ('tagon', 'italic_underlined'): '<i><u>',
            ('tagoff', 'italic_underlined'): '</u></i>',
            ('tagon', 'paragraph'): '<p>',
            ('tagoff', 'paragraph'): '</p>'
        }
        
        # Генерация кода HTML и сохранение в файл
        self._paragraph_maker(text)
        self._text_to_HTML(text)
        self._file_creator()

        # Открытие файла в браузере
        open_new_tab('result.html')


    def _paragraph_maker(self, text):
        '''Выделение параграфов в тексте'''
        pos = text.index('end')
        if pos[1] == '.':
            for i in range(1, int(pos[0]) + 2):
                if text.get(f'{str(i)}.0', f'{str(i)}.1') == '':
                    for j in range(i + 1, int(pos[0]) + 2):
                        if text.get(f'{str(j)}.0', f'{str(j)}.1') == '':
                            text.tag_add(
                                'paragraph', f'{str(i + 1)}.0', f'{str(j)}.1')
                            break
        else:
            for i in range(1, int(pos[:2]) + 2):
                if text.get(f'{str(i)}.0', f'{str(i)}.1') == '':
                    for j in range(i + 1, int(pos[:2]) + 2):
                        if text.get(f'{str(j)}.0', f'{str(j)}.1') == '':
                            text.tag_add(
                                'paragraph', f'{str(i + 1)}.0', f'{str(j)}.1')
                            break

    
    def _text_to_HTML(self, text):
        '''Перевод текста в код HTML'''
        content = text.dump('1.0', 'end', tag=True, text=True)
        html_text = []
        for key, value, _ in content:
            if key == "text":
                html_text.append(value)
            else:
                html_text.append(self.tag_to_html.get((key, value), ''))
        self.html_code = ''.join(html_text)
        self.html_code = self.html_code.replace('\n', '<br>')

    
    def _file_creator(self):
        '''Сохранение сгенерированного кода в файл'''
        with open('result.html', 'w') as file:
            file.write(self.html_code)