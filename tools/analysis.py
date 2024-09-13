'''
All functions that are general and can are useful in the analysis of pools of words
'''

'''
Given a GUESS and an ANS_POOL of possible answers, returns the average percentage of words eliminated.
'''
def get_avg_elimination(guess, ans_pool):
    percent_eliminated_sum = 0
    for i, potential_answer in enumerate(ans_pool):
        guess_result = simulate_guess(guess, potential_answer)
        percent_eliminated_sum += get_info_gained(guess, guess_result, ans_pool)
    return percent_eliminated_sum/len(ans_pool)

'''
What percentage of the ANS_POOL does this guess eliminte?
Given a GUESS, the GUESS_RESULT of the guess, and an ANS_POOL, returns the percentage of the pool that the guess eliminates.
'''
def get_info_gained(guess, guess_result, ans_pool):
    original_pool_size = len(ans_pool)
    new_pool_size = 0
    for potential_ans in ans_pool:
        if simulate_guess(guess, potential_ans) == guess_result:
            new_pool_size += 1
    return 1 - new_pool_size/original_pool_size


'''
Faster version of get_info_gained where instead of simulating a full guess, as much of the guess is needed is simulated.
Given a GUESS, the GUESS_RESULT, and an ANS_POOL, returns the precentage of the pool that that guess eliminates
'''
def fast_gig(guess, guess_result, ans_pool):
    original_pool_size = len(ans_pool)
    new_pool_size = 0
    for potential_answer in ans_pool:
        if could_be_ans(potential_answer, guess, guess_result):
            new_pool_size += 1
    return 1- new_pool_size/original_pool_size

'''
Faster alternative to simulate_guess. Used with fast_gig.
Given a GUESS, the GUESS_RESULT, and a potential answer, returns if the potential answer fits the information given by the guess.
'''
def could_be_ans(guess, guess_result, pot_answer):
    # guess_info = [(guess[i], guess_result[i]) for i in range(len(guess))]
    yellows = []
    for i in range(len(guess)):
        char_result = guess_result[i]

        if char_result == "G":
            if pot_answer[i] != guess[i]: return False

        elif char_result == ".":
            if guess[i] in pot_answer: return False
        
        elif char_result == "Y":
            if guess[i] not in pot_answer: return False
            elif guess[i] == pot_answer[i]: return False
            #Yellow small cases
            yellows.append(guess[i])

    '''
    Cases being checked:
    - If gr has two yellows, does pot_answer?  SPEED ..YY. CRANE (FALSE)
    - If gr has only one of a char...          SPEED ..Y.  EVONE (FALSE)
    '''  
    for yellow in yellows:
        # if yellows.count(yellow) != guess.count(yellow): False
        pass
        

    return True


        
        

    
     


'''
Given a GUESS and an ANSWER, returns the information that would be returned as a result of that guess
    returns: five char string where '.' represents a grey, 'Y' represents yellow, and 'G' represents green
'''
def simulate_guess(guess, answer):
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



# def answer_fits_guess(potential_answer, )


'''
Given a GUESS, GUESS_RESULT, and ANS_POOL (of potential answers), returns the list of remaining valid answers.
'''
def update_ans_pool(guess, guess_result, ans_pool):
    new_ans_pool = []
    for potential_ans in ans_pool:
        if simulate_guess(guess, potential_ans) == guess_result:
            new_ans_pool.append(potential_ans)
    return new_ans_pool


'''
Given an ANS_POOL and GUESS_POOL, eliminate guesses that are unrealistic.

'''
def update_guess_pool():
    pass