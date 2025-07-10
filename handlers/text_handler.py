class TextHandler:
    '''Класс для добавления и форматирования текста'''
    def __init__(self, text):
        # Доступ к текстовому полю
        self.text = text


    def word_select(self, text, pos, word):
        '''Выделяет слово'''
        if pos[1] == '.':
            end = pos[0] + '.' + str(len(word))
        else:
            end = pos[:2] + '.' + str(len(word))
        text.tag_add('subtitle', pos, end)


    def text_add(self, content, tag):
        '''Добавляет и форматирует текст'''
        pos = self.text.index('insert')
        self.text.insert(pos, content)
        end_pos = self.text.index('insert')
        self.text.tag_add(tag, pos, end_pos)