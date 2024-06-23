from parsing import Parser

def get_words_file():
    raw_words = open("raw_words.txt").readlines()
    raw_words = sorted(raw_words)
    raw_words = [word.upper() for word in raw_words]
    new_words = open("words.txt", "w")
    new_words.write("".join(raw_words))

def user_guess():
    guess = input("What is your next guess? ")
    while len(guess) != 5 or not guess.isalpha():
        guess = input("Guess isn't valid. What is your next guess? ")
    return guess.upper()

def user_guess_result():
    # info = input("Enter the result of the guess. Write your guess putting \"Y\" in place of a yellow character, \"G\" in place of a green character and \".\" in place of a grey character. \n \t Guess result: ")
    info = input("What was the result?     ")
    while len(info) != 5:
        info = input("Invalid. Please enter again: ")
    return info.upper()




def main():
    word_file = open("words.txt", "r")
    words = [word.strip() for word in word_file.readlines()]

    parser = Parser(words)

    word_found = False
    while len(words) > 1:
        guess = user_guess()
        info = user_guess_result()

        words = parser.update_words(guess, info)
        # parser.show_results()


    print(words[0], "is the word!")
main()

