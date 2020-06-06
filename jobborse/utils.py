import re

def get_3_first_words(pharse):
    words = []
    i = 0
    for word in pharse.split():
        if re.search('^\w+$', word):
            words.append(word)
            i += 1
            if i == 3:
                break
    return ' '.join(words)