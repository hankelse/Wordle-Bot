import analysis as anl
import in_out as io


'''
Gives a pool after a sequence of guesses 
    Previous guesses given [guess1, result1, guess2, result2]
'''
def simulate_mid_game(previous_guesses, og_pool):
    pool = og_pool
    for i in range(0, len(previous_guesses), 2):
        pool = anl.update_ans_pool(previous_guesses[i], previous_guesses[i+1], pool)
    return pool

'''
After being given a questionable suggestion by the companion...
Given a series of previous guesses and the results, tests the score of a given guess.
    Previous guesses given [guess1, result1, guess2, result2]
'''
def test_guess_in_pool(guess, ans_pool, previous_guesses):
    ans_pool = simulate_mid_game(previous_guesses, ans_pool)
    print(guess, "eliminates", anl.get_avg_elimination(guess, ans_pool), "on average.")

'''
From using test_guess_in_pool...

ans_pool = io.get_word_pool("word_lists/valid_answers.txt")
previous_guesses = ["IRATE", "...YY", "CHEST", "..Y.G"]

for guess in ["BAUDS", "TENDU", "TUBED", "IRATE", "BUNDT"]:
    test_guess_in_pool(guess, ans_pool, previous_guesses)
'''

'''
TESTING SIMULATE_GUESS
'''
GUESS = "CREME"
ANSWER = "SPEAR"
print(GUESS)
print(ANSWER)
print(anl.simulate_guess(GUESS, ANSWER))




