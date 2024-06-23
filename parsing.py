
class Parser:
    def __init__(self, words):
        self.words = words
        self.answer_info = [[letter.upper() for letter in "abcdefghijklmnopqrstuvwxyz"] for i in range(5)]
        self.found_letters = []

    #main function
    def update_words(self, guess, info):
        self.update_constraints(guess, info)
        self.apply_constraints()
        return self.words

    def update_constraints(self, guess, info):
        new_found_letters = []
        for char_index in range(len(guess)):
            letter = guess[char_index]
            result = info[char_index]
            if result == "G":
                self.answer_info[char_index] = [letter]
                new_found_letters.append(letter)
            elif result == "Y":
                if letter in self.answer_info[char_index]: 
                    self.answer_info[char_index].remove(letter)
                new_found_letters.append(letter)
            elif result == ".":
                for information in self.answer_info:
                    if letter in information: information.remove(letter)

        for yletter in self.found_letters:
            if yletter not in new_found_letters:
                new_found_letters.append(yletter)

        self.found_letters = new_found_letters

    def is_valid(self, word):
        for char_index in range(len(word)):
            letter = word[char_index]
            if letter not in self.answer_info[char_index]:
                return False
        word_letters = list(word)
        for letter in self.found_letters:
            if letter not in word_letters:
                return False
            else:
                word_letters.remove(letter) #removes matched letter for duplicates
        return True


    def apply_constraints(self):
        updated_words = []
        for word in self.words:
            if self.is_valid(word):
                updated_words.append(word)
        self.words = updated_words

    def show_results(self):
        print("---Parsing results---")
        for word in self.words: print(word, end="   ")
        print("\nThere are", len(self.words), " words remaining.")
        print("The answer contains the letters ", self.found_letters)