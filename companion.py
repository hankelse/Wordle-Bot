'''
Wordle Companion!
Shows the possible answers and gives suggested guesses as you play
07.03.24
'''

from tools import analysis as anl
from tools import in_out as io
import time

def rank_guesses(guess_pool, ans_pool):
    best_guess = "INVALID"
    best_score = 0
    
    average_guess_check_time = 0
    for i, pot_guess in enumerate(guess_pool):

        if TIME_ANALYSIS: start_time = time.time()
        
        #Get score
        score = anl.get_avg_elimination(pot_guess, ans_pool)
        #Compare score with current best
        if score > best_score:
            best_guess = pot_guess
            best_score = score
        elif score == best_score:
            if pot_guess in ans_pool:
                best_guess = pot_guess
        
        #--User Interaction--#
        if VERBOSE: print("Checked", pot_guess, "which yeilds", round(score, 3))
        if TIME_ANALYSIS: 
            num_left = len(guess_pool) - i - 1
            elapsed = time.time()-start_time
            average_guess_check_time = (average_guess_check_time*i + elapsed)/(i+1)
            print("\t\tElapsed: ", round(time.time()-start_time, 3), " \t\tEstimated time left:",time.strftime('%H:%M:%S', time.gmtime(round(average_guess_check_time*num_left))))
        
    print("Out of the ", len(guess_pool), "possible guesses...")
    print("The best is", best_guess)
    print("WITH", best_score)
    if best_guess in ans_pool:
        print("This guess could be the answer.")



# -----CONSTANTS---- #
ANS_POOL_FILE = "word_lists/valid_answers.txt"
GUESS_POOL_FILE = "word_lists/valid_guesses.txt"


# -----SETTINGS----- #
ALWAYS_SHOW_ANS_POOL = True
NUM_SUGGESTED_GUESSES = 10
TIME_ANALYSIS = True
VERBOSE = True
TIME_ESTIMATE_SCALER = 0.000125
SUGGEST_FIRST = False


def main():
    '''
    ERROR! Parser doesn't eliminate allow after stall is guessed and only one appears yellow.
    '''
    ans_pool = io.get_word_pool(ANS_POOL_FILE)
    guess_pool = io.get_word_pool(GUESS_POOL_FILE)
    
    guess_num = 0
    while len(ans_pool) > 1:
        starting_ans_pool_size = len(ans_pool)
        print("\nThere are", len(ans_pool), "valid answers remaining.\n")

        #Get guess and update pool
        if guess_num != 0 or not SUGGEST_FIRST:
            guess =  input("What is your guess?  ").upper()
            result = input("What was the result? ").upper()
            ans_pool = anl.update_ans_pool(guess, result, ans_pool)
        guess_num += 1


        print("\nThere are now", len(ans_pool), "valid answers remaining.\t\t (Reduced size by", io.percent(1- len(ans_pool)/starting_ans_pool_size)+")")
        choice = input("Would you like to see a list of them? (N (now), A (after), X (not at all)) ")
        if choice.upper() == "N": 
            print(ans_pool)
            input("Press enter to begin calculating the next guess.")

        print("Calculating suggested next guess.\t\t\t Estimated time:", time.strftime('%H:%M:%S', time.gmtime(round(len(guess_pool)*len(ans_pool)*TIME_ESTIMATE_SCALER))))

        #Rank guesses
        start = time.time()
        rank_guesses(guess_pool, ans_pool)
        print("That took", time.strftime('%H:%M:%S', time.gmtime(time.time()-start)))

        # print("\nThere are now", len(ans_pool), "valid answers remaining.\t\t (Reduced size by", io.percent(1- len(ans_pool)/starting_ans_pool_size)+")")
        # choice = input("Would you like to see the list of the possible answers? (Y or N) ")

        if choice.upper() == "A": 
            print(len(ans_pool), "valid answers remaining are...")
            print(ans_pool)

    if len(ans_pool) == 1:
        print(ans_pool[0])
    else:
        print("No answers fit the constraints provided.")


main()

    # ans_pool = ["ABACK", "BLACK", "FLACK", "QUACK", "WHACK", "ABACA", "ALACK", "GUACO", "KYACK", "LOACH", "LUACH", "THACK"]
'''
    first_guess = "CRANE"
    answer = "WIDER"
    result = anl.simulate_guess(first_guess, answer)
    ans_pool = anl.update_ans_pool(first_guess, result, ans_pool)

    next_guess = "TOILS"
    result = anl.simulate_guess(next_guess, answer)
    ans_pool = anl.update_ans_pool(next_guess, result, ans_pool)

    next_guess = "PAVED"
    result = anl.simulate_guess(next_guess, answer)
    ans_pool = anl.update_ans_pool(next_guess, result, ans_pool)

    print(len(ans_pool))

    print(anl.get_avg_elimination("WIDER", ans_pool))

    rank_guesses(guess_pool[0:], ans_pool[0:])
    print(ans_pool)
'''