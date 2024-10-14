# Wordle Bot

A next-guess calculator for the New York Times game, Wordle.

## Running the program

There are no external requirements for running the bot. The companion.py file is the main program and is ran by:

```bash
python3 companion.py
```

## What is Wordle?
[Wordle](www.nytimes.com/games/wordle/index.html) is an online word game in which players have six attempts to guess a five-letter word. After each guess, feedback is provided through colored tiles indicating whether letters are correct and in the right position, allowing players to refine their guesses. 



## What does the bot do?
After entering a guess you have made and the results, the bot first finds all of the potential answers. Next, the bot looks through all of the guesses that Wordle will accept, and finds the guess that on average will tell you the most information. 

## Findings

A common question when talking about WORDLE is what is the best starting word? The best starting words and the average percent they reduce the potential answer pool by are as follows:
```bash
1. RAISE: 0.973649734803074
2. ARISE: 0.9724726989443438
3. IRATE: 0.9724495612705204
4. ORATE: 0.972401419981435
5. AROSE: 0.9714811376644953
6. ALTER: 0.9697659642952114
7. SANER: 0.9697081201106513
8. LATER: 0.9696659498341652
9. SNARE: 0.9692882832872298
10. STARE: 0.9692031963576835
```
Note: These are the best starting words for the algorithm, which is largely dependent on the carefully pruned datasets I used. Many other bots that use larger datasets suggest SALET as a starting word which is more "honest" to the information a player has, but finds solutions less optimally. Additionally, saying that ADIEU, for example, one of the most popular starting words, is not a good one based on these results is a poor conclusion; What's most helpful for the algorithm isn't neccesarily most helpful for you! You should play with whatever word makes the most sense for the way your brain works!

## How Optimal is Your Starting Word?
Would you like to know how optimal your starting word is? Using:
```python
answer_pool = io.get_word_pool(ANS_POOL_FILE)
anl.get_avg_elimination(YOUR_STARTING_WORD, answer_pool)
```
you can find out on average what percent of the possible answers your go to starting word eliminates.


## Usage Notes

### First Guesses
According to the bot, the best starting guess is RAISE, which on average eliminates 97.4% of possible answers. By setting

```python
SUGGEST_FIRST = True
```
you can see the process that yeilds this. If you already know what starting word you would like, set this to False for convenience.

### Verbose Outputs
There are two settings that give you extra insight into the bot as it runs.
```python
VERBOSE = True
TIME_ANALYSIS = True
```
When the VERBOSE setting is active, as guesses are scored, the user can see the scores of the guess. When TIME_ANALYSIS is active, the user also sees the elapsed time in calculating the guess and the estimated time until the program is complete.





