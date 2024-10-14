'''
Wordle Companion!
Shows the possible answers and gives suggested guesses as you play
07.03.24
'''

from tools import analysis as anl
from tools import in_out as io
import time

"""
Given a word-pool of valid guesses and a word-pool of valid answers,
Finds the best guess yeilding the most information
using the tools from analysis.py.
"""
def rank_guesses(guess_pool, ans_pool):
    guess_scores = {}
    
    average_guess_check_time = 0
    for i, pot_guess in enumerate(guess_pool):

        if TIME_ANALYSIS: start_time = time.time()
        
        #Get score
        score = anl.get_avg_elimination(pot_guess, ans_pool)
        guess_scores[pot_guess] = score
        
        #--User Interaction--#
        if VERBOSE: print("Checked", pot_guess, "which yeilds", round(score, 3))
        if TIME_ANALYSIS: 
            num_left = len(guess_pool) - i - 1
            elapsed = time.time()-start_time
            average_guess_check_time = (average_guess_check_time*i + elapsed)/(i+1)
            print("\t\tElapsed: ", round(time.time()-start_time, 3), " \tEstimated time left:",time.strftime('%H:%M:%S', time.gmtime(round(average_guess_check_time*num_left))))
    print(f"\n  ================== RESULTS ==================  ")
    print("Out of the ", len(guess_pool), "possible guesses...")
    io.print_top_n_guesses(guess_scores, 10)



    ranked_guesses = anl.get_top_n_guesses(guess_scores)
    for guess, score in ranked_guesses:
        if guess in ans_pool:
            print(guess, "is the highest ranked guess that could be an answer with a score of", score)
            break


'''
Prompts user from guess and result until it gets a valid response
'''    
def get_round_info():
    guess =  input("What is your guess?  ").upper()
    result = input("What was the result? ").upper()

    #Make sure guesses are valid
    while not (io.guess_is_valid(guess) and io.result_is_valid(result)):
        print("Input not valid! Please try again.")
        guess =  input("What is your guess?  ").upper()
        result = input("What was the result? ").upper()
    
    return guess, result


'''
Displays opening message and instruction
'''
def greet():
    openning_message = '''
    \t\t\tHello! Welcome to my Wordle Companion!
    \nHere is the basics for how to use it:
    \t 1) Enter a guess in the terminal
    \t 2) Enter the result of your guess as a five letter string where: 
    \t\ti)   \"y\" corresponds to yellow letters, 
    \t\tii)  \"g\" corresponds to green letters, and 
    \t\tiii) \".\" corresponds to grey letters.
    \t    If the answer was APHID, a your inputs might look like this
    \t\tWhat is your guess?  adieu
    \t\tWhat was the result? gyy..
    \t 3) Repeat until you find your word!\n
Press enter to begin! '''
    input(openning_message) 

# -----CONSTANTS---- #
ANS_POOL_FILE = "word_lists/valid_answers.txt"
GUESS_POOL_FILE = "word_lists/valid_guesses.txt"


# -----SETTINGS----- #
ALWAYS_SHOW_ANS_POOL = True
NUM_SUGGESTED_GUESSES = 10
TIME_ANALYSIS = False
VERBOSE = False
SUGGEST_FIRST = False


def main():
    
    greet()

    # Gets the valid words from the files
    ans_pool = io.get_word_pool(ANS_POOL_FILE)
    guess_pool = io.get_word_pool(GUESS_POOL_FILE)
    
    #Main loop: while the answer hasn't been found, get the next guess and trim pools
    guess_num = 0
    while len(ans_pool) > 1:
        starting_ans_pool_size = len(ans_pool)
        print(f"\n====================GUESS {guess_num+1}====================")
        print("  There are", len(ans_pool), "valid answers remaining.\n")

        #Get guess and update pool
        if guess_num != 0 or not SUGGEST_FIRST:
            guess, result = get_round_info()
            ans_pool = anl.update_ans_pool(guess, result, ans_pool)
        guess_num += 1

        #Check if solution found
        if len(ans_pool) == 1:
            print("ANSWER FOUND! The word is:", ans_pool[0])
            return

        print("\nThere are now", len(ans_pool), "valid answers remaining.\t (Reduced size by", io.percent(1- len(ans_pool)/starting_ans_pool_size, 4)+")")
        choice = input("Would you like to see a list of them? (N (now), A (after finding best guess), X (not at all)) ")
        if choice.upper() == "N": 
            io.print_word_pool(ans_pool)
            input("Press enter to begin calculating the next guess ")

        #Rank guesses
        start = time.time()
        rank_guesses(guess_pool, ans_pool)

        print("(Calculated in", time.strftime('%H:%M:%S', time.gmtime(time.time()-start))+")")

        if choice.upper() == "A": 
            print(len(ans_pool), "valid answers remaining are...")
            io.print_word_pool(ans_pool)


    print("No answers fit the constraints provided.")

main()

