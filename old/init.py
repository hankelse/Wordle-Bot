from parsing import Parser
from analyzing import Analyzer
import time


def get_letter_freqs(words):
    letters = {letter : 0 for letter in "abcdefghijklmnopqrstuvwxyz".upper()}
    for word in words:
        for letter in word:
            letters[letter] += 1
    

        scores = list(sorted(letters.items(), key=lambda kv: [kv[1], kv[0]]))

    print("\n\n RESULTS:")
    for place in range(20):
        print(place, scores[place][0], letters[scores[place][0]])

    


def get_words_file():
    raw_words = open("./raw_words.txt").readlines()
    raw_words = sorted(raw_words)
    raw_words = [word.upper() for word in raw_words]
    words = raw_words

    new_words = open("./valid_guesses.txt", "w")
    new_words.write("".join(words))
    
    raw_words = open("./raw_possible_ans.txt").readlines()
    raw_words = sorted(raw_words)
    raw_words = [word.upper() for word in raw_words]
    words = raw_words

    new_words = open("./valid_answers.txt", "w")
    new_words.write("".join(words))

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

#Given a guess and an answer pool, it returns the average percentage of answers the guess eliminates for some answer in the pool
def test_guess(guess, answer_pool):
    analyzer = Analyzer(None, None)
    parser = Parser(None)
    average_info = 0
    for answer in answer_pool:
        result = analyzer.simulate_guess_result(guess, answer)
        percentage_eliminated = 100 - parser.get_guess_effect(answer_pool, guess, result)*100
        average_info += percentage_eliminated
    return(average_info/len(answer_pool))


#Get word pools
#Potential Answers: can't end in Ss
#First Guesses: no duplicated letters, no J,Q,Z,X
#Valid Guesses: all words
def get_word_pools():
    word_file = open("./valid_guesses.txt", "r")
    all_words = [word.strip() for word in word_file.readlines()]
    pot_ans = []
    first_guesses = []
    for word in all_words:
        good_guess = True
        for letter in word:
            if word.count(letter) > 1:
                good_guess = False
            if letter in "JQZXVWK":
                good_guess = False
        if good_guess:
            first_guesses.append(word)
    
    word_file = open("valid_answers.txt", "r")
    pot_ans = [word.strip() for word in word_file.readlines()]
    return all_words, pot_ans, first_guesses


#returns possible guesses ranked in order  worst-best, [(word, perc), ...]
def rank_guesses(GUESS_POOL, ANS_POOL, verbose=True):
    guess_scores = {}
    for guess in GUESS_POOL:
        guess_scores[guess] = test_guess(guess, ANS_POOL)
    guess_scores = list(sorted(guess_scores.items(), key=lambda kv: [kv[1], kv[0]]))
    if verbose: print(ANS_POOL)
    if verbose: print (guess_scores[-10:])

    #suggested guess: if there are ties at the best, choose one that could be the answer
    best_guesses = []
    top_score = 0
    for score in guess_scores:
        if score[1] > top_score:
            top_score = score[1]
            best_guesses = [score[1]]
        elif score[1] == top_score:
            best_guesses.append(score[1])
    best_guess_ans = [] # best_guesses that could be answers
    for guess in best_guesses:
        if guess in ANS_POOL:
            best_guess_ans.append(guess)
    if best_guess_ans == []: best_guess_ans = None
    if verbose: print("Of guesses with highest info, these could be answers:", best_guess_ans)
    if not verbose: return guess_scores, best_guess_ans

#simulates a round using the bots best suggestions. Returns number of guesses it took.
def simulate_round(answer, GUESS_POOL, ANS_POOL, starting_guess, starting_word_dict):
    analyzer = Analyzer(None, None)
    parser = Parser(None)

    simulation_running = True
    guesses = 1
    current_guess = starting_guess
    current_info = analyzer.simulate_guess_result(current_guess, answer)
    if current_info == "GGGGG": return 1
    while simulation_running:
        print("\t\tGuess","#"+str(guesses)+":",current_guess)
        print("\t\tInfo:    ", current_info)

        if guesses == 1 and current_info in starting_word_dict.keys():
            ANS_POOL = starting_word_dict[current_info]
            print("SAVED TIME WITH DICT")
        else:
            ANS_POOL = parser.update_words(current_guess, current_info, ANS_POOL)
            if guesses == 1: starting_word_dict[current_info] = ANS_POOL
        
        guess_scores, best_guess_ans = rank_guesses(GUESS_POOL, ANS_POOL, False)

        # print("best_guess_ans: ", best_guess_ans)
        # print("guess_scores: ", guess_scores)
        print(len(ANS_POOL), "potential answers remain")
        if len(ANS_POOL) == 1 or len(ANS_POOL) == 2: current_guess = ANS_POOL[0]
        elif best_guess_ans != None: current_guess=best_guess_ans[-1]
        else: current_guess=guess_scores[-1][0]
        guesses += 1

        current_info = analyzer.simulate_guess_result(current_guess, answer)
        if current_info == "GGGGG": simulation_running = False
        elif guesses == 6: 
            print("FAILED:", answer)
            simulation_running = False
        
    return guesses, starting_word_dict



 
only_parsing = True #Takes info and gives you the possible words
testing_specific = False #For testing a word, ans combo
testing_starting_word = False #For testing a word, against all answers
finding_best_guess = False #Given a pool, for finding best guess
companion = False #Descriptive companion with parsing and suggestions
test_bot = False #See how quickily the bot can solve on average
def main():
    # get_words_file()
    all_words, potential_answers, first_guesses = get_word_pools()
    # get_letter_freqs(potential_answers)
    # exit()
    potential_answers = potential_answers
    first_guesses = first_guesses

    parser = Parser(potential_answers)
    analyzer = Analyzer(first_guesses, potential_answers)

    if only_parsing:
        words = potential_answers
        while len(words) > 1:
            guess = user_guess()
            info = user_guess_result()
            words = parser.update_words(guess, info, words)
            parser.show_results()
        print(words[0], "is the word!")

    elif testing_specific:
        words = potential_answers
        test_guess = "CRANE"
        test_answer = "SAVOR"
        test_info = analyzer.simulate_guess_result(test_guess, test_answer)

        og_words = len(words)
        print(words)
        print(parser.get_guess_effect(words, test_guess, test_info))
        print("OG:", og_words)
        words = parser.update_words(test_guess, test_info, words)
        print(words)
        print("Now:", len(words))
        print("DIF:", og_words - len(words))
        print("Info:", test_info)
        print("Info gained:"+str(100-(len(words)/og_words)*100)+"%", "of info.")

        exit()

    elif testing_starting_word:
        # STARTING_WORD = "PZAZZ"
        STARTING_WORD = input("Enter a starting word: ").upper()
        while STARTING_WORD != "NO":
            ANSWER_POOL = potential_answers
            avg_percent_eliminated = 0
            for potential_ans in ANSWER_POOL:
                info = analyzer.simulate_guess_result(STARTING_WORD, potential_ans)
                percentage_eliminated = 1 - parser.get_guess_effect(ANSWER_POOL, STARTING_WORD, info)
                avg_percent_eliminated += percentage_eliminated
            avg_percent_eliminated = avg_percent_eliminated/len(ANSWER_POOL)
            print(STARTING_WORD, "eliminates", str(round(avg_percent_eliminated*100, 10))+"% of potential answers on average")
            STARTING_WORD = input("Enter a starting word (type \"NO\" to stop): ").upper()
    
    elif finding_best_guess:
        analyzer.get_next_word(potential_answers)
    
    elif companion:
        while len(potential_answers) > 1:
            guess = user_guess()
            info = user_guess_result()
            potential_answers = parser.update_words(guess, info, potential_answers)
            # could also update guess ppp
            rank_guesses(first_guesses, potential_answers)
        print(potential_answers[0], "is the word!")

    elif test_bot:
        avg_guesses = 0
        STARTING_WORD = "RAISE"
        ANSWER_POOL = potential_answers

        #Speed up program by using a dictionary for results of RAISE
        starting_word_dict = {}

        average_guess_check_time = 0
        for i, answer in enumerate(ANSWER_POOL):
            print("\nTesting: ", answer)
            start_time = time.time()
            rounds, starting_word_dict = simulate_round(answer, first_guesses, ANSWER_POOL, STARTING_WORD, starting_word_dict)
            avg_guesses += rounds
            print("Simulated round:", answer, "Result:", rounds)
            print("\t\t Average: ", round(avg_guesses/(i+1), 4))


            elapsed = time.time()-start_time
            if average_guess_check_time == 0 or elapsed < 2*average_guess_check_time: #ignores crazy outliers
                average_guess_check_time = (average_guess_check_time*i + elapsed)/(i+1)
            num_left = len(ANSWER_POOL) - i

            # time.strftime('%H:%M:%S', time.gmtime(round(elapsed*num_left)))
            print("\tAnalyzed "+str(i+1)+"/"+str(len(ANSWER_POOL))+". \t\t ")
            print("Elapsed: ", time.time()-start_time, "\t\tEstimated time left:",time.strftime('%H:%M:%S', time.gmtime(round(average_guess_check_time*num_left))))
            


main()


# word_file = open("words.txt", "r")
# words = [word.strip() for word in word_file.readlines()]
# print(len(words))
# get_words_file()
# word_file = open("words.txt", "r")
# words = [word.strip() for word in word_file.readlines()]
# print(len(words))
# analyzer = Analyzer()

    # test_guess = "BALMS"
    # test_answer = "MELON"
    # test_info = analyzer.simulate_guess_result(test_guess, test_answer)

    # og_words = len(words)
    # print(parser.get_guess_effect(words, test_guess, test_info))
    # print("OG:", og_words)
    # words = parser.update_words(test_guess, test_info)
    # print("Now:", len(words))
    # print("DIF:", og_words - len(words))
    # print("Info:", test_info)
    # exit()