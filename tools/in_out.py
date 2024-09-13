'''
Functions used for input and output
'''

def get_word_pool(file_name):
    word_file = open(file_name, "r")
    words = [word.strip() for word in word_file.readlines()]
    return words


def printl(num):
    for i in range(num):
        print("")

def percent(float):
    float = float * 100
    return str(float)+"%"