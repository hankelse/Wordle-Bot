'''
Running the wordle bot and using the top suggestions to see how quickily the bot solves on average.
'''
from tools import analysis as anl
from tools import in_out as io
import time
import random



ANS_POOL_FILE = "word_lists/valid_answers.txt"
GUESS_POOL_FILE = "word_lists/valid_guesses.txt"

ANS_POOL = io.get_word_pool(ANS_POOL_FILE) # Pool of potential answers for the bot's analysis
GUESS_POOL = io.get_word_pool(GUESS_POOL_FILE) # Pool of potential guesses



TIME_ANALYSIS = False

SALET_CACHE = {
        "GGG.." : ('AVIAN', 0.8),
        "GGG.Y" : ('SALTY', 0),
        "GGGY." : ('SALVE', 0),
        "GG.G." : ('SANER', 0.5),
        "GG..G" : ('SAINT', 0),
        "GG..." : ('BOSUN', 0.8125),
        "GG..Y" : ('SATYR', 0.5),
        "GG.Y." : ('SAUCE', 0),
        "GG.YY" : ('SAUTE', 0),
        "GGY.." : ('SADLY', 0),
        "G.G.G" : ('SPLIT', 0),
        "G.G.." : ('SULLY', 0.8),
        "G.GY." : ('SOLVE', 0),
        "G..GG" : ('SWEET', 0.5),
        "G..G." : ('HEWER', 0.9224952741020794),
        "G..GY" : ('ACRID', 0.6666666666666666),
        "G...G" : ('CHURN', 0.9252077562326871),
        "G...." : ('UNHIP', 0.9502551020408163),
        "G...Y" : ('MINOR', 0.9171597633136093),
        "G..YG" : ('SWEPT', 0.6666666666666666),
        "G..Y." : ('RHINO', 0.9393718042366695),
        "G..YY" : ('MINOR', 0.8760330578512397),
        "G.YGG" : ('SLEET', 0),
        "G.YG." : ('SPIEL', 0.6666666666666666),
        "G.YGY" : ('STEEL', 0),
        "G.Y.G" : ('STILT', 0.5),
        "G.Y.." : ('PLINK', 0.9131944444444443),
        "G.Y.Y" : ('STOOL', 0.6666666666666666),
        "G.YYG" : ('SPELT', 0.6666666666666666),
        "G.YY." : ('CHIME', 0.8600000000000001),
        "G.YYY" : ('STYLE', 0.5),
        "GYG.G" : ('SPLAT', 0),
        "GYG.." : ('SOLAR', 0),
        "GY..G" : ('CHAMP', 0.8),
        "GY..." : ('CRAMP', 0.935546875),
        "GY..Y" : ('PRINK', 0.8877551020408166),
        "GY.YG" : ('SWEAT', 0),
        "GY.Y." : ('GRAPH', 0.8979591836734694),
        "GY.YY" : ('DRAKE', 0.8148148148148149),
        "GYY.G" : ('SLANT', 0.5),
        "GYY.." : ('CHILD', 0.8757396449704142),
        "GYY.Y" : ('STALL', 0.5),
        "GYYY." : ('SHALE', 0.6666666666666666),
        "GYYYY" : ('STEAL', 0.6666666666666666),
        ".GGGG" : ('VALET', 0),
        ".GGG." : ('PALER', 0.5),
        ".GG.." : ('RALLY', 0.8333333333333334),
        ".GG.Y" : ('TALON', 0.6666666666666666),
        ".GGY." : ('VALVE', 0.6666666666666666),
        ".G.GG" : ('FACET', 0.5),
        ".G.G." : ('GRUMP', 0.8576388888888892),
        ".G.GY" : ('METER', 0.8200000000000001),
        ".G..G" : ('THING', 0.8984375),
        ".G..." : ('CORNY', 0.953004164187983),
        ".G..Y" : ('CORNY', 0.8894173602853743),
        ".G.Y." : ('CRUMB', 0.9074074074074076),
        ".G.YY" : ('HAUTE', 0.6666666666666666),
        ".GYG." : ('LYING', 0.8429752066115703),
        ".GYGY" : ('LATER', 0),
        ".GY.G" : ('VAULT', 0.5),
        ".GY.." : ('BRINY', 0.8950617283950619),
        ".GY.Y" : ('NATAL', 0.6666666666666666),
        ".GYY." : ('CADGE', 0.84375),
        ".GYYY" : ('LATHE', 0.6666666666666666),
        "..GGG" : ('INLET', 0.5),
        "..GG." : ('AFIRE', 0.8),
        "..G.G" : ('UNLIT', 0.5),
        "..G.." : ('DOILY', 0.9108367626886144),
        "..G.Y" : ('TULIP', 0.5),
        "..GY." : ('HIMBO', 0.90625),
        "..GYY" : ('TULLE', 0.5),
        "...GG" : ('ORING', 0.8875739644970417),
        "...G." : ('FROND', 0.9378985064197742),
        "...GY" : ('HUMOR', 0.9131944444444445),
        "....G" : ('GROIN', 0.9554419284149016),
        "....." : ('CORNU', 0.9726254581192024),
        "....Y" : ('NORTH', 0.9632233639805303),
        "...YG" : ('CURIO', 0.9297520661157026),
        "...Y." : ('NOIRE', 0.9658769513314973),
        "...YY" : ('TRITE', 0.956360946745562),
        "..YGG" : ('FLEET', 0),
        "..YG." : ('BROIL', 0.91941590048675),
        "..YGY" : ('MOTEL', 0.75),
        "..Y.G" : ('CLUNG', 0.9112426035502961),
        "..Y.." : ('CLOUD', 0.9521477400265268),
        "..Y.Y" : ('TROLL', 0.875),
        "..YYG" : ('ALECK', 0.8),
        "..YY." : ('GUILE', 0.9337775926697209),
        "..YYY" : ('TITLE', 0.8571428571428574),
        ".YGG." : ('ALLEY', 0.5),
        ".YG.G" : ('ALLOT', 0),
        ".YG.." : ('ALLAY', 0.8925619834710742),
        ".YGYG" : ('ECLAT', 0),
        ".YGY." : ('RELAY', 0.75),
        ".YGYY" : ('DELTA', 0),
        ".Y.G." : ('ENDER', 0.8571428571428574),
        ".Y.GY" : ('AFTER', 0),
        ".Y..G" : ('FIORD', 0.9199999999999997),
        ".Y..." : ('BRONC', 0.9632833525567083),
        ".Y..Y" : ('TONIC', 0.9342403628117915),
        ".Y.YG" : ('GRAND', 0.8994082840236689),
        ".Y.Y." : ('BEARD', 0.9510814341704165),
        ".Y.YY" : ('GRATE', 0.9149999999999998),
        ".YYG." : ('ANGEL', 0.5),
        ".YYGY" : ('ALTER', 0),
        ".YY.G" : ('FLING', 0.8571428571428574),
        ".YY.." : ('MONIC', 0.9333927378035203),
        ".YY.Y" : ('IOTAS', 0.9081632653061227),
        ".YYYG" : ('PECAN', 0.84375),
        ".YYY." : ('GLARE', 0.920449812578092),
        ".YYYY" : ('AMPLE', 0.8),
        "YGG.." : ('PALSY', 0),
        "YGGY." : ('FALSE', 0),
        "YG..G" : ('WAIST', 0),
        "YG..." : ('HINDS', 0.8800000000000002),
        "YG..Y" : ('NATTY', 0.7777777777777778),
        "YG.Y." : ('AURIC', 0.8),
        "YG.YY" : ('THWAP', 0.7777777777777778),
        "YGYG." : ('EASEL', 0),
        "YGY.." : ('NASAL', 0.75),
        "YGYY." : ('LAPSE', 0),
        "Y.GGG" : ('ISLET', 0),
        "Y.GY." : ('WELSH', 0.5),
        "Y..GG" : ('APRON', 0.8),
        "Y..G." : ('RUMOR', 0.875),
        "Y..GY" : ('ESTER', 0),
        "Y...G" : ('BORIC', 0.9099999999999999),
        "Y...." : ('HUMOR', 0.9433106575963711),
        "Y...Y" : ('GOURD', 0.8888888888888891),
        "Y..YG" : ('BIRCH', 0.816326530612245),
        "Y..Y." : ('CROUP', 0.9432132963988916),
        "Y..YY" : ('TROTH', 0.8888888888888891),
        "Y.YG." : ('LOSER', 0),
        "Y.Y.." : ('BOFFS', 0.8888888888888891),
        "Y.Y.Y" : ('LUSTY', 0),
        "Y.YY." : ('ACHOO', 0.8),
        "YY.GG" : ('ASSET', 0),
        "YY.G." : ('ASKEW', 0.5),
        "YY..G" : ('BORIC', 0.8333333333333334),
        "YY..." : ('CRAGS', 0.9134948096885815),
        "YY..Y" : ('TRASH', 0.6666666666666666),
        "YY.YG" : ('ABAFT', 0.6666666666666666),
        "YY.Y." : ('AURIC', 0.875),
        "YY.YY" : ('TEASE', 0),
        "YYY.G" : ('BLAST', 0),
        "YYY.." : ('CHAPS', 0.875),
        "YYYYG" : ('LEAST', 0),
        "YYYY." : ('LEASH', 0.6666666666666666),
}

CRANE_CACHE = {
    "GGGGG" : ('CRANE', 1),
    "GGGG." : ('CRANK', 1),
    "GGG.G" : ('AVANT', 0.6666666666666666),
    "GGG.." : ('AMYLS', 0.816326530612245),
    "GG.GG" : ('CRONE', 1),
    "GG.G." : ('CRONY', 1),
    "GG..G" : ('CREME', 0.75),
    "GG..." : ('WIMPS', 0.8994082840236689),
    "GG..Y" : ('DEEPS', 0.8800000000000002),
    "GG.Y." : ('CROWN', 1),
    "GGY.." : ('CROAK', 1),
    "GGY.Y" : ('CREAM', 0.5),
    "G.GG." : ('CLANK', 0.6666666666666666),
    "G.G.G" : ('CHASE', 0.6666666666666666),
    "G.G.." : ('CHIPS', 0.9112426035502961),
    "G.GY." : ('CHAIN', 1),
    "G..GG" : ('CLONE', 1),
    "G..G." : ('CLINK', 0.8),
    "G...G" : ('DOLTS', 0.909090909090909),
    "G...." : ('ILIUM', 0.9376000000000002),
    "G...Y" : ('ELECT', 0.8760330578512397),
    "G..Y." : ('CONIC', 0.875),
    "G..YY" : ('COVEN', 1),
    "G.YG." : ('CHINA', 0.5),
    "G.Y.G" : ('ABASE', 0.75),
    "G.Y.." : ('BOOTY', 0.8994082840236687),
    "G.Y.Y" : ('ALTHO', 0.8571428571428574),
    "G.YYG" : ('CANOE', 1),
    "G.YY." : ('ABLED', 0.75),
    "G.YYY" : ('CLEAN', 1),
    "GYG.." : ('ADMIT', 0.75),
    "GY.G." : ('CORNY', 1),
    "GY..G" : ('CURVE', 0.6666666666666666),
    "GY..." : ('GLORY', 0.8888888888888891),
    "GY..Y" : ('BEDEW', 0.816326530612245),
    "GY.Y." : ('CHURN', 1),
    "GYY.G" : ('CARVE', 1),
    "GYY.." : ('BIGOT', 0.875),
    "GYY.Y" : ('ACTED', 0.75),
    "GYYY." : ('CAIRN', 1),
    ".GGG." : ('DEFOG', 0.8333333333333334),
    ".GG.G" : ('DEBTS', 0.8165680473372781),
    ".GG.." : ('GILTS', 0.9297520661157024),
    ".GGY." : ('BIDET', 0.8571428571428574),
    ".G.GG" : ('ADIEU', 0.8),
    ".G.G." : ('BIGOT', 0.920415224913495),
    ".G.GY" : ('TREND', 1),
    ".G..G" : ('PIVOT', 0.9201183431952659),
    ".G..." : ('PILOT', 0.9542483660130714),
    ".G..Y" : ('DEFER', 0.9256198347107439),
    ".G.Y." : ('GIBED', 0.8),
    ".G.YY" : ('PREEN', 0.5),
    ".GYGY" : ('ARENA', 1),
    ".GY.G" : ('AROSE', 0.6666666666666666),
    ".GY.." : ('ARBOR', 0.888888888888889),
    ".GY.Y" : ('TUBED', 0.8641975308641975),
    ".GYY." : ('ORGAN', 0.75),
    "..GGG" : ('PLANE', 0.5),
    "..GG." : ('KELPS', 0.8984375),
    "..GGY" : ('MEANT', 0.5),
    "..G.G" : ('GLUTS', 0.9152892561983464),
    "..G.." : ('SPILT', 0.9562682215743441),
    "..G.Y" : ('HOTLY', 0.9135802469135803),
    "..GYG" : ('SNAKE', 0.5),
    "..GY." : ('SNAIL', 0.875),
    "...GG" : ('CHOPS', 0.9166666666666665),
    "...G." : ('GOUTS', 0.9554102259215222),
    "...GY" : ('BITSY', 0.9000000000000001),
    "....G" : ('TOILS', 0.9661668589004223),
    "....." : ('TOILS', 0.9741936416602837),
    "....Y" : ('SLEET', 0.9667059334118675),
    "...YG" : ('DEIST', 0.9297052154195012),
    "...Y." : ('PILOT', 0.9527272727272728),
    "...YY" : ('OLDEN', 0.938763376932224),
    "..YGG" : ('ATONE', 0.5),
    "..YG." : ('TINGS', 0.885),
    "..YGY" : ('AMEND', 0.6666666666666666),
    "..Y.G" : ('MAULS', 0.9337775926697209),
    "..Y.." : ('TOILS', 0.960793049676988),
    "..Y.Y" : ('STEAL', 0.9470699432892252),
    "..YYG" : ('AGILE', 0.8333333333333334),
    "..YY." : ('TOILS', 0.9434133091896789),
    "..YYY" : ('LAKES', 0.9024943310657598),
    ".YG.G" : ('BLIPS', 0.7755102040816328),
    ".YG.." : ('HOIST', 0.8993055555555555),
    ".YG.Y" : ('MALTY', 0.8395061728395062),
    ".YGYG" : ('SNARE', 1),
    ".YGY." : ('SNARL', 1),
    ".YGYY" : ('YEARN', 0.5),
    ".Y.GG" : ('BORNE', 1),
    ".Y.G." : ('ROUND', 0.75),
    ".Y..G" : ('SPROG', 0.9375000000000003),
    ".Y..." : ('TYROS', 0.9646913580246911),
    ".Y..Y" : ('TOILS', 0.913732867508735),
    ".Y.YG" : ('RINSE', 0.8),
    ".Y.Y." : ('BOOTH', 0.9112426035502961),
    ".Y.YY" : ('DINES', 0.9218106995884773),
    ".YYG." : ('RAINY', 1),
    ".YY.G" : ('ADLIB', 0.84375),
    ".YY.." : ('LORRY', 0.933017751479289),
    ".YY.Y" : ('MALTS', 0.8976),
    ".YYYG" : ('RANGE', 1),
    ".YYY." : ('RAYON', 0.9000000000000001),
    ".YYYY" : ('RAVEN', 0.8),
    "YGG.G" : ('ABAFT', 0.6666666666666666),
    "YGG.." : ('WRACK', 0.6666666666666666),
    "YG..G" : ('TRUCE', 0.6666666666666666),
    "YG..." : ('ABOUT', 0.8),
    "YG..Y" : ('WRECK', 0.5),
    "Y.GG." : ('SCANT', 1),
    "Y.G.G" : ('SCALE', 0.75),
    "Y.G.." : ('PLUSH', 0.8875739644970415),
    "Y.G.Y" : ('BELTS', 0.8),
    "Y.GY." : ('SNACK', 0.5),
    "Y.GYY" : ('ENACT', 1),
    "Y..GG" : ('SCONE', 0.5),
    "Y..G." : ('ICING', 1),
    "Y..GY" : ('SCENT', 1),
    "Y...G" : ('PIOUS', 0.8888888888888891),
    "Y...." : ('TULIP', 0.9573553719008262),
    "Y...Y" : ('LITHO', 0.9299999999999999),
    "Y..YG" : ('HINDS', 0.8429752066115703),
    "Y..Y." : ('TULIP', 0.9012345679012347),
    "Y..YY" : ('WENCH', 0.5),
    "Y.Y.G" : ('SAUCE', 0.5),
    "Y.Y.." : ('MOTIF', 0.9190672153635119),
    "Y.Y.Y" : ('FECAL', 0.8333333333333334),
    "Y.YYG" : ('LANCE', 0.5),
    "Y.YY." : ('PANIC', 0.8),
    "Y.YYY" : ('PECAN', 0.5),
    "YYG.G" : ('SCARE', 1),
    "YYG.." : ('SCARY', 0.6666666666666666),
    "YYG.Y" : ('REACT', 0.5),
    "YY..G" : ('SCORE', 0.6666666666666666),
    "YY..." : ('BOCCI', 0.8925619834710742),
    "YY..Y" : ('RECTO', 0.8800000000000002),
    "YY.Y." : ('SCORN', 0.5),
    "YY.YY" : ('NICER', 1),
    "YYY.G" : ('FARCE', 1),
    "YYY.." : ('SCRAP', 0.8571428571428574),
    "YYY.Y" : ('RECAP', 0.5),
    "YYYY." : ('RANCH', 0.5),
}

def get_salet_cache(ANS_POOL):
    salet_cache = {}
    for first in ["G", ".", "Y"]:
        for second in ["G", ".", "Y"]:
            for third in ["G", ".", "Y"]:
                for forth in ["G", ".", "Y"]:
                    for fifth in ["G", ".", "Y"]:
                        ans_pool = ANS_POOL
                        guess_result = first+second+third+forth+fifth
                        print(guess_result)
                        ans_pool = anl.update_ans_pool("SALET", guess_result, ans_pool)
                        if len(ans_pool) >0:
                            salet_cache[guess_result] = get_best_guess(ans_pool, GUESS_POOL)
    
    print("salet_cache = {")
    for key in salet_cache:
        print(f"\t\"{key}\" :", str(salet_cache[key])+",")
    print("}")
def get_crane_cache(ANS_POOL):
    crane_cache = {}
    for first in ["G", ".", "Y"]:
        for second in ["G", ".", "Y"]:
            for third in ["G", ".", "Y"]:
                for forth in ["G", ".", "Y"]:
                    for fifth in ["G", ".", "Y"]:
                        ans_pool = ANS_POOL
                        guess_result = first+second+third+forth+fifth
                        print(guess_result)
                        ans_pool = anl.update_ans_pool("CRANE", guess_result, ans_pool)
                        if len(ans_pool) >0:
                            crane_cache[guess_result] = get_best_guess(ans_pool, GUESS_POOL)
    
    print("salet_cache = {")
    for key in crane_cache:
        print(f"\t\"{key}\" :", str(crane_cache[key])+",")
    print("}")




def get_best_guess(ANS_POOL, GUESS_POOL):

    if len(ANS_POOL) == 1:
        return ANS_POOL[0], 1

    best_guess = "INVALID"
    best_score = 0
    average_guess_check_time = 0

    for i, pot_guess in enumerate(GUESS_POOL):
        if TIME_ANALYSIS: start_time = time.time()
        

        #Get score
        score = anl.get_avg_elimination(pot_guess, ANS_POOL)
        #Compare score with current best
        if score > best_score:
            best_guess = pot_guess
            best_score = score
        elif score == best_score:
            if pot_guess in ANS_POOL:
                best_guess = pot_guess
        
        #Analyze time
        if TIME_ANALYSIS: 
            num_left = len(GUESS_POOL) - i - 1
            elapsed = time.time()-start_time
            average_guess_check_time = (average_guess_check_time*i + elapsed)/(i+1)
            print("\t\tElapsed: ", round(time.time()-start_time, 3), " \t\tEstimated time left:",time.strftime('%H:%M:%S', time.gmtime(round(average_guess_check_time*num_left))))
    return best_guess, best_score
    





def run_bot(TESTING_POOL, ANS_POOL, GUESS_POOL):
    results = [[], [], [], [], [], [], []] #Answers solved in 1, 2, 3, 4, 5, 6, and not at all
    for i, test_answer in enumerate(TESTING_POOL):
        # print("\t Testing", test_answer)
        ans_pool = ANS_POOL
        guess_pool = GUESS_POOL

        next_guess = FIRST_GUESS
        solved = False
        num_guesses = 0

        while not solved:
            # print("next_guess = ", next_guess)
            guess_result = anl.simulate_guess(next_guess, test_answer)
            num_guesses += 1
            if guess_result == "GGGGG": 
                solved = True
                continue
            
            ans_pool = anl.update_ans_pool(next_guess, guess_result, ans_pool)

            if num_guesses == 1: best_guess, best_score = first_guess_cache[guess_result][0], first_guess_cache[guess_result][1]
            else: best_guess, best_score = get_best_guess(ans_pool, guess_pool)


            next_guess = best_guess
        
        if num_guesses <= 6: results[num_guesses-1].append(test_answer)
        else: results[6].append(test_answer)

        print("Got answer", test_answer, "in", num_guesses, "guesses! \t completed", f"{i}/{len(TESTING_POOL)} tests")


    return results

def show_results(results, num_tests):
    for i, result_list in enumerate(results):
        result_str = " ".join(result_list)
        print(f"{i+1}: {result_str}")
    
    avg = 0
    for i, result_list in enumerate(results):
        print(f"{i+1}: {len(result_list)}")
        avg += len(result_list) * (i+1)
    
    avg = avg / num_tests
    print("Average score:", avg)


    
# TESTING_POOL = [random.choice(ANS_POOL) for i in range(1000)] #The answers that get tested on
TESTING_POOL = ANS_POOL

FIRST_GUESS = "SALET"
first_guess_cache = SALET_CACHE

def main():
    
    results = run_bot(TESTING_POOL, ANS_POOL, GUESS_POOL)
    show_results(results, len(TESTING_POOL))
        
            
main()