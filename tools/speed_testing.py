import random
import time
import analysis as anl
import in_out as io

'''
Original implementation 2n
'''
def simulate_guess_result(guess, answer, extra=None):
        result_list = ["?", "?", "?", "?", "?"]
        g_chars = list(guess)
        a_chars= list(answer)
        #check for greens

        for i in range(len(answer)):
            if guess[i] == answer[i]: 
                g_chars[i] = "_"
                a_chars[i] = "_"
                result_list[i] = "G"
            
        #check for yellows
        for i in range(len(g_chars)):
            if g_chars[i] == "_": continue
            if g_chars[i] in a_chars:
                result_list[i] = "Y"
                a_chars.remove(g_chars[i])
            else:
                result_list[i] = "."
        return "".join(result_list)


def sim_guess_recursive(guess, answer, index):
    if len(guess) == index: return ""

    next_char = "?"
    if guess[index] == answer[index]: 
        next_char = "G"
        list(guess)[index] = "_"
        list(answer)[index] = "_"
    else:
        if guess[index] in answer:
            next_char = "Y"
            
            answer = answer.replace(guess[index], "_", 1)

        else:
            next_char = "."
    
    return next_char + sim_guess_recursive(guess, answer, index+1)
    


def compare_sim_guess_accuracy(func1, func2, num_tests):
    disagreements = 0
    guesses = [random.choice(guess_pool) for i in range(num_tests)]
    answers = [random.choice(ans_pool) for i in range(num_tests)]
    for i in range(num_tests):
        if func1(guesses[i], answers[i]) != func2(guesses[i], answers[i], 0):
            print("DISAGREEMENT! guess="+guesses[i], "answer="+answers[i])
            print(func1.__name__, "\toutput", func1(guesses[i], answers[i]))
            print(func2.__name__, "\toutput", func2(guesses[i], answers[i], 0))
            disagreements += 1
    print("Disagreed on", str(disagreements)+"/"+str(num_tests), "tests.")


def test_sim_guess_speed(num_random_pairs, ans_pool, guess_pool, sim_guess_function):

    guesses = [random.choice(guess_pool) for i in range(num_random_pairs)]
    answers = [random.choice(ans_pool) for i in range(num_random_pairs)]

    start_time = time.time()
    for i in range(num_random_pairs):
        sim_guess_function(guesses[i], answers[i])
    end_time = time.time()

    elapsed = end_time- start_time
    print("It took", sim_guess_function.__name__.upper(), round(elapsed, 3), "seconds to simulate the", num_random_pairs, "guesses.")
    print("\t Time per 5000 guesses:", 5000 * (elapsed/num_random_pairs))


'''
Testing 
'''


ans_pool = io.get_word_pool("word_lists/valid_answers.txt")
guess_pool = io.get_word_pool("word_lists/valid_guesses.txt")

# test_sim_guess_speed(250*1000, ans_pool, guess_pool, anl.simulate_guess)
# print("")

compare_sim_guess_accuracy(simulate_guess_result, sim_guess_recursive, 10000)