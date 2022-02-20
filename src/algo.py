import json, string
from itertools import product
from xmlrpc.client import Boolean
import random as rand

def main():
    words = load_words()
    # print(len(words))

    # sorted_counts = get_letter_counts(words)
    # letters = [sorted_counts[x][0] for x in range(10)]
    # print(letters)

    # best_starting_word = pick_best_starting_word(words, letters)
    # print(best_starting_word)

    # print(word_checker('toeas', 'toads'))
    
    # print(wordle_algo('shake', words))
    print(wordle_algo(words[rand.randint(0, len(words)-1)], words))

'''
Reads in all valid Wordle words from static/words.json
'''
# def load_words(path='./static/words.json'):
# def load_words(path='C:\\Users\\clare\\Documents\\csprojects\\wordle-solver\\static\\words.json'):
#     # open path (akak words.json) and read everything in path to a string
#     f = open(path).read()
#     words = set(json.loads(f)['words'])
#     return words
     
# def load_words(path='./static/words.txt'):
def load_words(path='C:\\Users\\clare\\Documents\\csprojects\\wordle-solver\\static\\words.txt'):
    with open(path) as file:
        words = [word.rstrip() for word in file]
    file.close()
    return words


'''
Gets the sorted counts of each letter in the word list
'''
def get_letter_counts(words):
    alphabet_list = list(string.ascii_lowercase)
    counts = dict()   
    for i in range(26):            
        counts[alphabet_list[i]] = str(words).count(alphabet_list[i])

    sorted_counts = sorted(counts.items(), key=lambda kvp: kvp[1], reverse=True)
    # for letter, count in sorted_counts:
    #     print(f'{letter} count: {count}')
    # S E A O R I L T N D
    # goal: using 5/7-10 most common letters, pick a word that narrows down the search space
    return sorted_counts

# given most common letters, try and make a word and see how many words are remaining
# pick the word that has the fewest remaining 
def pick_best_starting_word(words, letters):
    # generates a word
    # 10^5 = 100 racks
    # constant lookup time
    # generate all possible strings/words using letters

    # generate all possible five letter strings using letters
    # rule: you cannot use itertools.product
    words = set(words)
    start_words = set()
    for q in letters:
        for w in letters:
            for e in letters:
                for r in letters:
                    for t in letters:
                        if q+w+e+r+t in words:
                            start_words.add(q+w+e+r+t)

    max_word_coverage_count = ('', 0)

    for word in start_words:
        words_left = set()
        for n in word:
            words_left = words_left.union(set(filter(lambda x: n in x, words)))
        if len(words_left) > max_word_coverage_count[1]:
            max_word_coverage_count = (word, len(words_left))
    
    return(max_word_coverage_count)
            

# returns whether each letter of a guessed word is in the correct index, in the wrong index, or not in the word 
def word_checker(guess, word):
    # word = words[rand.randint(0, len(words)-1)]
    # word = 'money'
    # letters in right position, letters in wrong positions, letters not present
    green = []
    yellow = []
    black = []
    black_edge_case = []
    placeholder = []

    # check the chars update guess_result
    # x____, xax___
    for x in range(5):
        if guess[x] in word:
            if guess[x] == word[x]:
                green.append((guess[x], x))
            elif guess[x] != word[x]:
                if guess.count(guess[x]) == 1:
                    yellow.append((guess[x], x))
                else:
                    placeholder.append((guess[x], x))
        else:
            black.append((guess[x], x))
    # format: (letter, index)

    for n in placeholder:
        # this is separate from the above for loop as the # of letters in greens can only be counted after the whole word has been evaluated
        if [green[i][0] for i in range(len(green))].count(n[0]) < word.count(n[0]):
            yellow.append(n)
            # checks if all instances of this letter are "greened" (i.e. are there still opportunities to find the letter in its correct placement)
            # example: guess: 'aargh', correct_word: 'aroma': second letter of 'aargh' is yellow b/c there is still an "unfound" 'a' at the end of 'aroma'
        else:
            black_edge_case.append(n)
            # black_edge_case is when the letter at a particular index IS in the word, but at another index, and furthermore, has already been "greened"       
    return([green, yellow, black, black_edge_case])
    


    # guess_result is populated
    # first filter out words if we have correct letters in the right place
    # enemy e___, filter out all words that do not have an e at the start
    # remove all the words in words that do not contain the letters we have


def word_set_narrower(words, green, yellow, black, black_edge_case):
    possible_words = set(words)
    for n in green:
        possible_words = possible_words.intersection(set(filter(lambda x: x[n[1]] == n[0], possible_words)))
    for n in yellow:
        possible_words = possible_words.intersection(set(filter(lambda x: n[0] in x and x[n[1]] != n[0] and x.count(n[0]) > [g[0] for g in green].count(n[0]), possible_words)))
        # possible_words = possible_words.intersection(set(filter(lambda x: n[0] in x and x[n[1]] != n[0], possible_words)))
    for n in black:
        possible_words = possible_words.intersection(set(filter(lambda x: n[0] not in x, possible_words)))
    for n in black_edge_case:
        possible_words = possible_words.intersection(set(filter(lambda x: n[0] in x and x[n[1]] != n[0], possible_words)))        
    return(possible_words)

'''
Plays the game of wordle as optimally as possible
'''
def wordle_algo(word, words):
    # step 1: always play toeas
    guess = 'toeas'
    i = 1
    possible_words = set(words).copy()
    while guess != word:
        possible_words = word_set_narrower(possible_words, word_checker(guess, word)[0], word_checker(guess, word)[1], word_checker(guess, word)[2], word_checker(guess, word)[3],)
        sorted_counts = get_letter_counts(possible_words)
        if len(sorted_counts) >= 10:
            letters = [sorted_counts[x][0] for x in range(10)]
        else:
            letters = [sorted_counts[x][0] for x in range(len(sorted_counts))]
        print(f'{i}th guess: -----{guess}----- ({word_checker(guess, word)}) narrows the words down to {possible_words} (n={len(possible_words)}). \n (the word is {word})')
        guess = pick_best_starting_word(possible_words, letters)[0]
        i += 1
    if guess == word:
        print(f'{i}th guess: -----{guess}----- correctly identified {word}, out of {possible_words} left.')
        

if __name__ == '__main__':
    main()
