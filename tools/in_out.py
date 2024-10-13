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

def percent(float, decimal_places=-1):
    float = float * 100
    if (decimal_places > -1):
        float = round(float, decimal_places)
    return str(float)+"%"


def print_word_pool(ans_pool):
    for row_starting_index in range(0, len(ans_pool), 12): # Row is 12 words
        row_ending_index = min(row_starting_index+12, len(ans_pool))
        row = ans_pool[row_starting_index:row_ending_index]
        print("\t", end = "")
        for word in row:
            print(word, end=" ")
        print()