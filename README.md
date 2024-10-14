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

## Usage Notes

### First Guesses
According to the bot, the best starting guess is SALET, which on average tells you the most about your answer. By setting

```python
SUGGEST_FIRST = False
```
you can see the process that yeilds this, but for convenience, the default is True.

### Verbose Outputs
There are two settings that give you extra insight into the bot as it runs.
```python
VERBOSE = True
TIME_ANALYSIS = True
```
When the VERBOSE setting is active, as guesses are scored, the user can see the scores of the guess. When TIME_ANALYSIS is active, the user also sees the elapsed time in calculating the guess and the estimated time until the program is complete.





