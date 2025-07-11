from settings import Settings

class TextHandler:
    '''Класс для добавления и форматирования текста'''
    def __init__(self, text):
        # Доступ к текстовому полю
        self.text = text
        # Инициализация настроек
        self.settings = Settings()


    def text_add(self, content, tag):
        '''Добавляет и форматирует текст'''
        pos = self.text.index('insert')
        self.text.insert(pos, content)
        end_pos = self.text.index('insert')
        self.text.tag_add(tag, pos, end_pos)

    
    def empty_strings_cutter(self):
        '''Убирает лишние пустые строки'''
        pos = self.text.index('end')
        if pos[1] == '.':
            for i in range(1, int(pos[0])):
                if self.text.get(f'{str(i)}.0', f'{str(i)}.1') == '':
                    for _ in range(i + 1, int(pos[0])):
                        if self.text.get(
                            f'{str(i + 1)}.0', f'{str(i + 1)}.1') == '':
                            self.text.delete(
                                f'{str(i + 1)}.0', f'{str(i + 2)}.0')
                        else:
                            break
        else:
            for i in range(1, int(pos[:2])):
                if self.text.get(f'{str(i)}.0', f'{str(i)}.1') == '':
                    for _ in range(i + 1, int(pos[:2])):
                        if self.text.get(
                            f'{str(i + 1)}.0', f'{str(i + 1)}.1') == '':
                            self.text.delete(
                                f'{str(i + 1)}.0', f'{str(i + 2)}.0')
                        else:
                            break
    

    def paragraphs_selector(self):
        '''Выделяет выбранные абзацы'''
        i = 0
        for value in self.settings.paragraph_names.values():
            pos = self.text.search(value, '1.0', stopindex='end')
            if pos:
                if pos[1] == '.':
                    end = pos[0] + '.' + str(len(value))
                else:
                    end = pos[:2] + '.' + str(len(value))
                self.text.tag_add('subtitle', pos, end)
            i += 1