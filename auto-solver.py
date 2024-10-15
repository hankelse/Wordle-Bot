from tools import analysis as anl
from tools import in_out as io
import time, random


def get_random_word(word_pool):
    return random.choice(word_pool)

class Wordle_Solver:
    def __init__(self, ans_pool, guess_pool, threshold, starting_word, starting_word_cache=None):
        self.threshold = threshold
        self.starting_word = starting_word
        self.original_ans_pool = ans_pool
        self.ans_pool = ans_pool
        self.guess_pool = guess_pool

        if starting_word_cache == None:
            self.starting_word_cache = self.get_cache() 
        else:
            self.starting_word_cache = starting_word_cache

    def reset_ans_pool(self):
        self.ans_pool = []
        for pot_ans in self.original_ans_pool:
            self.ans_pool.append(pot_ans)

    def get_best_guess(self, unique_ans_pool=None):
        if unique_ans_pool != None:
            ans_pool = unique_ans_pool
        else:
            ans_pool = self.ans_pool

        guess_scores = {}
        average_guess_check_time = 0
        for i, pot_guess in enumerate(self.guess_pool):

            if TIME_ANALYSIS: start_time = time.time()
            
            #Get score
            score = anl.get_avg_elimination(pot_guess, ans_pool)
            guess_scores[pot_guess] = score
            
            #--Info Reporting--
            # if VERBOSE: print("Checked", pot_guess, "which yeilds", round(score, 3))
            if TIME_ANALYSIS: 
                num_left = len(self.guess_pool) - i - 1
                elapsed = time.time()-start_time
                average_guess_check_time = (average_guess_check_time*i + elapsed)/(i+1)
                print("\t\tElapsed: ", round(time.time()-start_time, 3), " \tEstimated time left:",time.strftime('%H:%M:%S', time.gmtime(round(average_guess_check_time*num_left))))
        
        #Print results
        # print(f"\n  ================== RESULTS ==================  ")
        # print("Out of the ", len(guess_pool), "possible guesses...")
        # io.print_top_n_guesses(guess_scores, 10)

        #Give best result that may be an answer
        ranked_guesses = anl.get_top_n_guesses(guess_scores)
        #If 2 words, guess one of them
        if (len(ans_pool) == 2):
            for guess, score in ranked_guesses:
                if guess in ans_pool:
                    return guess
        
        #If there is a good guess that could be an answer guess it
        for guess, score in ranked_guesses[0:self.threshold]:
            if guess in ans_pool:
                return guess
                
        #Else guess the best guess
        return ranked_guesses[0][0]


    def run_round(self, answer):
        self.reset_ans_pool()
        guesses = 2
        starting_result = anl.simulate_guess(self.starting_word, answer)
        self.ans_pool = anl.update_ans_pool(self.starting_word, starting_result, self.ans_pool)

        guess = self.starting_word_cache[starting_result]
        result = anl.simulate_guess(guess, answer)

        if VERBOSE:
            print("===GUESS 1===")
            print("GUESS:", self.starting_word)
            print("RESULT:", starting_result)
            print("===GUESS 2===")
            print("GUESS:", guess)
            print("RESULT:", result)
            if result.lower() == "ggggg":
                guesses -= 1

        self.ans_pool = anl.update_ans_pool(guess, result, self.ans_pool)
        if VERBOSE: print(len(self.ans_pool), "WORDS REMAIN")
        while (len(self.ans_pool) > 1):
            guesses += 1
            guess = self.get_best_guess()
            result = anl.simulate_guess(guess, answer)

            if VERBOSE:
                print(f"===GUESS {guesses}===")
                print("GUESS:", guess)
                print("RESULT:", result)
            self.ans_pool = anl.update_ans_pool(guess, result, self.ans_pool)

            if result.lower() == "ggggg":
                guesses -= 1
        guesses += 1

        found_answer = self.ans_pool[0]
        if found_answer == answer:
            if KINDA_VERBOSE: print("FOUND ANSWER:", found_answer, "in", guesses, "guesses.")
        else:
            print("Something went wrong.")
            print("FOUND ANSWER:", found_answer, "in", guesses, "guesses.")
            print("ACTUAL ANSWER:", answer)
            exit()
        return guesses

    def show_stats(self, results):
        #SHOW MEAN
        mean = (sum(results.values())/len(results.keys()))
        print("AVERAGE : ", mean)

        #MIN MAX
        print("MIN: ",min(results.values()))
        print("MAX: ",max(results.values()))
        

    def get_cache(self):
        cache = {}
        for first in ["G", ".", "Y"]:
            for second in ["G", ".", "Y"]:
                for third in ["G", ".", "Y"]:
                    for forth in ["G", ".", "Y"]:
                        for fifth in ["G", ".", "Y"]:
                            guess_result = first+second+third+forth+fifth
                            temp_ans_pool = anl.update_ans_pool(self.starting_word, guess_result, self.ans_pool)
                            if len(temp_ans_pool) > 0:
                                cache[guess_result] = self.get_best_guess(temp_ans_pool)
    
        return cache

    def run_on_all(self):
        results = {}
        for answer in self.ans_pool:
            guesses = self.run_round(answer)
            results[answer] = guesses

        self.show_stats(results)





TIME_ANALYSIS = False
VERBOSE = False
KINDA_VERBOSE = False

ANS_POOL_FILE = "word_lists/valid_answers.txt"
GUESS_POOL_FILE = "word_lists/valid_guesses.txt"
# STARTING_WORD = "SALET"
# THRESHOLD = 3

def main():
    ans_pool = io.get_word_pool(ANS_POOL_FILE)
    guess_pool = io.get_word_pool(GUESS_POOL_FILE)
    current_starting_word = "INVALID"
    starting_word_cache = None


    starting_words = ["RAISE", "CRANE", "SALET"]
    thresholds = [1, 2, 3]

    for starting_word in starting_words:
        for threshold in thresholds:
            if current_starting_word != starting_word:
                starting_word_cache = None
                current_starting_word = starting_word

            solver = Wordle_Solver(ans_pool, guess_pool, threshold, starting_word, starting_word_cache)
            print(f"RUNNING WITH: {starting_word} and threshold: {threshold}")

            solver.run_on_all()

            starting_word_cache = solver.starting_word_cache








    return

main()