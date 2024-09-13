
class Parser:
    def __init__(self, words):
        self.words = words
        self.answer_info = [[letter.upper() for letter in "abcdefghijklmnopqrstuvwxyz"] for i in range(5)]
        self.found_letters = []

    #main function
    def update_words(self, guess, info, words, found_letters=None):
        # if words == None: words = self.words
        # if found_letters == None: found)le

        answer_info, found_letters = self.update_constraints(guess, info)
        self.apply_constraints(words, answer_info, found_letters)
        return self.words

    def update_constraints(self, guess, info, answer_info = None, found_letters = None):
        if answer_info == None: answer_info = [[letter.upper() for letter in "abcdefghijklmnopqrstuvwxyz"] for i in range(5)]
        if found_letters == None: found_letters = []
        new_found_letters = []
        for char_index in range(len(guess)):
            letter = guess[char_index]
            result = info[char_index]
            if result == "G":
                answer_info[char_index] = [letter]
                new_found_letters.append(letter)
            elif result == "Y":
                if letter in answer_info[char_index]: 
                    answer_info[char_index].remove(letter)
                new_found_letters.append(letter)
            elif result == ".":
                for information in answer_info:
                    if letter in information: information.remove(letter)

        for yletter in found_letters:
            if yletter not in new_found_letters:
                new_found_letters.append(yletter)

        self.found_letters = new_found_letters
        found_letters = new_found_letters
        self.answer_info = answer_info
        return answer_info, found_letters

    def is_valid(self, word, answer_info, found_letters):
        # if answer_info == None: answer_info = [[letter.upper() for letter in "abcdefghijklmnopqrstuvwxyz"] for i in range(5)]
        # if found_letters == None: found_letters = []

        for char_index in range(len(word)):
            letter = word[char_index]
            if letter not in answer_info[char_index]: #if the letter it this spot can't be in this spot
                return False
        word_letters = list(word)
        for letter in found_letters:
            if letter not in word_letters:
                return False
            else:
                word_letters.remove(letter) #removes matched letter for duplicates
        return True


    def apply_constraints(self, words, answer_info, found_letters):
        updated_words = []
        for word in words:
            if self.is_valid(word, answer_info, found_letters):
                updated_words.append(word)
        self.words = updated_words
        return updated_words

    def show_results(self):
        print("---Parsing results---")
        for word in self.words: print(word, end="   ")
        print("\nThere are", len(self.words), " words remaining.")
        print("The answer contains the letters ", self.found_letters)

    #given a word pool, a guess, and the result of the guess, return the percentage of words from the pool remaining
    def get_guess_effect(self, word_pool, guess, guess_result):
        answer_info, found_letters = self.update_constraints(guess, guess_result)
        # print("\tanswer info:")
        # for place in answer_info: print("\t\t",place)
        # print("\t\tfound_letters:", found_letters)
        reduced_word_pool = self.apply_constraints(word_pool, answer_info, found_letters)
        return(len(reduced_word_pool)/len(word_pool))


    # def get_guess_effect(self, words, guess, guess_result, answer_info=None, found_letters=None):
    #     initial_word_count = len(words)
    #     # self.words = words
    #     # if answer_info != None: self.answer_info = answer_info
    #     # else: 
    #     answer_info = [[letter.upper() for letter in "abcdefghijklmnopqrstuvwxyz"] for i in range(5)]
    #     # if found_letters != None: self.found_letters = found_letters
    #     # else: 
    #     found_letters = []
    #     answer_info, found_letters = self.update_constraints(guess, guess_result, answer_info, found_letters)
        
    #     return initial_word_count - len(self.apply_constraints(words, answer_info, found_letters))
