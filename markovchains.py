import numpy as np


def add_alphabetically(lst, word):
    ''' Add word in lst in case that it does not exist in lst yet,
        and such that the alphabetical order is respected. '''

    for index, item in enumerate(lst):
        if item == word:
            return lst
        elif item > word:
            return lst[:index] + [word] + lst[index:]

    return lst + [word]


def get_couples(text):
    '''
    '''

    words_by_index = [""]
    couples = {}
    splitted_text = text.split()

    for word in splitted_text:
        words_by_index = add_alphabetically(words_by_index, word)

    for index, word in enumerate(words_by_index):
        couples[word] = []

    last_word = ""
    for word in splitted_text:
        couples[last_word].append(word)

        if word[-1] == "." or word[-1] == "?" or word[-1] == "!":
            couples[word].append("")
            last_word = ""
        else:
            last_word = word

    return couples


def generate_sentence(couples):
    '''
    '''

    chain = []
    last_word = ""

    while last_word == "" or (last_word[-1] != "." and last_word[-1] != "?" and \
        last_word[-1] != "!"):

        last_word = np.random.choice(couples[last_word])
        chain.append(last_word)

    return " ".join(chain)


text = open("Trump Speech.txt").read()
couples = get_couples(text)
for i in range(10):
    print(generate_sentence(couples))


