from parsing import Parser
import time

class Analyzer:
    def __init__(self, all_words, words):
        self.all_words = all_words
        self.parser = Parser(words)

    
    def get_next_word(self, words):
        self.words = words
        # num_words = len(words)
        guess_scores = {guess: 0 for guess in self.all_words}

        average_guess_check_time = 0

        for i, potential_guess in enumerate(self.all_words): #if this word was guessed...
            print(str("\tAnalyzing "+str(i+1)+"/"+str(len(self.all_words))+". \t\t Checking: "+str(potential_guess)))
            start = time.time()
            for potential_answer in self.words: # if this word was the answer...
                # print("If you guessed", potential_guess, "and", potential_answer, "was the answer...")
                #what would the result be?
                guess_result = self.simulate_guess_result(potential_guess, potential_answer)
                # print("\tResult of guess:", guess_result)

                #parse, getting the number of words eliminated by the guess
                percentage_words_remaining = self.parser.get_guess_effect(self.words, potential_guess, guess_result)

                guess_scores[potential_guess] += percentage_words_remaining
                # print("\t", potential_guess, "would eliminate all but", percentage_words_remaining, "% of words if", potential_answer, "was the answer.")
            guess_scores[potential_guess] = round(guess_scores[potential_guess]/len(self.words), 10) #get average

            elapsed = time.time()-start
            if average_guess_check_time == 0 or elapsed < 2*average_guess_check_time: #ignores crazy outliers
                average_guess_check_time = (average_guess_check_time*i + elapsed)/(i+1)
            num_left = len(self.all_words) - i

            # time.strftime('%H:%M:%S', time.gmtime(round(elapsed*num_left)))
            print("\tAnalyzed "+str(i+1)+"/"+str(len(self.all_words))+". \t\t ", potential_guess, "yeilds", str(round(100-guess_scores[potential_guess]*100, 10))+"%", "of info.")
            print("Elapsed: ", time.time()-start, "\t\tEstimated time left:",time.strftime('%H:%M:%S', time.gmtime(round(average_guess_check_time*num_left))))
            

        best = None
        best_score = 100
        for key in guess_scores:
            if guess_scores[key] < best_score:
                best = key
                best_score = guess_scores[key]
        
        

        guess_scores = list(sorted(guess_scores.items(), key=lambda kv: [kv[1], kv[0]]))

        print("\n\n RESULTS:")
        for place in range(20):
            print("\tThe #"+str(place+1)+" guess was", guess_scores[place][0], "which on avg yeilds", str(round(100-guess_scores[place][1]*100, 10))+"%", "of info.")

        #put them in file
        results_for_txt = []
        for i, score in enumerate(guess_scores):
            results_for_txt.append(str(i)+":  \t"+str(score[0])+" gave \t"+ str(round(100 - score[1]*100, 10))+"% info\n")
        bs_file = open("best_starts.txt", "w")
        bs_file.write("".join(results_for_txt))

    def simulate_guess_result(self, guess, answer):
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



        